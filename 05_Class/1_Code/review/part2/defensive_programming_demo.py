"""
示例：演示防御性编程

包含演示：
- 防御性编程：永远不要假设输入正确，使用循环和异常处理确保输入合法。
- while True + try-except：持续提示用户输入，直到输入有效。

运行：
    python defensive_programming_demo.py

注意：运行时会提示输入，输入无效时会重新提示。

作者：自动生成示例（中文注释）
"""


def get_positive_integer():
    """获取正整数的防御性函数"""
    while True:
        try:
            num = int(input('请输入一个正整数：'))
            if num <= 0:
                raise ValueError('必须是正整数')
            return num
        except ValueError as e:
            print(f'输入无效：{e}。请重新输入。')


def get_float_in_range(min_val, max_val):
    """获取指定范围内的浮点数的防御性函数"""
    while True:
        try:
            num = float(input(f'请输入一个介于 {min_val} 和 {max_val} 之间的浮点数：'))
            if not (min_val <= num <= max_val):
                raise ValueError(f'数值必须在 {min_val} 到 {max_val} 之间')
            return num
        except ValueError as e:
            print(f'输入无效：{e}。请重新输入。')


def get_list_of_integers():
    """获取整数列表的防御性函数"""
    while True:
        try:
            input_str = input('请输入用逗号分隔的整数列表（如 1,2,3）：')
            # 分割并转换为整数
            nums = [int(x.strip()) for x in input_str.split(',')]
            return nums
        except ValueError:
            print('输入包含非整数。请重新输入。')


def main():
    print('--- 防御性编程示例 ---')
    print('这些函数会持续提示，直到输入合法。')

    # 示例1：获取正整数
    pos_int = get_positive_integer()
    print(f'获取的正整数：{pos_int}')

    # 示例2：获取范围内的浮点数
    float_val = get_float_in_range(0.0, 100.0)
    print(f'获取的浮点数：{float_val}')

    # 示例3：获取整数列表
    int_list = get_list_of_integers()
    print(f'获取的整数列表：{int_list}')

    print('所有输入都已验证并获取成功！')


if __name__ == '__main__':
    main()