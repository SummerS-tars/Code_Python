#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片与参数文件匹配处理脚本

这个脚本用于处理项目中图片(.png)与对应参数文件(.txt)的匹配
根据图片文件命名中的部分与参数文件命名中的部分进行匹配
并重新组织文件结构

Author: GitHub Copilot
Date: 2025-10-07
"""

import os
import shutil
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime


class PicTxtPatcher:
    """图片与参数文件匹配处理器"""
    
    def __init__(self, base_path: str, enable_logging: bool = True):
        """
        初始化处理器
        
        Args:
            base_path: 基础路径，指向class_all目录
            enable_logging: 是否启用日志功能
        """
        self.base_path = Path(base_path)
        self.class_path = self.base_path / "class"
        self.class_unknown_path = self.base_path / "class_unknown"
        self.labels_path = self.base_path / "labels"
        self.train_path = self.labels_path / "train"
        self.val_path = self.labels_path / "val"
        
        # 统计信息
        self.stats = {
            'total_images': 0,
            'matched_images': 0,
            'unmatched_images': 0,
            'processed_classes': 0,
            'orphaned_txt_files': 0
        }
        
        # 设置日志
        self.enable_logging = enable_logging
        if enable_logging:
            self._setup_logging()
        else:
            self._setup_simple_logging()
    
    def _setup_logging(self):
        """设置日志配置"""
        log_filename = f"pic_txt_patcher_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_path = self.base_path / log_filename
        
        # 确保日志目录存在
        if not self.base_path.exists():
            # 如果基础路径不存在，使用当前目录
            log_path = Path.cwd() / log_filename
        
        # 创建文件处理器
        file_handler = logging.FileHandler(str(log_path), encoding='utf-8')
        console_handler = logging.StreamHandler()
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[file_handler, console_handler]
        )
        self.logger = logging.getLogger(__name__)
        
        # 保存处理器引用以便后续关闭
        self._file_handler = file_handler
        self._console_handler = console_handler
    
    def _setup_simple_logging(self):
        """设置简单的内存日志（用于测试）"""
        import io
        
        # 创建内存流作为日志输出
        self._log_stream = io.StringIO()
        
        # 创建处理器
        stream_handler = logging.StreamHandler(self._log_stream)
        console_handler = logging.StreamHandler()
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[stream_handler, console_handler]
        )
        self.logger = logging.getLogger(__name__)
        
        # 保存处理器引用
        self._file_handler = stream_handler
        self._console_handler = console_handler
    
    def extract_txt_filename_from_image(self, image_filename: str) -> Optional[str]:
        """
        从图片文件名提取对应的参数文件名
        
        Args:
            image_filename: 图片文件名 (如 Ada_2024_3_8_20_45-30_train.png)
        
        Returns:
            对应的参数文件名 (如 Ada_2024_3_8_20_45-30.txt) 或 None
        """
        # 移除扩展名
        name_without_ext = image_filename.rsplit('.', 1)[0]
        
        # 处理两种命名格式
        # 格式1: tag_time-tag_train/val
        # 格式2: time_hash-tag_train/val
        
        if name_without_ext.endswith('_train') or name_without_ext.endswith('_val'):
            # 移除 _train 或 _val 后缀
            txt_name = name_without_ext.rsplit('_', 1)[0] + '.txt'
            return txt_name
        
        return None
    
    def find_txt_file(self, txt_filename: str) -> Optional[Path]:
        """
        在labels目录下查找对应的txt文件
        
        Args:
            txt_filename: txt文件名
        
        Returns:
            找到的txt文件路径或None
        """
        # 在train目录中查找
        train_file = self.train_path / txt_filename
        if train_file.exists():
            return train_file
        
        # 在val目录中查找
        val_file = self.val_path / txt_filename
        if val_file.exists():
            return val_file
        
        return None
    
    def create_class_structure(self, class_dir: Path):
        """
        为类别目录创建新的结构 (pic, txt, unmatched)
        
        Args:
            class_dir: 类别目录路径
        """
        subdirs = ['pic', 'txt', 'unmatched']
        for subdir in subdirs:
            subdir_path = class_dir / subdir
            subdir_path.mkdir(exist_ok=True)
    
    def process_class_directory(self, class_dir: Path) -> Dict[str, int]:
        """
        处理单个类别目录
        
        Args:
            class_dir: 类别目录路径
        
        Returns:
            该类别的处理统计信息
        """
        class_stats = {
            'total_images': 0,
            'matched_images': 0,
            'unmatched_images': 0
        }
        
        self.logger.info(f"正在处理类别目录: {class_dir.name}")
        
        # 创建新的目录结构
        self.create_class_structure(class_dir)
        
        # 获取所有png文件
        png_files = list(class_dir.glob("*.png"))
        class_stats['total_images'] = len(png_files)
        
        for png_file in png_files:
            # 提取对应的txt文件名
            txt_filename = self.extract_txt_filename_from_image(png_file.name)
            
            if txt_filename is None:
                self.logger.warning(f"无法解析图片文件名: {png_file.name}")
                # 移动到unmatched目录
                dest_path = class_dir / 'unmatched' / png_file.name
                shutil.move(str(png_file), str(dest_path))
                class_stats['unmatched_images'] += 1
                continue
            
            # 查找对应的txt文件
            txt_file_path = self.find_txt_file(txt_filename)
            
            if txt_file_path:
                # 找到匹配的txt文件
                # 移动图片到pic目录
                pic_dest = class_dir / 'pic' / png_file.name
                shutil.move(str(png_file), str(pic_dest))
                
                # 复制txt文件到txt目录
                txt_dest = class_dir / 'txt' / txt_filename
                shutil.copy2(str(txt_file_path), str(txt_dest))
                
                class_stats['matched_images'] += 1
                self.logger.debug(f"匹配成功: {png_file.name} -> {txt_filename}")
            else:
                # 没有找到匹配的txt文件
                unmatched_dest = class_dir / 'unmatched' / png_file.name
                shutil.move(str(png_file), str(unmatched_dest))
                class_stats['unmatched_images'] += 1
                self.logger.warning(f"未找到匹配的txt文件: {png_file.name} -> {txt_filename}")
        
        return class_stats
    
    def find_orphaned_txt_files(self) -> List[Path]:
        """
        查找没有对应图片文件的txt文件（孤儿文件）
        
        Returns:
            孤儿txt文件列表
        """
        orphaned_files = []
        
        # 收集所有已处理的图片对应的txt文件名
        processed_txt_files = set()
        
        # 遍历所有类别目录收集已处理的txt文件
        for class_dir in self.class_path.iterdir():
            if class_dir.is_dir():
                txt_dir = class_dir / 'txt'
                if txt_dir.exists():
                    for txt_file in txt_dir.glob("*.txt"):
                        processed_txt_files.add(txt_file.name)
        
        for class_dir in self.class_unknown_path.iterdir():
            if class_dir.is_dir():
                txt_dir = class_dir / 'txt'
                if txt_dir.exists():
                    for txt_file in txt_dir.glob("*.txt"):
                        processed_txt_files.add(txt_file.name)
        
        # 检查labels目录下的txt文件
        for labels_subdir in [self.train_path, self.val_path]:
            if labels_subdir.exists():
                for txt_file in labels_subdir.glob("*.txt"):
                    if txt_file.name not in processed_txt_files:
                        orphaned_files.append(txt_file)
        
        return orphaned_files
    
    def process_all(self):
        """
        处理所有目录和文件
        """
        self.logger.info("开始处理图片与参数文件匹配...")
        
        # 检查基础路径是否存在
        if not self.base_path.exists():
            raise FileNotFoundError(f"基础路径不存在: {self.base_path}")
        
        # 处理class目录
        if self.class_path.exists():
            self.logger.info("处理class目录...")
            for class_dir in self.class_path.iterdir():
                if class_dir.is_dir():
                    stats = self.process_class_directory(class_dir)
                    self.stats['total_images'] += stats['total_images']
                    self.stats['matched_images'] += stats['matched_images']
                    self.stats['unmatched_images'] += stats['unmatched_images']
                    self.stats['processed_classes'] += 1
        
        # 处理class_unknown目录
        if self.class_unknown_path.exists():
            self.logger.info("处理class_unknown目录...")
            for class_dir in self.class_unknown_path.iterdir():
                if class_dir.is_dir():
                    stats = self.process_class_directory(class_dir)
                    self.stats['total_images'] += stats['total_images']
                    self.stats['matched_images'] += stats['matched_images']
                    self.stats['unmatched_images'] += stats['unmatched_images']
                    self.stats['processed_classes'] += 1
        
        # 查找孤儿txt文件
        orphaned_files = self.find_orphaned_txt_files()
        self.stats['orphaned_txt_files'] = len(orphaned_files)
        
        if orphaned_files:
            self.logger.warning(f"发现 {len(orphaned_files)} 个没有对应图片的txt文件:")
            for orphan in orphaned_files:
                self.logger.warning(f"  - {orphan}")
        
        self._print_summary()
    
    def _print_summary(self):
        """打印处理摘要"""
        self.logger.info("=" * 60)
        self.logger.info("处理完成! 统计摘要:")
        self.logger.info(f"处理的类别数量: {self.stats['processed_classes']}")
        self.logger.info(f"总图片数量: {self.stats['total_images']}")
        self.logger.info(f"成功匹配的图片: {self.stats['matched_images']}")
        self.logger.info(f"无法匹配的图片: {self.stats['unmatched_images']}")
        self.logger.info(f"孤儿txt文件: {self.stats['orphaned_txt_files']}")
        
        if self.stats['total_images'] > 0:
            match_rate = self.stats['matched_images'] / self.stats['total_images'] * 100
            self.logger.info(f"匹配成功率: {match_rate:.2f}%")
        
        self.logger.info("=" * 60)
    
    def cleanup_logging(self):
        """清理日志资源"""
        try:
            if hasattr(self, '_file_handler'):
                self._file_handler.close()
            if hasattr(self, '_console_handler'):
                self._console_handler.close()
            # 清理所有处理器
            for handler in self.logger.handlers[:]:
                handler.close()
                self.logger.removeHandler(handler)
        except Exception:
            pass  # 忽略清理时的错误


def main():
    """主函数"""
    # 设置基础路径 - 用户需要根据实际情况修改这个路径
    base_path = r"E:\_WorkingTemp\XiYuanTotalProcess\class_all"
    
    # 提示用户确认路径
    print(f"当前设置的基础路径: {base_path}")
    print("请确认这是正确的class_all目录路径")
    confirm = input("继续处理? (y/n): ").strip().lower()
    
    if confirm not in ['y', 'yes']:
        print("处理已取消")
        return
    
    try:
        # 创建处理器并开始处理
        patcher = PicTxtPatcher(base_path)
        patcher.process_all()
        
    except Exception as e:
        print(f"处理过程中发生错误: {e}")
        logging.error(f"处理过程中发生错误: {e}", exc_info=True)


if __name__ == "__main__":
    main()