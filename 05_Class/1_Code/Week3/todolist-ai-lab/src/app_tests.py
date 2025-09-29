# app_tests.py
# 目的：通过交互选项或一次性批量运行，打印“实际 vs 期望”，为学生制造可截图的失败证据
from pathlib import Path
from todo_io import write_tasks, read_tasks
from todo_logic import add_task, filter_tasks, longest_title_length, top_k_words

DATA = Path("todo.txt")

def scenario_1_utf8_roundtrip():
    print("=== 场景1：UTF-8 中文往返读写 ===")
    titles = ["买牛奶", "学习 Python", "写周报", "中文内容：你好，世界！"]
    write_tasks(DATA, titles)               # 期望：显式 encoding + with
    got = read_tasks(DATA)                  # 期望：显式 encoding
    print("写入:", titles)
    print("读取:", got)
    print("结果是否一致:", got == titles)   # 初始实现常见为 False/或异常
    print()

def scenario_2_missing_file_should_raise():
    print("=== 场景2：缺失文件应抛 FileNotFoundError ===")
    missing = Path("not_exist.txt")
    if missing.exists():
        missing.unlink()
    try:
        _ = read_tasks(missing)             # 期望：抛 FileNotFoundError
        print("未抛异常 ❌（期望抛 FileNotFoundError）")
    except FileNotFoundError:
        print("正确：抛出 FileNotFoundError ✅")
    print()

def scenario_3_add_task_dedup_keep_order():
    print("=== 场景3：添加任务需保序去重（性能可优化） ===")
    tasks = []
    for t in ["A", "B", "A", "C", "B", "D"]:
        tasks = add_task(tasks, t)
    print("输出:", tasks)
    print("期望: ['A', 'B', 'C', 'D']")
    print("结果是否正确:", tasks == ["A","B","C","D"])
    print("提示：虽然正确，但当前实现是 O(n^2)，可让 AI 优化为线性。")
    print()

def scenario_4_filter_logic_and_vs_or():
    print("=== 场景4：过滤逻辑应为 AND 而非 OR ===")
    tasks = ["buy milk", "write report", "learn python", "buy book"]
    done  = [False, True, False, True]
    # keyword='buy' 且 done=True -> 应该只保留既包含 'buy' 又已完成的任务：["buy book"]
    got = filter_tasks(tasks, keyword="buy", done_flags=done)
    print("输入:", list(zip(tasks, done)))
    print("过滤条件: keyword='buy' 且 done=True（期望 AND）")
    print("输出:", got)
    print("期望: ['buy book']")
    print("结果是否正确:", got == ["buy book"])  # 初始实现多半返回包含 'buy' 或 done=True 的更多项 -> False
    print()

def scenario_5_longest_title_length_and_empty():
    print("=== 场景5：最大标题长度 & 空列表边界 ===")
    titles = ["A", "study", "喝水", "refactor function"]
    print("输入:", titles)
    print("最大长度(期望 17):", longest_title_length(titles))  # "refactor function" 长度 17
    try:
        print("空列表测试（期望抛 ValueError）:")
        longest_title_length([])
        print("未抛出异常 ❌")
    except ValueError:
        print("正确：空列表抛 ValueError ✅")
    except Exception as e:
        print("抛出了其他异常 ❌", repr(e))
    print()

def scenario_6_top_k_words_case_and_perf():
    print("=== 场景6：Top-K 词频（大小写统一 & 性能） ===")
    titles = [
        "Buy Milk", "buy milk", "learn Python", "Learn python",
        "write report", "Buy book"
    ]
    # 期望大小写统一后：
    # buy(3), milk(2), python(2) 前三
    got = top_k_words(titles, k=3)
    print("输入:", titles)
    print("输出:", got)
    print("示例期望 (大小写统一后的一种可能): [('buy', 3), ('milk', 2), ('python', 2)]")
    print("提示：当前实现未归一化大小写，且存在 O(n^2) 可优化点。")
    print()

def run_all():
    scenario_1_utf8_roundtrip()
    scenario_2_missing_file_should_raise()
    scenario_3_add_task_dedup_keep_order()
    scenario_4_filter_logic_and_vs_or()
    scenario_5_longest_title_length_and_empty()
    scenario_6_top_k_words_case_and_perf()

def menu():
    while True:
        print("""
====== ToDoList 功能自检（打印版）======
1) UTF-8 中文往返读写
2) 缺失文件应抛 FileNotFoundError
3) 添加任务：保序去重（性能可优化）
4) 过滤逻辑：AND vs OR
5) 最大标题长度 & 空列表边界
6) Top-K 词频（大小写统一 & 性能）
7) 一次性运行全部
0) 退出
""")
        choice = input("选择功能编号：").strip()
        if choice == "1": scenario_1_utf8_roundtrip()
        elif choice == "2": scenario_2_missing_file_should_raise()
        elif choice == "3": scenario_3_add_task_dedup_keep_order()
        elif choice == "4": scenario_4_filter_logic_and_vs_or()
        elif choice == "5": scenario_5_longest_title_length_and_empty()
        elif choice == "6": scenario_6_top_k_words_case_and_perf()
        elif choice == "7": run_all()
        elif choice == "0": break
        else:
            print("无效选项，请重试。")

if __name__ == "__main__":
    menu()
