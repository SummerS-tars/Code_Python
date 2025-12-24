"""
示例：演示 Python 中其他控制结构

包含演示：
- 列表推导式
- 生成器表达式
- 异常处理与控制结构的结合

运行：
    python advanced_control_demo.py

作者：自动生成示例（中文注释）
"""


def list_comprehension_demo():
    print('--- 列表推导式示例 ---')

    # 基本列表推导式
    squares = [x**2 for x in range(1, 6)]
    print('平方列表：', squares)

    # 带条件的列表推导式
    even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
    print('偶数平方列表：', even_squares)

    # 嵌套列表推导式
    matrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]
    print('乘法表：', matrix)
    print()


def generator_expression_demo():
    print('--- 生成器表达式示例 ---')

    # 生成器表达式
    gen = (x**2 for x in range(1, 6))
    print('生成器对象：', gen)
    print('转换为列表：', list(gen))

    # 使用生成器节省内存
    large_gen = (x for x in range(1000000) if x % 2 == 0)
    print('大生成器（前10个）：', [next(large_gen) for _ in range(10)])
    print()


def exception_with_control_demo():
    print('--- 异常处理与控制结构的结合示例 ---')

    # 在循环中使用异常处理
    numbers = ['1', '2', 'abc', '4', 'def']
    valid_numbers = []

    for item in numbers:
        try:
            num = int(item)
            valid_numbers.append(num)
        except ValueError:
            print(f'跳过无效项：{item}')

    print('有效数字列表：', valid_numbers)
    print()

    # 在列表推导式中使用异常处理（使用函数）
    def safe_int(x):
        try:
            return int(x)
        except ValueError:
            return None

    mixed_list = ['1', '2', 'abc', '4', 'def']
    converted = [safe_int(x) for x in mixed_list if safe_int(x) is not None]
    print('转换后的有效数字：', converted)
    print()


def main():
    list_comprehension_demo()
    generator_expression_demo()
    exception_with_control_demo()


if __name__ == '__main__':
    main()