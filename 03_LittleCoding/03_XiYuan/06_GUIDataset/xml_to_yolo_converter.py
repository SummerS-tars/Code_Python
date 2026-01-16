#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XML到YOLO格式转换器
从Android UI XML层次结构中提取组件信息并转换为YOLO格式标注

支持多种标注方案：
1. 两类标注：文字(0) vs 图片(1)
2. 三类标注：文字(0) vs 图片(1) vs 可点击组件(2)
3. 细粒度标注：按Android组件类型分类
"""

import xml.etree.ElementTree as ET
import os
import argparse
from typing import List, Tuple, Dict
import re


def parse_bounds(bounds_str: str) -> Tuple[int, int, int, int]:
    """
    解析bounds字符串，返回 (x1, y1, x2, y2)
    
    Args:
        bounds_str: 格式如 "[0,0][1080,2376]"
        
    Returns:
        Tuple[int, int, int, int]: (x1, y1, x2, y2)
    """
    match = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds_str)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))
    return 0, 0, 0, 0


def get_component_type(node: ET.Element) -> str:
    """
    获取组件类型
    
    Args:
        node: XML节点
        
    Returns:
        str: 组件类型（如 'TextView', 'ImageView'等）
    """
    return node.get('class', '').split('.')[-1] if node.get('class') else ''


def is_clickable(node: ET.Element) -> bool:
    """
    判断节点是否可点击
    
    Args:
        node: XML节点
        
    Returns:
        bool: 是否可点击
    """
    return node.get('clickable', 'false').lower() == 'true'


def has_text(node: ET.Element) -> bool:
    """
    判断节点是否有文本内容
    
    Args:
        node: XML节点
        
    Returns:
        bool: 是否有文本
    """
    text = node.get('text', '').strip()
    content_desc = node.get('content-desc', '').strip()
    return bool(text or content_desc)


def is_visible(node: ET.Element) -> bool:
    """
    判断节点是否可见
    
    Args:
        node: XML节点
        
    Returns:
        bool: 是否可见
    """
    return node.get('visible-to-user', 'false').lower() == 'true'


def extract_components(xml_path: str, min_size: int = 10) -> List[Dict]:
    """
    从XML文件中提取所有UI组件
    
    Args:
        xml_path: XML文件路径
        min_size: 最小组件尺寸（过滤太小的组件）
        
    Returns:
        List[Dict]: 组件列表，每个组件包含 bounds, type, clickable, text 等信息
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except Exception as e:
        print(f"解析XML文件失败 {xml_path}: {e}")
        return []
    
    components = []
    
    def traverse(node: ET.Element, depth: int = 0):
        """递归遍历XML树"""
        # 获取bounds
        bounds_str = node.get('bounds', '')
        if not bounds_str:
            # 继续遍历子节点
            for child in node:
                traverse(child, depth + 1)
            return
        
        x1, y1, x2, y2 = parse_bounds(bounds_str)
        width = x2 - x1
        height = y2 - y1
        
        # 过滤太小的组件
        if width < min_size or height < min_size:
            for child in node:
                traverse(child, depth + 1)
            return
        
        # 过滤不可见的组件
        if not is_visible(node):
            for child in node:
                traverse(child, depth + 1)
            return
        
        # 获取组件信息
        comp_type = get_component_type(node)
        clickable = is_clickable(node)
        has_text_content = has_text(node)
        text = node.get('text', '') or node.get('content-desc', '')
        
        # 统计子组件数量（用于区分单个组件和组合布局）
        child_count = len([c for c in node if c.get('bounds')])
        
        # 统计子组件类型（用于识别商品卡片等复杂组件）
        child_types = []
        for child in node:
            if child.get('bounds'):
                child_type = get_component_type(child)
                if child_type:
                    child_types.append(child_type)
        
        # 判断是否可能是商品卡片（包含图片和文字的容器）
        has_image_child = 'ImageView' in child_types
        has_text_child = 'TextView' in child_types
        is_product_card = has_image_child and has_text_child and child_count >= 3
        
        # 存储组件信息
        component = {
            'bounds': (x1, y1, x2, y2),
            'type': comp_type,
            'clickable': clickable,
            'has_text': has_text_content,
            'text': text,
            'width': width,
            'height': height,
            'child_count': child_count,  # 子组件数量
            'has_content_desc': bool(node.get('content-desc', '').strip()),  # 是否有content-desc
            'is_product_card': is_product_card,  # 是否可能是商品卡片
            'child_types': child_types  # 子组件类型列表
        }
        
        components.append(component)
        
        # 继续遍历所有子节点（不管是什么类型，都继续遍历）
        for child in node:
            traverse(child, depth + 1)
    
    traverse(root)
    
    # 去重：如果子组件完全包含在父组件中，移除父组件
    components = remove_overlapping_parents(components)
    
    return components


