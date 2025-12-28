#!/usr/bin/env python3
"""
RePatcher: 在 PicTxtPatcher 处理完成、且图片被手动跨类移动后，
根据图片在 pic/ 下的当前位置，自动将对应的标注 txt 从原 class/txt 目录
迁移到正确的 class/txt 目录。

核心规则（与 PicTxtPatcher 保持一致）：
- 图片文件名示例：
  - Ada_2024_3_8_20_45-30_train.png  -> 标注：Ada_2024_3_8_20_45-30.txt
  - 2024_3_18_17_19_hash-5_val.png   -> 标注：2024_3_18_17_19_hash-5.txt
- 即：去掉扩展名与末尾的 "_train" 或 "_val" 后，加上 ".txt"。

扫描范围：
- {base}/class/**/pic 下的所有图片
- {base}/class_unknown/**/pic 下的所有图片（可通过 --no-unknown 关闭）
- 在所有 {base}/(class|class_unknown)/**/txt 下查找对应的 txt 文件。
- 可选：在 {base}/labels/train 与 {base}/labels/val 下回退查找（--labels-fallback）。

默认行为：
- 若在其他类的 txt 下找到唯一标注，则移动到图片所在类的 txt/ 下。
- 若目标已存在同名 txt：默认跳过，可用 --overwrite 覆盖；
  可用 --cleanup-duplicate 在内容一致时删除源重复文件。
- 若在多个位置均存在同名 txt：默认跳过（安全），可用 --prefer-latest 选最新修改时间者。

依赖：仅标准库。
"""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
import sys
import hashlib


IMG_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}


def _strip_class_duplicate_suffix(name: str) -> str:
    # 去掉任意次末尾的 _class_duplicate
    while name.endswith("_class_duplicate"):
        name = name[: -len("_class_duplicate")]
    return name


def _strip_trailing_numeric_groups(name: str) -> str:
    """去掉末尾形如 _123 或 _45 的数字段，可连续多次（如 _91_1）。"""
    changed = True
    s = name
    while changed and s:
        changed = False
        idx = s.rfind("_")
        if idx != -1:
            tail = s[idx + 1 :]
            if tail.isdigit():
                s = s[:idx]
                changed = True
    return s


def candidate_txt_names_from_image_filename(fname: str) -> List[str]:
    """生成可能的 txt 文件名候选列表（按优先级排序）。

    新规范：tag_train/val_class_duplicate.png
    - 标注没有 _class_duplicate 后缀，需要忽略该后缀。
    - 兼容两种情况：
      1) 旧规则：标注不包含 _train/_val，优先尝试 base.txt
      2) 某些数据：标注包含 _train/_val，回退尝试 base_train.txt 或 base_val.txt
    """
    stem = Path(fname).stem
    stem = _strip_class_duplicate_suffix(stem)

    # 先去掉尾部的数字分段，再识别 _train/_val，再次去掉可能残留的数字分段
    s = _strip_trailing_numeric_groups(stem)
    tv_suffix: Optional[str] = None
    if s.endswith("_train"):
        s = s[: -len("_train")]
        tv_suffix = "_train"
    elif s.endswith("_val"):
        s = s[: -len("_val")]
        tv_suffix = "_val"

    s = _strip_trailing_numeric_groups(s)

    candidates: List[str] = []
    if s:
        # 优先：无 _train/_val 的标准 txt 名
        candidates.append(s + ".txt")
        # 回退：包含 _train/_val 的 txt 名（部分数据集保留该后缀）
        if tv_suffix:
            candidates.append(s + tv_suffix + ".txt")

    # 去重保持顺序
    seen = set()
    uniq: List[str] = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            uniq.append(c)
    return uniq


def iter_image_files(pic_dir: Path) -> Iterable[Path]:
    for p in pic_dir.glob("*"):
        if p.is_file() and p.suffix.lower() in IMG_EXTS:
            yield p


