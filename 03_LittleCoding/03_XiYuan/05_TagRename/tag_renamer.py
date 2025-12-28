#!/usr/bin/env python3
"""
Tag & Label Renamer + Aggregator

根据 requirements.md：
- 递归处理 class_all 下的 class 与 class_unknown 子目录
- 仅修改文件名中的 tag 部分，保持 class 与 duplicate 两段数字不变
- 同步修改对应 txt 标注文件名中的 tag 部分（保持其它部分不变）
- 按 train/val 分类，汇总移动图片到 root/train|val，标签到 root/labels/train|val

使用：
  python tag_renamer.py --root E:\\...\\class_all --execute

默认 dry-run 仅输出将进行的操作；加 --execute 才会真正修改/移动。
"""
from __future__ import annotations

import argparse
import csv
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Tuple, List, Dict
import logging
from datetime import datetime


# ------------------------------
# 配置与实用函数
# ------------------------------

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
LOGGER = logging.getLogger("tag_renamer")


def is_image(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_EXTS


def ensure_dir(p: Path, dry_run: bool) -> None:
    if p.exists():
        return
    if dry_run:
        LOGGER.info(f"[dry-run] mkdir -p {p}")
    else:
        p.mkdir(parents=True, exist_ok=True)


def resolve_conflict(dest: Path, policy: str, dry_run: bool) -> Optional[Path]:
    """根据冲突策略返回可用的目标路径。
    policy: skip | overwrite | rename
    返回 None 表示 skip
    """
    if not dest.exists():
        return dest
    if policy == "skip":
        LOGGER.info(f"[skip/conflict] target exists -> {dest}")
        return None
    if policy == "overwrite":
        # 直接用原路径，后续执行时覆盖
        return dest
    if policy == "rename":
        parent = dest.parent
        stem = dest.stem
        suffix = dest.suffix
        i = 1
        while True:
            cand = parent / f"{stem}__dup{i}{suffix}"
            if not cand.exists():
                return cand
            i += 1
    raise ValueError(f"Unknown on-conflict policy: {policy}")


# ------------------------------
# 名称解析
# ------------------------------

TrainVal = str  # "train" | "val"


@dataclass
class ParsedImageName:
    trainval: TrainVal
    cls_num: int
    dup_num: int
    descriptor: str  # 去掉 _train/_val_与末尾两段数字后的前缀（可能包含时间/hash/tag等）


IMG_REGEX = re.compile(r"^(?P<prefix>.+?)_(?P<tv>train|val)_(?P<c>\d+)_(?P<d>\d+)$", re.IGNORECASE)


def parse_image_stem(stem: str) -> Optional[ParsedImageName]:
    m = IMG_REGEX.match(stem)
    if not m:
        return None
    tv = m.group("tv").lower()
    c = int(m.group("c"))
    d = int(m.group("d"))
    prefix = m.group("prefix")
    return ParsedImageName(trainval=tv, cls_num=c, dup_num=d, descriptor=prefix)


def determine_new_tag(pic_path: Path, root: Path) -> Optional[str]:
    """根据目录结构确定新 tag。
    - 已知类别: root/class/<ClassName>/pic -> tag = <ClassName>
    - 未知类别: root/class_unknown/<classN_suffix>/pic -> tag = suffix；若不匹配，则用该目录名
    返回 None 表示无法确定。
    """
    # 期望结构: .../<bucket>/<leaf>/pic/<file>
    # 其中 bucket in {class, class_unknown}
    try:
        pic_dir = pic_path.parent
        leaf = pic_dir.parent.name  # 类别目录名（如 Ada 或 class1_ikea）
        bucket = pic_dir.parent.parent.name  # class 或 class_unknown
        bucket_parent = pic_dir.parent.parent.parent
    except Exception:
        return None

    # 需确保 bucket_parent 为 root 目录
    if bucket_parent.resolve() != root.resolve():
        # 容忍更深层，只要路径中包含 class / class_unknown 也可
        parts = list(pic_path.parts)
        if "class" in parts:
            bucket = "class"
            leaf = parts[parts.index("class") + 1]
        elif "class_unknown" in parts:
            bucket = "class_unknown"
            leaf = parts[parts.index("class_unknown") + 1]
        else:
            return None

    if bucket == "class":
        return leaf
    if bucket == "class_unknown":
        m = re.match(r"class\d+_(.+)", leaf, re.IGNORECASE)
        if m:
            return m.group(1)
        return leaf
    return None


def compute_new_label_stem(old_descriptor: str, new_tag: str) -> str:
    """在 descriptor 内将最后一个 '-' 后的部分替换为 new_tag。
    若 descriptor 不包含 '-'，则追加 '-<new_tag>'。
    例如：
      'Adobe_...-8' + 'Ada' => 'Adobe_...-Ada'
      '2024_...-searchpage' + 'ikea' => '2024_...-ikea'
      'plain' + 'Ada' => 'plain-Ada'
    """
    if '-' in old_descriptor:
        i = old_descriptor.rfind('-')
        return old_descriptor[: i + 1] + new_tag
    return f"{old_descriptor}-{new_tag}"


# ------------------------------
# 重命名与移动
# ------------------------------

@dataclass
class ActionRecord:
    image_old: Path
    image_new: Optional[Path]
    label_old: Optional[Path]
    label_new: Optional[Path]
    trainval: Optional[str]
    moved_image_to: Optional[Path]
    moved_label_to: Optional[Path]
    status: str


def rename_image_and_label(img_path: Path, root: Path, dry_run: bool, on_conflict: str, verbose: bool) -> ActionRecord:
    rec = ActionRecord(
        image_old=img_path, image_new=None,
        label_old=None, label_new=None,
        trainval=None, moved_image_to=None, moved_label_to=None,
        status="pending",
    )

    parsed = parse_image_stem(img_path.stem)
    if not parsed:
        rec.status = "skip:unrecognized_image_name"
        if verbose:
            LOGGER.warning(f"[warn] 无法解析图片名: {img_path.name}")
        return rec
    rec.trainval = parsed.trainval

    new_tag = determine_new_tag(img_path, root)
    if not new_tag:
        rec.status = "skip:cannot_determine_tag"
        if verbose:
            LOGGER.warning(f"[warn] 无法确定新tag: {img_path}")
        return rec

    # 构造新图片名：<tag>_<class>_<duplicate>.<ext>
    final_img_stem = f"{new_tag}_{parsed.cls_num}_{parsed.dup_num}"
    new_img_name = f"{final_img_stem}{img_path.suffix.lower()}"
    new_img_path = img_path.with_name(new_img_name)
    if new_img_path == img_path:
        # 无需改名
        pass
    else:
        # 冲突处理（目标在同目录）
        target = resolve_conflict(new_img_path, on_conflict, dry_run)
        if target is None:
            rec.status = "skip:image_rename_conflict"
            return rec
        rec.image_new = target
        if dry_run:
            LOGGER.info(f"[dry-run] mv {img_path} -> {target}")
        else:
            if target.exists() and on_conflict == "overwrite":
                try:
                    target.unlink()
                except Exception:
                    pass
            img_path.rename(target)
            img_path = target

    # 寻找并重命名标签：严格以图片 descriptor 为 stem 完全匹配；
    # 重命名目标：使 label 最终与目标图片同名（仅扩展名不同）
    txt_dir = img_path.parent.parent / "txt"
    if txt_dir.exists() and txt_dir.is_dir():
        label_path = txt_dir / f"{parsed.descriptor}.txt"
        if label_path.exists():
            rec.label_old = label_path
            new_label_path = label_path.with_name(final_img_stem + label_path.suffix)
            if new_label_path != label_path:
                target = resolve_conflict(new_label_path, on_conflict, dry_run)
                if target is None:
                    if rec.status == "pending":
                        rec.status = "ok:image_renamed_label_conflict_skipped"
                else:
                    rec.label_new = target
                    if dry_run:
                        LOGGER.info(f"[dry-run] mv {label_path} -> {target}")
                    else:
                        if target.exists() and on_conflict == "overwrite":
                            try:
                                target.unlink()
                            except Exception:
                                pass
                        label_path.rename(target)
                if rec.status == "pending":
                    rec.status = "ok:renamed"
            else:
                # 已经与目标图片同名（仅后缀不同）
                if rec.status == "pending":
                    rec.status = "ok:label_already_target"
        else:
            rec.status = "ok:no_label_found"

    return rec


def move_to_aggregate(rec: ActionRecord, root: Path, dry_run: bool, on_conflict: str) -> ActionRecord:
    if not rec.trainval:
        return rec
    # 计算目标目录
    img_src = rec.image_new or rec.image_old
    tv = rec.trainval
    img_dst_dir = root / tv
    lbl_dst_dir = root / "labels" / tv
    ensure_dir(img_dst_dir, dry_run)
    ensure_dir(lbl_dst_dir, dry_run)

    # 移动图片
    target_img = resolve_conflict(img_dst_dir / img_src.name, on_conflict, dry_run)
    if target_img is not None:
        rec.moved_image_to = target_img
        if dry_run:
            LOGGER.info(f"[dry-run] mv {img_src} -> {target_img}")
        else:
            if target_img.exists() and on_conflict == "overwrite":
                try:
                    target_img.unlink()
                except Exception:
                    pass
            shutil.move(str(img_src), str(target_img))

    # 移动标签（若存在）
    lbl_src = rec.label_new or rec.label_old
    if lbl_src and lbl_src.exists():
        target_lbl = resolve_conflict(lbl_dst_dir / lbl_src.name, on_conflict, dry_run)
        if target_lbl is not None:
            rec.moved_label_to = target_lbl
            if dry_run:
                LOGGER.info(f"[dry-run] mv {lbl_src} -> {target_lbl}")
            else:
                if target_lbl.exists() and on_conflict == "overwrite":
                    try:
                        target_lbl.unlink()
                    except Exception:
                        pass
                shutil.move(str(lbl_src), str(target_lbl))

    return rec


# ------------------------------
# 主流程
# ------------------------------


def iter_pic_files(root: Path) -> Iterable[Path]:
    """遍历 root/class/**/pic/*.image 与 root/class_unknown/**/pic/*.image"""
    for bucket in ("class", "class_unknown"):
        base = root / bucket
        if not base.exists():
            continue
        for cat in base.iterdir():
            if not cat.is_dir():
                continue
            pic_dir = cat / "pic"
            if not pic_dir.exists():
                continue
            for f in pic_dir.iterdir():
                if f.is_file() and is_image(f):
                    yield f


def run(root: Path, dry_run: bool, on_conflict: str, verbose: bool, report_csv: Optional[Path]) -> None:
    actions: List[ActionRecord] = []
    total = 0
    for img in iter_pic_files(root):
        total += 1
        rec = rename_image_and_label(img, root, dry_run, on_conflict, verbose)
        rec = move_to_aggregate(rec, root, dry_run, on_conflict)
        actions.append(rec)

    # 汇总
    ok = sum(1 for a in actions if a.status.startswith("ok"))
    skipped = sum(1 for a in actions if a.status.startswith("skip"))
    LOGGER.info(f"Processed images: {total}, OK: {ok}, Skipped: {skipped}")

    if report_csv:
        if dry_run:
            LOGGER.info(f"[dry-run] write report -> {report_csv}")
        else:
            ensure_dir(report_csv.parent, dry_run=False)
            with report_csv.open("w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow([
                    "image_old", "image_new", "label_old", "label_new",
                    "trainval", "moved_image_to", "moved_label_to", "status",
                ])
                for a in actions:
                    w.writerow([
                        str(a.image_old), str(a.image_new or ""),
                        str(a.label_old or ""), str(a.label_new or ""),
                        a.trainval or "", str(a.moved_image_to or ""), str(a.moved_label_to or ""), a.status,
                    ])
            LOGGER.info(f"Report written: {report_csv}")


