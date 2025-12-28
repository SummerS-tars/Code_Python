#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片与参数文件匹配处理脚本 - 增强版本
支持配置文件、更好的错误处理和用户交互

Author: GitHub Copilot
Date: 2025-10-07
"""

import configparser
from pic_txt_patcher import PicTxtPatcher
from pathlib import Path
import sys


class ConfigurablePicTxtPatcher(PicTxtPatcher):
    """支持配置文件的图片与参数文件匹配处理器"""
    
    def __init__(self, config_file="config.ini"):
        """
        初始化处理器，从配置文件读取设置
        
        Args:
            config_file: 配置文件路径
        """
        self.config = configparser.ConfigParser()
        self.config_file = Path(config_file)
        
        # 加载配置
        self._load_config()
        
        # 获取基础路径
        base_path = self.config.get('Paths', 'base_path', fallback='')
        if not base_path:
            base_path = self._prompt_for_base_path()
        
        # 初始化父类
        super().__init__(base_path)
        
        # 应用配置设置
        self._apply_config()
    
    def _load_config(self):
        """加载配置文件"""
        if self.config_file.exists():
            self.config.read(self.config_file, encoding='utf-8')
            print(f"已加载配置文件: {self.config_file}")
        else:
            print(f"配置文件不存在: {self.config_file}")
            print("将使用默认设置，或者手动输入配置")
            self._create_default_config()
    
    def _create_default_config(self):
        """创建默认配置"""
        self.config['Paths'] = {
            'base_path': '',
        }
        self.config['Logging'] = {
            'log_level': 'INFO',
            'console_verbose': 'true'
        }
        self.config['Processing'] = {
            'create_backup': 'false',
            'show_progress': 'true'
        }
    
    def _apply_config(self):
        """应用配置设置"""
        # 设置日志级别
        log_level = self.config.get('Logging', 'log_level', fallback='INFO')
        import logging
        self.logger.setLevel(getattr(logging, log_level.upper()))
    
    def _prompt_for_base_path(self):
        """提示用户输入基础路径"""
        print("\n" + "="*60)
        print("配置基础路径")
        print("="*60)
        print("请输入包含以下目录的父目录路径:")
        print("- class/")
        print("- class_unknown/")  
        print("- labels/")
        print("")
        print("示例: E:\\_WorkingTemp\\XiYuanTotalProcess\\class_all")
        print("")
        
        while True:
            base_path = input("请输入基础路径: ").strip()
            if not base_path:
                print("路径不能为空，请重新输入")
                continue
            
            path_obj = Path(base_path)
            if not path_obj.exists():
                print(f"路径不存在: {base_path}")
                create = input("是否创建该路径? (y/n): ").strip().lower()
                if create in ['y', 'yes']:
                    try:
                        path_obj.mkdir(parents=True, exist_ok=True)
                        print(f"已创建路径: {base_path}")
                        break
                    except Exception as e:
                        print(f"创建路径失败: {e}")
                        continue
                else:
                    continue
            else:
                break
        
        # 保存到配置文件
        self.config.set('Paths', 'base_path', base_path)
        self._save_config()
        
        return base_path
    
    def _save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
            print(f"配置已保存到: {self.config_file}")
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def validate_structure(self):
        """验证目录结构"""
        print("\n验证目录结构...")
        
        required_dirs = [
            self.class_path,
            self.class_unknown_path,
            self.labels_path,
            self.train_path,
            self.val_path
        ]
        
        missing_dirs = []
        for dir_path in required_dirs:
            if not dir_path.exists():
                missing_dirs.append(str(dir_path))
        
        if missing_dirs:
            print("以下必需的目录不存在:")
            for missing in missing_dirs:
                print(f"  - {missing}")
            
            create_missing = input("\n是否创建缺失的目录? (y/n): ").strip().lower()
            if create_missing in ['y', 'yes']:
                for missing_dir in missing_dirs:
                    try:
                        Path(missing_dir).mkdir(parents=True, exist_ok=True)
                        print(f"已创建: {missing_dir}")
                    except Exception as e:
                        print(f"创建失败 {missing_dir}: {e}")
                        return False
            else:
                print("无法继续处理，请手动创建必需的目录")
                return False
        
        print("目录结构验证完成")
        return True
    
    def interactive_process(self):
        """交互式处理流程"""
        print("\n" + "="*60)
        print("图片与参数文件匹配处理")
        print("="*60)
        
        # 显示当前设置
        print(f"基础路径: {self.base_path}")
        print(f"class目录: {self.class_path}")
        print(f"class_unknown目录: {self.class_unknown_path}")
        print(f"labels目录: {self.labels_path}")
        print("")
        
        # 验证目录结构
        if not self.validate_structure():
            return False
        
        # 预览将要处理的文件
        self._preview_files()
        
        # 确认处理
        print("\n" + "="*60)
        confirm = input("确认开始处理? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("处理已取消")
            return False
        
        # 开始处理
        try:
            self.process_all()
            print("\n处理完成！")
            return True
        except Exception as e:
            print(f"处理过程中发生错误: {e}")
            return False
    
    def _preview_files(self):
        """预览将要处理的文件"""
        print("\n预览将要处理的文件:")
        
        total_images = 0
        
        # 统计class目录下的图片
        if self.class_path.exists():
            for class_dir in self.class_path.iterdir():
                if class_dir.is_dir():
                    png_files = list(class_dir.glob("*.png"))
                    total_images += len(png_files)
                    print(f"  class/{class_dir.name}: {len(png_files)} 张图片")
        
        # 统计class_unknown目录下的图片  
        if self.class_unknown_path.exists():
            for class_dir in self.class_unknown_path.iterdir():
                if class_dir.is_dir():
                    png_files = list(class_dir.glob("*.png"))
                    total_images += len(png_files)
                    print(f"  class_unknown/{class_dir.name}: {len(png_files)} 张图片")
        
        # 统计txt文件
        train_txt = len(list(self.train_path.glob("*.txt"))) if self.train_path.exists() else 0
        val_txt = len(list(self.val_path.glob("*.txt"))) if self.val_path.exists() else 0
        
        print(f"\n总计:")
        print(f"  图片文件: {total_images} 张")
        print(f"  训练参数文件: {train_txt} 个")
        print(f"  验证参数文件: {val_txt} 个")


def main():
    """主函数"""
    print("图片与参数文件匹配处理脚本 - 增强版")
    print("版本: 1.0")
    print("")
    
    try:
        # 创建配置化处理器
        patcher = ConfigurablePicTxtPatcher()
        
        # 交互式处理
        success = patcher.interactive_process()
        
        if success:
            print("\n所有操作已完成！")
        else:
            print("\n操作未完成或被取消")
            
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
    except Exception as e:
        print(f"\n发生意外错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()