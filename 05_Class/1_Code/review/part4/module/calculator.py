"""
模块：calculator（计算器）

提供基本的数学运算功能。

使用方法：
    import calculator
    result = calculator.add(5, 3)
    
或者：
    from calculator import add, multiply
    result = add(5, 3)
"""


def add(a, b):
    """
    计算两个数的和
    
    参数：
        a: 第一个数
        b: 第二个数
    
    返回：
        两个数的和
    """
    return a + b


def subtract(a, b):
    """计算两个数的差"""
    return a - b


def multiply(a, b):
    """计算两个数的积"""
    return a * b


def divide(a, b):
    """
    计算两个数的商
    
    参数：
        a: 被除数
        b: 除数（不能为0）
    
    返回：
        两个数的商
    
    异常：
        ZeroDivisionError: 当 b 为 0 时抛出
    """
    if b == 0:
        raise ZeroDivisionError('除数不能为零')
    return a / b


def power(a, b):
    """计算 a 的 b 次方"""
    return a ** b


def main():
    """模块的测试函数"""
    print('--- 计算器模块测试 ---')
    print('5 + 3 =', add(5, 3))
    print('10 - 4 =', subtract(10, 4))
    print('6 * 7 =', multiply(6, 7))
    print('20 / 4 =', divide(20, 4))
    print('2 ** 5 =', power(2, 5))
    
    try:
        print('10 / 0 =', divide(10, 0))
    except ZeroDivisionError as e:
        print('异常捕获:', e)


# 模块的自测代码，仅在直接运行时执行
if __name__ == '__main__':
    main()
    print('\n模块自测完成（这段代码仅在直接运行此模块时执行）')