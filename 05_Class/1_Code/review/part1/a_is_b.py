"""
示例：演示 Python 中 `is` 与 `==` 的区别，以及 id()、可变/不可变对象的行为

包含演示：
- 小整数缓存（-5 到 256）导致相同小整数字面量可能共用同一对象
- 如何通过构造新对象避免编译期/常量合并优化（例如使用 int()）
- 字符串驻留（intern）与 sys.intern 的用法
- 列表（可变对象）引用与 == 对比 is
- 使用 id() 查看对象地址并展示可变对象被修改时的影响

运行：
	python a_is_b.py

作者：自动生成示例（中文注释）
"""

import sys


def int_demo():
	print('--- 整数示例（int）---')
	a = 256
	b = 256
	print('a = 256; b = 256 -> a is b:', a is b)

	# 对于较大的整数，直接写字面量有时会被编译器/解释器优化成同一对象，
	# 为确保创建不同对象可以通过运行时构造：
	x = 257
	y = int('257')
	print("x = 257; y = int('257') -> x is y:", x is y)
	print('x == y ->', x == y)
	print('id(x) =', id(x))
	print('id(y) =', id(y))
	print()


def string_demo():
	print('--- 字符串示例（str）---')
	s1 = 'hello'
	s2 = 'hello'
	print("s1 = 'hello'; s2 = 'hello' -> s1 is s2:", s1 is s2)

	# 强制创建新字符串对象（拼接或用 str()）:
	s3 = ''.join(['he', 'llo'])
	print("s3 = ''.join(['he','llo']) -> s3 is s1:", s3 is s1)
	print('s3 == s1 ->', s3 == s1)

	# 使用 sys.intern 可以确保字符串被驻留（intern）以节省内存并允许 is 比较：
	s4 = sys.intern('this_is_interned')
	s5 = sys.intern('this_is_interned')
	print('使用 sys.intern -> s4 is s5:', s4 is s5)
	print()


def list_demo():
	print('--- 列表示例（可变对象）---')
	l1 = [1, 2, 3]
	l2 = l1  # l2 引用与 l1 同一对象
	l3 = [1, 2, 3]  # 内容相同，但不同对象

	print('l1 is l2 ->', l1 is l2)
	print('l1 is l3 ->', l1 is l3)
	print('l1 == l3 ->', l1 == l3)
	print('id(l1) =', id(l1))
	print('id(l3) =', id(l3))

	# 修改 l2，会同时影响 l1，因为它们是同一对象
	l2.append(4)
	print('在 l2 上 append(4) 后: l1 =', l1)
	print()


def main():
	int_demo()
	string_demo()
	list_demo()


if __name__ == '__main__':
	main()

