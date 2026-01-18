"""GUI dataset filter and renamer.

Filters dataset files based on available *_visualized images and renames
remaining files following the required naming scheme.
"""
from __future__ import annotations

import argparse
import re
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    import tkinter as tk
    from tkinter import filedialog
except Exception:  # pragma: no cover - optional GUI dependency
    tk = None
    filedialog = None

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
TEXT_EXTENSION = ".txt"
FILENAME_PATTERN = re.compile(
    r"^(?P<senary>.+)_(?P<id>\d+)_(?P<date>\d{8})_(?P<time>\d{6})(?P<visualized>_visualized)?$"
)


@dataclass(frozen=True)
class FileKey:
    senary: str
    orig_id: int
    date: str
    time: str


@dataclass
class FileInfo:
    path: Path
    key: FileKey
    is_visualized: bool
    extension: str


@dataclass
class RenamePlan:
    source: Path
    target: Path


@dataclass
class DatasetReport:
    deleted: list[Path]
    renamed: list[RenamePlan]
    skipped: list[Path]


@dataclass
class DatasetConfig:
    dry_run: bool = False
    verbose: bool = True
    process_all: bool = False


@dataclass
class DatasetContext:
    appname: str
    folder: Path


def parse_filename(path: Path) -> FileInfo | None:
    if not path.is_file():
        return None

    extension = path.suffix.lower()
    if extension not in IMAGE_EXTENSIONS and extension != TEXT_EXTENSION:
        return None

    match = FILENAME_PATTERN.match(path.stem)
    if not match:
        return None

    senary = match.group("senary")
    orig_id = int(match.group("id"))
    date = match.group("date")
    time = match.group("time")
    is_visualized = match.group("visualized") is not None

    key = FileKey(senary=senary, orig_id=orig_id, date=date, time=time)
    return FileInfo(path=path, key=key, is_visualized=is_visualized, extension=extension)


def iter_dataset_files(folder: Path) -> Iterable[FileInfo]:
    for path in folder.iterdir():
        info = parse_filename(path)
        if info:
            yield info


def build_context(folder: Path) -> DatasetContext:
    appname = folder.name
    if appname.startswith("dataset_"):
        appname = appname[len("dataset_") :]
    return DatasetContext(appname=appname, folder=folder)


def select_folder() -> Path | None:
    if tk is None or filedialog is None:
        return None
    root = tk.Tk()
    root.withdraw()
    selected = filedialog.askdirectory(title="选择 dataset_* 文件夹或根目录")
    return Path(selected) if selected else None


def filter_and_plan(context: DatasetContext, config: DatasetConfig) -> DatasetReport:
    files_by_key: dict[FileKey, dict[str, FileInfo]] = {}
    skipped: list[Path] = []

    for info in iter_dataset_files(context.folder):
        entry = files_by_key.setdefault(info.key, {})
        if info.extension == TEXT_EXTENSION:
            entry["txt"] = info
        elif info.is_visualized:
            entry["visualized"] = info
        else:
            entry["image"] = info

    visualized_keys = {key for key, entry in files_by_key.items() if "visualized" in entry}

    deleted: list[Path] = []
    for key, entry in files_by_key.items():
        if key not in visualized_keys:
            for item_key in ("image", "txt"):
                if item_key in entry:
                    deleted.append(entry[item_key].path)

    rename_plans: list[RenamePlan] = []
    ordered_keys = sorted(
        visualized_keys,
        key=lambda k: (k.orig_id, k.date, k.time, k.senary),
    )

    new_id_map: dict[int, int] = {}
    duplicate_counter: dict[tuple[str, int], int] = {}
    next_new_id = 1

    for key in ordered_keys:
        if key.orig_id not in new_id_map:
            new_id_map[key.orig_id] = next_new_id
            next_new_id += 1

        duplicate_key = (key.senary, key.orig_id)
        duplicate_counter[duplicate_key] = duplicate_counter.get(duplicate_key, 0) + 1
        new_id = new_id_map[key.orig_id]
        dul_times = duplicate_counter[duplicate_key]

        base_name = f"{context.appname}_{key.senary}_{new_id}_{dul_times}"
        entry = files_by_key[key]

        if "visualized" in entry:
            visualized_info = entry["visualized"]
            rename_plans.append(
                RenamePlan(
                    source=visualized_info.path,
                    target=context.folder / f"{base_name}_visualized{visualized_info.extension}",
                )
            )

        if "image" in entry:
            image_info = entry["image"]
            rename_plans.append(
                RenamePlan(
                    source=image_info.path,
                    target=context.folder / f"{base_name}{image_info.extension}",
                )
            )

        if "txt" in entry:
            txt_info = entry["txt"]
            rename_plans.append(
                RenamePlan(
                    source=txt_info.path,
                    target=context.folder / f"{base_name}{TEXT_EXTENSION}",
                )
            )

    return DatasetReport(deleted=deleted, renamed=rename_plans, skipped=skipped)


