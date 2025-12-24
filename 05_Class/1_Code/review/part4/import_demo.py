"""
示例：演示不同的模块导入方式

包含演示：
- 导入整个模块
- 从模块中导入特定内容
- 导入模块并指定别名

运行：
    python import_demo.py

作者：自动生成示例（中文注释）
"""


def import_demo():
    print('--- 模块导入方式演示 ---')

    # 1. 导入整个模块
    print("1. 导入整个模块：")
    import random
    print("   使用 random.random():", random.random())

    # 2. 从模块中导入特定内容
    print("2. 从模块中导入特定内容：")
    from math import sqrt, pi
    print("   使用 sqrt(16):", sqrt(16))
    print("   使用 pi:", pi)

    # 3. 导入模块并指定别名
    print("3. 导入模块并指定别名：")
    import string as str_mod
    print("   使用 str_mod.digits:", str_mod.digits)
    print("   使用 str_mod.ascii_letters[:10]:", str_mod.ascii_letters[:10])

    # 4. 导入函数并指定别名
    print("4. 导入函数并指定别名：")
    from random import randint as ri
    print("   使用 ri(1, 100):", ri(1, 100))

    print("导入方式演示完成。")


def main():
    import_demo()


if __name__ == '__main__':
    main()
