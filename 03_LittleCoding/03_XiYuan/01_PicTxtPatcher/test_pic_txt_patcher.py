#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片与参数文件匹配处理脚本测试文件

这个脚本用于测试pic_txt_patcher.py的功能
包括创建测试数据和验证处理结果

Author: GitHub Copilot
Date: 2025-10-07
"""

import os
import tempfile
import shutil
from pathlib import Path
import unittest
from pic_txt_patcher import PicTxtPatcher


class TestPicTxtPatcher(unittest.TestCase):
    """测试PicTxtPatcher类"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建临时目录
        self.test_dir = Path(tempfile.mkdtemp())
        # 禁用文件日志以避免权限问题
        self.patcher = PicTxtPatcher(str(self.test_dir), enable_logging=False)
        
        # 创建测试目录结构
        self._create_test_structure()
    
    def tearDown(self):
        """清理测试环境"""
        # 清理日志资源
        if hasattr(self.patcher, 'cleanup_logging'):
            self.patcher.cleanup_logging()
        
        # 等待一小段时间确保文件句柄完全释放
        import time
        time.sleep(0.1)
        
        # 尝试删除临时目录
        try:
            shutil.rmtree(self.test_dir)
        except PermissionError:
            # 如果还是有权限问题，等待更长时间再试
            time.sleep(0.5)
            try:
                shutil.rmtree(self.test_dir)
            except PermissionError:
                # 如果仍然失败，记录警告但不抛出异常
                print(f"Warning: Could not remove temporary directory {self.test_dir}")
    
    def _create_test_structure(self):
        """创建测试用的目录结构和文件"""
        # 创建基础目录结构
        (self.test_dir / "class" / "Ada").mkdir(parents=True)
        (self.test_dir / "class" / "Bob").mkdir(parents=True)
        (self.test_dir / "class_unknown" / "class1_ikea").mkdir(parents=True)
        (self.test_dir / "labels" / "train").mkdir(parents=True)
        (self.test_dir / "labels" / "val").mkdir(parents=True)
        
        # 创建测试图片文件（空文件即可）
        test_images = [
            "class/Ada/Ada_2024_3_8_20_45-30_train.png",
            "class/Ada/Ada_2024_3_8_20_45-31_val.png",
            "class/Bob/Bob_2024_3_9_10_30-40_train.png",
            "class_unknown/class1_ikea/2024_3_18_17_19_e8ba0101cbc74242b48af70a57dafdf5-5_train.png",
            "class_unknown/class1_ikea/2024_3_18_17_20_f9cb0202dbc74242b48af70a57dafdf6-6_val.png"
        ]
        
        for img_path in test_images:
            full_path = self.test_dir / img_path
            full_path.touch()
        
        # 创建对应的txt文件
        test_txt_files = [
            "labels/train/Ada_2024_3_8_20_45-30.txt",
            "labels/val/Ada_2024_3_8_20_45-31.txt",
            "labels/train/Bob_2024_3_9_10_30-40.txt",
            "labels/train/2024_3_18_17_19_e8ba0101cbc74242b48af70a57dafdf5-5.txt",
            "labels/val/2024_3_18_17_20_f9cb0202dbc74242b48af70a57dafdf6-6.txt",
            "labels/train/orphan_file.txt"  # 孤儿文件
        ]
        
        for txt_path in test_txt_files:
            full_path = self.test_dir / txt_path
            full_path.write_text("test content")
    
    def test_extract_txt_filename_from_image(self):
        """测试文件名提取功能"""
        # 测试正常的图片文件名
        result1 = self.patcher.extract_txt_filename_from_image("Ada_2024_3_8_20_45-30_train.png")
        self.assertEqual(result1, "Ada_2024_3_8_20_45-30.txt")
        
        result2 = self.patcher.extract_txt_filename_from_image("2024_3_18_17_19_e8ba0101cbc74242b48af70a57dafdf5-5_val.png")
        self.assertEqual(result2, "2024_3_18_17_19_e8ba0101cbc74242b48af70a57dafdf5-5.txt")
        
        # 测试异常文件名
        result3 = self.patcher.extract_txt_filename_from_image("invalid_name.png")
        self.assertIsNone(result3)
    
    def test_find_txt_file(self):
        """测试txt文件查找功能"""
        # 测试能找到的文件
        result1 = self.patcher.find_txt_file("Ada_2024_3_8_20_45-30.txt")
        self.assertIsNotNone(result1)
        if result1:
            self.assertTrue(result1.exists())
        
        # 测试找不到的文件
        result2 = self.patcher.find_txt_file("nonexistent.txt")
        self.assertIsNone(result2)
    
    def test_process_all(self):
        """测试完整处理流程"""
        # 执行处理
        self.patcher.process_all()
        
        # 验证目录结构是否创建
        self.assertTrue((self.test_dir / "class" / "Ada" / "pic").exists())
        self.assertTrue((self.test_dir / "class" / "Ada" / "txt").exists())
        self.assertTrue((self.test_dir / "class" / "Ada" / "unmatched").exists())
        
        # 验证文件是否正确移动
        self.assertTrue((self.test_dir / "class" / "Ada" / "pic" / "Ada_2024_3_8_20_45-30_train.png").exists())
        self.assertTrue((self.test_dir / "class" / "Ada" / "txt" / "Ada_2024_3_8_20_45-30.txt").exists())
        
        # 验证统计信息
        self.assertGreater(self.patcher.stats['total_images'], 0)
        self.assertGreater(self.patcher.stats['matched_images'], 0)


