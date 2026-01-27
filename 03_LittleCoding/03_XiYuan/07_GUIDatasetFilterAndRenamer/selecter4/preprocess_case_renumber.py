"""Preprocess dataset folders by normalizing appname to lowercase and renumbering new_id.

This script copies files to a new output root and keeps source untouched.
Input format: {appname}_{new_id}_{dul_times}(.jpg|_visualized.jpg|.txt)
"""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


@dataclass(frozen=True)
class Record:
    appname: str
    new_id: str
    dul_times: str
    base_name: str


@dataclass(frozen=True)
class FileGroup:
    record: Record
    image: Path
    visualized: Path
    label: Path


@dataclass(frozen=True)
class PlannedCopy:
    source: Path
    target: Path


def parse_base_name(stem: str) -> Record | None:
    if stem.endswith("_visualized"):
        stem = stem[: -len("_visualized")]

    parts = stem.rsplit("_", 2)
    if len(parts) != 3:
        return None

    appname, new_id, dul_times = parts
    if not appname or not new_id or not dul_times:
        return None

    return Record(appname=appname, new_id=new_id, dul_times=dul_times, base_name=stem)


def collect_groups(folder: Path) -> List[FileGroup]:
    files_by_base: Dict[str, Dict[str, Path]] = {}
    records: Dict[str, Record] = {}

    for path in folder.iterdir():
        if not path.is_file():
            continue
        if path.name.startswith(".__tmp__"):
            continue
        if path.suffix.lower() not in {".jpg", ".txt"}:
            continue

        record = parse_base_name(path.stem)
        if record is None:
            continue

        base = record.base_name
        records[base] = record
        files_by_base.setdefault(base, {})
        if path.suffix.lower() == ".jpg" and path.stem.endswith("_visualized"):
            files_by_base[base]["visualized"] = path
        elif path.suffix.lower() == ".jpg":
            files_by_base[base]["image"] = path
        elif path.suffix.lower() == ".txt":
            files_by_base[base]["label"] = path

    groups: List[FileGroup] = []
    for base, mapping in files_by_base.items():
        if {"image", "visualized", "label"}.issubset(mapping.keys()):
            record = records.get(base)
            if record is None:
                continue
            groups.append(
                FileGroup(
                    record=record,
                    image=mapping["image"],
                    visualized=mapping["visualized"],
                    label=mapping["label"],
                )
            )

    return groups


def gather_dataset_folders(root: Path, recursive: bool) -> List[Path]:
    folders: List[Path] = []
    if root.is_dir() and root.name.startswith("dataset_"):
        folders.append(root)

    if root.is_dir():
        if recursive:
            folders.extend([path for path in root.rglob("dataset_*") if path.is_dir()])
        else:
            folders.extend([path for path in root.iterdir() if path.is_dir() and path.name.startswith("dataset_")])

    unique = {path.resolve(): path for path in folders}
    return sorted(unique.values())


def _id_sort_key(value: str) -> Tuple[int, int | str]:
    if value.isdigit():
        return (0, int(value))
    return (1, value)


def build_id_map(groups_by_app: Dict[str, Dict[Tuple[str, str], List[FileGroup]]]) -> Dict[Tuple[str, str, str], int]:
    mapping: Dict[Tuple[str, str, str], int] = {}
    for appname, keys in groups_by_app.items():
        ordered_keys = sorted(keys.keys(), key=lambda item: (item[0], _id_sort_key(item[1])))
        for index, (dataset_name, original_id) in enumerate(ordered_keys):
            mapping[(appname, dataset_name, original_id)] = index + 1
    return mapping


def plan_copies(
    groups_by_app: Dict[str, Dict[Tuple[str, str], List[FileGroup]]],
    id_map: Dict[Tuple[str, str, str], int],
    output_root: Path,
) -> List[PlannedCopy]:
    plans: List[PlannedCopy] = []

    for appname, keys in groups_by_app.items():
        for (dataset_name, original_id), groups in keys.items():
            new_id = id_map[(appname, dataset_name, original_id)]
            for group in groups:
                new_base = f"{appname}_{new_id}_{group.record.dul_times}"
                target_folder = output_root / dataset_name
                target_folder.mkdir(parents=True, exist_ok=True)
                plans.extend(
                    [
                        PlannedCopy(
                            source=group.image,
                            target=target_folder / f"{new_base}.jpg",
                        ),
                        PlannedCopy(
                            source=group.visualized,
                            target=target_folder / f"{new_base}_visualized.jpg",
                        ),
                        PlannedCopy(
                            source=group.label,
                            target=target_folder / f"{new_base}.txt",
                        ),
                    ]
                )

    return plans


def execute_plans(plans: Iterable[PlannedCopy], dry_run: bool) -> int:
    count = 0
    for plan in plans:
        if plan.target.exists():
            raise SystemExit(f"目标文件已存在: {plan.target}")
        count += 1
        if dry_run:
            print(f"[dry-run] copy {plan.source.name} -> {plan.target}")
        else:
            shutil.copy2(plan.source, plan.target)
    return count


def process(root: Path, output_root: Path, recursive: bool, dry_run: bool) -> Dict[str, int]:
    folders = gather_dataset_folders(root, recursive=recursive)
    if not folders:
        raise SystemExit("未找到 dataset_* 目录")

    groups_by_app: Dict[str, Dict[Tuple[str, str], List[FileGroup]]] = {}
    total_groups = 0
    for folder in folders:
        dataset_name = folder.name
        for group in collect_groups(folder):
            total_groups += 1
            appname = group.record.appname.lower()
            key = (dataset_name, group.record.new_id)
            groups_by_app.setdefault(appname, {}).setdefault(key, []).append(group)

    id_map = build_id_map(groups_by_app)
    plans = plan_copies(groups_by_app, id_map, output_root)
    copied = execute_plans(plans, dry_run=dry_run)

    return {
        "datasets": len(folders),
        "groups": total_groups,
        "copies": copied,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Preprocess datasets: normalize appname to lowercase and renumber new_id.",
    )
    parser.add_argument("root", type=Path, help="dataset_* 根目录或单个 dataset_* 目录")
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="输出目录（用于中间备份）",
    )
    parser.add_argument("--recursive", action="store_true", help="递归扫描 dataset_* 目录")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不执行复制")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    root = args.root
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"目录不存在: {root}")

    summary = process(root, output_root=args.output, recursive=args.recursive, dry_run=args.dry_run)
    print(
        "完成："
        f"共处理 {summary['datasets']} 个目录，"
        f"收集 {summary['groups']} 组文件，"
        f"复制 {summary['copies']} 个文件。"
    )


if __name__ == "__main__":
    main()
