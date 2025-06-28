# FRP Controller - frpc 管理工具

一个简单的 frpc 交互式管理工具，用于管理 FRP 客户端配置和进程。

## 快速开始

### 方法1：自动设置（推荐）

使用提供的设置脚本来自动创建虚拟环境并安装依赖：

**PowerShell（推荐）：**

```powershell
.\setup_venv.ps1
```

**命令提示符：**

```cmd
setup_venv.bat
```

**高级选项：**

```powershell
# 强制重新创建虚拟环境
.\setup_venv.ps1 -Force

# 使用自定义虚拟环境名称
.\setup_venv.ps1 -VenvName "myenv"
```

设置完成后，每次使用时只需运行激活脚本：

- **PowerShell**: `.\activate_venv.ps1`
- **命令提示符**: `activate_venv.bat`

然后运行程序：

```bash
python FRPController.py
```

### 方法2：手动设置

1. **创建虚拟环境：**

   ```bash
   python -m venv venv
   ```

2. **激活虚拟环境：**

   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **安装依赖：**

   ```bash
   pip install -r requirements.txt
   ```

4. **运行程序：**

   ```bash
   python FRPController.py
   ```

## 文件结构

```txt
01_frpController/
├── frpc.exe             # FRP 客户端程序
├── frpc.toml            # 配置文件
├── frpcStart_en.ps1     # PowerShell 启动脚本（英文版）
├── FRPController.py     # Python 管理工具
├── requirements.txt     # Python 依赖
├── setup_venv.ps1       # 虚拟环境设置脚本（PowerShell）
├── setup_venv.bat       # 虚拟环境设置脚本（批处理）
├── activate_venv.ps1    # 虚拟环境激活脚本（PowerShell）
├── activate_venv.bat    # 虚拟环境激活脚本（批处理）
├── logs/                # 日志文件目录
├── venv/                # 虚拟环境目录（自动创建）
└── README.md           # 说明文档
```

## 环境要求

- **Python 3.7+** - 确保已安装 Python 并添加到 PATH
- **Windows 系统** - 此工具专为 Windows 设计

### 依赖安装

**自动安装（推荐）：**
运行 `setup_venv.ps1` 或 `setup_venv.bat` 会自动安装所有依赖。

**手动安装：**
```bash
pip install -r requirements.txt
```

**依赖列表：**
- `toml` - TOML 配置文件解析

## 使用方法

### 1. PowerShell 脚本 (frpcStart.ps1)

直接管理 frpc 进程：

```powershell
# 启动 frpc
.\frpcStart.ps1 -Action start

# 停止 frpc
.\frpcStart.ps1 -Action stop

# 重启 frpc
.\frpcStart.ps1 -Action restart

# 查看状态
.\frpcStart.ps1 -Action status

# 查看日志
.\frpcStart.ps1 -Action log

# 使用自定义配置文件
.\frpcStart.ps1 -Action start -ConfigFile custom.toml
```

### 2. Python 管理工具 (FRPController.py)

运行交互式管理界面：

```bash
python FRPController.py
```

#### 功能菜单

1. **启动 frpc** - 启动 FRP 客户端进程
2. **停止 frpc** - 停止 FRP 客户端进程  
3. **重启 frpc** - 重启 FRP 客户端进程
4. **查看状态** - 显示 frpc 进程状态
5. **查看日志 (PowerShell)** - 通过 PowerShell 显示最新日志
6. **查看日志文件 (Python)** - 浏览和查看历史日志文件
7. **显示服务器配置** - 查看服务器连接配置
8. **显示代理配置** - 列出所有代理配置
9. **添加代理** - 添加新的代理配置
10. **删除代理** - 删除指定代理配置
11. **修改代理** - 修改现有代理配置
12. **重新加载配置** - 重新读取配置文件

#### 支持的代理类型

- **TCP** - TCP 端口转发
- **UDP** - UDP 端口转发  
- **HTTP** - HTTP 网站代理（需要子域名）
- **HTTPS** - HTTPS 网站代理（需要子域名）

## 配置文件 (frpc.toml)

### 服务器配置

```toml
serverAddr = "your.server.ip"
serverPort = 7000
auth.method = "token"
auth.token = "your-token"
```

### 代理配置示例

```toml
# TCP 代理示例
[[proxies]]
name = "ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 6000

# HTTP 代理示例
[[proxies]]
name = "web"
type = "http"
localIP = "127.0.0.1"
localPort = 80
subDomain = "web"
```

## 注意事项

1. **Windows 系统** - 此工具专为 Windows 设计
2. **PowerShell 执行策略** - 如果无法运行 PowerShell 脚本，请以管理员身份运行：

   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **防火墙** - 确保防火墙允许 frpc.exe 的网络访问
4. **配置备份** - 建议在修改配置前备份 frpc.toml 文件

## 日志文件

### 日志管理增强功能

- **日志目录**: 所有日志文件自动保存在 `logs/` 子目录中
- **时间戳命名**: 每次启动创建新的带时间戳的日志文件 (如：`frpc_20241220_143052.log`)
- **ANSI 代码清理**: 自动移除 frpc 输出中的颜色代码，确保日志清晰可读
- **分离错误日志**: 错误信息单独保存在 `.err` 文件中
- **操作记录**: 启动/停止操作会自动记录到相应的日志文件中

### 日志文件查看

- **PowerShell 方式**: 使用 `.\frpcStart.ps1 -Action log` 查看最新日志
- **Python 方式**: 在管理工具中选择 "查看日志文件" 浏览所有历史日志
- **手动查看**: 直接打开 `logs/` 目录中的日志文件

## 新增功能特点

### 🚀 PowerShell 脚本增强

- ✅ **自动日志目录管理** - 自动创建和管理 `logs/` 目录
- ✅ **时间戳日志文件** - 每次启动生成唯一的日志文件
- ✅ **ANSI 代码清理** - 后台任务自动清理日志中的颜色代码
- ✅ **操作日志记录** - 启动/停止操作详细记录到日志
- ✅ **进程信息增强** - 记录进程 PID 和启动时间

### 🐍 Python 管理工具增强

- ✅ **双重日志查看** - PowerShell 和 Python 两种日志查看方式
- ✅ **历史日志浏览** - 查看所有历史日志文件
- ✅ **智能日志展示** - 自动显示文件大小和修改时间
- ✅ **错误日志分离** - 单独显示错误日志内容
- ✅ **快速日志预览** - 支持查看最新 20 行日志

## 故障排除

1. **无法启动** - 检查 frpc.exe 是否存在
2. **连接失败** - 检查服务器地址和端口配置
3. **权限问题** - 以管理员身份运行程序
4. **端口冲突** - 检查本地端口是否被占用