def remove_overlapping_parents(components: List[Dict]) -> List[Dict]:
    """
    改进的智能去重策略：
    1. 优先保留具体类型组件（TextView, ImageView等）
    2. 只保留有实际内容或交互的布局容器
    3. 严格过滤空白容器
    """
    if len(components) <= 1:
        return components
    
    # 定义具体类型组件（这些必须保留）
    specific_types = ['TextView', 'ImageView', 'Button', 'EditText', 
                     'CheckBox', 'RadioButton', 'Switch', 'ProgressBar', 
                     'SeekBar', 'ToggleButton', 'ImageButton']
    
    # 定义布局容器类型
    layout_types = ['FrameLayout', 'LinearLayout', 'RelativeLayout', 
                    'ConstraintLayout', 'ViewGroup', 'RecyclerView', 
                    'ViewPager', 'ScrollView', 'HorizontalScrollView',
                    'NestedScrollView', 'DrawerLayout', 'CoordinatorLayout']
    
    # 按面积从大到小排序
    components_sorted = sorted(components, 
                              key=lambda x: -(x['width'] * x['height']))
    
    filtered = []
    
    for comp in components_sorted:
        x1, y1, x2, y2 = comp['bounds']
        comp_type = comp['type']
        clickable = comp['clickable']
        has_text = comp.get('has_text', False)
        has_content_desc = comp.get('has_content_desc', False)
        child_count = comp.get('child_count', 0)
        area = comp['width'] * comp['height']
        
        # === 规则1: 具体类型组件直接保留 ===
        if comp_type in specific_types:
            # 但要排除被相同bounds的其他具体类型组件覆盖的情况
            has_same_bounds_specific = False
            for other in filtered:
                if other['bounds'] == comp['bounds'] and other['type'] in specific_types:
                    has_same_bounds_specific = True
                    break
            
            if not has_same_bounds_specific:
                filtered.append(comp)
            continue
        
        # === 规则2: 可点击组件保留 ===
        if clickable:
            # 检查是否已有相同bounds的可点击组件
            has_same_clickable = False
            for other in filtered:
                if other['bounds'] == comp['bounds'] and other['clickable']:
                    has_same_clickable = True
                    break
            
            if not has_same_clickable:
                filtered.append(comp)
            continue
        
        # === 规则3: View类型特殊处理 ===
        if comp_type == 'View':
            # View如果没有子组件、不可点击、没有文本，很可能是装饰性的
            if child_count == 0 and not clickable and not has_text:
                # 检查是否被其他组件完全包含
                is_contained = False
                for other in filtered:
                    ox1, oy1, ox2, oy2 = other['bounds']
                    if ox1 <= x1 and oy1 <= y1 and ox2 >= x2 and oy2 >= y2:
                        if other['type'] in specific_types or other['clickable']:
                            is_contained = True
                            break
                
                if not is_contained:
                    filtered.append(comp)
            else:
                filtered.append(comp)
            continue
        
        # === 规则4: 布局容器严格筛选 ===
        if comp_type in layout_types:
            # 容器保留条件（必须满足至少一个）：
            should_keep = False
            
            # 4.1 有文本或content-desc（内容容器）
            if has_text or has_content_desc:
                should_keep = True
            
            # 4.2 可点击（交互容器）
            elif clickable:
                should_keep = True
            
            # 4.3 有子组件且面积适中（组合布局）
            # 关键修改：提高面积下限，避免保留太小的容器
            elif child_count > 0 and 50000 < area < 2000000:
                should_keep = True
            
            # 4.4 商品卡片（包含图片和文字的容器）
            elif comp.get('is_product_card', False):
                should_keep = True
            
            # 如果不满足任何条件，不保留
            if not should_keep:
                continue
            
            # 检查是否被其他组件完全包含
            is_contained = False
            for other in filtered:
                ox1, oy1, ox2, oy2 = other['bounds']
                
                # 跳过bounds完全相同的情况
                if other['bounds'] == comp['bounds']:
                    # 如果bounds相同但类型不同，检查是否已有更具体的类型
                    if other['type'] in specific_types or other['clickable']:
                        is_contained = True
                        break
                    continue
                
                # 检查是否被完全包含
                if ox1 <= x1 and oy1 <= y1 and ox2 >= x2 and oy2 >= y2:
                    # 被具体类型或可点击组件包含时，不保留当前容器
                    if other['type'] in specific_types or other['clickable']:
                        is_contained = True
                        break
                    
                    # 被另一个容器包含，且面积差异很大时（>5倍），不保留
                    other_area = other['width'] * other['height']
                    if other['type'] in layout_types and other_area > area * 5:
                        is_contained = True
                        break
            
            if not is_contained:
                filtered.append(comp)
            continue
        
        # === 规则5: 其他未知类型 ===
        # 检查是否被包含
        is_contained = False
        for other in filtered:
            ox1, oy1, ox2, oy2 = other['bounds']
            if ox1 <= x1 and oy1 <= y1 and ox2 >= x2 and oy2 >= y2:
                if other['type'] in specific_types or other['clickable']:
                    is_contained = True
                    break
        
        if not is_contained:
            filtered.append(comp)
    
    return filtered


