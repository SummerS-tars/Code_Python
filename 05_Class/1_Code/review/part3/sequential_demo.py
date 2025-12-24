"""
示例：演示 Python 中顺序结构

包含演示：
- 顺序结构：程序从上到下依次执行代码。

运行：
    python sequential_demo.py

作者：自动生成示例（中文注释）
"""


def sequential_demo():
    print('--- 顺序结构示例 ---')
    print('程序从上到下依次执行：')

    # 第一步：变量赋值
    a = 10
    print('第一步：a = 10')

    # 第二步：另一个赋值
    b = 20
    print('第二步：b = 20')

    # 第三步：计算
    c = a + b
    print('第三步：c = a + b =', c)

    # 第四步：输出结果
    print('第四步：输出结果 c =', c)

    print('顺序执行完成。')


def main():
    sequential_demo()


if __name__ == '__main__':
    main()