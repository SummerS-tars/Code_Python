"""
示例：演示 Python 中分支结构

包含演示：
- if-elif-else 语句
- 条件表达式（三元运算符）
- 嵌套 if 语句

运行：
    python branching_demo.py

作者：自动生成示例（中文注释）
"""


def if_elif_else_demo():
    print('--- if-elif-else 示例 ---')
    score = int(input('请输入成绩（0-100）：'))

    if score >= 90:
        grade = 'A'
    elif score >= 80:
        grade = 'B'
    elif score >= 70:
        grade = 'C'
    elif score >= 60:
        grade = 'D'
    else:
        grade = 'F'

    print(f'成绩 {score} 对应的等级：{grade}')
    print()


def conditional_expression_demo():
    print('--- 条件表达式示例 ---')
    age = int(input('请输入年龄：'))

    # 条件表达式：值1 if 条件 else 值2
    status = '成年' if age >= 18 else '未成年'
    print(f'年龄 {age}：{status}')

    # 另一个示例
    num = int(input('请输入一个数字：'))
    result = '正数' if num > 0 else ('负数' if num < 0 else '零')
    print(f'数字 {num} 是：{result}')
    print()


def nested_if_demo():
    print('--- 嵌套 if 示例 ---')
    username = input('请输入用户名：')
    password = input('请输入密码：')

    if username == 'admin':
        if password == '123456':
            print('登录成功！')
        else:
            print('密码错误！')
    else:
        print('用户名不存在！')
    print()


def main():
    if_elif_else_demo()
    conditional_expression_demo()
    nested_if_demo()


if __name__ == '__main__':
    main()