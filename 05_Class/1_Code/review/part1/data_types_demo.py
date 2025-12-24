"""
示例：演示 Python 中基本数据类型的特性

包含演示：
- 整数（int）：无长度限制、二进制（0b）、八进制（0o）、十六进制（0x）
- 浮点数（float）：精度误差、容差比较
- 布尔值（bool）：True/False 与整数转换
- 字符串（str）：单引号、双引号、三引号、转义字符、原始字符串（r''）
- 类型转换：显式转换（int()、float()、str()）、隐式转换（混合运算）

运行：
    python data_types_demo.py

作者：自动生成示例（中文注释）
"""


def int_demo():
    print('--- 整数（int）示例 ---')
    # 无长度限制
    big_int = 123456789012345678901234567890
    print('大整数：', big_int)

    # 不同进制表示
    decimal = 42
    binary = 0b101010  # 二进制
    octal = 0o52       # 八进制
    hexadecimal = 0x2A # 十六进制
    print('十进制：', decimal)
    print('二进制 0b101010：', binary)
    print('八进制 0o52：', octal)
    print('十六进制 0x2A：', hexadecimal)
    print('它们都相等：', decimal == binary == octal == hexadecimal)
    print()


def float_demo():
    print('--- 浮点数（float）示例 ---')
    # 精度误差
    a = 0.1 + 0.2
    print('0.1 + 0.2 =', a)  # 可能不是 0.3
    print('a == 0.3 ->', a == 0.3)

    # 使用容差比较
    tolerance = 1e-9
    print('使用容差比较：abs(a - 0.3) < 1e-9 ->', abs(a - 0.3) < tolerance)
    print()


def bool_demo():
    print('--- 布尔值（bool）示例 ---')
    true_val = True
    false_val = False
    print('True =', true_val, '; False =', false_val)

    # 与整数转换
    print('int(True) =', int(true_val))
    print('int(False) =', int(false_val))
    print('bool(1) =', bool(1))
    print('bool(0) =', bool(0))
    print('bool(5) =', bool(5))  # 非零为 True
    print()


def str_demo():
    print('--- 字符串（str）示例 ---')
    # 不同引号
    single = '单引号字符串'
    double = "双引号字符串"
    triple = '''三引号字符串
可以换行'''
    print('单引号：', single)
    print('双引号：', double)
    print('三引号：', triple)

    # 转义字符
    escaped = '使用\\n换行\\t制表'
    print('转义字符：', escaped)

    # 原始字符串
    raw = r'原始字符串：\n 不转义'
    print('原始字符串：', raw)
    print()


def conversion_demo():
    print('--- 类型转换示例 ---')
    # 显式转换
    num_str = '123'
    print('str 到 int：int("123") =', int(num_str))
    print('str 到 float：float("123.45") =', float('123.45'))
    print('int 到 str：str(456) =', str(456))

    # 隐式转换
    int_val = 5
    float_val = 2.5
    result = int_val + float_val  # int 自动转换为 float
    print('隐式转换：5 (int) + 2.5 (float) =', result, '; 类型：', type(result))
    print()


def main():
    int_demo()
    float_demo()
    bool_demo()
    str_demo()
    conversion_demo()


if __name__ == '__main__':
    main()