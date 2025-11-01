from typing import List, Optional, Dict, Tuple, Any
import gm_core
from gm_core import subject_statistics
import gm_data
SUBJECTS = gm_data.SUBJECTS

# Optional precise width calculation for terminals (handles CJK width)
try:
    from wcwidth import wcswidth  # type: ignore
except Exception:
    wcswidth = None


def clear_screen() -> None:
    import os

    try:
        os.system("cls" if os.name == "nt" else "clear")
    except Exception:
        pass


def _disp_width(s: str) -> int:
    if wcswidth is None:
        return len(s)
    return max(0, wcswidth(s))


def _pad_right(s: str, width: int) -> str:
    cur = _disp_width(s)
    if cur >= width:
        return s
    return s + " " * (width - cur)


def _pad_left(s: str, width: int) -> str:
    cur = _disp_width(s)
    if cur >= width:
        return s
    return " " * (width - cur) + s


def _flatten_records(records: Dict[str, Dict[str, int]], filter_sid: Optional[str] = None) -> List[Tuple[str, str, int]]:
    rows: List[Tuple[str, str, int]] = []
    if filter_sid is not None:
        subj_map = records.get(filter_sid, {})
        for subj in SUBJECTS:
            if subj in subj_map:
                rows.append((filter_sid, subj, subj_map[subj]))
        for subj, score in subj_map.items():
            if subj not in SUBJECTS:
                rows.append((filter_sid, subj, score))
        return rows
    # all records
    for sid in sorted(records.keys()):
        subj_map = records[sid]
        for subj in SUBJECTS:
            if subj in subj_map:
                rows.append((sid, subj, subj_map[subj]))
        # include non-standard subjects
        for subj, score in subj_map.items():
            if subj not in SUBJECTS:
                rows.append((sid, subj, score))
    return rows


def print_records(records: Dict[str, Dict[str, int]], filter_sid: Optional[str] = None) -> None:
    rows = _flatten_records(records, filter_sid)
    if not rows:
        print("当前没有任何记录。")
        return

    hdr_idx = "Index"
    hdr_id = "StudentID"
    hdr_subj = "Subject"
    hdr_score = "Score"

    idx_w = max(_disp_width(hdr_idx), max((_disp_width(str(i)) for i in range(len(rows))), default=0))
    id_w = max(_disp_width(hdr_id), max((_disp_width(sid) for sid, _, _ in rows), default=0))
    subj_w = max(_disp_width(hdr_subj), max((_disp_width(subj) for _, subj, _ in rows), default=0))
    score_w = max(_disp_width(hdr_score), max((_disp_width(str(score)) for _, _, score in rows), default=0))

    print(f"{_pad_right(hdr_idx, idx_w)} | {_pad_right(hdr_id, id_w)} | {_pad_right(hdr_subj, subj_w)} | {_pad_right(hdr_score, score_w)}")
    print(f"{('-'*idx_w)}-+-{('-'*id_w)}-+-{('-'*subj_w)}-+-{('-'*score_w)}")
    for i, (sid, subj, score) in enumerate(rows):
        print(f"{_pad_left(str(i), idx_w)} | {_pad_right(sid, id_w)} | {_pad_right(subj, subj_w)} | {_pad_left(str(score), score_w)}")


def display_records_interactive(records: Dict[str, Dict[str, int]], title: Optional[str] = None, filter_sid: Optional[str] = None) -> None:
    clear_screen()
    if title:
        print(title)
    print_records(records, filter_sid)
    try:
        input("\n按 Enter 返回主菜单...")
    except Exception:
        pass
    clear_screen()


def print_statistics(records: Dict[str, Dict[str, int]]) -> None:
    stats = subject_statistics(records)
    col1 = "Subject"
    col2 = "Average"
    col3 = "Max(student)"
    col4 = "Min(student)"

    rows = []
    for subj in SUBJECTS:
        info = stats.get(subj, {})
        avg_val = info.get("average")
        if avg_val is None:
            avg_str = "-"
            maxs_str = "-"
            mins_str = "-"
        else:
            avg_str = f"{avg_val:.2f}"
            max_info = info.get("max")
            min_info = info.get("min")
            if isinstance(max_info, tuple) and len(max_info) == 2:
                maxs_str = f"{max_info[1]}({max_info[0]})"
            else:
                maxs_str = "-"
            if isinstance(min_info, tuple) and len(min_info) == 2:
                mins_str = f"{min_info[1]}({min_info[0]})"
            else:
                mins_str = "-"
        rows.append((subj, avg_str, maxs_str, mins_str))

    w1 = max(_disp_width(col1), max((_disp_width(r[0]) for r in rows), default=0))
    w2 = max(_disp_width(col2), max((_disp_width(r[1]) for r in rows), default=0))
    w3 = max(_disp_width(col3), max((_disp_width(r[2]) for r in rows), default=0))
    w4 = max(_disp_width(col4), max((_disp_width(r[3]) for r in rows), default=0))

    sep = f"+-{'-'*w1}-+-{'-'*w2}-+-{'-'*w3}-+-{'-'*w4}-+"
    header = f"| {_pad_right(col1, w1)} | {_pad_left(col2, w2)} | {_pad_right(col3, w3)} | {_pad_right(col4, w4)} |"
    print(sep)
    print(header)
    print(sep)
    for subj, avg_str, maxs_str, mins_str in rows:
        print(f"| {_pad_right(subj, w1)} | {_pad_left(avg_str, w2)} | {_pad_right(maxs_str, w3)} | {_pad_right(mins_str, w4)} |")
    print(sep)


def display_statistics_interactive(records: Dict[str, Dict[str, int]], title: Optional[str] = None) -> None:
    clear_screen()
    if title:
        print(title)
    print_statistics(records)
    try:
        input("\n按 Enter 返回主菜单...")
    except Exception:
        pass
    clear_screen()


def display_message_interactive(message: str) -> None:
    clear_screen()
    print(message)
    try:
        input("\n按 Enter 返回主菜单...")
    except Exception:
        pass
    clear_screen()
