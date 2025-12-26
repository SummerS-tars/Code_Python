"""
示例：演示 Python 中列表与元组

包含演示：
- 序列基础操作
- 列表操作（CRUD）
- 列表推导式
- 元组操作
- 生成器表达式
- 序列解包
- 切片操作

运行：
    python lists_tuples_demo.py

作者：自动生成示例（中文注释）
"""


def sequence_basics():
    print('--- 序列基础操作示例 ---')
    lst = [3, 1, 4, 1, 5]
    tup = (1, 2, 3, 4, 5)

    print('列表：', lst)
    print('元组：', tup)

    print('len(lst) =', len(lst))
    print('min(lst) =', min(lst))
    print('max(lst) =', max(lst))
    print('sum(lst) =', sum(lst))
    print('3 in lst =', 3 in lst)
    print('sorted(lst) =', sorted(lst))  # 不修改原列表
    print('reversed(lst) =', list(reversed(lst)))  # 转换为列表查看
    print('enumerate(lst) =', list(enumerate(lst)))
    print()


def list_operations():
    print('--- 列表操作示例 ---')
    # 创建
    lst = []
    print('空列表：', lst)
    lst = [1, 2, 3]
    print('初始列表：', lst)

    # C
    lst.append(4)
    print('append(4)：', lst)
    lst.insert(1, 1.5)
    print('insert(1, 1.5)：', lst)
    lst.extend([5, 6])
    print('extend([5, 6])：', lst)

    # R
    print('lst[2] =', lst[2])
    print('lst.index(3) =', lst.index(3))
    print('lst.count(1) =', lst.count(1))

    # U
    lst[0] = 0
    print('lst[0] = 0：', lst)
    lst.sort()
    print('sort()：', lst)
    lst.reverse()
    print('reverse()：', lst)

    # D
    popped = lst.pop()
    print('pop() 返回：', popped, '；列表：', lst)
    lst.remove(1.5)
    print('remove(1.5)：', lst)
    del lst[0]
    print('del lst[0]：', lst)
    lst.clear()
    print('clear()：', lst)
    print()


def list_comprehension_demo():
    print('--- 列表推导式示例 ---')
    # 基本
    squares = [x**2 for x in range(1, 6)]
    print('平方：', squares)

    # 带条件
    evens = [x for x in range(10) if x % 2 == 0]
    print('偶数：', evens)

    # 嵌套
    matrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]
    print('乘法表：', matrix)
    print()


def tuple_operations():
    print('--- 元组操作示例 ---')
    # 创建
    tup = ()
    print('空元组：', tup)
    tup = (1, 2, 3)
    print('元组：', tup)
    single = (42,)  # 单元素元组
    print('单元素元组：', single)

    # 不可变性
    # tup[0] = 0  # 会报错
    print('元组不可修改')

    # 作为字典键
    d = {(1, 2): 'tuple key'}
    print('元组作为字典键：', d)

    # 不可变性理解
    nested = ([1, 2], 3)
    nested[0].append(3)  # 可以修改内部可变对象
    nested[0].append([1,2])
    print('嵌套元组，修改内部列表：', nested)
    print()


def generator_expression_demo():
    print('--- 生成器表达式示例 ---')
    gen = (x**2 for x in range(1, 6))
    print('生成器：', gen)
    print('转换为列表：', list(gen))

    # 节省内存
    large_gen = (x for x in range(1000) if x % 2 == 0)
    print('大生成器前5个：', [next(large_gen) for _ in range(5)])
    print()


def unpacking_demo():
    print('--- 序列解包示例 ---')
    # 基本解包
    x, y = 1, 2
    print('x, y = 1, 2 -> x={}, y={}'.format(x, y))
    
    x, y, z = (3, 4, 5)
    print('x, y, z = (3,4,5) -> x={}, y={}, z={}'.format(x, y, z))
    
    a, b, c = [1, 2, 3]
    print('a, b, c = [1, 2, 3] -> a={}, b={}, c={}'.format(a, b, c))

    # 通配符
    x, *y, z = [1, 2, 3, 4, 5]
    print('x, *y, z = [1,2,3,4,5] -> x={}, y={}, z={}'.format(x, y, z))

    # 交换变量
    m, n = 10, 20
    print('交换前：m={}, n={}'.format(m, n))
    m, n = n, m
    print('交换后：m={}, n={}'.format(m, n))
    print()


def slicing_demo():
    print('--- 切片操作示例 ---')
    lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print('原列表：', lst)

    # 基本切片
    print('lst[2:5] =', lst[2:5])
    print('lst[:3] =', lst[:3])
    print('lst[7:] =', lst[7:])
    print('lst[::2] =', lst[::2])  # 步长2

    # 反向切片
    print('lst[::-1] =', lst[::-1])

    # 浅拷贝
    copy_lst = lst[:]
    copy_lst[0] = 99
    print('浅拷贝后修改copy_lst[0]=99，原列表：', lst)

    # 原地修改
    lst[1:4] = [10, 20, 30]
    print('lst[1:4] = [10,20,30] ->', lst)
    print()


def main():
    sequence_basics()
    list_operations()
    list_comprehension_demo()
    tuple_operations()
    generator_expression_demo()
    unpacking_demo()
    slicing_demo()


if __name__ == '__main__':
    main()