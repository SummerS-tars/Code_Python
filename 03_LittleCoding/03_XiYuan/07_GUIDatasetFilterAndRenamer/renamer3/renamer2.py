"""Renamer2.

将中间格式 {appname}_{senary}_{new_id}_{dul_times}.* 重命名为最终格式
{appname}_{new_id}_{dul_times}.*，其中 new_id 为合并 senary+new_id 后的顺序号。
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


@dataclass(frozen=True)
class Record:
    appname: str
    senary: str
    original_id: str
    dul_times: str
    base_name: str


@dataclass(frozen=True)
class RenamePlan:
    source: Path
    temporary: Path
    target: Path


def parse_base_name(stem: str) -> Record | None:
    """Parse base filename without extension.

    Expected format: {appname}_{senary}_{new_id}_{dul_times}
    """
    if stem.endswith("_visualized"):
        stem = stem[: -len("_visualized")]

    parts = stem.rsplit("_", 3)
    if len(parts) != 4:
        return None

    appname, senary, original_id, dul_times = parts
    if not appname or not senary or not original_id or not dul_times:
        return None

    return Record(
        appname=appname,
        senary=senary,
        original_id=original_id,
        dul_times=dul_times,
        base_name=f"{appname}_{senary}_{original_id}_{dul_times}",
    )


def collect_candidates(folder: Path) -> Tuple[Dict[str, Record], Dict[str, Dict[str, Path]]]:
    records: Dict[str, Record] = {}
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
        records[base] = record
        files_by_base.setdefault(base, {})
        if path.suffix.lower() == ".jpg" and path.stem.endswith("_visualized"):
            files_by_base[base]["visualized"] = path
        elif path.suffix.lower() == ".jpg":
            files_by_base[base]["image"] = path
        elif path.suffix.lower() == ".txt":
            files_by_base[base]["text"] = path

    return records, files_by_base


def find_complete_sets(files_by_base: Dict[str, Dict[str, Path]]) -> List[str]:
    complete_bases: List[str] = []
    for base, file_map in files_by_base.items():
        if {"visualized", "image", "text"}.issubset(file_map.keys()):
            complete_bases.append(base)
    return complete_bases


def _sorted_values(values: Iterable[str]) -> List[str]:
    def sort_key(value: str) -> Tuple[int, str]:
        if value.isdigit():
            return (0, f"{int(value):012d}")
        return (1, value)

    return sorted(values, key=sort_key)


def _sorted_senary_id(keys: Iterable[Tuple[str, str]]) -> List[Tuple[str, str]]:
    def key_func(item: Tuple[str, str]) -> Tuple[str, Tuple[int, str]]:
        senary, original_id = item
        return (senary, (0, f"{int(original_id):012d}") if original_id.isdigit() else (1, original_id))

    return sorted(keys, key=key_func)


def _unique_temp_path(folder: Path, base_name: str, suffix: str) -> Path:
    candidate = folder / f".__tmp__{base_name}{suffix}"
    if not candidate.exists():
        return candidate

    index = 1
    while True:
        candidate = folder / f".__tmp__{base_name}__{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def build_rename_plans(
    folder: Path,
    records: Dict[str, Record],
    remaining_bases: Iterable[str],
) -> List[RenamePlan]:
    remaining_records = [records[base] for base in remaining_bases]

    key_map: Dict[str, Dict[Tuple[str, str], int]] = {}
    for record in remaining_records:
        key_map.setdefault(record.appname, {})

    for appname in key_map:
        keys = _sorted_senary_id(
            {
                (record.senary, record.original_id)
                for record in remaining_records
                if record.appname == appname
            }
        )
        key_map[appname] = {key: index + 1 for index, key in enumerate(keys)}

    plans: List[RenamePlan] = []
    for record in remaining_records:
        new_id = key_map[record.appname][(record.senary, record.original_id)]
        new_base = f"{record.appname}_{new_id}_{record.dul_times}"

        for suffix in (".jpg", "_visualized.jpg", ".txt"):
            source = folder / f"{record.base_name}{suffix}"
            if not source.exists():
                continue
            temporary = _unique_temp_path(folder, record.base_name, suffix)
            target = folder / f"{new_base}{suffix}"
            plans.append(RenamePlan(source=source, temporary=temporary, target=target))

    return plans


def apply_rename_plans(plans: Iterable[RenamePlan], dry_run: bool) -> int:
    plans = [plan for plan in plans if plan.source.name != plan.target.name]
    if not plans:
        return 0

    sources = {plan.source for plan in plans}
    targets = [plan.target for plan in plans]
    duplicate_targets = {target for target in targets if targets.count(target) > 1}
    if duplicate_targets:
        raise SystemExit(
            "发现重命名目标冲突：" + ", ".join(sorted({path.name for path in duplicate_targets}))
        )

    existing_targets = [target for target in targets if target.exists() and target not in sources]
    if existing_targets:
        raise SystemExit(
            "目标文件已存在，无法覆盖：" + ", ".join(sorted({path.name for path in existing_targets}))
        )

    rename_count = 0
    for plan in plans:
        if not plan.source.exists():
            continue
        rename_count += 1
        if dry_run:
            print(f"[dry-run] rename {plan.source.name} -> {plan.target.name}")
        else:
            plan.source.rename(plan.temporary)

    if dry_run:
        return rename_count

    for plan in plans:
        if plan.temporary.exists():
            plan.temporary.rename(plan.target)

    return rename_count


def process_folder(folder: Path, dry_run: bool = False) -> Dict[str, int]:
    records, files_by_base = collect_candidates(folder)
    remaining_bases = find_complete_sets(files_by_base)
    plans = build_rename_plans(folder, records, remaining_bases)
    renamed = apply_rename_plans(plans, dry_run=dry_run)

    return {
        "renamed": renamed,
        "remaining_sets": len(remaining_bases),
    }


def _gather_dataset_folders(root: Path, recursive: bool) -> List[Path]:
    candidates: List[Path] = []
    if root.is_dir() and root.name.startswith("dataset_"):
        candidates.append(root)

    if root.is_dir():
        if recursive:
            candidates.extend([path for path in root.rglob("dataset_*") if path.is_dir()])
        else:
            candidates.extend([path for path in root.iterdir() if path.is_dir() and path.name.startswith("dataset_")])

    unique = {path.resolve(): path for path in candidates}
    return sorted(unique.values())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Renamer2: remove senary field and renumber new_id in dataset folders.",
    )
    parser.add_argument(
        "folder",
        type=Path,
        help="包含 dataset_* 子目录的根目录或单个 dataset_* 目录",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="递归查找 dataset_* 子目录",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印操作，不执行重命名",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    root = args.folder

    if not root.exists() or not root.is_dir():
        raise SystemExit(f"目录不存在: {root}")

    folders = _gather_dataset_folders(root, recursive=args.recursive)
    if not folders:
        raise SystemExit("未找到 dataset_* 目录")

    total_renamed = 0
    total_sets = 0
    for folder in folders:
        summary = process_folder(folder, dry_run=args.dry_run)
        total_renamed += summary["renamed"]
        total_sets += summary["remaining_sets"]
        print(
            f"{folder.name}: 重命名 {summary['renamed']} 个文件，"
            f"保留 {summary['remaining_sets']} 组文件。"
        )

    print(
        "完成："
        f"重命名 {total_renamed} 个文件，"
        f"共处理 {len(folders)} 个目录，"
        f"累计 {total_sets} 组文件。"
    )


if __name__ == "__main__":
    main()