def convert_to_yolo_format(bounds: Tuple[int, int, int, int], 
                          img_width: int, 
                          img_height: int) -> Tuple[float, float, float, float]:
    """
    将绝对坐标转换为YOLO格式（归一化的中心点坐标和宽高）
    
    Args:
        bounds: (x1, y1, x2, y2)
        img_width: 图像宽度
        img_height: 图像高度
        
    Returns:
        Tuple[float, float, float, float]: (x_center, y_center, width, height) 归一化
    """
    x1, y1, x2, y2 = bounds
    
    # 计算中心点和宽高
    center_x = (x1 + x2) / 2.0
    center_y = (y1 + y2) / 2.0
    width = x2 - x1
    height = y2 - y1
    
    # 归一化
    x_center_norm = center_x / img_width
    y_center_norm = center_y / img_height
    width_norm = width / img_width
    height_norm = height / img_height
    
    return x_center_norm, y_center_norm, width_norm, height_norm


def assign_class_id(component: Dict, scheme: str = 'two_class'):
    """
    根据标注方案分配类别ID
    
    设计目标：
    - two_class: 只区分文字(0) / 图片(1)
    - three_class: 在 two_class 的基础上，**额外**增加一层「可点击(2)」信息，
      不改变原始 0 / 1 的数量（即一个可点击的 TextView 会生成两条标注：0 和 2）
    - fine_grained: 按组件类型细分
    
    Args:
        component: 组件信息字典
        scheme: 标注方案
        
    Returns:
        int 或 List[int]:
            - two_class / fine_grained: 返回单个 int
            - three_class: 返回 List[int]，可能包含 [0]、[1] 或 [0, 2] / [1, 2]
    """
    comp_type = component['type']
    clickable = component['clickable']
    has_text_content = component['has_text']
    
    # 基础二分类：文字(0) vs 图片(1)
    def base_two_class_id() -> int:
        if comp_type == 'ImageView' or (comp_type == 'View' and not has_text_content):
            return 1  # 图片
        else:
            return 0  # 文字（包括TextView、Button等）
    
    if scheme == 'two_class':
        # 完全等价于原先的 two_class 行为
        return base_two_class_id()
    
    elif scheme == 'three_class':
        # 在 two_class 的基础上，增加一层「可点击」信息
        ids = [base_two_class_id()]
        if clickable:
            # 额外增加一个类别 2（可点击），即使与 0/1 重叠也没关系
            ids.append(2)
        
        # 同时标注组件类型（从3开始编号）
        # 布局容器类型映射
        layout_type_mapping = {
            'FrameLayout': 3,
            'LinearLayout': 4,
            'RelativeLayout': 5,
            'ConstraintLayout': 6,
            'ViewGroup': 7,
            'RecyclerView': 8,
            'ViewPager': 9,
            'ScrollView': 10,
            'HorizontalScrollView': 11,
            'NestedScrollView': 12,
            'DrawerLayout': 13,
            'CoordinatorLayout': 14,
        }
        
        # 如果组件类型在映射中，也添加对应的类别ID
        if comp_type in layout_type_mapping:
            ids.append(layout_type_mapping[comp_type])
        
        return ids
    
    elif scheme == 'fine_grained':
        # 细粒度标注：按Android组件类型
        type_mapping = {
            'TextView': 0,
            'ImageView': 1,
            'Button': 2,
            'EditText': 3,
            'CheckBox': 4,
            'RadioButton': 5,
            'Switch': 6,
            'ProgressBar': 7,
            'SeekBar': 8,
            'View': 9,  # 通用View
        }
        return type_mapping.get(comp_type, 10)  # 其他类型默认为10
    
    elif scheme == 'by_type' or scheme == 'component_type':
        # 按实际组件类型分配类别ID（用于GAT网络保留组件类型信息）
        # 所有布局容器和组件类型都有独立的类别ID
        type_mapping = {
            # 布局容器
            'FrameLayout': 0,
            'LinearLayout': 1,
            'RelativeLayout': 2,
            'ConstraintLayout': 3,
            'ViewGroup': 4,
            'RecyclerView': 5,
            'ViewPager': 6,
            'ScrollView': 7,
            'HorizontalScrollView': 8,
            'NestedScrollView': 9,
            'DrawerLayout': 10,
            'CoordinatorLayout': 11,
            # 具体组件
            'TextView': 12,
            'ImageView': 13,
            'Button': 14,
            'EditText': 15,
            'CheckBox': 16,
            'RadioButton': 17,
            'Switch': 18,
            'ProgressBar': 19,
            'SeekBar': 20,
            'ToggleButton': 21,
            'ImageButton': 22,
            'View': 23,  # 通用View
        }
        # 如果类型不在映射中，返回24（其他类型）
        return type_mapping.get(comp_type, 24)
    
    else:
        raise ValueError(f"未知的标注方案: {scheme}")


