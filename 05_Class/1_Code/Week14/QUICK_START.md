# Week 14 Lab 13 - 快速使用指南

## 🚀 快速开始

### 方法一：直接运行主程序

```powershell
# 1. 打开 PowerShell
# 2. 进入项目目录
cd "E:\_ComputerLearning\7_Programming_Python\Code_Python\05_Class\1_Code\Week14"

# 3. 运行程序
E:/_ComputerLearning/7_Programming_Python/Code_Python/venv/Scripts/python.exe weather_crawler.py
```

### 方法二：使用启动脚本（推荐）

```powershell
# 1. 进入项目目录
cd "E:\_ComputerLearning\7_Programming_Python\Code_Python\05_Class\1_Code\Week14"

# 2. 运行启动脚本
.\run.ps1
```

### 方法三：运行测试脚本

```powershell
# 查看功能演示
E:/_ComputerLearning/7_Programming_Python/Code_Python/venv/Scripts/python.exe test_weather.py
```

## 📖 使用示例

### 示例 1：查询当前天气

```text
请选择功能：
1. 查询城市当前天气
2. 查询城市天气预报
3. 查询并保存天气数据到JSON
4. 退出程序

请输入选项 (1-4): 1
请输入城市名称（中文或英文）: 北京

正在获取 北京 的天气信息...

🌤️  天气查询结果
============================================================
城市          : 北京
温度          : 1°C
体感温度        : -3°C
天气描述        : 少云
湿度          : 40%
风速          : 15 km/h
...
```

### 示例 2：支持的城市名称

✅ **中文城市名**
- 北京、上海、广州、深圳
- 成都、杭州、武汉、西安
- 重庆、南京、天津等

✅ **英文城市名**
- Beijing, Shanghai, London
- New York, Paris, Tokyo
- Sydney, Berlin 等

✅ **拼音**
- Beijing, Shanghai, Guangzhou 等

## ⚙️ 功能说明

### 功能 1：查询当前天气
- 显示实时温度、体感温度
- 天气描述、湿度、气压
- 风向、风速、能见度
- 紫外线指数、云量等

### 功能 2：查询天气预报
- 未来 1-7 天的天气预报
- 最高/最低温度
- 日出/日落时间
- 天气状况描述

### 功能 3：保存数据到 JSON
- 将天气数据保存为 JSON 文件
- 支持自定义文件名
- UTF-8 编码，支持中文

## 🔧 常见问题

### Q：提示找不到 requests 模块？
**A：** 依赖已经安装，如果还有问题，手动安装：
```powershell
E:/_ComputerLearning/7_Programming_Python/Code_Python/venv/Scripts/python.exe -m pip install requests
```

### Q：查询失败或超时？
**A：** 
1. 检查网络连接
2. 尝试使用英文城市名
3. 稍后再试

### Q：如何退出程序？
**A：** 
- 选择菜单选项 4
- 或按 Ctrl+C

## 📊 测试验证

程序已通过测试，验证结果：
- ✅ 北京天气查询成功
- ✅ 上海天气查询成功  
- ✅ 伦敦天气查询成功
- ✅ 天气预报功能正常
- ✅ JSON 保存功能正常

## 📁 项目文件

```
Week14/
├── weather_crawler.py      # 主程序
├── test_weather.py        # 测试脚本
├── config.py              # 配置文件
├── requirements.txt       # 依赖列表
├── run.ps1               # 启动脚本
├── README.md             # 详细说明
├── PROJECT_SUMMARY.md    # 项目总结
└── QUICK_START.md        # 快速指南（本文件）
```

## 🎯 实验要求对照

| 要求项   | 状态 | 说明                     |
| -------- | ---- | ------------------------ |
| HTTP API | ✅    | 使用 wttr.in RESTful API |
| Requests | ✅    | HTTP 请求库              |
| JSON     | ✅    | 解析和保存 JSON 数据     |
| 数据获取 | ✅    | 获取天气信息             |
| 数据处理 | ✅    | 解析和展示数据           |

## 💡 提示

1. **首次使用**：建议先运行 `test_weather.py` 查看效果
2. **网络要求**：需要联网才能查询天气
3. **城市名称**：支持中英文，推荐使用拼音或英文
4. **数据来源**：使用免费的 wttr.in API，无需注册

## 📞 支持

如有问题，请查看：
- `README.md` - 完整使用文档
- `PROJECT_SUMMARY.md` - 项目技术总结

---

**祝使用愉快！** 🎉
