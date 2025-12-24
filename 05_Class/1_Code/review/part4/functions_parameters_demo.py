"""
示例：演示 Python 中函数的参数传递

包含演示：
- 位置参数
- 默认值参数
- 关键词参数
- 可变长度参数 (*args, **kwargs)
- 赋值传递（可变vs不可变对象）
- 参数顺序规则

运行：
    python functions_parameters_demo.py

作者：自动生成示例（中文注释）
"""


def position_params(a, b, c):
    """位置参数示例"""
    return a + b + c


def default_params(name, age=18, city='Beijing'):
    """默认值参数示例"""
    return f'{name} 来自 {city}，年龄 {age}'


def keyword_params(a, b, c):
    """关键词参数调用示例"""
    return f'a={a}, b={b}, c={c}'


def varargs_demo(*args):
    """可变长度位置参数示例"""
    print('可变长度位置参数：', args)
    return sum(args) if all(isinstance(x, (int, float)) for x in args) else None


def keyword_varargs_demo(**kwargs):
    """可变长度关键词参数示例"""
    print('可变长度关键词参数：', kwargs)
    for key, value in kwargs.items():
        print(f'  {key} = {value}')


def mixed_params(a, b=10, *args, **kwargs):
    """混合参数示例"""
    print(f'位置参数 a={a}, 默认参数 b={b}')
    print(f'可变位置参数 args={args}')
    print(f'可变关键词参数 kwargs={kwargs}')


def mutable_immutable_demo():
    """演示不可变 vs 可变对象作为参数"""
    print('--- 不可变对象（int）---')
    
    def modify_int(x):
        x = 100
        print('函数内部：x =', x)
    
    num = 5
    print('外部：num =', num)
    modify_int(num)
    print('调用后：num =', num, '（未改变）')
    
    print('\n--- 可变对象（list）---')
    
    def modify_list(lst):
        lst.append(4)
        print('函数内部：lst =', lst)
    
    my_list = [1, 2, 3]
    print('外部：my_list =', my_list)
    modify_list(my_list)
    print('调用后：my_list =', my_list, '（改变了！）')


def mutable_default_param_demo():
    """演示可变对象作为默认值参数的陷阱"""
    print('--- 可变对象作为默认值参数的陷阱 ---')
    
    def bad_function(x, lst=[]):
        lst.append(x)
        return lst
    
    print('第一次调用：', bad_function(1))
    print('第二次调用：', bad_function(2))  # 会包含第一次的结果！
    print('第三次调用：', bad_function(3))
    print('注意：默认值列表被共享了！')
    
    print('\n--- 正确的做法 ---')
    
    def good_function(x, lst=None):
        if lst is None:
            lst = []
        lst.append(x)
        return lst
    
    print('第一次调用：', good_function(1))
    print('第二次调用：', good_function(2))
    print('第三次调用：', good_function(3))
    print('现在每次调用都是独立的')


def main():
    print('--- 位置参数示例 ---')
    print(position_params(1, 2, 3))
    
    print('\n--- 默认值参数示例 ---')
    print(default_params('Bob'))
    print(default_params('Charlie', 25))
    print(default_params('Diana', 30, 'Shanghai'))
    
    print('\n--- 关键词参数示例 ---')
    print(keyword_params(a=1, c=3, b=2))
    
    print('\n--- 可变长度位置参数示例 ---')
    print('sum:', varargs_demo(1, 2, 3, 4, 5))
    
    print('\n--- 可变长度关键词参数示例 ---')
    keyword_varargs_demo(name='Eve', age=28, city='Shenzhen')
    
    print('\n--- 混合参数示例 ---')
    mixed_params(10, 20, 30, 40, key1='value1', key2='value2')
    
    print('\n--- 不可变 vs 可变对象 ---')
    mutable_immutable_demo()
    
    print('\n')
    mutable_default_param_demo()


if __name__ == '__main__':
    main()