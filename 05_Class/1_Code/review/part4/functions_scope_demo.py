"""
示例：演示 Python 中函数的作用域

包含演示：
- 局部作用域（Local）
- 全局作用域（Global）
- 闭包作用域（Enclosing）
- 内置作用域（Built-in）
- LEGB规则
- global 关键字

运行：
    python functions_scope_demo.py

作者：自动生成示例（中文注释）
"""

# 全局变量
global_var = 'I am global'


def scope_example():
    """演示基本作用域"""
    local_var = 'I am local'
    print('全局变量：', global_var)
    print('局部变量：', local_var)


def modify_global():
    """演示修改全局变量"""
    global global_var
    print('修改前：', global_var)
    global_var = 'Modified global'
    print('修改后：', global_var)


def legb_demo():
    """演示 LEGB 规则"""
    x = 'Global scope'  # 实际上是局部的，因为这个函数内
    
    def inner_function():
        x = 'Local scope'  # 局部
        print('在内层函数中，x =', x)
    
    inner_function()
    print('在外层函数中，x =', x)


def closure_example():
    """闭包示例"""
    multiplier = 3
    
    def multiply(x):
        return x * multiplier  # multiplier 来自 Enclosing 作用域
    
    return multiply


def demonstrate_closure():
    print('--- 闭包示例 ---')
    multiply_by_3 = closure_example()
    print('multiply_by_3(5) =', multiply_by_3(5))
    print('multiply_by_3(10) =', multiply_by_3(10))


def scope_lookup_demo():
    """演示变量查找顺序（LEGB）"""
    print('--- LEGB 规则演示 ---')
    
    # 全局变量
    name = 'Global'
    
    def outer():
        name = 'Enclosing'  # Enclosing 作用域
        
        def inner():
            name = 'Local'  # Local 作用域
            print('Local 中访问 name:', name)
        
        inner()
        print('Enclosing 中访问 name:', name)
    
    outer()
    print('Global 中访问 name:', name)


def builtin_scope_demo():
    """演示内置作用域"""
    print('--- 内置作用域示例 ---')
    print('len([1,2,3]) =', len([1, 2, 3]))  # len 来自内置作用域
    print('max([1,5,3]) =', max([1, 5, 3]))  # max 来自内置作用域


def scope_conflict_demo():
    """演示作用域冲突"""
    print('--- 作用域冲突示例 ---')
    
    def func1():
        x = 10
        print('func1 中 x =', x)
    
    def func2():
        x = 20
        print('func2 中 x =', x)
    
    func1()
    func2()
    # 两个函数有各自的局部 x，互不影响


def main():
    print('--- 基本作用域示例 ---')
    scope_example()
    
    print('\n--- 修改全局变量 ---')
    print('全局变量初始值：', global_var)
    modify_global()
    print('模块级全局变量现在是：', global_var)
    
    print('\n--- LEGB 规则示例 ---')
    legb_demo()
    
    print('\n')
    demonstrate_closure()
    
    print('\n')
    scope_lookup_demo()
    
    print('\n')
    builtin_scope_demo()
    
    print('\n')
    scope_conflict_demo()


if __name__ == '__main__':
    main()