def apply_report(report: DatasetReport, config: DatasetConfig) -> None:
    if config.verbose:
        print(f"删除 {len(report.deleted)} 个文件，重命名 {len(report.renamed)} 个文件。")

    if config.dry_run:
        for path in report.deleted:
            print(f"[DRY-RUN] 删除: {path}")
        for plan in report.renamed:
            if plan.source != plan.target:
                print(f"[DRY-RUN] 重命名: {plan.source.name} -> {plan.target.name}")
        return

    for path in report.deleted:
        if path.exists():
            path.unlink()

    temp_mapping: list[RenamePlan] = []
    for plan in report.renamed:
        if not plan.source.exists() or plan.source == plan.target:
            continue
        temp_path = plan.source.with_name(f".tmp_{uuid.uuid4().hex}{plan.source.suffix}")
        plan.source.rename(temp_path)
        temp_mapping.append(RenamePlan(source=temp_path, target=plan.target))

    for plan in temp_mapping:
        if plan.target.exists():
            plan.target.unlink()
        plan.source.rename(plan.target)


def process_dataset_folder(folder: Path, config: DatasetConfig) -> DatasetReport:
    context = build_context(folder)
    if config.verbose:
        print(f"\n处理数据集: {folder} (app: {context.appname})")
    report = filter_and_plan(context, config)
    apply_report(report, config)
    return report


def find_dataset_folders(root: Path) -> list[Path]:
    if root.name.startswith("dataset_"):
        return [root]

    return sorted(
        [path for path in root.iterdir() if path.is_dir() and path.name.startswith("dataset_")]
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="根据 visualized 图片过滤并重命名 GUI 数据集",
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="dataset_* 文件夹或其父目录 (为空时弹出选择框)",
    )
    parser.add_argument("--dry-run", action="store_true", help="只预览，不执行删除/重命名")
    parser.add_argument("--quiet", action="store_true", help="减少输出")
    parser.add_argument(
        "--all",
        action="store_true",
        help="当 path 为父目录时，处理所有 dataset_* 子目录",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or [])

    folder: Path | None
    if args.path:
        folder = Path(args.path)
    else:
        folder = select_folder()

    if folder is None:
        print("未选择任何目录，已退出。")
        return 1

    if not folder.exists():
        print(f"路径不存在: {folder}")
        return 1

    config = DatasetConfig(
        dry_run=args.dry_run,
        verbose=not args.quiet,
        process_all=args.all,
    )

    if config.process_all:
        dataset_folders = find_dataset_folders(folder)
        if not dataset_folders:
            print("未发现 dataset_* 目录")
            return 1
        for dataset_folder in dataset_folders:
            process_dataset_folder(dataset_folder, config)
    else:
        if folder.is_dir() and folder.name.startswith("dataset_"):
            process_dataset_folder(folder, config)
        else:
            dataset_folders = find_dataset_folders(folder)
            if len(dataset_folders) == 1:
                process_dataset_folder(dataset_folders[0], config)
            else:
                print("请指定 dataset_* 目录，或使用 --all 处理父目录")
                return 1

    print("\n处理完成。")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