def main():
    ap = argparse.ArgumentParser(description="Tag & Label Renamer + Aggregator")
    ap.add_argument("--root", required=True, help="class_all 根目录路径")
    ap.add_argument("--execute", action="store_true", help="实际执行（默认仅dry-run预览）")
    ap.add_argument("--on-conflict", choices=["skip", "overwrite", "rename"], default="skip", help="文件名冲突策略")
    ap.add_argument("--verbose", action="store_true", help="输出更多调试信息")
    ap.add_argument("--report", default=None, help="输出CSV报告路径，可选")
    ap.add_argument("--log", default=None, help="日志文件路径。若未指定且为dry-run，将默认写入 root/logs/tag_renamer_dryrun_<timestamp>.log")

    args = ap.parse_args()
    root = Path(args.root)
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"root 不存在或不是目录: {root}")

    dry_run = not args.execute
    report_csv = Path(args.report) if args.report else None

    # 设置日志
    log_path: Optional[Path] = None
    if args.log:
        log_path = Path(args.log)
    elif dry_run:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = root / "logs" / f"tag_renamer_dryrun_{ts}.log"

    setup_logger(log_path, args.verbose)

    LOGGER.info(f"root={root}")
    LOGGER.info(f"mode={'dry-run' if dry_run else 'execute'} on_conflict={args.on_conflict}")
    run(root=root, dry_run=dry_run, on_conflict=args.on_conflict, verbose=args.verbose, report_csv=report_csv)

# ------------------------------
# 日志配置
# ------------------------------

def setup_logger(log_path: Optional[Path], verbose: bool) -> logging.Logger:
    LOGGER.setLevel(logging.DEBUG if verbose else logging.INFO)
    # 清空旧 handler，避免重复
    if LOGGER.handlers:
        for h in list(LOGGER.handlers):
            LOGGER.removeHandler(h)

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG if verbose else logging.INFO)
    sh.setFormatter(fmt)
    LOGGER.addHandler(sh)

    if log_path is not None:
        ensure_dir(log_path.parent, dry_run=False)
        fh = logging.FileHandler(str(log_path), encoding="utf-8")
        fh.setLevel(logging.DEBUG if verbose else logging.INFO)
        fh.setFormatter(fmt)
        LOGGER.addHandler(fh)
        LOGGER.info(f"Logging to file: {log_path}")

    return LOGGER


if __name__ == "__main__":
    main()
