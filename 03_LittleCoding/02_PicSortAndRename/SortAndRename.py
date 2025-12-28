#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图像数据集整理脚本
根据文件命名规则将图像和标注文件分类、移动并重命名

文件命名规则：
- 原始PNG: tag_time-tag_train/val_class_duplicate.png
- 对应TXT: tag_time-tag.txt
- 目标PNG: tag_class_duplicate.png
- 目标TXT: tag_class_duplicate.txt
"""

import os
import re
import shutil
from pathlib import Path
from typing import Tuple, Optional, Dict


class DatasetProcessor:
    def __init__(self, root_path: str):
        """
        初始化数据集处理器
        
        Args:
            root_path: 数据集根目录路径
        """
        self.root_path = Path(root_path)
        self.pic_path = self.root_path / "pic"
        self.txt_path = self.root_path / "txt"
        
        # 创建输出目录
        self.train_path = self.root_path / "train"
        self.val_path = self.root_path / "val"
        self.error_pic_path = self.root_path / "error" / "pic"
        self.error_txt_path = self.root_path / "error" / "txt"
        
        # 统计计数器
        self.stats = {
            'train_success': 0,
            'val_success': 0,
            'pic_error': 0,
            'txt_error': 0,
            'total_processed': 0
        }
    
    def create_directories(self):
        """创建必要的目录结构"""
        directories = [
            self.train_path,
            self.val_path,
            self.error_pic_path,
            self.error_txt_path
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        print(f"✓ 已创建目录结构")
    
    def parse_filename(self, filename: str) -> Optional[Dict[str, str]]:
        """
        解析文件名，提取各个组件
        
        Args:
            filename: 文件名 (不包含扩展名)
            
        Returns:
            包含解析结果的字典，如果解析失败返回None
        """
        # 匹配模式: tag_time-tag_train/val_class_duplicate
        pattern = r'^(.+?)_(.+?)-(.+?)_(train|val)_(\d+)_(\d+)$'
        match = re.match(pattern, filename)
        
        if match:
            tag_prefix, time_part, tag_suffix, dataset_type, class_id, duplicate_id = match.groups()
            tag = f"{tag_prefix}_{time_part}-{tag_suffix}"
            
            return {
                'tag': tag,
                'tag_prefix': tag_prefix,
                'time_tag': f"{time_part}-{tag_suffix}",
                'dataset_type': dataset_type,
                'class_id': class_id,
                'duplicate_id': duplicate_id,
                'new_name': f"{tag_prefix}_{class_id}_{duplicate_id}"
            }
        
        return None
    
    def find_corresponding_txt(self, png_info: Dict[str, str]) -> Optional[Path]:
        """
        根据PNG文件信息查找对应的TXT文件
        
        Args:
            png_info: PNG文件解析信息
            
        Returns:
            对应的TXT文件路径，如果找不到返回None
        """
        # TXT文件名格式: tag_time-tag.txt
        txt_filename = f"{png_info['tag']}.txt"
        txt_file_path = self.txt_path / txt_filename
        
        if txt_file_path.exists():
            return txt_file_path
        
        return None
    
    def process_file_pair(self, png_file: Path, png_info: Dict[str, str]) -> bool:
        """
        处理PNG和对应的TXT文件对
        
        Args:
            png_file: PNG文件路径
            png_info: PNG文件解析信息
            
        Returns:
            处理是否成功
        """
        try:
            # 确定目标目录
            if png_info['dataset_type'] == 'train':
                target_dir = self.train_path
            else:  # val
                target_dir = self.val_path
            
            # 新的文件名
            new_png_name = f"{png_info['new_name']}.png"
            new_txt_name = f"{png_info['new_name']}.txt"
            
            # 目标路径
            target_png_path = target_dir / new_png_name
            target_txt_path = target_dir / new_txt_name
            
            # 查找对应的TXT文件
            txt_file = self.find_corresponding_txt(png_info)
            
            if txt_file is None:
                print(f"⚠️  警告: 找不到对应的TXT文件: {png_info['tag']}.txt")
                # 移动PNG到错误目录
                error_png_path = self.error_pic_path / png_file.name
                shutil.move(str(png_file), str(error_png_path))
                self.stats['pic_error'] += 1
                return False
            
            # 移动并重命名PNG文件
            shutil.move(str(png_file), str(target_png_path))
            
            # 移动并重命名TXT文件
            shutil.move(str(txt_file), str(target_txt_path))
            
            # 更新统计
            if png_info['dataset_type'] == 'train':
                self.stats['train_success'] += 1
            else:
                self.stats['val_success'] += 1
            
            print(f"✓ 处理成功: {png_file.name} -> {new_png_name}")
            return True
            
        except Exception as e:
            print(f"❌ 处理失败: {png_file.name}, 错误: {str(e)}")
            
            # 移动到错误目录
            try:
                error_png_path = self.error_pic_path / png_file.name
                if png_file.exists():
                    shutil.move(str(png_file), str(error_png_path))
                
                txt_file = self.find_corresponding_txt(png_info)
                if txt_file and txt_file.exists():
                    error_txt_path = self.error_txt_path / txt_file.name
                    shutil.move(str(txt_file), str(error_txt_path))
                    
            except Exception as move_error:
                print(f"❌ 移动到错误目录失败: {str(move_error)}")
            
            self.stats['pic_error'] += 1
            return False
    
    def process_orphaned_txt_files(self):
        """处理没有对应PNG文件的孤立TXT文件"""
        if not self.txt_path.exists():
            return
        
        txt_files = list(self.txt_path.glob("*.txt"))
        orphaned_count = 0
        
        for txt_file in txt_files:
            try:
                error_txt_path = self.error_txt_path / txt_file.name
                shutil.move(str(txt_file), str(error_txt_path))
                orphaned_count += 1
            except Exception as e:
                print(f"❌ 移动孤立TXT文件失败: {txt_file.name}, 错误: {str(e)}")
        
        if orphaned_count > 0:
            print(f"⚠️  移动了 {orphaned_count} 个孤立的TXT文件到错误目录")
            self.stats['txt_error'] += orphaned_count
    
    def process_dataset(self):
        """处理整个数据集"""
        print("🚀 开始处理数据集...")
        
        # 检查输入目录
        if not self.pic_path.exists():
            print(f"❌ 错误: pic目录不存在: {self.pic_path}")
            return
        
        if not self.txt_path.exists():
            print(f"❌ 错误: txt目录不存在: {self.txt_path}")
            return
        
        # 创建输出目录
        self.create_directories()
        
        # 获取所有PNG文件
        png_files = list(self.pic_path.glob("*.png"))
        
        if not png_files:
            print("❌ 错误: pic目录中没有找到PNG文件")
            return
        
        print(f"📊 找到 {len(png_files)} 个PNG文件")
        
        # 处理每个PNG文件
        processed_count = 0
        for png_file in png_files:
            self.stats['total_processed'] += 1
            
            # 解析文件名
            filename_without_ext = png_file.stem
            png_info = self.parse_filename(filename_without_ext)
            
            if png_info is None:
                print(f"⚠️  文件名格式不正确: {png_file.name}")
                # 移动到错误目录
                try:
                    error_png_path = self.error_pic_path / png_file.name
                    shutil.move(str(png_file), str(error_png_path))
                    self.stats['pic_error'] += 1
                except Exception as e:
                    print(f"❌ 移动错误文件失败: {str(e)}")
                continue
            
            # 处理文件对
            if self.process_file_pair(png_file, png_info):
                processed_count += 1
        
        # 处理孤立的TXT文件
        self.process_orphaned_txt_files()
        
        # 输出统计结果
        self.print_statistics()
    
    def print_statistics(self):
        """打印处理统计结果"""
        print("\n" + "="*50)
        print("📈 处理统计结果")
        print("="*50)
        print(f"总处理文件数:     {self.stats['total_processed']}")
        print(f"训练集成功:       {self.stats['train_success']}")
        print(f"验证集成功:       {self.stats['val_success']}")
        print(f"成功总数:         {self.stats['train_success'] + self.stats['val_success']}")
        print(f"PNG错误文件:      {self.stats['pic_error']}")
        print(f"TXT错误文件:      {self.stats['txt_error']}")
        print(f"错误总数:         {self.stats['pic_error'] + self.stats['txt_error']}")
        print("="*50)
        
        success_rate = (self.stats['train_success'] + self.stats['val_success']) / max(self.stats['total_processed'], 1) * 100
        print(f"成功率:           {success_rate:.1f}%")


def main():
    """主函数"""
    print("🖼️  图像数据集整理工具")
    print("="*50)
    
    # 获取用户输入的路径
    while True:
        root_path = input("请输入数据集根目录路径: ").strip()
        
        if not root_path:
            print("❌ 路径不能为空，请重新输入")
            continue
        
        root_path = Path(root_path)
        
        if not root_path.exists():
            print(f"❌ 路径不存在: {root_path}")
            continue
        
        if not root_path.is_dir():
            print(f"❌ 路径不是目录: {root_path}")
            continue
        
        break
    
    # 确认操作
    print(f"\n将要处理的目录: {root_path}")
    print("预期目录结构:")
    print("  - pic/        (包含PNG图像文件)")
    print("  - txt/        (包含对应的TXT标注文件)")
    print("\n处理后将创建:")
    print("  - train/      (训练集文件)")
    print("  - val/        (验证集文件)")
    print("  - error/      (异常文件)")
    
    confirm = input("\n确认继续处理? (y/N): ").strip().lower()
    
    if confirm not in ['y', 'yes']:
        print("❌ 操作已取消")
        return
    
    # 开始处理
    processor = DatasetProcessor(str(root_path))
    processor.process_dataset()
    
    print("\n✅ 数据集处理完成!")


if __name__ == "__main__":
    main()
