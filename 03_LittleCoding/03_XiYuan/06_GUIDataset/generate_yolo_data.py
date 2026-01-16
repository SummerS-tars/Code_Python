#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
import config  # 接入动态路径配置
from xml_to_yolo_converter import convert_xml_to_yolo, parse_bounds
# 直接导入你上传的可视化工具函数
from visualize_yolo_labels import visualize_with_opencv

def process_single_file(xml_path, image_path, output_dir, scheme, min_size):
    """处理单对文件并生成可视化图"""
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(xml_path))[0]
    
    # 1. 自动从 XML 确定图像尺寸（不写死 1080x2376）
    img_width, img_height = 1080, 2376 # 默认
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(xml_path)
        root_bounds = tree.getroot().get('bounds', '')
        if root_bounds:
            _, _, img_width, img_height = parse_bounds(root_bounds)
    except:
        pass

    # 2. 生成 YOLO .txt 标注
    yolo_output_path = os.path.join(output_dir, f"{base_name}.txt")
    convert_xml_to_yolo(xml_path, yolo_output_path, img_width, img_height, scheme, min_size)
    
    # 3. 复制图片到数据集目录并生成可视化核对图
    output_image_path = os.path.join(output_dir, f"{base_name}.jpg")
    shutil.copy2(image_path, output_image_path)
    
    visualized_output_path = os.path.join(output_dir, f"{base_name}_visualized.jpg")
    # 调用你上传的可视化模块
    visualize_with_opencv(output_image_path, yolo_output_path, visualized_output_path, scheme, show_labels=True)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='朱文凯的自动化数据集处理器')
    # 路径默认从 config.py 读取
    parser.add_argument('--data_dir', type=str, default=config.SAVE_DIR)
    parser.add_argument('--output_dir', type=str, default=config.OUTPUT_DIR)
    # 默认使用三类标注（含GAT布局类别）
    parser.add_argument('--scheme', type=str, default='three_class')
    parser.add_argument('--min_size', type=int, default=10)
    
    args = parser.parse_args()
    
    if not os.path.exists(args.data_dir):
        print(f"❌ 未找到文件夹: {args.data_dir}")
        return

    xml_files = [f for f in os.listdir(args.data_dir) if f.endswith('.xml')]
    print(f"🚀 开始处理 [{config.APP_NAME}] 的 {len(xml_files)} 个页面...")
    
    for xml_file in xml_files:
        base = os.path.splitext(xml_file)[0]
        img_path = os.path.join(args.data_dir, base + ".jpg")
        if os.path.exists(img_path):
            process_single_file(os.path.join(args.data_dir, xml_file), img_path, args.output_dir, args.scheme, args.min_size)

    print(f"\n✅ 处理完成！请在 {args.output_dir} 中核对可视化图片，检查是否有漏框。")

if __name__ == '__main__':
    main()