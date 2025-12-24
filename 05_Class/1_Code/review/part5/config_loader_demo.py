"""
示例：配置加载器与管理

包含演示：
- 从 JSON 文件加载配置
- 验证配置的必要字段
- 与默认值合并
- 创建默认配置文件
- 错误恢复机制

运行：
    python config_loader_demo.py

作者：自动生成示例（中文注释）
"""

import json
import os


# 默认配置常量
DEFAULT_CONFIG = {
    'app_name': 'MyApp',
    'version': '1.0.0',
    'debug': False,
    'log_level': 'INFO',
    'server': {
        'host': 'localhost',
        'port': 8000,
        'timeout': 30
    },
    'database': {
        'engine': 'sqlite',
        'path': './data.db',
        'max_connections': 10
    },
    'features': {
        'enable_cache': True,
        'cache_ttl': 3600,
        'enable_auth': True
    }
}


def load_config(config_file='config.json'):
    """
    加载配置文件
    
    参数：
        config_file (str): 配置文件路径
    
    返回：
        dict: 配置字典
    """
    if not os.path.exists(config_file):
        print(f'配置文件 {config_file} 不存在，使用默认配置')
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f'成功加载配置文件：{config_file}')
        return config
    except json.JSONDecodeError as e:
        print(f'配置文件 JSON 格式错误：{e}，使用默认配置')
        return DEFAULT_CONFIG.copy()
    except Exception as e:
        print(f'加载配置失败：{e}，使用默认配置')
        return DEFAULT_CONFIG.copy()


def validate_config(config):
    """
    验证配置的必要字段
    
    参数：
        config (dict): 要验证的配置
    
    返回：
        tuple: (是否有效, 错误信息列表)
    """
    errors = []
    
    # 验证必要字段
    if 'app_name' not in config:
        errors.append('缺少必要字段：app_name')
    
    if 'server' not in config or not isinstance(config['server'], dict):
        errors.append('缺少必要字段：server（应为字典）')
    else:
        if 'host' not in config['server']:
            errors.append('缺少必要字段：server.host')
        if 'port' not in config['server']:
            errors.append('缺少必要字段：server.port')
        elif not isinstance(config['server']['port'], int):
            errors.append('server.port 应为整数')
    
    if 'database' not in config or not isinstance(config['database'], dict):
        errors.append('缺少必要字段：database（应为字典）')
    else:
        if 'engine' not in config['database']:
            errors.append('缺少必要字段：database.engine')
    
    return len(errors) == 0, errors


def merge_with_defaults(config, defaults):
    """
    将配置与默认值合并（递归）
    
    参数：
        config (dict): 用户配置
        defaults (dict): 默认配置
    
    返回：
        dict: 合并后的配置
    """
    result = defaults.copy()
    
    for key, value in config.items():
        if key in defaults and isinstance(defaults[key], dict) and isinstance(value, dict):
            # 递归合并嵌套字典
            result[key] = merge_with_defaults(value, defaults[key])
        else:
            result[key] = value
    
    return result


def save_config(config, config_file='config.json'):
    """
    保存配置文件
    
    参数：
        config (dict): 要保存的配置
        config_file (str): 配置文件路径
    """
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f'配置已保存到：{config_file}')
    except Exception as e:
        print(f'保存配置失败：{e}')


def demo_basic_loading():
    """演示：基本加载"""
    print('--- 演示 1：基本加载 ---')
    
    # 模拟 1：配置文件不存在
    config = load_config('missing_config.json')
    print(f'加载的配置：app_name={config["app_name"]}, version={config["version"]}')
    print()


def demo_create_default():
    """演示：创建默认配置文件"""
    print('--- 演示 2：创建默认配置 ---')
    
    config_file = 'default_config.json'
    save_config(DEFAULT_CONFIG, config_file)
    
    # 验证创建的文件
    with open(config_file, 'r', encoding='utf-8') as f:
        content = f.read()
    print('创建的配置文件内容（前 300 字符）：')
    print(content[:300] + '...')
    print()


def demo_load_and_validate():
    """演示：加载并验证配置"""
    print('--- 演示 3：加载并验证 ---')
    
    # 创建一个测试配置文件
    test_config = {
        'app_name': 'TestApp',
        'server': {
            'host': '0.0.0.0',
            'port': 5000
        },
        'database': {
            'engine': 'postgres'
        }
    }
    
    with open('test_config.json', 'w', encoding='utf-8') as f:
        json.dump(test_config, f)
    
    # 加载并验证
    config = load_config('test_config.json')
    is_valid, errors = validate_config(config)
    
    if is_valid:
        print('✓ 配置验证成功')
    else:
        print('✗ 配置验证失败：')
        for error in errors:
            print(f'  - {error}')
    print()


def demo_merge_with_defaults():
    """演示：与默认值合并"""
    print('--- 演示 4：与默认值合并 ---')
    
    # 部分配置
    partial_config = {
        'app_name': 'CustomApp',
        'server': {
            'port': 9000  # 只覆盖 port，host 使用默认
        }
    }
    
    # 合并
    merged = merge_with_defaults(partial_config, DEFAULT_CONFIG)
    
    print('部分配置：')
    print(f'  app_name={partial_config["app_name"]}')
    print(f'  server.port={partial_config["server"]["port"]}')
    print()
    
    print('合并后的配置：')
    print(f'  app_name={merged["app_name"]}')
    print(f'  server.host={merged["server"]["host"]} （来自默认值）')
    print(f'  server.port={merged["server"]["port"]} （来自用户配置）')
    print(f'  database.engine={merged["database"]["engine"]} （来自默认值）')
    print()


def demo_invalid_config():
    """演示：处理无效的配置"""
    print('--- 演示 5：处理无效配置 ---')
    
    # 创建无效的 JSON 文件
    with open('invalid_config.json', 'w') as f:
        f.write('{ invalid json content }')
    
    config = load_config('invalid_config.json')
    is_valid, errors = validate_config(config)
    print(f'配置验证结果：有效={is_valid}')
    print()


def demo_nested_config():
    """演示：处理嵌套配置"""
    print('--- 演示 6：嵌套配置管理 ---')
    
    # 复杂配置
    complex_config = {
        'app_name': 'ComplexApp',
        'environments': {
            'development': {
                'server': {'host': 'localhost', 'port': 3000},
                'debug': True
            },
            'production': {
                'server': {'host': '0.0.0.0', 'port': 8000},
                'debug': False
            }
        }
    }
    
    # 保存
    save_config(complex_config, 'complex_config.json')
    
    # 加载并显示
    loaded = load_config('complex_config.json')
    print('已加载复杂配置')
    print(f'  开发环境 host: {loaded["environments"]["development"]["server"]["host"]}')
    print(f'  生产环境 debug: {loaded["environments"]["production"]["debug"]}')
    print()


def cleanup():
    """清理示例文件"""
    files = [
        'default_config.json',
        'test_config.json',
        'invalid_config.json',
        'complex_config.json'
    ]
    
    for file in files:
        if os.path.exists(file):
            os.remove(file)
    
    print('清理示例文件完成')


def main():
    print('=' * 50)
    print('配置加载器与管理演示')
    print('=' * 50)
    print()
    
    demo_basic_loading()
    
    demo_create_default()
    
    demo_load_and_validate()
    
    demo_merge_with_defaults()
    
    demo_invalid_config()
    
    demo_nested_config()
    
    cleanup()


if __name__ == '__main__':
    main()