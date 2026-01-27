"""Detect or resolve filename collisions across dataset_* folders.

If collisions exist for same appname_{new_id}_{dul_times} across different dataset folders,
we can renumber new_id per appname to avoid duplicates.
"""

from __future__ import annotations

import argparse
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
class RenamePlan:
    source: Path
    temporary: Path
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


def collect_records(folder: Path) -> Dict[str, Record]:
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
        records[record.base_name] = record

    return records


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


def detect_collisions(folders: Iterable[Path]) -> Dict[str, List[Path]]:
    collision_map: Dict[str, List[Path]] = {}
    seen: Dict[str, Path] = {}
    for folder in folders:
        for record in collect_records(folder).values():
            base = record.base_name
            if base in seen:
                collision_map.setdefault(base, [seen[base]])
                collision_map[base].append(folder)
            else:
                seen[base] = folder
    return collision_map


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


def build_rename_plans(folders: Iterable[Path]) -> List[RenamePlan]:
    records_by_folder: Dict[Path, Dict[str, Record]] = {}
    for folder in folders:
        records_by_folder[folder] = collect_records(folder)

    all_records = [record for folder in records_by_folder.values() for record in folder.values()]
    app_map: Dict[str, Dict[str, int]] = {}
    for record in all_records:
        app_map.setdefault(record.appname, {})

    for appname in app_map:
        ids = _sorted_values({record.new_id for record in all_records if record.appname == appname})
        app_map[appname] = {old: index + 1 for index, old in enumerate(ids)}

    plans: List[RenamePlan] = []
    for folder, records in records_by_folder.items():
        for record in records.values():
            new_id = app_map[record.appname][record.new_id]
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


def process(root: Path, recursive: bool, dry_run: bool, fix: bool) -> Dict[str, int]:
    folders = gather_dataset_folders(root, recursive=recursive)
    if not folders:
        raise SystemExit("未找到 dataset_* 目录")

    collisions = detect_collisions(folders)
    if not collisions:
        return {"collisions": 0, "renamed": 0, "datasets": len(folders)}

    if not fix:
        print("发现以下同名文件：")
        for base, locations in collisions.items():
            names = ", ".join(sorted({loc.name for loc in locations}))
            print(f"  {base} -> {names}")
        return {"collisions": len(collisions), "renamed": 0, "datasets": len(folders)}

    plans = build_rename_plans(folders)
    renamed = apply_rename_plans(plans, dry_run=dry_run)
    return {"collisions": len(collisions), "renamed": renamed, "datasets": len(folders)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Detect/resolve dataset filename collisions.")
    parser.add_argument("root", type=Path, help="dataset_* 根目录或单个 dataset_* 目录")
    parser.add_argument("--recursive", action="store_true", help="递归扫描 dataset_* 目录")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不执行重命名")
    parser.add_argument("--fix", action="store_true", help="执行重排 new_id")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    root = args.root
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"目录不存在: {root}")

    summary = process(root, recursive=args.recursive, dry_run=args.dry_run, fix=args.fix)
    print(
        "完成："
        f"共处理 {summary['datasets']} 个目录，"
        f"发现 {summary['collisions']} 处同名，"
        f"重命名 {summary['renamed']} 个文件。"
    )


if __name__ == "__main__":
    main()
