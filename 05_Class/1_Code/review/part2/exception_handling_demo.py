"""
示例：演示 Python 中异常处理机制

包含演示：
- try-except：捕获异常
- try-except-else：无异常时执行else
- try-except-finally：无论如何执行finally
- 多个except块：处理不同异常
- 通用异常处理

运行：
    python exception_handling_demo.py

作者：自动生成示例（中文注释）
"""


def basic_try_except():
    print('--- 基本 try-except 示例 ---')
    try:
        num = int(input('请输入一个整数：'))
        result = 10 / num
        print(f'10 除以 {num} = {result}')
    except ValueError:
        print('输入不是有效整数！')
    except ZeroDivisionError:
        print('不能除以零！')
    print()


def try_except_else():
    print('--- try-except-else 示例 ---')
    try:
        x = int(input('请输入一个数字：'))
        y = 100 / x
    except (ValueError, ZeroDivisionError) as e:
        print(f'错误：{e}')
    else:
        print(f'计算成功：100 / {x} = {y}')
    print()


def try_except_finally():
    print('--- try-except-finally 示例 ---')
    try:
        file = open('example.txt', 'r')
        content = file.read()
        print('文件内容：', content)
    except FileNotFoundError:
        print('文件不存在！')
    finally:
        print('finally 块：无论如何都会执行（通常用于清理资源）')
        # 注意：这里没有 file.close() 因为文件没打开，但演示结构
    print()


def multiple_exceptions():
    print('--- 多个 except 块示例 ---')
    try:
        lst = [1, 2, 3]
        index = int(input('请输入索引（0-2）：'))
        value = lst[index]
        result = 10 / value
        print(f'lst[{index}] = {value}, 10 / {value} = {result}')
    except IndexError:
        print('索引超出范围！')
    except ZeroDivisionError:
        print('列表中不能有零值！')
    except ValueError:
        print('输入不是整数！')
    except Exception as e:  # 通用异常，最后处理
        print(f'其他错误：{e}')
    print()


def main():
    print('异常处理演示：')
    basic_try_except()
    try_except_else()
    try_except_finally()
    multiple_exceptions()


if __name__ == '__main__':
    main()