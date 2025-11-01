import json
import os
from typing import List, Tuple

DATA_FILE = os.path.join(os.path.dirname(__file__), "grades.json")
SUBJECTS = ["Math", "English", "Chinese", "Physics", "Chemistry"]


def load_data(path: str = DATA_FILE) -> Tuple[List[dict], int]:
    records = []
    skipped = 0
    if not os.path.exists(path):
        return records, skipped
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                return [], 0
            for item in data:
                if (
                    isinstance(item, dict)
                    and "student_id" in item
                    and "subject" in item
                    and "score" in item
                ):
                    try:
                        sid = str(item["student_id"]).strip()
                        subj = str(item["subject"]).strip()
                        score = int(item["score"])
                    except Exception:
                        skipped += 1
                        continue
                    if sid == "" or subj == "" or not (0 <= score <= 100):
                        skipped += 1
                        continue
                    records.append({"student_id": sid, "subject": subj, "score": score})
                else:
                    skipped += 1
    except Exception:
        return [], 0
    return records, skipped


def save_data(records: List[dict], path: str = DATA_FILE) -> bool:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False
