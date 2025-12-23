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

# 线路颜色（如缺失则前端可回退为灰色）
LINE_COLORS = {
    '1号线': '#E3002C',
    '2号线': '#80BC00',
    '3号线': '#FFD600',
    '4号线': '#48227F',
    '5号线': '#BB31A3',
    '6号线': '#C77EB5',
    '7号线': '#F68F1E',
    '8号线': '#009DD7',
    '9号线': '#9C58A9',
    '10号线': '#C6AFCE',
    '10号线(支线)': '#C6AFCE',
    '11号线': '#9D7AD2',
    '11号线(支线)': '#9D7AD2',
    '12号线': '#008C95',
    '13号线': '#E0A243',
    '14号线': '#7D2E83',
    '15号线': '#C1A7E2',
    '16号线': '#5BB6D7',
    '17号线': '#6E76A6',
    '18号线': '#00A0E9',
    '浦江线': '#9ACD32',
}

# 系统配置
SYSTEM_CONFIG = {
    'version': '1.0.0',
    'encoding': 'utf-8',
    'debug': False
}
