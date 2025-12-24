"""
示例：演示 re 模块的使用

包含演示：
- 正则表达式匹配
- 查找和替换
- 贪婪vs懒惰匹配

运行：
    python re_demo.py

作者：自动生成示例（中文注释）
"""

import re


def re_demo():
    print('--- re模块示例 ---')

    # 示例文本
    text = "我的邮箱是 example123@email.com，另一个是 test_456@domain.org。电话：138-1234-5678 或 15012345678。"

    # 查找所有邮箱地址
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    print("找到的邮箱:", emails)

    # 查找所有电话号码（简单模式）
    phone_pattern = r'\b1[3-9]\d{9}\b'
    phones = re.findall(phone_pattern, text)
    print("找到的电话:", phones)

    # 替换文本
    replaced = re.sub(r'\d+', '[数字]', text)
    print("替换数字后:", replaced)

    # 使用compile提高效率
    compiled_pattern = re.compile(r'\w+')
    words = compiled_pattern.findall("Hello world 123 test")
    print("单词列表:", words)

    # 贪婪vs懒惰匹配
    html = "<div><p>内容1</p><p>内容2</p></div>"
    greedy_match = re.findall(r'<p>.*</p>', html)
    lazy_match = re.findall(r'<p>.*?</p>', html)
    print("贪婪匹配:", greedy_match)
    print("懒惰匹配:", lazy_match)


def main():
    re_demo()


if __name__ == '__main__':
    main()
