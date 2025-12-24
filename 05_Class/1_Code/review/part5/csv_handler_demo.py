"""
示例：CSV 文件读写

包含演示：
- csv.reader() 读取 CSV 文件
- csv.writer() 写入 CSV 文件
- 处理表格数据
- csv.DictReader 和 csv.DictWriter 高级用法

运行：
    python csv_handler_demo.py

作者：自动生成示例（中文注释）
"""

import csv
import os


def demo_write_csv():
    """演示写入 CSV 文件"""
    print('--- 写入 CSV 文件 ---')
    
    # 准备数据
    data = [
        ['姓名', '年龄', '城市'],
        ['Alice', 25, 'Beijing'],
        ['Bob', 30, 'Shanghai'],
        ['Charlie', 28, 'Guangzhou'],
        ['Diana', 26, 'Shenzhen']
    ]
    
    # 写入 CSV 文件
    # newline='' 可以防止多余的空行出现
    with open('students.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    print('CSV 文件写入完成')


def demo_read_csv():
    """演示读取 CSV 文件"""
    print('--- 读取 CSV 文件 ---')
    
    with open('students.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                print(f'表头：{row}')
            else:
                print(f'  {row}')
    print()


def demo_dict_writer():
    """演示字典形式的 CSV 写入"""
    print('--- 字典形式的 CSV 写入 ---')
    
    # 字典形式的数据
    data = [
        {'姓名': 'Emma', '年龄': 27, '城市': 'Hangzhou'},
        {'姓名': 'Frank', '年龄': 29, '城市': 'Chengdu'},
        {'姓名': 'Grace', '年龄': 24, '城市': 'Wuhan'}
    ]
    
    fieldnames = ['姓名', '年龄', '城市']
    
    with open('more_students.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()  # 写入表头
        writer.writerows(data)
    
    print('字典形式的 CSV 文件写入完成')


def demo_dict_reader():
    """演示字典形式的 CSV 读取"""
    print('--- 字典形式的 CSV 读取 ---')
    
    with open('more_students.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            print(f'第 {i} 行：{dict(row)}')
    print()


def demo_data_analysis():
    """演示 CSV 数据分析"""
    print('--- CSV 数据分析 ---')
    
    # 读取数据并分析
    ages = []
    with open('students.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头
        for row in reader:
            ages.append(int(row[1]))
    
    print(f'平均年龄：{sum(ages) / len(ages):.1f}')
    print(f'最小年龄：{min(ages)}')
    print(f'最大年龄：{max(ages)}')
    print()


def demo_csv_with_different_delimiter():
    """演示使用不同分隔符的 CSV"""
    print('--- 不同分隔符的 CSV ---')
    
    data = [
        ['Name', 'Score', 'Grade'],
        ['Alice', 85, 'B'],
        ['Bob', 92, 'A'],
        ['Charlie', 78, 'C']
    ]
    
    # 使用分号作为分隔符
    with open('scores.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(data)
    
    print('使用分号分隔符的 CSV 文件写入完成')
    
    # 读取时指定分隔符
    with open('scores.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            print(row)
    print()


def cleanup():
    """清理示例文件"""
    files = ['students.csv', 'more_students.csv', 'scores.csv']
    for file in files:
        if os.path.exists(file):
            os.remove(file)
    print('清理示例文件完成')


def main():
    print('=' * 50)
    print('CSV 文件读写演示')
    print('=' * 50)
    print()
    
    demo_write_csv()
    print()
    
    demo_read_csv()
    
    demo_dict_writer()
    print()
    
    demo_dict_reader()
    
    demo_data_analysis()
    
    demo_csv_with_different_delimiter()
    
    cleanup()


if __name__ == '__main__':
    main()