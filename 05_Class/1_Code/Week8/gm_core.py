from typing import List, Dict, Tuple, Any

import gm_data

SUBJECTS = gm_data.SUBJECTS


def valid_student_id(student_id: str) -> bool:
    return isinstance(student_id, str) and student_id.strip() != ""


def valid_subject(subject: str) -> bool:
    return subject in SUBJECTS


def valid_score(score: int) -> bool:
    try:
        s = int(score)
    except Exception:
        return False
    return 0 <= s <= 100


def list_student_subjects(records: Dict[str, Dict[str, int]], student_id: str) -> List[Tuple[str, int]]:
    """Return list of (subject, score) for the given student_id."""
    subjects = records.get(student_id, {})
    # stable order by SUBJECTS then others
    ordered: List[Tuple[str, int]] = []
    for subj in SUBJECTS:
        if subj in subjects:
            ordered.append((subj, subjects[subj]))
    for subj, sc in subjects.items():
        if subj not in SUBJECTS:
            ordered.append((subj, sc))
    return ordered


def add_record(records: Dict[str, Dict[str, int]], student_id: str, subject: str, score: int) -> Tuple[bool, str]:
    if not valid_student_id(student_id):
        return False, "学号不能为空"
    if not valid_subject(subject):
        return False, f"科目必须是 {SUBJECTS} 之一"
    if not valid_score(score):
        return False, "分数必须是 0-100 的整数"

    score = int(score)
    if student_id not in records:
        records[student_id] = {}
    if subject in records[student_id]:
        return False, "该学号的该科目已存在，不能重复添加"
    records[student_id][subject] = score
    return True, "添加成功"


def update_record(records: Dict[str, Dict[str, int]], student_id: str, subject: str, new_score: int) -> Tuple[bool, str]:
    if not valid_score(new_score):
        return False, "分数必须是 0-100 的整数"
    if student_id not in records or subject not in records[student_id]:
        return False, "未找到该学号的该科目记录"
    records[student_id][subject] = int(new_score)
    return True, "修改成功"


def delete_record(records: Dict[str, Dict[str, int]], student_id: str, subject: str) -> Tuple[bool, str]:
    if student_id not in records or subject not in records[student_id]:
        return False, "未找到该学号的该科目记录"
    del records[student_id][subject]
    if not records[student_id]:
        # remove empty student bucket
        del records[student_id]
    return True, "删除成功"


def subject_statistics(records: Dict[str, Dict[str, int]]) -> Dict[str, Dict[str, Any]]:
    """Compute statistics per subject.

    Returns: {subject: {average: float|None, max: (sid,score)|None, min: (sid,score)|None, count: int}}
    """
    by_subject: Dict[str, List[Tuple[str, int]]] = {s: [] for s in SUBJECTS}
    for sid, subj_map in records.items():
        if not isinstance(subj_map, dict):
            continue
        for subj, score in subj_map.items():
            try:
                subj_str = str(subj)
                score_int = int(score)
            except Exception:
                continue
            if subj_str in by_subject and 0 <= score_int <= 100:
                by_subject[subj_str].append((sid, score_int))

    stats: Dict[str, Dict[str, Any]] = {}
    for subj in SUBJECTS:
        entries = by_subject.get(subj, [])
        if not entries:
            stats[subj] = {"average": None, "max": None, "min": None, "count": 0}
            continue
        total = sum(score for _, score in entries)
        avg = total / len(entries)
        max_entry = max(entries, key=lambda x: x[1])
        min_entry = min(entries, key=lambda x: x[1])
        stats[subj] = {
            "average": avg,
            "max": max_entry,  # (student_id, score)
            "min": min_entry,  # (student_id, score)
            "count": len(entries),
        }

    return stats
