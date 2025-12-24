"""
示例：演示 Python 中运算符的使用

包含演示：
- 算术运算符：+ - * / // % **
- 比较运算符：== != > < >= <=
- 逻辑运算符：and or not，短路求值
- 赋值运算符：= += -= *= /=
- 位运算符：& | ^ ~ << >>
- 成员运算符：in not in
- 身份运算符：is is not
- 其他运算符：lambda、if-else表达式
- 运算符优先级示例

运行：
    python operators_demo.py

作者：自动生成示例（中文注释）
"""


def arithmetic_demo():
    print('--- 算术运算符示例 ---')
    a = 10
    b = 3
    print('a =', a, '; b =', b)
    print('a + b =', a + b)  # 加法
    print('a - b =', a - b)  # 减法
    print('a * b =', a * b)  # 乘法
    print('a / b =', a / b)  # 除法
    print('a // b =', a // b)  # 取整除
    print('a % b =', a % b)  # 取余
    print('a ** b =', a ** b)  # 幂运算
    print()


def comparison_demo():
    print('--- 比较运算符示例 ---')
    x = 5
    y = 10
    print('x =', x, '; y =', y)
    print('x == y ->', x == y)
    print('x != y ->', x != y)
    print('x > y ->', x > y)
    print('x < y ->', x < y)
    print('x >= y ->', x >= y)
    print('x <= y ->', x <= y)
    print()


def logical_demo():
    print('--- 逻辑运算符示例 ---')
    p = True
    q = False
    print('p =', p, '; q =', q)
    print('p and q ->', p and q)
    print('p or q ->', p or q)
    print('not p ->', not p)

    # 短路求值示例
    print('--- 短路求值示例 ---')
    def func1():
        print('func1 called')
        return True
    def func2():
        print('func2 called')
        return False
    print('func1() 与 func2() 调用输出：')
    func1()
    func2()
    print('False and func1() ->', False and func1())  # func1 不调用
    print('True or func2() ->', True or func2())      # func2 不调用
    print()


def assignment_demo():
    print('--- 赋值运算符示例 ---')
    z = 5
    print('z =', z)
    z += 3  # z = z + 3
    print('z += 3 -> z =', z)
    z -= 2  # z = z - 2
    print('z -= 2 -> z =', z)
    z *= 4  # z = z * 4
    print('z *= 4 -> z =', z)
    z /= 2  # z = z / 2
    print('z /= 2 -> z =', z)
    print()


def bitwise_demo():
    print('--- 位运算符示例 ---')
    m = 12  # 二进制 1100
    n = 7   # 二进制 0111
    print('m =', m, '(二进制 1100); n =', n, '(二进制 0111)')
    print('m & n =', m & n)   # 按位与
    print('m | n =', m | n)   # 按位或
    print('m ^ n =', m ^ n)   # 按位异或
    print('~m =', ~m)         # 按位取反
    print('m << 1 =', m << 1) # 左移
    print('m >> 1 =', m >> 1) # 右移
    print()


def membership_demo():
    print('--- 成员运算符示例 ---')
    lst = [1, 2, 3, 4, 5]
    print('lst =', lst)
    print('3 in lst ->', 3 in lst)
    print('6 not in lst ->', 6 not in lst)
    print()


def identity_demo():
    print('--- 身份运算符示例 ---')
    a = [1, 2, 3]
    b = a
    c = [1, 2, 3]
    print('a = [1,2,3]; b = a; c = [1,2,3]')
    print('a is b ->', a is b)
    print('a is c ->', a is c)
    print('a is not c ->', a is not c)
    print()


def other_demo():
    print('--- 其他运算符示例 ---')
    # lambda 表达式
    square = lambda x: x ** 2
    print('lambda x: x**2; square(5) =', square(5))

    # if-else 表达式
    num = 10
    result = '正数' if num > 0 else '非正数'
    print('num =', num, '; "正数" if num > 0 else "非正数" ->', result)
    print()


def precedence_demo():
    print('--- 运算符优先级示例 ---')
    # 括号最高
    expr1 = 2 + 3 * 4  # 3*4 先算
    expr2 = (2 + 3) * 4  # 括号优先
    print('2 + 3 * 4 =', expr1)
    print('(2 + 3) * 4 =', expr2)

    # 指数高于乘除
    expr3 = 2 * 3 ** 2  # 3**2 先算
    print('2 * 3 ** 2 =', expr3)

    # 比较低于算术
    expr4 = 5 > 3 + 2  # 3+2 先算
    print('5 > 3 + 2 ->', expr4)

    # 逻辑最低
    expr5 = True and 5 > 3  # 5>3 先算
    print('True and 5 > 3 ->', expr5)
    print()


def main():
    arithmetic_demo()
    comparison_demo()
    logical_demo()
    assignment_demo()
    bitwise_demo()
    membership_demo()
    identity_demo()
    other_demo()
    precedence_demo()


if __name__ == '__main__':
    main()