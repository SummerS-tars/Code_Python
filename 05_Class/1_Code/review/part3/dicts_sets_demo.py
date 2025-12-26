"""
示例：演示 Python 中字典和集合

包含演示：
- 字典操作（CRUD）
- 集合操作（CRUD、数学运算）
- 性能对比（列表vs字典查找）

运行：
    python dicts_sets_demo.py

作者：自动生成示例（中文注释）
"""


def dict_operations():
    print('--- 字典操作示例 ---')
    # 创建
    d = {}
    print('空字典：', d)
    d = {'name': 'Alice', 'age': 25}
    print('初始字典：', d)

    # 更多创建方式
    d_from_list = dict([('a', 1), ('b', 2)])
    print('从列表创建：', d_from_list)
    d_from_zip = dict(zip(['x', 'y', 'z'], [10, 20, 30]))
    print('从zip创建：', d_from_zip)
    d_fromkeys = dict.fromkeys(['key1', 'key2', 'key3'], 'default_value')
    print('fromkeys创建：', d_fromkeys)

    # C/U
    d['city'] = 'Beijing'
    print('d["city"] = "Beijing"：', d)
    d.setdefault('country', 'China')
    print('setdefault("country", "China")：', d)
    d['age'] = 26  # 更新
    print('更新 age：', d)

    # R
    print('d["name"] =', d['name'])
    print('d.get("age") =', d.get('age'))
    print('d.get("salary", "N/A") =', d.get('salary', 'N/A'))
    print('keys()：', list(d.keys()))
    print('values()：', list(d.values()))
    print('items()：', list(d.items()))

    # D
    del d['city']
    print('del d["city"]：', d)
    popped = d.pop('age')
    print('pop("age") 返回：', popped, '；字典：', d)
    last = d.popitem()
    print('popitem() 返回：', last, '；字典：', d)
    d.clear()
    print('clear()：', d)
    print()


def set_operations():
    print('--- 集合操作示例 ---')
    # 创建
    s = set()
    print('空集合：', s)
    s = {1, 2, 3}
    print('初始集合：', s)
    fs = frozenset([4, 5, 6])
    print('不可变集合：', fs)

    # C
    s.add(4)
    print('add(4)：', s)
    s.update([5, 6])
    print('update([5, 6])：', s)

    # R
    print('4 in s =', 4 in s)
    print('len(s) =', len(s))

    # D
    s.remove(4)
    print('remove(4)：', s)
    s.discard(10)  # 不存在也不报错
    print('discard(10)：', s)
    popped = s.pop()
    print('pop() 返回：', popped, '；集合：', s)

    # 数学运算
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}
    print('a =', a, '; b =', b)
    print('并集 a | b =', a | b)
    print('交集 a & b =', a & b)
    print('差集 a - b =', a - b)
    print('对称差集 a ^ b =', a ^ b)
    print('a 是 b 的子集？ a <= b =', a <= b)
    print('a 是 b 的超集？ a >= b =', a >= b)
    print()


def performance_comparison():
    print('--- 性能对比示例 ---')
    import time

    # 创建大数据集
    large_list = list(range(100000))
    large_dict = {i: i for i in range(100000)}

    # 测试查找性能
    target = 99999
    iterations = 1000

    # 列表查找（线性）
    start = time.perf_counter()
    for _ in range(iterations):
        found_in_list = target in large_list
    list_time = time.perf_counter() - start

    # 字典查找（哈希）
    start = time.perf_counter()
    for _ in range(iterations):
        found_in_dict = target in large_dict
    dict_time = time.perf_counter() - start

    print('查找 {} 在 100000 个元素中（重复 {} 次）：'.format(target, iterations))
    print('列表查找：{}，总耗时：{:.6f} 秒'.format(found_in_list, list_time))
    print('字典查找：{}，总耗时：{:.6f} 秒'.format(found_in_dict, dict_time))
    print('字典查找快 {:.1f} 倍'.format(list_time / dict_time if dict_time > 0 else float('inf')))
    print()


def main():
    dict_operations()
    set_operations()
    performance_comparison()


if __name__ == '__main__':
    main()