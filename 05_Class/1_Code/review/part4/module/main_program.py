"""
主程序：演示模块化设计

这个程序演示如何：
1. 导入和使用自定义模块
2. 模块化设计的优势
3. 自顶向下的设计方法

运行方法：
    python main_program.py

前提条件：
    确保 calculator.py 和 file_handler.py 在同一目录下
"""

# 导入自定义模块
import calculator
from file_handler import write_file, read_file, count_lines


def perform_calculations():
    """演示计算器模块的使用"""
    print('--- 模块化演示：计算器功能 ---')
    print('计算 10 + 5 =', calculator.add(10, 5))
    print('计算 20 - 8 =', calculator.subtract(20, 8))
    print('计算 6 * 7 =', calculator.multiply(6, 7))
    print('计算 30 / 5 =', calculator.divide(30, 5))
    print('计算 2 ^ 10 =', calculator.power(2, 10))
    print()


def perform_file_operations():
    """演示文件处理模块的使用"""
    print('--- 模块化演示：文件操作 ---')
    
    # 创建一个测试文件并写入数据
    filename = 'data.txt'
    content = '这是一个演示文件\n包含多行内容\n用于展示文件模块的功能\n'
    
    print(f'写入文件 {filename}...')
    write_file(filename, content)
    
    print('读取文件内容：')
    file_content = read_file(filename)
    print(file_content)
    
    print(f'文件行数：{count_lines(filename)}')
    
    # 清理
    import os
    os.remove(filename)
    print(f'已删除测试文件 {filename}')
    print()


def demonstrate_modular_design():
    """演示模块化设计的优势"""
    print('--- 模块化设计的优势演示 ---')
    print('1. 代码复用：calculator 模块可以在任何需要计算的地方使用')
    print('2. 易于维护：文件操作的逻辑集中在 file_handler 模块中')
    print('3. 易于扩展：可以轻松添加新的功能模块而不影响现有代码')
    print('4. 易于测试：每个模块都可以独立测试')
    print()


def main():
    """主程序入口"""
    print('=' * 50)
    print('Python 模块化设计演示')
    print('=' * 50)
    print()
    
    # 调用各个演示函数
    perform_calculations()
    perform_file_operations()
    demonstrate_modular_design()
    
    print('=' * 50)
    print('演示完成！')
    print('=' * 50)
    print()
    print('这个程序展示了自顶向下的模块化设计：')
    print('1. 主程序（main_program.py）：协调各个模块')
    print('2. 专用模块（calculator.py）：提供计算功能')
    print('3. 专用模块（file_handler.py）：提供文件操作功能')
    print()
    print('每个模块都是高内聚的，专注于完成特定功能。')


if __name__ == '__main__':
    main()