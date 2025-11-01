import json
import os
from typing import Dict, Tuple, Any

DATA_FILE = os.path.join(os.path.dirname(__file__), "grades_dict.json")
SUBJECTS = ["Math", "English", "Chinese", "Physics", "Chemistry"]


def load_data(path: str = DATA_FILE) -> Tuple[Dict[str, Dict[str, int]], int]:
    """Load records from JSON.

    Dictionary structure:
    { "S001": {"Math": 95, "English": 88}, ... }

    Backward compatibility: if file contains a list of dicts (list-version),
    convert to dict-structure.
    """
    records: Dict[str, Dict[str, int]] = {}
    skipped = 0
    if not os.path.exists(path):
        return records, skipped
    try:
        with open(path, "r", encoding="utf-8") as f:
            data: Any = json.load(f)
            if isinstance(data, dict):
                # Expected dict format
                for sid, subj_map in data.items():
                    if not isinstance(subj_map, dict):
                        skipped += 1
                        continue
                    sid_str = str(sid).strip()
                    if not sid_str:
                        skipped += 1
                        continue
                    records[sid_str] = {}
                    for subj, score in subj_map.items():
                        try:
                            subj_str = str(subj).strip()
                            score_int = int(score)
                        except Exception:
                            skipped += 1
                            continue
                        if subj_str and 0 <= score_int <= 100:
                            records[sid_str][subj_str] = score_int
                        else:
                            skipped += 1
            elif isinstance(data, list):
                # Convert from list-version
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
                        records.setdefault(sid, {})[subj] = score
                    else:
                        skipped += 1
            else:
                # Unknown format
                return {}, 0
    except Exception:
        # If file malformed, treat as empty but don't crash
        return {}, 0
    return records, skipped


def save_data(records: Dict[str, Dict[str, int]], path: str = DATA_FILE) -> bool:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False