def create_demo_structure():
    """创建演示用的目录结构和文件"""
    demo_dir = Path("demo_test_data")
    
    if demo_dir.exists():
        print(f"目录 {demo_dir} 已存在，是否删除并重新创建? (y/n): ", end="")
        if input().strip().lower() not in ['y', 'yes']:
            return
        shutil.rmtree(demo_dir)
    
    print(f"创建演示数据结构在: {demo_dir.absolute()}")
    
    # 创建目录结构
    (demo_dir / "class" / "Ada").mkdir(parents=True)
    (demo_dir / "class" / "Bob").mkdir(parents=True)
    (demo_dir / "class_unknown" / "class1_ikea").mkdir(parents=True)
    (demo_dir / "class_unknown" / "class2_unknown").mkdir(parents=True)
    (demo_dir / "labels" / "train").mkdir(parents=True)
    (demo_dir / "labels" / "val").mkdir(parents=True)
    
    # 创建示例图片文件
    demo_images = [
        # class目录下的文件
        "class/Ada/Ada_2024_3_8_20_45-30_train.png",
        "class/Ada/Ada_2024_3_8_20_45-31_val.png",
        "class/Ada/Ada_2024_3_8_20_45-32_train.png",  # 这个没有对应的txt
        "class/Bob/Bob_2024_3_9_10_30-40_train.png",
        "class/Bob/Bob_2024_3_9_10_30-41_val.png",
        
        # class_unknown目录下的文件
        "class_unknown/class1_ikea/2024_3_18_17_19_e8ba0101cbc74242b48af70a57dafdf5-5_train.png",
        "class_unknown/class1_ikea/2024_3_18_17_20_f9cb0202dbc74242b48af70a57dafdf6-6_val.png",
        "class_unknown/class2_unknown/2024_3_19_18_21_a1b2c3d4e5f6-7_train.png",
        "class_unknown/class2_unknown/invalid_filename.png",  # 这个文件名格式不对
    ]
    
    for img_path in demo_images:
        full_path = demo_dir / img_path
        full_path.write_text(f"# 这是图片文件: {img_path}")
        print(f"创建图片文件: {img_path}")
    
    # 创建示例txt文件
    demo_txt_files = [
        # 对应的txt文件
        "labels/train/Ada_2024_3_8_20_45-30.txt",
        "labels/val/Ada_2024_3_8_20_45-31.txt",
        "labels/train/Bob_2024_3_9_10_30-40.txt",
        "labels/val/Bob_2024_3_9_10_30-41.txt",
        "labels/train/2024_3_18_17_19_e8ba0101cbc74242b48af70a57dafdf5-5.txt",
        "labels/val/2024_3_18_17_20_f9cb0202dbc74242b48af70a57dafdf6-6.txt",
        "labels/train/2024_3_19_18_21_a1b2c3d4e5f6-7.txt",
        
        # 孤儿txt文件（没有对应图片）
        "labels/train/orphan_file_1.txt",
        "labels/val/orphan_file_2.txt",
    ]
    
    for txt_path in demo_txt_files:
        full_path = demo_dir / txt_path
        full_path.write_text(f"# 这是参数文件: {txt_path}\nparameter1=value1\nparameter2=value2")
        print(f"创建参数文件: {txt_path}")
    
    print(f"\n演示数据创建完成！")
    print(f"目录结构: {demo_dir.absolute()}")
    print("\n你可以使用以下命令测试脚本:")
    print(f"python pic_txt_patcher.py")
    print("（记得在main函数中修改base_path为demo_test_data的绝对路径）")


def main():
    """主函数"""
    print("PicTxtPatcher 测试和演示工具")
    print("1. 运行单元测试")
    print("2. 创建演示数据")
    print("3. 退出")
    
    choice = input("请选择操作 (1-3): ").strip()
    
    if choice == "1":
        print("运行单元测试...")
        unittest.main(argv=[''], exit=False, verbosity=2)
    elif choice == "2":
        create_demo_structure()
    elif choice == "3":
        print("退出")
    else:
        print("无效选择")


if __name__ == "__main__":
    main()