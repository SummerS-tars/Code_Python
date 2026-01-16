#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
升级版 YOLO 标注可视化工具
适配 2025-12-02 GAT 扩展协议 (支持 0-14 类) 并对接 config 模块
"""

import os
import argparse
import cv2
import numpy as np
from typing import List, Tuple
import config  # 导入你独立出来的配置模块

def read_yolo_label(label_path: str) -> List[Tuple[int, float, float, float, float]]:
    """读取YOLO格式标注文件"""
    annotations = []
    if not os.path.exists(label_path):
        return annotations
    with open(label_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 5:
                annotations.append((int(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])))
    return annotations

def yolo_to_bbox(x_center, y_center, width, height, img_width, img_height):
    """将YOLO格式转换为边界框坐标"""
    x1 = int((x_center - width / 2) * img_width)
    y1 = int((y_center - height / 2) * img_height)
    x2 = int((x_center + width / 2) * img_width)
    y2 = int((y_center + height / 2) * img_height)
    return x1, y1, x2, y2

def get_class_name_ascii(class_id: int, scheme: str = 'three_class') -> str:
    """根据类别ID获取对应的英文名称，适配 15 类协议"""
    if scheme == 'three_class':
        names = {
            0: 'text', 1: 'image', 2: 'clickable',
            3: 'FrameLayout', 4: 'LinearLayout', 5: 'RelativeLayout',
            6: 'ConstraintLayout', 7: 'ViewGroup', 8: 'RecyclerView',
            9: 'ViewPager', 10: 'ScrollView', 11: 'HorizontalScrollView',
            12: 'NestedScrollView', 13: 'DrawerLayout', 14: 'CoordinatorLayout'
        }
        return names.get(class_id, f'class_{class_id}')
    return f'class_{class_id}'

def get_class_color(class_id: int) -> Tuple[int, int, int]:
    """为不同类别分配颜色 (BGR格式)"""
    colors = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255),
        (0, 255, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0),
        (128, 0, 128), (0, 128, 128), (192, 192, 192), (64, 64, 64), (255, 165, 0)
    ]
    return colors[class_id % len(colors)]

def visualize_with_opencv(image_path, label_path, output_path, scheme='three_class', show_labels=True):
    img = cv2.imread(image_path)
    if img is None: return
    h, w = img.shape[:2]
    annotations = read_yolo_label(label_path)

    # 新增：用于记录每个坐标点已绘制的标签高度，防止重叠
    label_offsets = {}

    for class_id, x_c, y_c, nw, nh in annotations:
        x1, y1, x2, y2 = yolo_to_bbox(x_c, y_c, nw, nh, w, h)
        color = get_class_color(class_id)
        name = get_class_name_ascii(class_id, scheme)
        
        # 始终绘制边界框（线条重合没关系，颜色会叠加）
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        if show_labels:
            label = f"{name}({class_id})"
            font_scale = 0.4
            thickness = 1
            (tw, th), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
            
            # 计算该坐标点目前的偏移量
            pos_key = (x1, y1)
            current_offset = label_offsets.get(pos_key, 0)
            
            # 动态调整标签高度：向上堆叠
            text_y = y1 - current_offset - 5
            
            # 绘制标签背景
            cv2.rectangle(img, (x1, text_y - th), (x1 + tw, text_y + baseline), color, -1)
            # 绘制标签文字
            cv2.putText(img, label, (x1, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
            
            # 更新该位置的偏移量，为下一个标签留出空间
            label_offsets[pos_key] = current_offset + th + 10 

    cv2.imwrite(output_path, img)

def batch_visualize(image_dir, label_dir, output_dir, scheme):
    """批量处理文件夹中的所有标注文件"""
    os.makedirs(output_dir, exist_ok=True)
    label_files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]
    for label_file in label_files:
        base = label_file.replace('.txt', '')
        img_path = os.path.join(image_dir, base + ".jpg")
        if os.path.exists(img_path):
            output_path = os.path.join(output_dir, f"{base}_visualized.jpg")
            visualize_with_opencv(img_path, os.path.join(label_dir, label_file), output_path, scheme)

def main():
    parser = argparse.ArgumentParser(description='YOLO标注可视化工具')
    # 路径默认从 config 模块中动态读取
    parser.add_argument('--image_dir', type=str, default=config.OUTPUT_DIR)
    parser.add_argument('--label_dir', type=str, default=config.OUTPUT_DIR)
    parser.add_argument('--output_dir', type=str, default=config.OUTPUT_DIR)
    parser.add_argument('--scheme', type=str, default='three_class')
    
    args = parser.parse_args()
    
    if args.image_dir and os.path.exists(args.image_dir):
        print(f"🎨 正在可视化 [{config.APP_NAME}] 的数据集...")
        batch_visualize(args.image_dir, args.label_dir, args.output_dir, args.scheme)
        print(f"✅ 完成！结果保存在: {args.output_dir}")
    else:
        print(f"❌ 错误: 找不到目录 {args.image_dir}")

if __name__ == '__main__':
    main()