"""File storage utilities for survey data.

Provides:
- load_data(filepath): Load list of survey dicts from JSON file.
- save_data(filepath, data): Save list of survey dicts to JSON file.

Both functions ensure robustness with proper exception handling.
"""
from __future__ import annotations
import json
from typing import List, Dict


def load_data(filepath: str) -> List[Dict]:
    """Load surveys from a JSON file.

    Requirements:
    - If the file does not exist, return an empty list.
    - If the file is corrupted (invalid JSON), return an empty list and warn.
    - If the content is not a list, also return an empty list and warn.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        else:
            print("警告：surveys.json 内容不是列表结构，已忽略并返回空列表。")
            return []
    except FileNotFoundError:
        # First run: file may not exist
        return []
    except json.JSONDecodeError:
        print("警告：surveys.json 文件损坏或不是合法的 JSON，已返回空列表。")
        return []


def save_data(filepath: str, data: List[Dict]) -> None:
    """Save surveys to a JSON file.

    Overwrites the whole file with pretty-printed JSON.
    """
    # Ensure data is a list for safety
    if not isinstance(data, list):
        raise ValueError("save_data 期望 data 为列表类型")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
