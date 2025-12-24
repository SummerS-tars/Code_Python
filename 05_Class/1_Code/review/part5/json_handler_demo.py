"""
示例：JSON 文件读写与数据序列化

包含演示：
- json.dump() 写入 JSON 文件
- json.load() 读取 JSON 文件
- json.dumps() 序列化为字符串
- json.loads() 反序列化字符串
- Python 对象到 JSON 的类型转换
- 复杂嵌套数据结构

运行：
    python json_handler_demo.py

作者：自动生成示例（中文注释）
"""

import json
import os


def demo_dump_load():
    """演示 dump 和 load（文件操作）"""
    print('--- json.dump() 和 json.load() ---')
    
    # Python 对象
    data = {
        'name': 'Alice',
        'age': 25,
        'city': 'Beijing',
        'hobbies': ['reading', 'coding', 'hiking'],
        'is_student': True,
        'gpa': None
    }
    
    # 写入 JSON 文件
    with open('person.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print('JSON 文件写入完成')
    print('文件内容：')
    with open('person.json', 'r', encoding='utf-8') as f:
        print(f.read())
    
    # 读取 JSON 文件
    with open('person.json', 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)
    
    print('读取的数据：', loaded_data)
    print()


def demo_dumps_loads():
    """演示 dumps 和 loads（字符串操作）"""
    print('--- json.dumps() 和 json.loads() ---')
    
    # Python 对象
    person = {
        'name': 'Bob',
        'age': 30,
        'skills': ['Python', 'JavaScript', 'SQL']
    }
    
    # 序列化为 JSON 字符串
    json_string = json.dumps(person, ensure_ascii=False, indent=2)
    print('JSON 字符串：')
    print(json_string)
    
    # 反序列化
    parsed_data = json.loads(json_string)
    print('解析后的数据：', parsed_data)
    print()


def demo_type_conversion():
    """演示 Python 类型到 JSON 类型的转换"""
    print('--- Python 类型与 JSON 类型转换 ---')
    
    data = {
        'string': 'Hello',
        'integer': 42,
        'float': 3.14,
        'boolean_true': True,
        'boolean_false': False,
        'null_value': None,
        'list': [1, 2, 3],
        'dict': {'nested': 'value'},
        'tuple': (4, 5, 6)  # 元组会转换为列表
    }
    
    json_string = json.dumps(data, indent=2)
    print('转换结果：')
    print(json_string)
    print()


def demo_nested_structure():
    """演示复杂嵌套数据结构"""
    print('--- 复杂嵌套结构 ---')
    
    company_data = {
        'company_name': 'Tech Corp',
        'departments': [
            {
                'name': 'Engineering',
                'employees': [
                    {'id': 1, 'name': 'Alice', 'salary': 80000},
                    {'id': 2, 'name': 'Bob', 'salary': 75000}
                ]
            },
            {
                'name': 'Sales',
                'employees': [
                    {'id': 3, 'name': 'Charlie', 'salary': 70000}
                ]
            }
        ]
    }
    
    # 写入文件
    with open('company.json', 'w', encoding='utf-8') as f:
        json.dump(company_data, f, ensure_ascii=False, indent=2)
    
    print('复杂数据结构写入完成')
    
    # 读取并展示
    with open('company.json', 'r', encoding='utf-8') as f:
        loaded = json.load(f)
    
    print(f'公司：{loaded["company_name"]}')
    for dept in loaded['departments']:
        print(f'  部门：{dept["name"]}')
        for emp in dept['employees']:
            print(f'    员工：{emp["name"]}，薪资：{emp["salary"]}')
    print()


def demo_pretty_print():
    """演示格式化输出"""
    print('--- 格式化输出 ---')
    
    data = {'name': 'Diana', 'items': [1, 2, 3, 4, 5]}
    
    # 紧凑格式
    compact = json.dumps(data, separators=(',', ':'))
    print('紧凑格式：', compact)
    
    # 美化格式（默认）
    pretty = json.dumps(data, indent=2)
    print('美化格式：')
    print(pretty)
    print()


def demo_error_handling():
    """演示错误处理"""
    print('--- 错误处理 ---')
    
    # 有效的 JSON
    try:
        valid_json = '{"name": "Eve", "age": 28}'
        data = json.loads(valid_json)
        print('有效的 JSON 解析成功：', data)
    except json.JSONDecodeError as e:
        print('JSON 解码错误：', e)
    
    # 无效的 JSON
    try:
        invalid_json = "{'name': 'Frank'}"  # 使用单引号不符合 JSON 标准
        data = json.loads(invalid_json)
    except json.JSONDecodeError as e:
        print('捕获到 JSON 解码错误（预期）')
    
    # 文件不存在
    try:
        with open('nonexistent.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print('捕获到文件不存在错误（预期）')
    print()


def cleanup():
    """清理示例文件"""
    files = ['person.json', 'company.json']
    for file in files:
        if os.path.exists(file):
            os.remove(file)
    print('清理示例文件完成')


def main():
    print('=' * 50)
    print('JSON 文件读写演示')
    print('=' * 50)
    print()
    
    demo_dump_load()
    
    demo_dumps_loads()
    
    demo_type_conversion()
    
    demo_nested_structure()
    
    demo_pretty_print()
    
    demo_error_handling()
    
    cleanup()


if __name__ == '__main__':
    main()