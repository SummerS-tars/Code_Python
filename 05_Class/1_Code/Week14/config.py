"""
配置文件 - 天气爬虫系统
包含API配置和常用城市列表
"""

# API 配置
API_CONFIG = {
    # wttr.in 免费天气API（无需密钥）
    "wttr_base_url": "https://wttr.in",
    
    # 可选：如果使用OpenWeatherMap API
    "openweather_api_key": "",  # 在这里填入你的API密钥
    "openweather_base_url": "https://api.openweathermap.org/data/2.5",
}

# 常用城市列表（中文/英文对照）
POPULAR_CITIES = {
    "北京": "Beijing",
    "上海": "Shanghai",
    "广州": "Guangzhou",
    "深圳": "Shenzhen",
    "成都": "Chengdu",
    "杭州": "Hangzhou",
    "武汉": "Wuhan",
    "西安": "Xian",
    "重庆": "Chongqing",
    "南京": "Nanjing",
    "天津": "Tianjin",
    "苏州": "Suzhou",
    "长沙": "Changsha",
    "郑州": "Zhengzhou",
    "青岛": "Qingdao",
    "大连": "Dalian",
    "厦门": "Xiamen",
    "纽约": "New York",
    "伦敦": "London",
    "东京": "Tokyo",
    "巴黎": "Paris",
    "悉尼": "Sydney",
}

# 请求配置
REQUEST_CONFIG = {
    "timeout": 10,  # 请求超时时间（秒）
    "retry_times": 3,  # 重试次数
    "lang": "zh-cn",  # 默认语言
}

# 数据存储配置
STORAGE_CONFIG = {
    "default_filename": "weather_data.json",
    "encoding": "utf-8",
}