def sha1sum(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class MoveDecision:
    image: Path
    txt_name: str  # 选中的目标 txt 文件名（或候选中的第一个）
    desired_txt_dir: Path
    found_sources: List[Path]
    chosen_source: Optional[Path]
    reason: str


@dataclass
class Stats:
    images_scanned: int = 0
    already_correct: int = 0
    moved: int = 0
    skipped_existing_dest: int = 0
    skipped_multi_sources: int = 0
    not_found: int = 0
    errors: int = 0
    cleaned_duplicates: int = 0


def build_all_txt_index(base: Path, include_unknown: bool = True) -> Dict[str, List[Path]]:
    """构建所有 txt 文件的索引：文件名 -> [路径列表]。
    仅在 {base}/class 与（可选）{base}/class_unknown 下的 txt 目录中查找。
    """
    index: Dict[str, List[Path]] = {}

    def add_from(root: Path):
        for txt_dir in root.glob("**/txt"):
            if not txt_dir.is_dir():
                continue
            for t in txt_dir.glob("*.txt"):
                index.setdefault(t.name, []).append(t)

    class_dir = base / "class"
    if class_dir.is_dir():
        add_from(class_dir)
    if include_unknown:
        cu = base / "class_unknown"
        if cu.is_dir():
            add_from(cu)
    return index


def find_class_root(base: Path, path: Path) -> Optional[Tuple[Path, str]]:
    """给定任意 path，返回 (类目录路径, 类名)；例如 base/class/Ada/pic/x.png -> (base/class/Ada, 'Ada')。
    若无法解析，返回 None。
    """
    try:
        parts = path.resolve().parts
        base_parts = base.resolve().parts
        # 找到 'class' 或 'class_unknown' 后的下一个即类名
        for i in range(len(base_parts), len(parts)):
            if parts[i] in ("class", "class_unknown"):
                if i + 1 < len(parts):
                    class_name = parts[i + 1]
                    class_dir = Path(*parts[: i + 2])
                    return class_dir, class_name
        return None
    except Exception:
        return None


def choose_one(paths: List[Path], prefer_latest: bool) -> Optional[Path]:
    if not paths:
        return None
    if len(paths) == 1:
        return paths[0]
    if prefer_latest:
        return max(paths, key=lambda p: p.stat().st_mtime)
    return None


def plan_moves(
    base: Path,
    include_unknown: bool,
    prefer_latest: bool,
    labels_fallback: bool,
) -> List[MoveDecision]:
    """为所有图片生成迁移决策列表。"""
    decisions: List[MoveDecision] = []
    txt_index = build_all_txt_index(base, include_unknown)

    def collect_pic_dirs(root: Path) -> List[Path]:
        return [p for p in root.glob("**/pic") if p.is_dir()]

    pic_dirs: List[Path] = []
    class_dir = base / "class"
    if class_dir.is_dir():
        pic_dirs += collect_pic_dirs(class_dir)
    if include_unknown:
        cu = base / "class_unknown"
        if cu.is_dir():
            pic_dirs += collect_pic_dirs(cu)

    # labels fallback 目录
    labels_train = base / "labels" / "train"
    labels_val = base / "labels" / "val"

    for pic_dir in pic_dirs:
        class_root = find_class_root(base, pic_dir)
        if not class_root:
            continue
        class_dir_path, class_name = class_root
        desired_txt_dir = class_dir_path / "txt"

        for img in iter_image_files(pic_dir):
            cand_names = candidate_txt_names_from_image_filename(img.name)
            if not cand_names:
                decisions.append(MoveDecision(img, "", desired_txt_dir, [], None, "cannot-extract-txt-name"))
                continue

            # 收集所有候选的来源路径
            found_list: List[Path] = []
            path_to_name: Dict[Path, str] = {}
            for name in cand_names:
                for p in txt_index.get(name, []):
                    found_list.append(p)
                    path_to_name[p] = name

            # 若 labels 回退开启，且尚未发现，则尝试在 labels 下查找候选名
            if labels_fallback and not found_list:
                for name in cand_names:
                    for labdir in (labels_train, labels_val):
                        cand = labdir / name
                        if cand.is_file():
                            found_list.append(cand)
                            path_to_name[cand] = name

            # 若目标目录已存在任意候选名，则视为已就位
            already = None
            for name in cand_names:
                p = desired_txt_dir / name
                if p.exists():
                    already = p
                    break
            if already is not None and already in found_list:
                decisions.append(MoveDecision(img, already.name, desired_txt_dir, [already], already, "already-correct"))
                continue
            elif already is not None and already.exists():
                # 目标已有，但源索引没包含（例如 labels fallback 情况），也直接视为已就位
                decisions.append(MoveDecision(img, already.name, desired_txt_dir, [already], already, "already-correct"))
                continue

            chosen = choose_one(found_list, prefer_latest)
            if chosen is None and len(found_list) > 1:
                decisions.append(MoveDecision(img, cand_names[0], desired_txt_dir, found_list, None, "multi-sources"))
            elif chosen is None and not found_list:
                decisions.append(MoveDecision(img, cand_names[0], desired_txt_dir, [], None, "not-found"))
            else:
                # 将 txt_name 设为与 chosen 对应的文件名
                assert chosen is not None
                chosen_name = path_to_name.get(chosen, cand_names[0])
                decisions.append(MoveDecision(img, chosen_name, desired_txt_dir, found_list, chosen, "move-needed"))

    return decisions


def apply_moves(
    decisions: List[MoveDecision],
    dry_run: bool,
    overwrite: bool,
    cleanup_duplicate: bool,
) -> Stats:
    stats = Stats()
    for d in decisions:
        stats.images_scanned += 1
        try:
            if d.reason == "already-correct":
                stats.already_correct += 1
                continue
            if d.reason == "not-found":
                stats.not_found += 1
                continue
            if d.reason == "multi-sources" and d.chosen_source is None:
                stats.skipped_multi_sources += 1
                continue
            if d.reason not in {"move-needed", "multi-sources"}:
                # 其他情况，如 cannot-extract-txt-name
                stats.errors += 1
                continue

            assert d.chosen_source is not None
            src = d.chosen_source
            dst_dir = d.desired_txt_dir
            dst_dir.mkdir(parents=True, exist_ok=True)
            dst = dst_dir / d.txt_name

            if dst.exists():
                if overwrite:
                    if not dry_run:
                        shutil.move(str(src), str(dst))
                    stats.moved += 1
                else:
                    # 若内容相同，且启用清理，则删除源重复文件
                    if cleanup_duplicate and src.is_file() and dst.is_file():
                        try:
                            if sha1sum(src) == sha1sum(dst):
                                if not dry_run:
                                    src.unlink()
                                stats.cleaned_duplicates += 1
                                # 视为已在目标处，无需计为 skipped_existing_dest
                                continue
                        except Exception:
                            pass
                    stats.skipped_existing_dest += 1
                continue

            # 正常移动；从 labels 回退源复制的情况，src 可能在 labels 下，我们也统一用 move，若想保留 labels 可改为 copy。
            if not dry_run:
                # 若源在 labels 下，则采用 copy 到目标 + 保留源（更安全）
                if "/labels/" in str(src.as_posix()) or src.as_posix().endswith("/labels/train/" + d.txt_name) or src.as_posix().endswith("/labels/val/" + d.txt_name):
                    shutil.copy2(str(src), str(dst))
                else:
                    shutil.move(str(src), str(dst))
            stats.moved += 1
        except Exception:
            stats.errors += 1
    return stats


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Move txt annotations to follow images' new classes after manual moves")
    p.add_argument("--base", required=True, help="base 目录（包含 class、class_unknown、labels）")
    p.add_argument("--no-unknown", action="store_true", help="不扫描 class_unknown")
    p.add_argument("--dry-run", action="store_true", help="仅显示将要执行的动作，不实际移动")
    p.add_argument("--overwrite", action="store_true", help="若目标已存在同名文件则覆盖")
    p.add_argument("--cleanup-duplicate", action="store_true", help="当源与目标内容一致时删除源重复文件（安全清理）")
    p.add_argument("--prefer-latest", action="store_true", help="当同名 txt 存在多个来源时，选择修改时间最新者；否则跳过")
    p.add_argument("--labels-fallback", action="store_true", help="在 base/labels/train,val 下回退查找缺失的 txt（复制到目标，保留源）")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    base = Path(args.base).expanduser().resolve()
    include_unknown = not args.no_unknown

    if not base.exists():
        print(f"[ERROR] base 不存在: {base}")
        return 2

    decisions = plan_moves(
        base=base,
        include_unknown=include_unknown,
        prefer_latest=args.prefer_latest,
        labels_fallback=args.labels_fallback,
    )

    # 简短预览
    will_move = [d for d in decisions if d.reason in ("move-needed", "multi-sources") and d.chosen_source is not None]
    print(f"将处理图片: {len(decisions)}，计划移动的标注: {len(will_move)}，dry-run={args.dry_run}")

    for d in will_move[:20]:  # 仅预览前 20 条
        print(f"MOVE {d.txt_name}: {d.chosen_source} -> {d.desired_txt_dir / d.txt_name}")
    if len(will_move) > 20:
        print(f"... 其余 {len(will_move) - 20} 项省略")

    stats = apply_moves(
        decisions=decisions,
        dry_run=args.dry_run,
        overwrite=args.overwrite,
        cleanup_duplicate=args.cleanup_duplicate,
    )

    print("\n=== Summary ===")
    print(f"images_scanned       : {stats.images_scanned}")
    print(f"already_correct      : {stats.already_correct}")
    print(f"moved                : {stats.moved}")
    print(f"skipped_existing_dest: {stats.skipped_existing_dest}")
    print(f"skipped_multi_sources: {stats.skipped_multi_sources}")
    print(f"not_found            : {stats.not_found}")
    print(f"cleaned_duplicates   : {stats.cleaned_duplicates}")
    print(f"errors               : {stats.errors}")

    # 打印未找到的详细信息，便于排查
    if stats.not_found > 0:
        print("\n=== Not Found Details ===")
        for d in decisions:
            if d.reason == "not-found":
                cands = candidate_txt_names_from_image_filename(d.image.name)
                print(f"- IMG: {d.image}")
                print(f"  candidates: {', '.join(cands) if cands else '(none)'}")
                print(f"  target_dir: {d.desired_txt_dir}")
                print(f"  labels_fallback: {args.labels_fallback}")

    # 返回码：有错误返回 1，否则 0
    return 1 if stats.errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
