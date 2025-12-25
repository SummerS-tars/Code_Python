"""
示例：第三方模块安装与管理

包含演示：
- pip 命令格式和使用
- 包的安装、卸载、查看
- 虚拟环境管理
- requirements.txt 文件的使用

注意：此示例主要展示命令格式，不会实际执行安装操作
需要网络连接和管理员权限才能实际执行

运行：
    python pip_management_demo.py

作者：自动生成示例（中文注释）
"""

import subprocess
import sys
import os


def demo_pip_commands():
    """演示 pip 命令格式（不实际执行）"""
    print('--- pip 命令格式演示 ---')

    commands = [
        {
            'name': '安装包',
            'command': 'pip install package_name',
            'description': '安装指定的包',
            'example': 'pip install pandas'
        },
        {
            'name': '安装特定版本',
            'command': 'pip install package_name==version',
            'description': '安装指定版本的包',
            'example': 'pip install pandas==2.0.0'
        },
        {
            'name': '从 requirements.txt 安装',
            'command': 'pip install -r requirements.txt',
            'description': '从文件安装多个包',
            'example': 'pip install -r requirements.txt'
        },
        {
            'name': '卸载包',
            'command': 'pip uninstall package_name',
            'description': '卸载指定的包',
            'example': 'pip uninstall pandas'
        },
        {
            'name': '查看已安装包',
            'command': 'pip list',
            'description': '列出所有已安装的包及其版本',
            'example': 'pip list'
        },
        {
            'name': '显示包信息',
            'command': 'pip show package_name',
            'description': '显示指定包的详细信息',
            'example': 'pip show pandas'
        },
        {
            'name': '升级包',
            'command': 'pip install --upgrade package_name',
            'description': '升级指定的包到最新版本',
            'example': 'pip install --upgrade pandas'
        },
        {
            'name': '导出依赖',
            'command': 'pip freeze > requirements.txt',
            'description': '将当前环境的所有包导出到文件',
            'example': 'pip freeze > requirements.txt'
        }
    ]

    for cmd in commands:
        print(f"\n{cmd['name']}:")
        print(f"  命令: {cmd['command']}")
        print(f"  说明: {cmd['description']}")
        print(f"  示例: {cmd['example']}")

    print()


def demo_requirements_file():
    """演示 requirements.txt 文件的使用"""
    print('--- requirements.txt 文件示例 ---')

    requirements_content = """# 数据分析相关包
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0

# 机器学习包
scikit-learn>=1.3.0
tensorflow>=2.13.0

# 开发工具
jupyter>=1.0.0
ipykernel>=6.0.0

# 其他工具
requests>=2.31.0
beautifulsoup4>=4.12.0
"""

    # 创建示例 requirements.txt 文件
    with open('example_requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements_content)

    print('已创建 example_requirements.txt 文件')
    print('文件内容：')
    print(requirements_content)

    # 演示如何从文件安装（命令格式）
    print('安装命令：')
    print('  pip install -r example_requirements.txt')
    print()


def demo_virtual_environment():
    """演示虚拟环境管理"""
    print('--- 虚拟环境管理 ---')

    venv_commands = [
        {
            'name': '创建虚拟环境',
            'command': 'python -m venv myenv',
            'description': '创建名为 myenv 的虚拟环境'
        },
        {
            'name': '激活虚拟环境 (Windows)',
            'command': 'myenv\\Scripts\\activate',
            'description': '激活虚拟环境'
        },
        {
            'name': '激活虚拟环境 (Linux/Mac)',
            'command': 'source myenv/bin/activate',
            'description': '激活虚拟环境'
        },
        {
            'name': '退出虚拟环境',
            'command': 'deactivate',
            'description': '退出当前虚拟环境'
        },
        {
            'name': '删除虚拟环境',
            'command': 'rmdir /s myenv  (Windows) 或 rm -rf myenv (Linux/Mac)',
            'description': '删除虚拟环境目录'
        }
    ]

    for cmd in venv_commands:
        print(f"\n{cmd['name']}:")
        print(f"  命令: {cmd['command']}")
        print(f"  说明: {cmd['description']}")

    print()


def demo_package_info():
    """演示获取已安装包的信息"""
    print('--- 查看已安装包信息 ---')

    try:
        # 尝试获取 pip 版本
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'],
                              capture_output=True, text=True, check=True)
        print(f"pip 版本: {result.stdout.strip()}")

        # 查看已安装的包（限制输出）
        result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--format=freeze'],
                              capture_output=True, text=True, check=True)

        installed_packages = result.stdout.strip().split('\n')
        print(f"\n已安装包数量: {len(installed_packages)}")

        # 显示前10个包
        print("前10个已安装包:")
        for i, pkg in enumerate(installed_packages[:10]):
            print(f"  {i+1}. {pkg}")

        if len(installed_packages) > 10:
            print(f"  ... 还有 {len(installed_packages) - 10} 个包")

    except subprocess.CalledProcessError as e:
        print(f"执行 pip 命令失败: {e}")
    except FileNotFoundError:
        print("未找到 pip 命令，请确保 Python 已正确安装")

    print()


def demo_import_test():
    """测试一些常用包的导入"""
    print('--- 常用包导入测试 ---')

    test_packages = [
        ('pandas', 'pd'),
        ('numpy', 'np'),
        ('matplotlib', 'plt'),
        ('seaborn', 'sns'),
        ('scikit-learn', 'sklearn'),
        ('requests', None),
        ('json', None),  # 标准库
        ('csv', None),   # 标准库
    ]

    for package, alias in test_packages:
        try:
            if alias:
                exec(f"import {package} as {alias}")
                print(f"✓ {package} ({alias}) - 已安装")
            else:
                exec(f"import {package}")
                print(f"✓ {package} - 已安装")
        except ImportError:
            print(f"✗ {package} - 未安装")
        except Exception as e:
            print(f"? {package} - 导入错误: {e}")

    print()


def cleanup():
    """清理示例文件"""
    files = ['example_requirements.txt']
    for file in files:
        if os.path.exists(file):
            os.remove(file)
    print('清理示例文件完成')


def main():
    print('=' * 50)
    print('第三方模块安装与管理演示')
    print('=' * 50)
    print()

    demo_pip_commands()

    demo_requirements_file()

    demo_virtual_environment()

    demo_package_info()

    demo_import_test()

    cleanup()


if __name__ == '__main__':
    main()