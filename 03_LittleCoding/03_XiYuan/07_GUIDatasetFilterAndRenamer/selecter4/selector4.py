"""Dataset selector for train/val split.

Input format: {appname}_{new_id}_{dul_times}(.jpg|_visualized.jpg|.txt)
Output structure:
    dataset/
        images/{data,val}
        labels/{data,val}
        visualized/{data,val}

Config file (json):
    - val_ratio: float, ratio of large groups put into val (at least one)
    - prob_pick_single_from_small_multi: float, probability to pick one image from small multi group
    - small_group_threshold: int, boundary for small vs large groups
    - random_seed: int, seed for reproducibility
"""

from __future__ import annotations

import argparse
import json
import random
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
class PlannedMove:
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


def collect_groups(folder: Path) -> Dict[str, Dict[str, Path]]:
    files_by_base: Dict[str, Dict[str, Path]] = {}
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
        files_by_base.setdefault(base, {})
        if path.suffix.lower() == ".jpg" and path.stem.endswith("_visualized"):
            files_by_base[base]["visualized"] = path
        elif path.suffix.lower() == ".jpg":
            files_by_base[base]["image"] = path
        elif path.suffix.lower() == ".txt":
            files_by_base[base]["label"] = path

    return files_by_base


def build_complete_groups(folder: Path) -> List[FileGroup]:
    groups: List[FileGroup] = []
    for base, mapping in collect_groups(folder).items():
        if {"image", "visualized", "label"}.issubset(mapping.keys()):
            record = parse_base_name(base)
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


def group_by_app_id(groups: Iterable[FileGroup]) -> Dict[Tuple[str, str], List[FileGroup]]:
    result: Dict[Tuple[str, str], List[FileGroup]] = {}
    for group in groups:
        key = (group.record.appname, group.record.new_id)
        result.setdefault(key, []).append(group)
    return result


def choose_val_groups(
    grouped: Dict[Tuple[str, str], List[FileGroup]],
    val_ratio: float,
    prob_pick_single_from_small_multi: float,
    small_group_threshold: int,
    rng: random.Random,
) -> Tuple[List[FileGroup], List[FileGroup]]:
    val_groups: List[FileGroup] = []
    data_groups: List[FileGroup] = []

    for items in grouped.values():
        count = len(items)
        if count == 1:
            data_groups.extend(items)
            continue

        if count <= small_group_threshold:
            if rng.random() < prob_pick_single_from_small_multi:
                chosen = rng.choice(items)
                val_groups.append(chosen)
                data_groups.extend([item for item in items if item != chosen])
            else:
                data_groups.extend(items)
            continue

        val_count = max(1, int(round(count * val_ratio)))
        chosen_items = rng.sample(items, k=val_count)
        val_groups.extend(chosen_items)
        data_groups.extend([item for item in items if item not in chosen_items])

    return data_groups, val_groups


def build_output_structure(output_root: Path) -> Dict[str, Dict[str, Path]]:
    structure = {
        "images": {"data": output_root / "images" / "data", "val": output_root / "images" / "val"},
        "labels": {"data": output_root / "labels" / "data", "val": output_root / "labels" / "val"},
        "visualized": {
            "data": output_root / "visualized" / "data",
            "val": output_root / "visualized" / "val",
        },
    }
    for group in structure.values():
        for path in group.values():
            path.mkdir(parents=True, exist_ok=True)
    return structure


def plan_moves(groups: Iterable[FileGroup], output_root: Path, split: str) -> List[PlannedMove]:
    structure = build_output_structure(output_root)
    planned: List[PlannedMove] = []
    for group in groups:
        planned.extend(
            [
                PlannedMove(
                    source=group.image,
                    target=structure["images"][split] / group.image.name,
                ),
                PlannedMove(
                    source=group.label,
                    target=structure["labels"][split] / group.label.name,
                ),
                PlannedMove(
                    source=group.visualized,
                    target=structure["visualized"][split] / group.visualized.name,
                ),
            ]
        )
    return planned


def execute_moves(plans: Iterable[PlannedMove], dry_run: bool) -> int:
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


def load_config(path: Path) -> Dict[str, float | int]:
    if not path.exists():
        raise SystemExit(f"配置文件不存在: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    prob_small = data.get("prob_pick_single_from_small_multi", data.get("prob_pick_single_from_multi", 0.0))
    return {
        "val_ratio": float(data.get("val_ratio", 0.1)),
        "prob_pick_single_from_small_multi": float(prob_small),
        "small_group_threshold": int(data.get("small_group_threshold", 3)),
        "random_seed": int(data.get("random_seed", 42)),
    }


def process(root: Path, output_root: Path, config: Dict[str, float | int], recursive: bool, dry_run: bool) -> Dict[str, int]:
    folders = gather_dataset_folders(root, recursive=recursive)
    if not folders:
        raise SystemExit("未找到 dataset_* 目录")

    groups: List[FileGroup] = []
    for folder in folders:
        groups.extend(build_complete_groups(folder))

    grouped = group_by_app_id(groups)
    rng = random.Random(int(config["random_seed"]))
    data_groups, val_groups = choose_val_groups(
        grouped,
        val_ratio=float(config["val_ratio"]),
        prob_pick_single_from_small_multi=float(config["prob_pick_single_from_small_multi"]),
        small_group_threshold=int(config["small_group_threshold"]),
        rng=rng,
    )

    data_plans = plan_moves(data_groups, output_root, "data")
    val_plans = plan_moves(val_groups, output_root, "val")

    total = execute_moves(data_plans + val_plans, dry_run=dry_run)

    return {
        "datasets": len(folders),
        "groups": len(groups),
        "data_groups": len(data_groups),
        "val_groups": len(val_groups),
        "files_copied": total,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dataset selector (train/val split).")
    parser.add_argument("root", type=Path, help="dataset_* 根目录或单个 dataset_* 目录")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("dataset"),
        help="输出目录（默认 dataset）",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config.json"),
        help="配置文件路径（默认 config.json）",
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

    config = load_config(args.config)
    summary = process(
        root=root,
        output_root=args.output,
        config=config,
        recursive=args.recursive,
        dry_run=args.dry_run,
    )

    print(
        "完成："
        f"共处理 {summary['datasets']} 个目录，"
        f"收集 {summary['groups']} 组文件，"
        f"训练集 {summary['data_groups']} 组，"
        f"验证集 {summary['val_groups']} 组，"
        f"复制 {summary['files_copied']} 个文件。"
    )


if __name__ == "__main__":
    main()
