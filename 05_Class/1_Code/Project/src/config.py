"""配置文件

该模块包含系统的配置参数。
"""

import os

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 文档目录
DOC_DIR = os.path.join(PROJECT_ROOT, 'doc')

# 默认数据文件路径
DEFAULT_DATA_FILE = os.path.join(DOC_DIR, '线路.csv')

# 系统配置
SYSTEM_CONFIG = {
    'version': '1.0.0',
    'encoding': 'utf-8',
    'debug': False
}
