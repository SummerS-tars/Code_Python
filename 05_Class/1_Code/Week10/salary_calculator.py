#!/usr/bin/env python3
"""
salary_calculator.py

一个可交互运行也可通过命令行参数运行的薪资计算器。

功能：
- 输入员工姓名、基本工资、奖金（交互或命令行参数）
- 计算应发工资（基本工资 + 奖金）
- 使用可配置的免征点和分级税率计算个税
- 输出格式化工资条

命令行示例：
python salary_calculator.py --name Alice --base 8000 --bonus 1200

作者: AI 生成（供课程作业使用）
"""
from __future__ import annotations
import argparse
from typing import List, Tuple
import json
import os


def calculate_gross(base_salary: float, bonus: float) -> float:
    """计算应发工资（基本工资 + 奖金）。"""
    return base_salary + bonus


def calculate_taxable(gross: float, threshold: float) -> float:
    """计算应纳税所得额（若小于等于免征点则为0）。"""
    taxable = gross - threshold
    return taxable if taxable > 0 else 0.0


def calculate_progressive_tax(taxable_income: float, brackets: List[Tuple[float, float]]) -> float:
    """
    根据分级税率计算税额。

    brackets: 列表，形如 [(upper1, rate1), (upper2, rate2), ..., (inf, rateN)]
    upper 是该档的累计上限（从小到大），rate 是该档的税率（小数表示）。
    """
    if taxable_income <= 0:
        return 0.0

    tax = 0.0
    prev_limit = 0.0
    remaining = taxable_income

    for upper, rate in brackets:
        if taxable_income <= prev_limit:
            break
        # 本档应税额 = min(upper - prev_limit, taxable_income - prev_limit)
        taxable_in_this_bracket = min(upper - prev_limit, taxable_income - prev_limit)
        if taxable_in_this_bracket > 0:
            tax += taxable_in_this_bracket * rate
        prev_limit = upper
    return tax


def format_salary_slip(name: str, gross: float, tax: float, net: float) -> str:
    """返回格式化的工资条字符串。"""
    lines = [
        "工资条",
        "——————————————",
        f"员工：{name}",
        f"应发工资：{gross:,.2f}",
        f"扣税金额：{tax:,.2f}",
        f"实发工资：{net:,.2f}",
        "——————————————",
    ]
    return "\n".join(lines)


def prompt_for_missing_values(name: str | None, base: float | None, bonus: float | None) -> Tuple[str, float, float]:
    """仅提示缺失的字段，保留已有的命令行参数值。"""
    final_name = name if name is not None else ""
    if not final_name:
        final_name = input("请输入员工姓名: ").strip() or "员工"

    final_base = base
    while final_base is None:
        try:
            s = input("请输入基本工资: ").strip()
            final_base = float(s)
        except ValueError:
            print("输入无效，请输入数字。")

    final_bonus = bonus
    while final_bonus is None:
        try:
            s = input("请输入奖金/津贴: ").strip()
            final_bonus = float(s) if s != "" else 0.0
        except ValueError:
            print("输入无效，请输入数字。")

    return final_name, final_base, final_bonus


def load_tax_config(path: str) -> Tuple[float, List[Tuple[float, float]]]:
    """从 JSON 配置加载免征点和分级税率。

    期望格式：
    {
      "threshold": 5000.0,
      "brackets": [[3000, 0.03], [12000, 0.10], ..., [null, 0.45]]
    }

    如果最后一档使用 null 或不填写上限，请使用 null 或 "inf" 表示无限大。
    """
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    threshold = float(cfg.get("threshold", 5000.0))
    raw_brackets = cfg.get("brackets", [])
    brackets: List[Tuple[float, float]] = []
    for upper, rate in raw_brackets:
        if upper is None or (isinstance(upper, str) and str(upper).lower() == "inf"):
            upper_val = float("inf")
        else:
            upper_val = float(upper)
        brackets.append((upper_val, float(rate)))

    return threshold, brackets


def main():
    parser = argparse.ArgumentParser(description="薪资计算器（可交互或命令行）")
    parser.add_argument("--name", help="员工姓名")
    parser.add_argument("--base", type=float, help="基本工资")
    parser.add_argument("--bonus", type=float, default=0.0, help="奖金/津贴")
    parser.add_argument("--threshold", type=float, default=5000.0, help="月度免征点/免税额，默认5000")
    parser.add_argument("--config", help="税率配置文件（JSON），默认查找同目录下的 tax_config.json")
    args = parser.parse_args()

    # 默认演示分级税率（示例）：
    # 该列表是逐级的累计上限（单位：同税前货币），税率为小数。
    # 可按课程或实际税表替换。
    default_brackets = [
        (3000.0, 0.03),
        (12000.0, 0.10),
        (25000.0, 0.20),
        (35000.0, 0.25),
        (55000.0, 0.30),
        (80000.0, 0.35),
        (float("inf"), 0.45),
    ]

    # 加载税率配置（优先使用 --config 指定的文件，否则查找同目录 tax_config.json）
    config_path = None
    if args.config:
        config_path = args.config
    else:
        # 尝试查找与当前脚本同目录下的 tax_config.json
        script_dir = os.path.dirname(os.path.abspath(__file__))
        candidate = os.path.join(script_dir, "tax_config.json")
        if os.path.exists(candidate):
            config_path = candidate

    if config_path:
        try:
            threshold, brackets = load_tax_config(config_path)
        except Exception as e:
            print(f"加载税率配置失败（{config_path}）：{e}，将使用默认税率与阈值。")
            threshold = args.threshold
            brackets = default_brackets
    else:
        threshold = args.threshold
        brackets = default_brackets

    # 对可能部分通过命令行提供的值，仅提示缺失项
    name, base, bonus = prompt_for_missing_values(args.name, args.base, args.bonus)

    gross = calculate_gross(base, bonus)
    taxable = calculate_taxable(gross, threshold)
    tax = calculate_progressive_tax(taxable, brackets)
    net = gross - tax

    print(format_salary_slip(name, gross, tax, net))


if __name__ == "__main__":
    main()
