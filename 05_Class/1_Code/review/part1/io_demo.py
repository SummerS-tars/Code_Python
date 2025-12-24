"""
示例：演示 Python 中基本输入输出操作

包含演示：
- input()：获取用户输入，返回字符串，类型转换
- print()：输出到控制台，sep和end参数
- f-string：格式化输出，嵌入变量和表达式
- eval()：将字符串作为Python表达式求值

运行：
    python io_demo.py

注意：input() 示例中使用了预设值模拟用户输入，实际运行时可取消注释并手动输入。

作者：自动生成示例（中文注释）
"""


def input_demo():
    print('--- input() 示例 ---')
    # input() 返回字符串，需要类型转换
    # 模拟用户输入（实际运行时可取消注释下一行，并注释掉 name = 'Alice'）
    # name = input('请输入您的名字：')
    name = 'Alice'  # 模拟输入
    print('输入的名字：', name, '; 类型：', type(name))

    # 类型转换示例
    # age_str = input('请输入您的年龄：')
    age_str = '25'  # 模拟输入
    age = int(age_str)  # 转换为整数
    print('输入的年龄字符串：', age_str, '; 转换为整数：', age, '; 类型：', type(age))

    # 浮点数转换
    # height_str = input('请输入您的身高（米）：')
    height_str = '1.75'  # 模拟输入
    height = float(height_str)
    print('输入的身高字符串：', height_str, '; 转换为浮点数：', height, '; 类型：', type(height))
    print()


def print_demo():
    print('--- print() 示例 ---')
    # 基本输出
    print('Hello, World!')

    # 多个值，默认分隔符空格
    print('Python', 'is', 'fun')

    # 指定 sep 参数
    print('Python', 'is', 'fun', sep='-')

    # 指定 end 参数，默认换行
    print('这行不换行', end=' ')
    print('继续在这行')

    # 结合 sep 和 end
    print('A', 'B', 'C', sep=', ', end='!\n')
    print()


def fstring_demo():
    print('--- f-string 示例 ---')
    name = 'Bobby'
    age = 30
    height = 1.80
    pi = 3.1415926535

    # 基本嵌入变量
    print(f'名字：{name}，年龄：{age}')

    # 嵌入表达式
    print(f'明年年龄：{age + 1}')

    # 格式化数字
    print(f'身高：{height:.2f} 米')

    # 复杂表达式
    status = '成年' if age >= 18 else '未成年'
    print(f'{name} 是 {status}，身高 {height:.1f} 米')

    # 更多格式化细节
    print('--- 更多 f-string 格式化选项 ---')

    # 宽度和对齐
    print(f'左对齐10位：{"left":<10} | 右对齐10位：{"right":>10} | 居中10位：{"center":^10} | ')

    # 填充字符
    print(f'填充*左对齐：{"fill":*<10} | 填充0右对齐：{42:0>5} | 填充-居中：{"hi":-^10} | ')

    # 数字格式化
    print(f'整数：{42:d} | 浮点：{pi:.3f} | 科学计数：{12345:e} | 百分比：{0.85:.1%} | ')

    # 字符串宽度
    print(f'字符串宽度：{name:>10} | 截断：{name:.3} | ')  # 注意：.3 是精度，但对字符串是截断前3字符

    # 组合
    print(f'组合：{pi:10.2f} | {age:04d} | ')
    print()


def eval_demo():
    print('--- eval() 示例 ---')
    # eval() 将字符串作为表达式求值
    expr1 = '2 + 3 * 4'
    result1 = eval(expr1)
    print(f'eval("{expr1}") = {result1}')

    # 变量环境
    x = 10
    expr2 = 'x * 2 + 5'
    result2 = eval(expr2)
    print(f'x = {x}; eval("{expr2}") = {result2}')

    # 列表和函数
    expr3 = '[i**2 for i in range(5)]'
    result3 = eval(expr3)
    print(f'eval("{expr3}") = {result3}')

    # 更复杂的批量赋值
    p, q, r = [1, 2, 3]
    print(f'p, q, r = [1, 2, 3] 后 p = {p}, q = {q}, r = {r}')

    # 复合赋值和批量赋值示例（使用 exec() 执行语句）
    print('--- eval() 示例（用于语句执行，如赋值）---')
    a, b = eval('1, 2')  # 初始化变量
    print(f'a, b = eval("1, 2") 后 a = {a}, b = {b}')

    # 注意：eval() 和 exec() 都有安全风险，仅用于可信输入
    print('注意：eval() 和 exec() 可执行任意代码，使用时需谨慎')
    print()


def main():
    input_demo()
    print_demo()
    fstring_demo()
    eval_demo()


if __name__ == '__main__':
    main()