"""
示例：演示 random 模块的使用

包含演示：
- 生成随机数
- 从序列中选择
- 打乱顺序

运行：
    python random_demo.py

作者：自动生成示例（中文注释）
"""

import random


def random_demo():
    print('--- random模块示例 ---')

    # 生成随机浮点数
    print("随机浮点数 [0,1):", random.random())

    # 生成随机整数
    print("随机整数 [1,10]:", random.randint(1, 10))

    # 从序列中随机选择
    fruits = ['苹果', '香蕉', '橙子', '葡萄']
    print("随机水果:", random.choice(fruits))

    # 从序列中随机选择多个不重复元素
    print("随机选择2个水果:", random.sample(fruits, 2))

    # 打乱列表顺序
    numbers = [1, 2, 3, 4, 5]
    random.shuffle(numbers)
    print("打乱后的列表:", numbers)


def main():
    random_demo()


if __name__ == '__main__':
    main()
