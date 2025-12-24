"""
示例：演示 Python 中函数的基本概念与定义

包含演示：
- 函数的基本定义
- 文档字符串（Docstring）
- 返回值

运行：
    python functions_basic_demo.py

作者：自动生成示例（中文注释）
"""


def greet(name):
    """
    问候函数
    
    参数：
        name (str): 被问候的人的名字
    
    返回：
        问候信息 (str)
    """
    return f'Hello, {name}!'


def add(a, b):
    """计算两个数的和"""
    return a + b


def factorial(n):
    """计算阶乘"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def no_return_func():
    """不返回值的函数，默认返回 None"""
    print('这个函数没有 return 语句')


def main():
    print('--- 函数基本定义示例 ---')
    
    # 调用函数
    print(greet('Alice'))
    print(add(5, 3))
    print('5! =', factorial(5))
    
    # 查看文档字符串
    print('\n--- 查看文档字符串 ---')
    print(help(greet))
    print()
    
    # 无返回值的函数
    result = no_return_func()
    print('无返回值函数返回：', result)


if __name__ == '__main__':
    main()