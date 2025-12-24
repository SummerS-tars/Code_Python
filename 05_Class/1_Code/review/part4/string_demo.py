"""
示例：演示 string 模块的使用

包含演示：
- 常用常量
- 字符串操作
- 生成随机密码

运行：
    python string_demo.py

作者：自动生成示例（中文注释）
"""

import string
import random


def string_demo():
    print('--- string模块示例 ---')

    # 常用常量
    print("数字:", string.digits)
    print("字母:", string.ascii_letters)
    print("标点:", string.punctuation)

    # 生成随机密码
    password_chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(password_chars, k=8))
    print("随机密码:", password)

    # 字符串操作
    text = "Hello World Python"

    # 联接
    words = ["Hello", "World", "Python"]
    joined = " ".join(words)
    print("联接字符串:", joined)

    # 分割
    split_text = text.split()
    print("分割字符串:", split_text)

    # 对齐
    print("居中对齐:", text.center(20, '-'))
    print("左对齐:", text.ljust(20, '-'))
    print("右对齐:", text.rjust(20, '-'))

    # 查找与检查
    print("查找 'World':", text.find("World"))
    print("以 'Hello' 开头:", text.startswith("Hello"))
    print("'123' 是数字:", "123".isdigit())


def main():
    string_demo()


if __name__ == '__main__':
    main()
