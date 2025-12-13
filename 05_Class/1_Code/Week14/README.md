# Week 14 Lab 13 - 天气查询爬虫系统

## 项目简介

这是一个基于 Python 的网络爬虫程序，使用 **HTTP API**、**Requests** 和 **JSON** 技术实现天气数据的获取与处理。

### 功能特点

✅ **实时天气查询** - 获取全球任意城市的当前天气信息  
✅ **天气预报** - 查询未来多天的天气预报  
✅ **数据导出** - 将天气数据保存为 JSON 格式  
✅ **友好界面** - 交互式命令行界面  
✅ **无需API密钥** - 使用免费的 wttr.in API

## 技术栈

- **Python 3.x**
- **Requests** - HTTP 请求库
- **JSON** - 数据解析和存储
- **wttr.in API** - 免费天气数据接口

## 文件结构

```
Week14/
├── weather_crawler.py    # 主程序文件
├── config.py            # 配置文件
├── requirements.txt     # 依赖列表
└── README.md           # 使用说明（本文件）
```

## 安装步骤

### 1. 安装依赖

使用 pip 安装所需的 Python 包：

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install requests
```

### 2. 验证安装

运行以下命令验证 requests 库是否安装成功：

```bash
python -c "import requests; print('Requests 版本:', requests.__version__)"
```

## 使用方法

### 启动程序

在 Week14 目录下运行：

```bash
python weather_crawler.py
```

### 功能菜单

程序启动后会显示以下菜单：

```
请选择功能：
1. 查询城市当前天气
2. 查询城市天气预报
3. 查询并保存天气数据到JSON
4. 退出程序
```

### 使用示例

#### 示例 1：查询当前天气

```
请输入选项 (1-4): 1
请输入城市名称（中文或英文）: 北京

🌤️  天气查询结果
============================================================
城市        : 北京
区域        : Beijing
国家        : China
观测时间    : 2025-12-13 14:30
温度        : 5°C
体感温度    : 2°C
天气描述    : 晴朗
湿度        : 45%
降水量      : 0.0 mm
气压        : 1020 mb
能见度      : 10 km
风向        : N
风速        : 15 km/h
紫外线指数  : 2
云量        : 20%
============================================================
```

#### 示例 2：查询天气预报

```
请输入选项 (1-4): 2
请输入城市名称（中文或英文）: 上海
预报天数 (1-7，默认3天): 3

📅 未来 3 天天气预报
============================================================

第 1 天:
  日期      : 2025-12-13
  最高温度  : 12°C
  最低温度  : 8°C
  天气      : 多云
  紫外线指数: 3
  日出      : 06:48 AM
  日落      : 04:52 PM
...
```

#### 示例 3：保存数据到 JSON

```
请输入选项 (1-4): 3
请输入城市名称（中文或英文）: 深圳
正在获取 深圳 的天气信息...

🌤️  天气查询结果
[显示天气信息...]

请输入保存的文件名 (默认: weather_data.json): shenzhen_weather.json
✅ 数据已保存到 shenzhen_weather.json
```

## 核心代码说明

### 1. HTTP API 请求

使用 `requests` 库发送 HTTP GET 请求：

```python
response = requests.get(url, timeout=10)
response.raise_for_status()  # 检查请求状态
```

### 2. JSON 数据解析

解析 API 返回的 JSON 数据：

```python
weather_data = response.json()
current = data['current_condition'][0]
temperature = current.get('temp_C', 'N/A')
```

### 3. 数据处理与展示

提取关键信息并格式化展示：

```python
weather_info = {
    "城市": city,
    "温度": f"{current.get('temp_C', 'N/A')}°C",
    "天气描述": current.get('weatherDesc', [{}])[0].get('value', 'N/A'),
    # ... 更多字段
}
```

### 4. JSON 文件保存

将数据保存为 JSON 格式：

```python
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
```

## API 说明

### wttr.in API

本程序使用免费的 [wttr.in](https://wttr.in) 天气 API：

- **无需注册**：不需要 API 密钥
- **全球覆盖**：支持世界各地城市查询
- **中文支持**：支持中文城市名和天气描述
- **JSON 格式**：返回结构化的 JSON 数据

**API 端点示例**：
```
https://wttr.in/Beijing?format=j1&lang=zh-cn
```

**参数说明**：
- `format=j1` - 返回 JSON 格式数据
- `lang=zh-cn` - 使用中文语言

## 扩展功能

如需使用其他 API（如 OpenWeatherMap），可以在 `config.py` 中配置：

```python
API_CONFIG = {
    "openweather_api_key": "your_api_key_here",
    "openweather_base_url": "https://api.openweathermap.org/data/2.5",
}
```

## 常见问题

### Q1: 提示 "ModuleNotFoundError: No module named 'requests'"

**解决方法**：安装 requests 库
```bash
pip install requests
```

### Q2: 查询时提示超时

**解决方法**：
- 检查网络连接
- 尝试使用英文城市名
- 增加超时时间（在代码中修改 `timeout` 参数）

### Q3: 中文城市名无法识别

**解决方法**：
- 使用拼音或英文名称（如 "Beijing" 代替 "北京"）
- 参考 `config.py` 中的常用城市列表

### Q4: JSON 数据保存失败

**解决方法**：
- 检查文件写入权限
- 确保文件名合法（不包含特殊字符）

## 实验要求对照

✅ **使用 HTTP API**：通过 requests 库调用 wttr.in RESTful API  
✅ **使用 Requests**：所有网络请求均通过 requests 库实现  
✅ **使用 JSON**：API 返回 JSON 格式数据，程序解析并处理 JSON  
✅ **数据获取**：成功获取天气信息、预报等数据  
✅ **数据处理**：解析、提取、格式化天气数据并展示  

## 项目亮点

1. **完整的错误处理**：包含网络错误、JSON 解析错误等异常处理
2. **用户友好**：交互式菜单、清晰的输出格式、中文界面
3. **代码规范**：使用类型提示、文档字符串、符合 PEP 8 规范
4. **功能丰富**：不仅查询当前天气，还支持预报和数据导出
5. **配置灵活**：分离的配置文件，易于扩展和修改

## 学习要点

通过本项目，你将学习到：

1. ✅ 如何使用 `requests` 库发送 HTTP 请求
2. ✅ 如何处理 API 返回的 JSON 数据
3. ✅ 如何进行异常处理和错误管理
4. ✅ 如何设计交互式命令行程序
5. ✅ 如何进行数据的读取、解析和存储

## 作者信息

- **作者**：SummerS-tars
- **日期**：2025年12月13日
- **实验**：Week 14 Lab 13

## 许可证

本项目仅用于学习和教育目的。

---

**提示**：首次运行前请确保已安装所有依赖！

```bash
pip install -r requirements.txt
python weather_crawler.py
```
