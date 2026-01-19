"""Dataset stats helper.

统计有效三件套的 app 列表、每个 app 的数据组数量，以及每个 app 内 duplicate times 最大为 1 的 id 占比。
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple


@dataclass(frozen=True)
class Record:
    appname: str
    original_id: str
    original_dul: str
    base_name: str


def parse_base_name(stem: str) -> Record | None:
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


def _iter_files(folder: Path, recursive: bool) -> Iterable[Path]:
    if recursive:
        yield from folder.rglob("*")
        return
    yield from folder.iterdir()


def collect_valid_bases(folder: Path, recursive: bool) -> Tuple[Dict[str, Record], Set[str]]:
    records: Dict[str, Record] = {}
    files_by_base: Dict[str, Set[str]] = {}

    for path in _iter_files(folder, recursive):
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
        files_by_base.setdefault(base, set())
        if path.suffix.lower() == ".jpg" and path.stem.endswith("_visualized"):
            files_by_base[base].add("visualized")
        elif path.suffix.lower() == ".jpg":
            files_by_base[base].add("image")
        elif path.suffix.lower() == ".txt":
            files_by_base[base].add("text")

    valid_bases = {
        base for base, parts in files_by_base.items() if {"visualized", "image", "text"}.issubset(parts)
    }
    valid_records = {base: record for base, record in records.items() if base in valid_bases}
    return valid_records, valid_bases


def compute_stats(folder: Path, recursive: bool = False) -> Dict[str, Dict[str, float]]:
    records, _ = collect_valid_bases(folder, recursive=recursive)

    ids_by_app: Dict[str, Set[str]] = {}
    dul_by_app_id: Dict[Tuple[str, str], List[int]] = {}

    for record in records.values():
        ids_by_app.setdefault(record.appname, set()).add(record.original_id)
        dul_by_app_id.setdefault((record.appname, record.original_id), [])
        dul_value = int(record.original_dul) if record.original_dul.isdigit() else 0
        dul_by_app_id[(record.appname, record.original_id)].append(dul_value)

    stats: Dict[str, Dict[str, float]] = {}
    for appname, id_set in ids_by_app.items():
        total_ids = len(id_set)
        single_ids = 0
        total_items = sum(1 for record in records.values() if record.appname == appname)
        for original_id in id_set:
            dul_values = dul_by_app_id.get((appname, original_id), [0])
            if max(dul_values) <= 1:
                single_ids += 1
        ratio = (single_ids / total_ids) if total_ids else 0.0
        stats[appname] = {
            "groups": float(total_ids),
            "total_items": float(total_items),
            "single_ratio": ratio,
        }

    total_groups = sum(int(values["groups"]) for values in stats.values())
    total_items = sum(int(values["total_items"]) for values in stats.values())
    total_single_ids = sum(
        int(values["groups"] * values["single_ratio"]) for values in stats.values()
    )
    total_ratio = (total_single_ids / total_groups) if total_groups else 0.0
    stats["__total__"] = {
        "groups": float(total_groups),
        "total_items": float(total_items),
        "single_ratio": total_ratio,
    }

    return stats


def print_stats(stats: Dict[str, Dict[str, float]]) -> None:
    apps = sorted(app for app in stats.keys() if app != "__total__")
    print(f"app 数量：{len(apps)}")
    for app in apps:
        groups = int(stats[app]["groups"])
        items = int(stats[app]["total_items"])
        ratio = stats[app]["single_ratio"] * 100
        print(f"- {app}: 数据组 {groups}，总量 {items}，single-id 占比 {ratio:.2f}%")

    if "__total__" in stats:
        total_groups = int(stats["__total__"]["groups"])
        total_items = int(stats["__total__"]["total_items"])
        total_ratio = stats["__total__"]["single_ratio"] * 100
        print(
            f"汇总：数据组 {total_groups}，总量 {total_items}，single-id 占比 {total_ratio:.2f}%"
        )


def write_csv(stats: Dict[str, Dict[str, float]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["appname", "groups", "total_items", "single_ratio"])
        for app in sorted(stats.keys()):
            writer.writerow(
                [
                    app,
                    int(stats[app]["groups"]),
                    int(stats[app]["total_items"]),
                    f"{stats[app]['single_ratio']:.6f}",
                ]
            )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="统计 app 与 duplicate times 情况")
    parser.add_argument("folder", type=Path, help="包含 process_1 文件的目录")
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="递归扫描子目录",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="输出 CSV 文件路径",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    folder = args.folder

    if not folder.exists() or not folder.is_dir():
        raise SystemExit(f"目录不存在: {folder}")

    stats = compute_stats(folder, recursive=args.recursive)
    print_stats(stats)

    if args.output:
        write_csv(stats, args.output)


if __name__ == "__main__":
    main()
