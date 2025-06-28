#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FRP Controller - 交互式 frpc 管理工具
功能：
1. 启动、停止、重启 frpc 进程
2. 读取和显示配置文件
3. 管理 proxy 配置（增删改查）
4. 提供配置模板
"""

import os
import sys
import json
import subprocess
import platform
from pathlib import Path
from typing import Dict, List, Any, Optional

# Handle PyInstaller executable environment
def get_resource_path():
    """Get the path to resource files (works in both dev and exe environments)"""
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    meipass = getattr(sys, '_MEIPASS', None)
    if meipass:
        # Running as PyInstaller executable
        return Path(meipass)
    else:
        # Running as Python script
        return Path(__file__).parent

# 检查并导入 toml 库
try:
    import tomllib  # Python 3.11+
    def load_toml(file_path):
        with open(file_path, 'rb') as f:
            return tomllib.load(f)
except ImportError:
    try:
        import toml
        def load_toml(file_path):
            return toml.load(file_path)
    except ImportError:
        print("错误: 需要安装 toml 库")
        print("请运行: pip install toml")
        sys.exit(1)

class FRPController:
    def __init__(self):
        self.script_dir = get_resource_path()
        self.config_file = self.script_dir / "frpc.toml"
        # Use English version to avoid encoding issues
        self.ps_script = self.script_dir / "frpcStart_en.ps1"
        self.logs_dir = self.script_dir / "logs"
        self.config_data = {}
        self.load_config()
        
        # 配置模板
        self.proxy_templates = {
            'tcp': {
                'name': '',
                'type': 'tcp',
                'localIP': '127.0.0.1',
                'localPort': 0,
                'remotePort': 0
            },
            'udp': {
                'name': '',
                'type': 'udp',
                'localIP': '127.0.0.1',
                'localPort': 0,
                'remotePort': 0
            },
            'http': {
                'name': '',
                'type': 'http',
                'localIP': '127.0.0.1',
                'localPort': 0,
                'subDomain': ''
            },
            'https': {
                'name': '',
                'type': 'https',
                'localIP': '127.0.0.1',
                'localPort': 0,
                'subDomain': ''
            }
        }

    def load_config(self):
        """加载配置文件"""
        try:
            # Show resource directory for debugging
            if hasattr(sys, '_MEIPASS'):
                print(f"📦 运行环境: 可执行文件 (资源目录: {self.script_dir})")
            else:
                print(f"🐍 运行环境: Python脚本 (脚本目录: {self.script_dir})")
                
            if self.config_file.exists():
                self.config_data = load_toml(self.config_file)
                print(f"✓ 配置文件加载成功: {self.config_file}")
            else:
                print(f"⚠ 配置文件不存在: {self.config_file}")
                self.config_data = {'proxies': []}
        except Exception as e:
            print(f"✗ 加载配置文件失败: {e}")
            self.config_data = {'proxies': []}

    def clean_ansi_codes(self, text: str) -> str:
        """移除ANSI转义序列"""
        import re
        # 移除ANSI转义序列
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
    
    def process_temp_logs(self):
        """处理临时日志文件，清理ANSI代码"""
        try:
            if not self.logs_dir.exists():
                return
                
            # 查找最新的临时日志文件
            temp_files = list(self.logs_dir.glob("*.temp"))
            if not temp_files:
                return
                
            latest_temp = max(temp_files, key=lambda x: x.stat().st_mtime)
            final_log = latest_temp.with_suffix('')  # 移除.temp后缀
            
            # 读取临时文件并清理ANSI代码
            if latest_temp.exists():
                try:
                    with open(latest_temp, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                    
                    if content.strip():
                        cleaned_content = self.clean_ansi_codes(content)
                        
                        # 写入到最终日志文件
                        with open(final_log, 'w', encoding='utf-8') as f:
                            f.write(cleaned_content)
                        
                        print(f"✓ 日志文件已清理并保存到: {final_log.name}")
                        
                        # 可选：删除临时文件
                        # latest_temp.unlink()
                        
                except Exception as e:
                    print(f"⚠ 处理日志文件时出错: {e}")
                    
        except Exception as e:
            print(f"⚠ 日志处理失败: {e}")

    def save_config(self):
        """保存配置文件"""
        try:
            import toml
            with open(self.config_file, 'w', encoding='utf-8') as f:
                toml.dump(self.config_data, f)
            print(f"✓ 配置已保存到: {self.config_file}")
            return True
        except Exception as e:
            print(f"✗ 保存配置失败: {e}")
            return False

    def run_powershell_script(self, action: str) -> bool:
        """运行PowerShell脚本"""
        try:
            if platform.system() != "Windows":
                print("⚠ 此功能仅支持Windows系统")
                return False
                
            cmd = [
                "powershell.exe", 
                "-ExecutionPolicy", "Bypass",
                "-File", str(self.ps_script),
                "-Action", action
            ]
            
            # For 'start' action, use non-blocking approach
            if action.lower() == 'start':
                print("✓ 正在后台启动 frpc...")
                try:
                    # Use Popen for non-blocking execution (UTF-8 for English script)
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        encoding='utf-8',
                        errors='replace'
                    )
                    
                    # Wait longer to allow background job to process initial logs
                    try:
                        stdout, stderr = process.communicate(timeout=10)
                        if stdout:
                            print(stdout)
                        if stderr:
                            print(f"错误: {stderr}")
                        return process.returncode == 0
                    except subprocess.TimeoutExpired:
                        # Process is still running, which is expected for start action
                        print("✓ frpc 启动命令已发送，进程正在后台运行")
                        print("✓ 日志处理任务正在后台运行，请稍后查看日志文件")
                        
                        # 给PowerShell后台任务一些时间处理日志
                        import time
                        time.sleep(3)
                        
                        # 作为备份，用Python处理日志文件
                        print("🔧 正在使用Python备份方案清理日志文件...")
                        self.process_temp_logs()
                        
                        return True
                        
                except Exception as e:
                    print(f"✗ 启动失败: {e}")
                    return False
            
            # For other actions (stop, status, etc.), use blocking approach with timeout
            else:
                # Try multiple encoding strategies (UTF-8 first for English script)
                encodings_to_try = ['utf-8', 'gbk', 'cp936', 'utf-16', 'latin1']
                result = None
                
                for encoding in encodings_to_try:
                    try:
                        result = subprocess.run(
                            cmd, 
                            capture_output=True, 
                            text=True, 
                            encoding=encoding,
                            errors='replace',
                            timeout=15  # Shorter timeout for non-start actions
                        )
                        break
                    except (UnicodeDecodeError, subprocess.TimeoutExpired):
                        continue
                
                # If all encodings failed, try with bytes
                if result is None:
                    try:
                        result = subprocess.run(cmd, capture_output=True, text=False, timeout=15)
                        stdout = result.stdout.decode('utf-8', errors='replace') if result.stdout else ""
                        stderr = result.stderr.decode('utf-8', errors='replace') if result.stderr else ""
                        
                        if stdout:
                            print(stdout)
                        if stderr:
                            print(f"错误: {stderr}")
                            
                        return result.returncode == 0
                    except subprocess.TimeoutExpired:
                        print("⚠ PowerShell脚本执行超时")
                        return False
                    except Exception as e:
                        print(f"✗ 解码输出失败: {e}")
                        return False
                
                if result and result.stdout:
                    print(result.stdout)
                if result and result.stderr:
                    print(f"错误: {result.stderr}")
                    
                return result.returncode == 0 if result else False
            
        except Exception as e:
            print(f"✗ 执行脚本失败: {e}")
            return False

    def show_server_config(self):
        """显示服务器配置"""
        print("\n" + "="*50)
        print("FRP 服务器配置")
        print("="*50)
        
        if 'serverAddr' in self.config_data:
            print(f"服务器地址: {self.config_data['serverAddr']}")
        if 'serverPort' in self.config_data:
            print(f"服务器端口: {self.config_data['serverPort']}")
        if 'auth' in self.config_data:
            auth = self.config_data['auth']
            if isinstance(auth, dict):
                print(f"认证方式: {auth.get('method', 'N/A')}")
                print(f"Token: {auth.get('token', 'N/A')[:10]}...")

    def show_proxies(self):
        """显示所有代理配置"""
        print("\n" + "="*50)
        print("代理配置列表")
        print("="*50)
        
        if 'proxies' not in self.config_data or not self.config_data['proxies']:
            print("暂无代理配置")
            return
        
        for i, proxy in enumerate(self.config_data['proxies'], 1):
            print(f"\n[{i}] {proxy.get('name', 'Unnamed')}")
            print(f"    类型: {proxy.get('type', 'N/A')}")
            print(f"    本地: {proxy.get('localIP', 'N/A')}:{proxy.get('localPort', 'N/A')}")
            
            if proxy.get('type') in ['tcp', 'udp']:
                print(f"    远程: {proxy.get('remotePort', 'N/A')}")
            elif proxy.get('type') in ['http', 'https']:
                print(f"    子域名: {proxy.get('subDomain', 'N/A')}")

    def add_proxy(self):
        """添加新的代理配置"""
        print("\n" + "="*50)
        print("添加新代理配置")
        print("="*50)
        
        print("选择代理类型:")
        for i, ptype in enumerate(self.proxy_templates.keys(), 1):
            print(f"{i}. {ptype.upper()}")
        
        try:
            choice = int(input("请选择 (1-4): "))
            proxy_types = list(self.proxy_templates.keys())
            if 1 <= choice <= len(proxy_types):
                proxy_type = proxy_types[choice - 1]
            else:
                print("无效选择")
                return
        except ValueError:
            print("无效输入")
            return
        
        # 复制模板
        new_proxy = self.proxy_templates[proxy_type].copy()
        
        # 收集用户输入
        print(f"\n配置 {proxy_type.upper()} 代理:")
        
        name = input("代理名称: ").strip()
        if not name:
            print("代理名称不能为空")
            return
        new_proxy['name'] = name
        
        # 检查名称是否已存在
        existing_names = [p.get('name') for p in self.config_data.get('proxies', [])]
        if name in existing_names:
            print(f"代理名称 '{name}' 已存在")
            return
        
        try:
            local_port = int(input(f"本地端口 (默认: {new_proxy['localPort']}): ") or new_proxy['localPort'])
            new_proxy['localPort'] = local_port
            
            local_ip = input(f"本地IP (默认: {new_proxy['localIP']}): ") or new_proxy['localIP']
            new_proxy['localIP'] = local_ip
            
            if proxy_type in ['tcp', 'udp']:
                remote_port = int(input("远程端口: "))
                new_proxy['remotePort'] = remote_port
            elif proxy_type in ['http', 'https']:
                subdomain = input("子域名: ").strip()
                if not subdomain:
                    print("子域名不能为空")
                    return
                new_proxy['subDomain'] = subdomain
                
        except ValueError:
            print("端口必须是数字")
            return
        
        # 添加到配置
        if 'proxies' not in self.config_data:
            self.config_data['proxies'] = []
        
        self.config_data['proxies'].append(new_proxy)
        
        if self.save_config():
            print(f"✓ 代理 '{name}' 添加成功")

    def delete_proxy(self):
        """删除代理配置"""
        if 'proxies' not in self.config_data or not self.config_data['proxies']:
            print("暂无代理配置可删除")
            return
        
        print("\n" + "="*50)
        print("删除代理配置")
        print("="*50)
        
        self.show_proxies()
        
        try:
            index = int(input(f"\n请选择要删除的代理 (1-{len(self.config_data['proxies'])}): "))
            if 1 <= index <= len(self.config_data['proxies']):
                proxy_name = self.config_data['proxies'][index - 1].get('name', 'Unnamed')
                confirm = input(f"确认删除代理 '{proxy_name}'? (y/N): ").lower()
                if confirm == 'y':
                    del self.config_data['proxies'][index - 1]
                    if self.save_config():
                        print(f"✓ 代理 '{proxy_name}' 删除成功")
                else:
                    print("已取消删除")
            else:
                print("无效选择")
        except ValueError:
            print("无效输入")

    def modify_proxy(self):
        """修改代理配置"""
        if 'proxies' not in self.config_data or not self.config_data['proxies']:
            print("暂无代理配置可修改")
            return
        
        print("\n" + "="*50)
        print("修改代理配置")
        print("="*50)
        
        self.show_proxies()
        
        try:
            index = int(input(f"\n请选择要修改的代理 (1-{len(self.config_data['proxies'])}): "))
            if 1 <= index <= len(self.config_data['proxies']):
                proxy = self.config_data['proxies'][index - 1]
                proxy_type = proxy.get('type', 'tcp')
                
                print(f"\n修改代理: {proxy.get('name', 'Unnamed')} ({proxy_type})")
                print("直接回车保留当前值")
                
                # 修改各项配置
                new_name = input(f"代理名称 [{proxy.get('name', '')}]: ").strip()
                if new_name:
                    proxy['name'] = new_name
                
                new_local_ip = input(f"本地IP [{proxy.get('localIP', '127.0.0.1')}]: ").strip()
                if new_local_ip:
                    proxy['localIP'] = new_local_ip
                
                new_local_port = input(f"本地端口 [{proxy.get('localPort', 0)}]: ").strip()
                if new_local_port:
                    try:
                        proxy['localPort'] = int(new_local_port)
                    except ValueError:
                        print("端口必须是数字，保留原值")
                
                if proxy_type in ['tcp', 'udp']:
                    new_remote_port = input(f"远程端口 [{proxy.get('remotePort', 0)}]: ").strip()
                    if new_remote_port:
                        try:
                            proxy['remotePort'] = int(new_remote_port)
                        except ValueError:
                            print("端口必须是数字，保留原值")
                elif proxy_type in ['http', 'https']:
                    new_subdomain = input(f"子域名 [{proxy.get('subDomain', '')}]: ").strip()
                    if new_subdomain:
                        proxy['subDomain'] = new_subdomain
                
                if self.save_config():
                    print("✓ 代理配置修改成功")
            else:
                print("无效选择")
        except ValueError:
            print("无效输入")

    def show_logs(self):
        """显示日志文件"""
        print("\n" + "="*50)
        print("日志文件管理")
        print("="*50)
        
        if not self.logs_dir.exists():
            print("日志目录不存在")
            return
        
        # 查找所有日志文件
        log_files = list(self.logs_dir.glob("frpc_*.log"))
        if not log_files:
            print("未找到任何日志文件")
            return
        
        # 按修改时间排序，最新的在前
        log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        print("可用的日志文件:")
        for i, log_file in enumerate(log_files, 1):
            size = log_file.stat().st_size / 1024  # KB
            mtime = log_file.stat().st_mtime
            from datetime import datetime
            time_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{i}] {log_file.name} ({size:.1f}KB) - {time_str}")
        
        print(f"[{len(log_files) + 1}] 显示最新日志文件的末尾20行")
        print("0. 返回主菜单")
        
        try:
            choice = int(input(f"请选择 (0-{len(log_files) + 1}): "))
            if choice == 0:
                return
            elif choice == len(log_files) + 1:
                # 显示最新日志的末尾
                latest_log = log_files[0]
                self._show_log_content(latest_log, tail_lines=20)
            elif 1 <= choice <= len(log_files):
                selected_log = log_files[choice - 1]
                self._show_log_content(selected_log)
            else:
                print("无效选择")
        except ValueError:
            print("无效输入")
    
    def _show_log_content(self, log_file: Path, tail_lines: Optional[int] = None):
        """显示日志文件内容"""
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                print(f"日志文件 {log_file.name} 为空")
                return
            
            lines = content.strip().split('\n')
            
            if tail_lines:
                lines = lines[-tail_lines:] if len(lines) > tail_lines else lines
                print(f"\n{log_file.name} - 最新 {len(lines)} 行:")
            else:
                print(f"\n{log_file.name} - 完整内容:")
            
            print("-" * 60)
            for line in lines:
                print(line)
            print("-" * 60)
            
            # 检查是否有对应的错误日志
            err_file = log_file.with_suffix('.log.err')
            if err_file.exists():
                try:
                    with open(err_file, 'r', encoding='utf-8') as f:
                        err_content = f.read().strip()
                    if err_content:
                        print(f"\n错误日志 ({err_file.name}):")
                        print("-" * 60)
                        err_lines = err_content.split('\n')
                        if tail_lines:
                            err_lines = err_lines[-tail_lines:] if len(err_lines) > tail_lines else err_lines
                        for line in err_lines:
                            print(line)
                        print("-" * 60)
                    else:
                        print(f"\n✓ 无错误日志")
                except Exception as e:
                    print(f"读取错误日志失败: {e}")
            
        except Exception as e:
            print(f"读取日志文件失败: {e}")

    def show_menu(self):
        """显示主菜单"""
        print("\n" + "="*50)
        print("FRP Controller - 管理工具")
        print("="*50)
        print("1. 启动 frpc")
        print("2. 停止 frpc")
        print("3. 重启 frpc")
        print("4. 查看状态")
        print("5. 查看日志 (PowerShell)")
        print("6. 查看日志文件 (Python)")
        print("7. 显示服务器配置")
        print("8. 显示代理配置")
        print("9. 添加代理")
        print("10. 删除代理")
        print("11. 修改代理")
        print("12. 重新加载配置")
        print("13. 手动清理日志文件")
        print("0. 退出")
        print("="*50)

    def run(self):
        """运行主程序"""
        print("FRP Controller 启动...")
        
        while True:
            self.show_menu()
            
            try:
                choice = input("请选择操作 (0-13): ").strip()
                
                if choice == '0':
                    print("退出程序")
                    break
                elif choice == '1':
                    print("正在启动 frpc...")
                    self.run_powershell_script('start')
                elif choice == '2':
                    print("正在停止 frpc...")
                    self.run_powershell_script('stop')
                elif choice == '3':
                    print("正在重启 frpc...")
                    self.run_powershell_script('restart')
                elif choice == '4':
                    print("查看 frpc 状态...")
                    self.run_powershell_script('status')
                elif choice == '5':
                    print("查看 frpc 日志 (PowerShell)...")
                    self.run_powershell_script('log')
                elif choice == '6':
                    self.show_logs()
                elif choice == '7':
                    self.show_server_config()
                elif choice == '8':
                    self.show_proxies()
                elif choice == '9':
                    self.add_proxy()
                elif choice == '10':
                    self.delete_proxy()
                elif choice == '11':
                    self.modify_proxy()
                elif choice == '12':
                    print("重新加载配置...")
                    self.load_config()
                elif choice == '13':
                    print("手动清理日志文件...")
                    self.process_temp_logs()
                else:
                    print("无效选择，请重新输入")
                    
            except KeyboardInterrupt:
                print("\n\n程序被中断，退出...")
                break
            except Exception as e:
                print(f"发生错误: {e}")
            
            input("\n按回车键继续...")

if __name__ == "__main__":
    controller = FRPController()
    controller.run()
