"""
示例：演示 Python 中变量作为对象引用的概念

包含演示：
- 变量赋值：变量是对象的引用（标签）
- 使用 id() 查看对象地址
- 使用 type() 查看对象类型
- 不可变对象（如 int）的赋值行为：修改变量不影响其他引用同一对象的变量
- 可变对象（如 list）的赋值行为：修改对象会影响所有引用该对象的变量

运行：
    python variable_demo.py

作者：自动生成示例（中文注释）
"""


def immutable_demo():
    print('--- 不可变对象示例（int）---')
    a = 10
    print('a = 10')
    print('id(a) =', id(a))
    print('type(a) =', type(a))
    print('a =', a)

    # b 引用与 a 同一对象
    b = a
    print('b = a  # b 引用与 a 同一对象')
    print('id(b) =', id(b))
    print('b is a ->', b is a)

    # 修改 a
    a = 15
    print('a = 15  # 重新赋值给新对象')
    print('id(a) =', id(a))
    print('b is a ->', b is a)
    print('a =', a, '; b =', b)

    # 修改 b（重新赋值给新对象），a 不受影响
    b = 20
    print('b = 20  # 重新赋值给新对象')
    print('id(b) =', id(b))
    print('b is a ->', b is a)
    print('a =', a, '; b =', b)
    print()


def mutable_demo():
    print('--- 可变对象示例（list）---')
    l1 = [1, 2, 3]
    print('l1 = [1, 2, 3]')
    print('id(l1) =', id(l1))
    print('type(l1) =', type(l1))
    print('l1 =', l1)

    # l2 引用与 l1 同一对象
    l2 = l1
    print('l2 = l1  # l2 引用与 l1 同一对象')
    print('id(l2) =', id(l2))
    print('l2 is l1 ->', l2 is l1)

    # 修改 l2（修改对象内容），l1 受影响
    l2.append(4)
    print('l2.append(4)  # 修改对象内容')
    print('l1 =', l1, '; l2 =', l2)
    print('id(l1) =', id(l1), '; id(l2) =', id(l2))

    # 现在修改 l1，l2 也会受影响，因为它们引用同一对象
    l1.append(5)
    print('l1.append(5)  # 再次修改对象内容')
    print('l1 =', l1, '; l2 =', l2)
    print('id(l1) =', id(l1), '; id(l2) =', id(l2))

    # 现在让 l2 指向一个新对象（复制 l1 的内容，但创建新对象）
    l2 = l1.copy()
    print('l2 = l1.copy()  # l2 现在指向新对象')
    print('l2 is l1 ->', l2 is l1)
    print('l1 =', l1, '; l2 =', l2)
    print('id(l1) =', id(l1), '; id(l2) =', id(l2))

    # 现在修改 l1，l2 不受影响
    l1.append(6)
    print('l1.append(6)  # 修改 l1，l2 不受影响')
    print('l1 =', l1, '; l2 =', l2)
    print('id(l1) =', id(l1), '; id(l2) =', id(l2))
    print()

def main():
    immutable_demo()
    mutable_demo()


if __name__ == '__main__':
    main()