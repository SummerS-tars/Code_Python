"""
示例：演示 Python 中循环结构

包含演示：
- while 循环
- for 循环
- 循环控制：break, continue, pass
- 嵌套循环

运行：
    python loops_demo.py

作者：自动生成示例（中文注释）
"""


def while_loop_demo():
    print('--- while 循环示例 ---')
    count = 1
    while count <= 5:
        print(f'计数：{count}')
        count += 1
    print()


def for_loop_demo():
    print('--- for 循环示例 ---')
    fruits = ['苹果', '香蕉', '橙子']
    for fruit in fruits:
        print(f'水果：{fruit}')
    print()

    # 遍历字符串
    for char in 'Python':
        print(f'字符：{char}')
    print()


def break_continue_pass_demo():
    print('--- break, continue, pass 示例 ---')

    # break 示例
    print('break 示例：遇到 3 时停止')
    for i in range(1, 6):
        if i == 3:
            break
        print(f'数字：{i}')
    print()

    # continue 示例
    print('continue 示例：跳过 3')
    for i in range(1, 6):
        if i == 3:
            continue
        print(f'数字：{i}')
    print()

    # pass 示例
    print('pass 示例：占位符')
    for i in range(1, 4):
        if i == 2:
            pass  # 不执行任何操作
        print(f'处理：{i}')
    print()


def nested_loops_demo():
    print('--- 嵌套循环示例 ---')
    for i in range(1, 4):  # 外层循环
        print(f'外层：{i}')
        for j in range(1, 4):  # 内层循环
            print(f'  内层：{i},{j}')
        print()
    print()


def main():
    while_loop_demo()
    for_loop_demo()
    break_continue_pass_demo()
    nested_loops_demo()


if __name__ == '__main__':
    main()