def convert_xml_to_yolo(xml_path: str, 
                        output_path: str,
                        img_width: int = 1080,
                        img_height: int = 2376,
                        scheme: str = 'two_class',
                        min_size: int = 10):
    """
    将XML文件转换为YOLO格式标注文件
    
    Args:
        xml_path: XML文件路径
        output_path: 输出YOLO标注文件路径
        img_width: 图像宽度（默认1080，从XML中可获取）
        img_height: 图像高度（默认2376，从XML中可获取）
        scheme: 标注方案
        min_size: 最小组件尺寸
    """
    # 提取组件
    components = extract_components(xml_path, min_size=min_size)
    
    if not components:
        print(f"警告: {xml_path} 中未找到有效组件")
        # 创建空文件
        with open(output_path, 'w') as f:
            pass
        return
    
    # 如果XML中有根节点bounds，使用它来确定图像尺寸
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        root_bounds = root.get('bounds', '')
        if root_bounds:
            _, _, img_width, img_height = parse_bounds(root_bounds)
    except:
        pass
    
    # 转换为YOLO格式
    yolo_lines = []
    for comp in components:
        class_ids = assign_class_id(comp, scheme)
        # 兼容返回单个 int 或多个类别ID 的情况
        if isinstance(class_ids, int):
            class_ids = [class_ids]
        x_center, y_center, width, height = convert_to_yolo_format(
            comp['bounds'], img_width, img_height
        )
        for class_id in class_ids:
            yolo_line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
            yolo_lines.append(yolo_line)
    
    # 写入文件
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(yolo_lines))
    
    print(f"转换完成: {xml_path} -> {output_path} ({len(yolo_lines)} 个组件)")


def batch_convert(xml_dir: str,
                  output_dir: str,
                  img_width: int = 1080,
                  img_height: int = 2376,
                  scheme: str = 'two_class',
                  min_size: int = 10):
    """
    批量转换XML文件到YOLO格式
    
    Args:
        xml_dir: XML文件目录
        output_dir: 输出目录
        img_width: 图像宽度
        img_height: 图像高度
        scheme: 标注方案
        min_size: 最小组件尺寸
    """
    xml_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]
    
    print(f"找到 {len(xml_files)} 个XML文件")
    print(f"标注方案: {scheme}")
    
    for xml_file in xml_files:
        xml_path = os.path.join(xml_dir, xml_file)
        # 输出文件名：将.xml替换为.txt
        output_file = xml_file.replace('.xml', '.txt')
        output_path = os.path.join(output_dir, output_file)
        
        convert_xml_to_yolo(xml_path, output_path, img_width, img_height, scheme, min_size)


def main():
    parser = argparse.ArgumentParser(description='XML到YOLO格式转换器')
    parser.add_argument('--xml_dir', type=str, required=True,
                       help='XML文件目录')
    parser.add_argument('--output_dir', type=str, required=True,
                       help='输出YOLO标注文件目录')
    parser.add_argument('--scheme', type=str, default='two_class',
                       choices=['two_class', 'three_class', 'fine_grained'],
                       help='标注方案: two_class(两类), three_class(三类), fine_grained(细粒度)')
    parser.add_argument('--img_width', type=int, default=1080,
                       help='图像宽度（默认1080）')
    parser.add_argument('--img_height', type=int, default=2376,
                       help='图像高度（默认2376）')
    parser.add_argument('--min_size', type=int, default=10,
                       help='最小组件尺寸（默认10像素）')
    parser.add_argument('--single_file', type=str, default=None,
                       help='转换单个XML文件（测试用）')
    
    args = parser.parse_args()
    
    if args.single_file:
        # 单文件转换
        output_file = os.path.basename(args.single_file).replace('.xml', '.txt')
        output_path = os.path.join(args.output_dir, output_file)
        convert_xml_to_yolo(args.single_file, output_path, 
                           args.img_width, args.img_height, 
                           args.scheme, args.min_size)
    else:
        # 批量转换
        batch_convert(args.xml_dir, args.output_dir,
                     args.img_width, args.img_height,
                     args.scheme, args.min_size)


if __name__ == '__main__':
    main()

