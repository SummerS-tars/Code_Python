"""
示例：演示 Python 中错误的分类

包含演示：
- 语法错误（Syntax Error）：代码不符合语法规则，无法解析。
- 运行时错误（Runtime Error）：执行时发生的异常，如 NameError, TypeError 等。
- 逻辑错误（Logical Error）：代码运行但结果错误。

运行：
    python error_types_demo.py

注意：语法错误示例被注释掉，避免运行时崩溃。

作者：自动生成示例（中文注释）
"""


def syntax_error_demo():
    print('--- 语法错误示例 ---')
    print('语法错误：代码不符合 Python 语法规则，导致解析失败。')
    print('示例（注释掉以避免错误）：')
    print('# print("Hello World"  # 缺少右括号')
    print('# 或 if True print("yes")  # 缺少冒号')
    print('这些会导致 SyntaxError，无法运行。')
    print()


def runtime_error_demo():
    print('--- 运行时错误示例 ---')

    # NameError: 变量未定义
    try:
        print(undefined_var)
    except NameError as e:
        print(f'NameError: {e}')

    # TypeError: 类型不兼容
    try:
        result = "hello" + 5
    except TypeError as e:
        print(f'TypeError: {e}')

    # ValueError: 值不合法
    try:
        num = int("abc")
    except ValueError as e:
        print(f'ValueError: {e}')

    # ZeroDivisionError: 除以零
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f'ZeroDivisionError: {e}')

    # IndexError: 索引超出范围
    try:
        lst = [1, 2, 3]
        print(lst[5])
    except IndexError as e:
        print(f'IndexError: {e}')

    # KeyError: 字典键不存在
    try:
        d = {"a": 1}
        print(d["b"])
    except KeyError as e:
        print(f'KeyError: {e}')

    print()


def logical_error_demo():
    print('--- 逻辑错误示例 ---')
    print('逻辑错误：代码语法正确，能运行，但结果不符合预期。')
    # 示例：计算平均值时忘记转换为 float
    scores = [85, 90, 78, 92, 88]
    total = sum(scores)
    count = len(scores)
    average = total / count  # 这是正确的，但假设逻辑错误：average = total // count
    print(f'分数：{scores}')
    print(f'总分：{total}，数量：{count}')
    print(f'平均分（正确）：{average}')

    # 模拟逻辑错误：使用整除，导致精度丢失
    wrong_average = total // count
    print(f'平均分（逻辑错误，整除）：{wrong_average}  # 丢失小数部分')
    print('逻辑错误需要通过测试和调试发现。')
    print()


def main():
    syntax_error_demo()
    runtime_error_demo()
    logical_error_demo()


if __name__ == '__main__':
    main()