"""Cleaner and Renamer 1.

删除未匹配的三件套（.jpg / _visualized.jpg / .txt），并对剩余文件重命名。
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


@dataclass(frozen=True)
class Record:
    appname: str
    original_id: str
    original_dul: str
    base_name: str  # without suffix or extension


@dataclass(frozen=True)
class RenamePlan:
    source: Path
    temporary: Path
    target: Path


def parse_base_name(stem: str) -> Record | None:
    """Parse base filename without extension.

    Expected format: {appname}_{id}_{dul_times}
    """
    if stem.endswith("_visualized"):
        stem = stem[: -len("_visualized")]

    parts = stem.rsplit("_", 2)
    if len(parts) != 3:
        return None

    appname, original_id, original_dul = parts
    if not appname or not original_id or not original_dul:
        return None

    return Record(
        appname=appname,
        original_id=original_id,
        original_dul=original_dul,
        base_name=f"{appname}_{original_id}_{original_dul}",
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


def find_unmatched(files_by_base: Dict[str, Dict[str, Path]]) -> Tuple[List[Path], List[str]]:
    to_delete: List[Path] = []
    remaining_bases: List[str] = []

    for base, file_map in files_by_base.items():
        if {"visualized", "image", "text"}.issubset(file_map.keys()):
            remaining_bases.append(base)
            continue

        to_delete.extend(file_map.values())

    return to_delete, remaining_bases


def _sorted_values(values: Iterable[str]) -> List[str]:
    def sort_key(value: str) -> Tuple[int, str]:
        if value.isdigit():
            return (0, f"{int(value):012d}")
        return (1, value)

    return sorted(values, key=sort_key)


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
    id_map: Dict[str, Dict[str, int]] = {}
    for record in remaining_records:
        id_map.setdefault(record.appname, {})

    for appname in id_map:
        ids = _sorted_values(
            {record.original_id for record in remaining_records if record.appname == appname}
        )
        id_map[appname] = {original_id: index + 1 for index, original_id in enumerate(ids)}

    dul_times_map: Dict[Tuple[str, str], Dict[str, int]] = {}
    for record in remaining_records:
        dul_times_map.setdefault((record.appname, record.original_id), {})

    for appname, original_id in dul_times_map:
        dul_values = _sorted_values(
            {
                record.original_dul
                for record in remaining_records
                if record.appname == appname and record.original_id == original_id
            }
        )
        dul_times_map[(appname, original_id)] = {
            value: index + 1 for index, value in enumerate(dul_values)
        }

    plans: List[RenamePlan] = []
    for record in remaining_records:
        new_id = id_map[record.appname][record.original_id]
        new_dul = dul_times_map[(record.appname, record.original_id)][record.original_dul]
        new_base = f"{record.appname}_{new_id}_{new_dul}"

        for suffix in (".jpg", "_visualized.jpg", ".txt"):
            source = folder / f"{record.base_name}{suffix}"
            if not source.exists():
                continue
            temporary = _unique_temp_path(folder, record.base_name, suffix)
            target = folder / f"{new_base}{suffix}"
            plans.append(RenamePlan(source=source, temporary=temporary, target=target))

    return plans


def apply_deletions(paths: Iterable[Path], dry_run: bool) -> None:
    for path in paths:
        if not path.exists():
            continue
        if dry_run:
            print(f"[dry-run] delete {path.name}")
        else:
            path.unlink()


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
    to_delete, remaining_bases = find_unmatched(files_by_base)
    apply_deletions(to_delete, dry_run=dry_run)

    plans = build_rename_plans(folder, records, remaining_bases)
    renamed = apply_rename_plans(plans, dry_run=dry_run)

    return {
        "deleted": len(to_delete),
    "renamed": renamed,
        "remaining_sets": len(remaining_bases),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Cleaner and Renamer 1: remove unmatched files and renumber IDs.",
    )
    parser.add_argument(
        "folder",
        type=Path,
        help="包含 process_1 文件的目录",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印操作，不进行删除或重命名",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    folder = args.folder

    if not folder.exists() or not folder.is_dir():
        raise SystemExit(f"目录不存在: {folder}")

    summary = process_folder(folder, dry_run=args.dry_run)
    print(
        "完成："
        f"删除 {summary['deleted']} 个文件，"
        f"重命名 {summary['renamed']} 个文件，"
        f"保留 {summary['remaining_sets']} 组文件。"
    )


if __name__ == "__main__":
    main()
