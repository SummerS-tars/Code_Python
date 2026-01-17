# config.py
import os

# 1. 根据你的最新 STF 截图更新的设备地址
DEVICE_ADDR = "10.176.65.211:7469" #

# 2. 当前正在采集的 App 名称。修改此处会自动切换所有读写路径
# 例如: 'eleme', 'zhifubao', 'alipay', '12306'
APP_NAME = "tencent_meeting"

# 3. 动态生成文件夹路径
# 采集原始数据：./data_collection_appname
SAVE_DIR = f"./data_collection_{APP_NAME}"
# 产出 YOLO 数据集：./dataset_appname
OUTPUT_DIR = f"./dataset_{APP_NAME}"

# 启动时自动检查并创建采集目录
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)