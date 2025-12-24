"""
示例：综合函数实战示例

包含实战场景：
- 数据处理：计算列表的统计信息
- 文本处理：分析字符串
- 验证器：输入验证函数
- 装饰器风格：函数包装

运行：
    python functions_practical_demo.py

作者：自动生成示例（中文注释）
"""


def list_statistics(*numbers):
    """
    计算数值列表的统计信息
    
    参数：
        *numbers: 任意数量的数值
    
    返回：
        字典，包含 count, sum, avg, min, max
    """
    if not numbers:
        return None
    
    return {
        'count': len(numbers),
        'sum': sum(numbers),
        'avg': sum(numbers) / len(numbers),
        'min': min(numbers),
        'max': max(numbers)
    }


def count_words(text):
    """统计文本中的单词数和字符数"""
    words = text.split()
    return {
        'word_count': len(words),
        'char_count': len(text),
        'char_count_no_space': len(text.replace(' ', ''))
    }


def validate_email(email):
    """简单的电子邮件验证"""
    if '@' not in email or '.' not in email.split('@')[1]:
        return False
    return True


def validate_password(pwd):
    """密码验证：至少8个字符，包含大小写和数字"""
    if len(pwd) < 8:
        return False, '密码长度至少8个字符'
    if not any(c.isupper() for c in pwd):
        return False, '密码需要包含大写字母'
    if not any(c.islower() for c in pwd):
        return False, '密码需要包含小写字母'
    if not any(c.isdigit() for c in pwd):
        return False, '密码需要包含数字'
    return True, '密码有效'


def repeat(times):
    """装饰器风格：重复执行函数"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator


def process_data(data, *filters, sort_by=None):
    """
    处理数据的多功能函数
    
    参数：
        data: 要处理的数据列表（字典）
        *filters: 过滤函数
        sort_by: 排序键
    """
    # 应用所有过滤
    result = data
    for filter_func in filters:
        result = list(filter(filter_func, result))
    
    # 排序
    if sort_by:
        result = sorted(result, key=sort_by)
    
    return result


def data_pipeline(data, *operations):
    """数据管道：按顺序应用一系列操作"""
    result = data
    for operation in operations:
        result = operation(result)
    return result


def main():
    print('--- 数据统计示例 ---')
    stats = list_statistics(10, 20, 30, 40, 50)
    print('统计信息：', stats)
    
    print('\n--- 文本分析示例 ---')
    text = 'Python is a powerful programming language'
    word_info = count_words(text)
    print(f'文本："{text}"')
    print('分析结果：', word_info)
    
    print('\n--- 验证示例 ---')
    emails = ['user@example.com', 'invalid.email', 'test@domain.co.uk']
    for email in emails:
        print(f'{email} 是否有效：{validate_email(email)}')
    
    print('\n--- 密码验证示例 ---')
    passwords = ['simple', 'Simple123', 'NoDigit123ABC']
    for pwd in passwords:
        valid, msg = validate_password(pwd)
        print(f'"{pwd}" - {msg}')
    
    print('\n--- 数据处理示例 ---')
    students = [
        {'name': 'Alice', 'score': 85, 'grade': 'B'},
        {'name': 'Bob', 'score': 92, 'grade': 'A'},
        {'name': 'Charlie', 'score': 78, 'grade': 'C'},
        {'name': 'Diana', 'score': 88, 'grade': 'B'}
    ]
    
    # 过滤分数大于80的学生，按分数排序
    filtered = process_data(
        students,
        lambda s: s['score'] >= 80,
        sort_by=lambda s: s['score']
    )
    print('分数大于等于80的学生（按分数排序）：')
    for student in filtered:
        print(f"  {student['name']}: {student['score']}")
    
    print('\n--- 数据管道示例 ---')
    numbers = [1, 2, 3, 4, 5]
    result = data_pipeline(
        numbers,
        lambda lst: list(map(lambda x: x * 2, lst)),  # 每个数乘以2
        lambda lst: list(filter(lambda x: x > 5, lst))  # 过滤大于5的
    )
    print(f'{numbers} 经过管道处理：{result}')


if __name__ == '__main__':
    main()