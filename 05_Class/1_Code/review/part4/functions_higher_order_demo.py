"""
示例：演示 Python 中高阶函数与 Lambda 表达式

包含演示：
- map() 函数
- filter() 函数
- sorted() 函数（自定义排序规则）
- Lambda 表达式基础
- Lambda 与高阶函数结合

运行：
    python functions_higher_order_demo.py

作者：自动生成示例（中文注释）
"""


def map_demo():
    """map() 函数示例"""
    print('--- map() 函数示例 ---')
    
    def square(x):
        return x ** 2
    
    numbers = [1, 2, 3, 4, 5]
    squared = list(map(square, numbers))
    print(f'{numbers} 平方后：{squared}')
    
    # 使用 lambda
    squared_lambda = list(map(lambda x: x ** 2, numbers))
    print(f'使用 lambda：{squared_lambda}')


def filter_demo():
    """filter() 函数示例"""
    print('--- filter() 函数示例 ---')
    
    def is_even(x):
        return x % 2 == 0
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    evens = list(filter(is_even, numbers))
    print(f'{numbers} 中的偶数：{evens}')
    
    # 使用 lambda
    evens_lambda = list(filter(lambda x: x % 2 == 0, numbers))
    print(f'使用 lambda：{evens_lambda}')


def sorted_with_key():
    """sorted() 函数自定义排序规则"""
    print('--- sorted() 函数示例 ---')
    
    students = [
        {'name': 'Alice', 'score': 85},
        {'name': 'Bob', 'score': 90},
        {'name': 'Charlie', 'score': 78}
    ]
    
    # 按分数排序
    sorted_by_score = sorted(students, key=lambda s: s['score'])
    print('按分数排序：')
    for student in sorted_by_score:
        print(f'  {student["name"]}: {student["score"]}')
    
    # 按名字排序
    sorted_by_name = sorted(students, key=lambda s: s['name'])
    print('按名字排序：')
    for student in sorted_by_name:
        print(f'  {student["name"]}: {student["score"]}')


def lambda_basics():
    """Lambda 表达式基础"""
    print('--- Lambda 表达式基础 ---')
    
    # 简单 lambda
    add = lambda x, y: x + y
    print(f'add(3, 5) = {add(3, 5)}')
    
    # 条件 lambda
    max_value = lambda a, b: a if a > b else b
    print(f'max_value(10, 20) = {max_value(10, 20)}')
    
    # 列表生成的 lambda
    operations = [
        lambda x: x + 10,
        lambda x: x * 2,
        lambda x: x ** 2
    ]
    
    for i, op in enumerate(operations):
        print(f'operations[{i}](5) = {op(5)}')


def lambda_with_map_filter():
    """Lambda 与 map/filter 结合"""
    print('--- Lambda 与高阶函数结合 ---')
    
    # 链式操作
    numbers = [1, 2, 3, 4, 5]
    
    # 过滤偶数，然后平方
    result = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numbers)))
    print(f'{numbers} 中偶数的平方：{result}')
    
    # 或者使用列表推导式（更Pythonic）
    result_comp = [x ** 2 for x in numbers if x % 2 == 0]
    print(f'使用列表推导式：{result_comp}')


def higher_order_function_demo():
    """自定义高阶函数"""
    print('--- 自定义高阶函数 ---')
    
    def apply_twice(func, x):
        """应用函数两次"""
        return func(func(x))
    
    print('apply_twice(lambda x: x * 2, 5) =', apply_twice(lambda x: x * 2, 5))
    print('apply_twice(lambda x: x + 1, 5) =', apply_twice(lambda x: x + 1, 5))
    
    def compose(f, g):
        """函数组合：返回一个函数，其计算 f(g(x))"""
        return lambda x: f(g(x))
    
    add_one = lambda x: x + 1
    square = lambda x: x ** 2
    
    composed = compose(add_one, square)
    print('compose(lambda x: x+1, lambda x: x**2)(5) =', composed(5))  # (5**2) + 1 = 26


def main():
    map_demo()
    print()
    
    filter_demo()
    print()
    
    sorted_with_key()
    print()
    
    lambda_basics()
    print()
    
    lambda_with_map_filter()
    print()
    
    higher_order_function_demo()


if __name__ == '__main__':
    main()