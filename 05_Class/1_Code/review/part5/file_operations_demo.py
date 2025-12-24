"""
示例：文件读写基础与持久化

包含演示：
- open() 函数和各种文件模式
- with 语句管理文件上下文
- 读取文件的多种方式
- 写入和追加文件内容
- 文件指针位置管理

运行：
    python file_operations_demo.py

作者：自动生成示例（中文注释）
"""


def demo_basic_read_write():
    """演示基本的读写操作"""
    print('--- 基本读写操作 ---')
    
    # 写入文件
    with open('example.txt', 'w', encoding='utf-8') as f:
        f.write('Hello, World!\n')
        f.write('This is line 2.\n')
        f.write('This is line 3.\n')
    print('文件写入完成')
    
    # 读取整个文件
    with open('example.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    print('文件内容：')
    print(content)


def demo_readlines():
    """演示逐行读取"""
    print('--- 逐行读取 ---')
    
    with open('example.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()  # 返回列表，每个元素包含换行符
    
    print(f'共有 {len(lines)} 行')
    for i, line in enumerate(lines, 1):
        print(f'第 {i} 行：{line.strip()}')
    print()


def demo_readline():
    """演示逐行读取（一次一行）"""
    print('--- 单行读取（for循环） ---')
    
    with open('example.txt', 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1): # 类似生成器的行为
            print(f'第 {i} 行：{line.strip()}')
    print()


def demo_append():
    """演示追加模式"""
    print('--- 追加模式 ---')
    
    # 原始内容
    print('原始内容：')
    with open('example.txt', 'r', encoding='utf-8') as f:
        print(f.read())
    
    # 追加新内容
    with open('example.txt', 'a', encoding='utf-8') as f:
        f.write('This is appended line 4.\n')
        f.write('This is appended line 5.\n')
    
    print('追加后的内容：')
    with open('example.txt', 'r', encoding='utf-8') as f:
        print(f.read())


def demo_read_write_mode():
    """演示读写模式（r+ 和 w+）"""
    print('--- 读写模式 ---')
    
    # w+ 模式：写入并读取
    with open('rw_example.txt', 'w+', encoding='utf-8') as f:
        f.write('Line 1\n')
        f.write('Line 2\n')
        f.write('Line 3\n')
        
        # 回到文件开头读取
        f.seek(0)
        content = f.read()
        print('w+ 模式下的内容：')
        print(content)
    
    # r+ 模式：读取并修改
    with open('rw_example.txt', 'r+', encoding='utf-8') as f:
        f.seek(0)
        content = f.read()
        print('原始内容：')
        print(content)
        
        # 从开头写入（覆盖）
        f.seek(0)
        f.write('Modified content\n')
    
    print('修改后的内容：')
    with open('rw_example.txt', 'r', encoding='utf-8') as f:
        print(f.read())
    print()


def demo_file_pointer():
    """演示文件指针操作"""
    print('--- 文件指针操作 ---')
    
    with open('example.txt', 'r', encoding='utf-8') as f:
        # 读取前 10 个字符
        print('前 10 个字符：', f.read(10))
        print('当前指针位置：', f.tell())
        
        # 回到开头
        f.seek(0)
        print('回到开头后的指针位置：', f.tell())
        
        # 读取下一行
        first_line = f.readline()
        print('第一行：', first_line.strip())
        print('当前指针位置：', f.tell())
    print()


def demo_exception_handling():
    """演示异常处理"""
    print('--- 异常处理 ---')
    
    # 尝试读取不存在的文件
    try:
        with open('nonexistent.txt', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print('捕获异常：文件不存在')
    
    # 权限错误示例（注释掉，避免权限问题）
    try:
        with open('example.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        print('文件成功打开')
    except PermissionError:
        print('权限不足')
    except IOError as e:
        print(f'IO错误：{e}')
    print()


def cleanup():
    """清理示例文件"""
    import os
    files = ['example.txt', 'rw_example.txt']
    for file in files:
        if os.path.exists(file):
            os.remove(file)
    print('清理示例文件完成')


def main():
    print('=' * 50)
    print('文件读写基础演示')
    print('=' * 50)
    print()
    
    demo_basic_read_write()
    print()
    
    demo_readlines()
    
    demo_readline()
    
    demo_append()
    print()
    
    demo_read_write_mode()
    
    demo_file_pointer()
    
    demo_exception_handling()
    
    cleanup()


if __name__ == '__main__':
    main()