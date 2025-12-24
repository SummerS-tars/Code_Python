"""
模块：file_handler（文件处理）

提供文件操作的功能，包括读取、写入、追加等。

使用方法：
    from file_handler import read_file, write_file
    content = read_file('example.txt')
"""


def read_file(filename):
    """
    读取文件内容
    
    参数：
        filename: 要读取的文件名
    
    返回：
        文件内容字符串
    
    异常：
        FileNotFoundError: 文件不存在
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f'文件 {filename} 不存在')


def write_file(filename, content):
    """
    将内容写入文件（覆盖）
    
    参数：
        filename: 要写入的文件名
        content: 要写入的内容
    
    返回：
        写入的字符数
    """
    with open(filename, 'w', encoding='utf-8') as f:
        return f.write(content)


def append_file(filename, content):
    """
    将内容追加到文件末尾
    
    参数：
        filename: 要追加的文件名
        content: 要追加的内容
    
    返回：
        追加的字符数
    """
    with open(filename, 'a', encoding='utf-8') as f:
        return f.write(content)


def count_lines(filename):
    """
    计算文件的行数
    
    参数：
        filename: 要统计的文件名
    
    返回：
        文件的行数
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except FileNotFoundError:
        raise FileNotFoundError(f'文件 {filename} 不存在')


def main():
    """模块的测试函数"""
    print('--- 文件处理模块测试 ---')
    
    # 创建测试文件
    test_file = 'test_file.txt'
    
    # 写入测试
    print('写入文件...')
    write_file(test_file, 'Hello, World!\n')
    print(f'写入完成')
    
    # 追加测试
    print('追加内容...')
    append_file(test_file, 'This is a test.\n')
    print('追加完成')
    
    # 读取测试
    print('读取文件内容：')
    content = read_file(test_file)
    print(content)
    
    # 计行数测试
    print(f'文件行数：{count_lines(test_file)}')
    
    # 清理测试文件
    import os
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f'测试文件 {test_file} 已删除')


# 模块的自测代码，仅在直接运行时执行
if __name__ == '__main__':
    main()
    print('\n模块自测完成（这段代码仅在直接运行此模块时执行）')