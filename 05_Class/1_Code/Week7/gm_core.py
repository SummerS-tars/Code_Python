from typing import List, Tuple, Optional, Dict
import gm_data
SUBJECTS = gm_data.SUBJECTS


def valid_student_id(s: str) -> bool:
    return isinstance(s, str) and s.strip() != ""


def valid_subject(s: str) -> bool:
    return s in SUBJECTS


def valid_score(v: str) -> Optional[int]:
    try:
        n = int(v)
    except Exception:
        return None
    if 0 <= n <= 100:
        return n
    return None


def find_records(records: List[dict], student_id: str) -> List[Tuple[int, dict]]:
    out: List[Tuple[int, dict]] = []
    for idx, r in enumerate(records):
        if r.get("student_id") == student_id:
            out.append((idx, r))
    return out


def add_record(records: List[dict], student_id: str, subject: str, score: int) -> Tuple[bool, str]:
    for r in records:
        if r["student_id"] == student_id and r["subject"] == subject:
            return False, "重复记录：该学生已有此科目成绩。"
    records.append({"student_id": student_id, "subject": subject, "score": score})
    return True, "添加成功。"


def update_record(records: List[dict], index: int, new_score: int) -> Tuple[bool, str]:
    if 0 <= index < len(records):
        records[index]["score"] = new_score
        return True, "修改成功。"
    return False, "索引越界，修改失败。"


def delete_record(records: List[dict], index: int) -> Tuple[bool, str]:
    if 0 <= index < len(records):
        records.pop(index)
        return True, "删除成功。"
    return False, "索引越界，删除失败。"


def subject_statistics(records: List[dict]) -> Dict[str, Dict[str, Optional[object]]]:
    stats: Dict[str, Dict[str, Optional[object]]] = {}
    for subj in SUBJECTS:
        subj_scores = [(r["student_id"], r["score"]) for r in records if r["subject"] == subj]
        if not subj_scores:
            stats[subj] = {"average": None, "max": None, "min": None}
            continue
        scores = [s for _, s in subj_scores]
        avg = sum(scores) / len(scores)
        max_score = max(scores)
        min_score = min(scores)
        max_students = [sid for sid, s in subj_scores if s == max_score]
        min_students = [sid for sid, s in subj_scores if s == min_score]
        stats[subj] = {
            "average": round(avg, 2),
            "max": {"score": max_score, "students": max_students},
            "min": {"score": min_score, "students": min_students},
        }
    return stats
