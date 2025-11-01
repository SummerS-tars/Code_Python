#!/usr/bin/env python3
"""grade_manager.py - main entrypoint that wires modules together.

This file is intentionally small: it imports the core, data, and display
modules (gm_core, gm_data, gm_display) and exposes the same interactive
CLI behavior as before.
"""
from __future__ import annotations

import sys
from gm_data import load_data, save_data, DATA_FILE
import gm_core as core
import gm_display as disp


def run_demo() -> None:
    print("运行 demo...")
    # always use fresh sample data for demo (don't load from file)
    records = []
    core.add_record(records, "S001", "Math", 95)
    core.add_record(records, "S001", "English", 88)
    core.add_record(records, "S002", "Math", 76)
    core.add_record(records, "S003", "Physics", 89)
    core.add_record(records, "S004", "Math", 95)

    disp.print_records(records)
    print("\n按学号查询 S001:")
    matches = core.find_records(records, "S001")
    for idx, r in matches:
        print(f"[{idx}] {r}")

    print("\n修改索引 1 的分数为 90:")
    ok, msg = core.update_record(records, 1, 90)
    print(msg)
    disp.print_records(records)

    print("\n删除索引 2 的记录:")
    ok, msg = core.delete_record(records, 2)
    print(msg)
    disp.print_records(records)

    print("\n科目统计:")
    disp.print_statistics(records)


def main_loop() -> None:
    records, skipped = load_data()
    if skipped:
        print(f"加载时跳过 {skipped} 条格式错误的记录。")

    while True:
        disp.clear_screen()
        print("\n主菜单：")
        print("1. 添加记录")
        print("2. 查询学号")
        print("3. 修改记录")
        print("4. 删除记录")
        print("5. 统计（按科目）")
        print("6. 列出所有记录")
        print("7. 保存并退出")
        print("8. 退出但不保存")
        choice = input("选择操作 (1-8): ").strip()

        if choice == "1":
            disp.clear_screen()
            sid = input("输入学号: ").strip()
            if not core.valid_student_id(sid):
                disp.display_message_interactive("学号不能为空。")
                continue
            print(f"可用科目：{', '.join(core.SUBJECTS)}")
            subj = input("输入科目: ").strip()
            if not core.valid_subject(subj):
                disp.display_message_interactive("科目无效（必须从预设科目中选择）。")
                continue
            sc = input("输入分数 (0-100): ").strip()
            n = core.valid_score(sc)
            if n is None:
                disp.display_message_interactive("分数无效，必须是 0-100 之间的整数。")
                continue
            ok, msg = core.add_record(records, sid, subj, n)
            disp.display_message_interactive(msg)
        elif choice == "2":
            disp.clear_screen()
            sid = input("输入要查询的学号: ").strip()
            matches = core.find_records(records, sid)
            if not matches:
                disp.display_message_interactive("未找到匹配记录。")
            else:
                matched_records = [r for _, r in matches]
                disp.display_records_interactive(matched_records, title=f"学号 {sid} 的记录：")
        elif choice == "3":
            disp.clear_screen()
            sid = input("输入要修改的学号: ").strip()
            matches = core.find_records(records, sid)
            if not matches:
                disp.display_message_interactive("未找到匹配记录。")
                continue
            for idx, r in matches:
                print(f"索引 {idx}: 科目={r['subject']} 分数={r['score']}")
            sel = input("输入要修改的记录索引: ").strip()
            try:
                sel_i = int(sel)
            except Exception:
                disp.display_message_interactive("索引无效。")
                continue
            sc = input("输入新分数 (0-100): ").strip()
            n = core.valid_score(sc)
            if n is None:
                disp.display_message_interactive("分数无效。")
                continue
            ok, msg = core.update_record(records, sel_i, n)
            disp.display_message_interactive(msg)
        elif choice == "4":
            disp.clear_screen()
            sid = input("输入要删除记录的学号: ").strip()
            matches = core.find_records(records, sid)
            if not matches:
                disp.display_message_interactive("未找到匹配记录。")
                continue
            for idx, r in matches:
                print(f"索引 {idx}: 科目={r['subject']} 分数={r['score']}")
            sel = input("输入要删除的记录索引: ").strip()
            try:
                sel_i = int(sel)
            except Exception:
                disp.display_message_interactive("索引无效。")
                continue
            ok, msg = core.delete_record(records, sel_i)
            disp.display_message_interactive(msg)
        elif choice == "5":
            disp.display_statistics_interactive(records, title="科目统计：")
        elif choice == "6":
            disp.display_records_interactive(records, title="所有记录：")
        elif choice == "7":
            disp.clear_screen()
            ok = save_data(records)
            if ok:
                disp.display_message_interactive(f"已保存到 {DATA_FILE}")
            else:
                disp.display_message_interactive("保存失败，请检查文件权限。")
            print("退出程序。")
            break
        elif choice == "8":
            disp.clear_screen()
            ans = input("确定不保存直接退出吗？(y/N): ").strip().lower()
            if ans == "y":
                disp.display_message_interactive("退出（未保存）。")
                break
            else:
                continue
        else:
            disp.display_message_interactive("无效选项，请输入 1-8。")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
        sys.exit(0)
    main_loop()
