"""Main module for the survey CLI app.

Features:
- Ask 3 questions: name (str), age (int), favorite language (str from options)
- Append each completed survey to surveys.json (top-level list)
- Robust input handling with try/except and retries
- Loop until user chooses to exit
"""
from __future__ import annotations
from typing import Dict, List

from storage import load_data, save_data

SURVEYS_FILE = "surveys.json"  # store in current folder
LANGUAGE_OPTIONS = ["Python", "Java", "C++", "JavaScript", "Other"]


def ask_name() -> str:
    while True:
        name = input("您的姓名是？: ").strip()
        if name:
            return name
        print("姓名不能为空，请重新输入！")


def ask_age() -> int:
    while True:
        age_str = input("您的年龄是？(请输入整数): ").strip()
        try:
            age = int(age_str)
            if age < 0:
                print("年龄不能为负数，请重新输入！")
                continue
            return age
        except ValueError:
            print("年龄必须是数字，请重新输入！")


def ask_language() -> str:
    # Show options and accept case-insensitive input
    print("您最喜欢的编程语言是？可选:")
    print(", ".join(LANGUAGE_OPTIONS))
    while True:
        lang = input("请输入以上选项之一（不区分大小写），或直接输入 Other: ").strip()
        # Normalize for comparison but keep canonical casing from options
        for opt in LANGUAGE_OPTIONS:
            if lang.lower() == opt.lower():
                return opt
        # If not matching any option, treat as free text but label as Other
        if lang:
            # If user typed a custom value, keep it but still allow beyond options
            # Assignment requires type string; accepting any string fits.
            # We return exactly user input if it's not a predefined option.
            return lang
        print("输入不能为空，请重新输入！")


def collect_one_survey() -> Dict:
    name = ask_name()
    age = ask_age()
    language = ask_language()
    return {"name": name, "age": age, "language": language}


def should_continue() -> bool:
    while True:
        ans = input("是否要继续进行下一份问卷调查？(yes/no): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("请输入 yes 或 no！")


def main():
    print("欢迎使用问卷数据收集工具！")
    while True:
        survey = collect_one_survey()

        # Load existing data, append, then save
        surveys: List[Dict] = load_data(SURVEYS_FILE)
        surveys.append(survey)
        save_data(SURVEYS_FILE, surveys)

        print("本次问卷已成功保存到 surveys.json。")
        if not should_continue():
            print("感谢您的参与，程序已退出。")
            break


if __name__ == "__main__":
    main()
