"""
示例：演示 math 模块的使用

包含演示：
- 数论函数
- 取整与绝对值
- 幂与对数
- 三角函数
- 常量

运行：
    python math_demo.py

作者：自动生成示例（中文注释）
"""

import math


def math_demo():
    print('--- math模块示例 ---')

    # 数论函数
    print("组合数 C(5,2):", math.comb(5, 2))
    print("排列数 P(5,2):", math.perm(5, 2))
    print("阶乘 5!:", math.factorial(5))
    print("最大公约数 gcd(12,18):", math.gcd(12, 18))

    # 取整与绝对值
    print("向上取整 ceil(3.2):", math.ceil(3.2))
    print("向下取整 floor(3.8):", math.floor(3.8))
    print("绝对值 fabs(-5.5):", math.fabs(-5.5))

    # 幂与对数
    print("平方根 sqrt(16):", math.sqrt(16))
    print("自然对数 log(e):", math.log(math.e))
    print("以10为底的对数 log10(100):", math.log10(100))

    # 三角函数
    print("sin(π/2):", math.sin(math.pi/2))
    print("cos(0):", math.cos(0))
    print("角度转弧度 degrees(π):", math.degrees(math.pi))
    print("弧度转角度 radians(180):", math.radians(180))

    # 常量
    print("π:", math.pi)
    print("e:", math.e)


def main():
    math_demo()


if __name__ == '__main__':
    main()
