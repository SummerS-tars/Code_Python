"""
Week 14 Lab 13 - 网络爬虫：天气查询系统
使用 HTTP API、Requests 和 JSON 实现天气数据获取与处理

作者: SummerS-tars
日期: 2025年12月13日
"""

import requests
import json
from datetime import datetime
from typing import Dict, Optional
import sys


class WeatherCrawler:
    """天气爬虫类，用于获取和处理天气数据"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化天气爬虫
        
        Args:
            api_key: OpenWeatherMap API密钥（可选，使用免费API）
        """
        # 使用免费的天气API - wttr.in (无需API key)
        self.base_url = "https://wttr.in"
        self.api_key = api_key
        
    def get_weather_by_city(self, city: str, lang: str = "zh-cn") -> Optional[Dict]:
        """
        根据城市名获取天气信息
        
        Args:
            city: 城市名称（中文或英文）
            lang: 语言设置，默认中文
            
        Returns:
            包含天气信息的字典，失败返回None
        """
        try:
            # 使用wttr.in的JSON格式API
            url = f"{self.base_url}/{city}?format=j1&lang={lang}"
            
            print(f"正在获取 {city} 的天气信息...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # 解析JSON数据
            weather_data = response.json()
            
            # 提取并整理关键信息
            return self._parse_weather_data(weather_data, city)
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 获取天气数据失败: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            return None
            
    def _parse_weather_data(self, data: Dict, city: str) -> Dict:
        """
        解析API返回的天气数据
        
        Args:
            data: 原始API响应数据
            city: 城市名称
            
        Returns:
            整理后的天气信息字典
        """
        try:
            current = data['current_condition'][0]
            nearest_area = data.get('nearest_area', [{}])[0]
            
            # 提取关键信息
            weather_info = {
                "城市": city,
                "区域": nearest_area.get('areaName', [{}])[0].get('value', city),
                "国家": nearest_area.get('country', [{}])[0].get('value', ''),
                "观测时间": current.get('localObsDateTime', ''),
                "温度": f"{current.get('temp_C', 'N/A')}°C",
                "体感温度": f"{current.get('FeelsLikeC', 'N/A')}°C",
                "天气描述": current.get('lang_zh-cn', [{}])[0].get('value', 
                                current.get('weatherDesc', [{}])[0].get('value', 'N/A')),
                "湿度": f"{current.get('humidity', 'N/A')}%",
                "降水量": f"{current.get('precipMM', 'N/A')} mm",
                "气压": f"{current.get('pressure', 'N/A')} mb",
                "能见度": f"{current.get('visibility', 'N/A')} km",
                "风向": current.get('winddir16Point', 'N/A'),
                "风速": f"{current.get('windspeedKmph', 'N/A')} km/h",
                "紫外线指数": current.get('uvIndex', 'N/A'),
                "云量": f"{current.get('cloudcover', 'N/A')}%"
            }
            
            return weather_info
            
        except (KeyError, IndexError) as e:
            print(f"⚠️ 解析数据时出现问题: {e}")
            return {"错误": "数据解析失败"}
    
    def display_weather(self, weather_info: Dict) -> None:
        """
        格式化显示天气信息
        
        Args:
            weather_info: 天气信息字典
        """
        if not weather_info:
            print("❌ 无天气数据可显示")
            return
            
        if "错误" in weather_info:
            print(f"❌ {weather_info['错误']}")
            return
            
        print("\n" + "="*60)
        print(f"🌤️  天气查询结果")
        print("="*60)
        
        for key, value in weather_info.items():
            print(f"{key:12s}: {value}")
        
        print("="*60 + "\n")
    
    def get_weather_forecast(self, city: str, days: int = 3) -> Optional[list]:
        """
        获取未来几天的天气预报
        
        Args:
            city: 城市名称
            days: 预报天数（默认3天）
            
        Returns:
            天气预报列表，失败返回None
        """
        try:
            url = f"{self.base_url}/{city}?format=j1&lang=zh-cn"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            weather_forecast = data.get('weather', [])[:days]
            
            forecast_list = []
            for day in weather_forecast:
                forecast_info = {
                    "日期": day.get('date', ''),
                    "最高温度": f"{day.get('maxtempC', 'N/A')}°C",
                    "最低温度": f"{day.get('mintempC', 'N/A')}°C",
                    "天气": day.get('hourly', [{}])[4].get('lang_zh-cn', [{}])[0].get('value', 'N/A'),
                    "紫外线指数": day.get('uvIndex', 'N/A'),
                    "日出": day.get('astronomy', [{}])[0].get('sunrise', 'N/A'),
                    "日落": day.get('astronomy', [{}])[0].get('sunset', 'N/A')
                }
                forecast_list.append(forecast_info)
            
            return forecast_list
            
        except Exception as e:
            print(f"❌ 获取天气预报失败: {e}")
            return None
    
    def display_forecast(self, forecast_list: list) -> None:
        """
        显示天气预报信息
        
        Args:
            forecast_list: 天气预报列表
        """
        if not forecast_list:
            print("❌ 无预报数据可显示")
            return
        
        print("\n" + "="*60)
        print(f"📅 未来 {len(forecast_list)} 天天气预报")
        print("="*60)
        
        for idx, forecast in enumerate(forecast_list, 1):
            print(f"\n第 {idx} 天:")
            for key, value in forecast.items():
                print(f"  {key:10s}: {value}")
        
        print("="*60 + "\n")
    
    def save_to_json(self, data: Dict, filename: str = "weather_data.json") -> bool:
        """
        将天气数据保存到JSON文件
        
        Args:
            data: 要保存的数据
            filename: 文件名
            
        Returns:
            保存成功返回True，否则返回False
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"✅ 数据已保存到 {filename}")
            return True
        except Exception as e:
            print(f"❌ 保存文件失败: {e}")
            return False


def main():
    """主函数 - 交互式天气查询"""
    print("="*60)
    print("🌈 欢迎使用天气查询爬虫系统")
    print("="*60)
    print("本程序使用 HTTP API、Requests 和 JSON 技术")
    print("可以查询全球各地的实时天气信息\n")
    
    # 创建爬虫实例
    crawler = WeatherCrawler()
    
    while True:
        print("\n请选择功能：")
        print("1. 查询城市当前天气")
        print("2. 查询城市天气预报")
        print("3. 查询并保存天气数据到JSON")
        print("4. 退出程序")
        
        choice = input("\n请输入选项 (1-4): ").strip()
        
        if choice == '1':
            city = input("请输入城市名称（中文或英文）: ").strip()
            if city:
                weather_info = crawler.get_weather_by_city(city)
                crawler.display_weather(weather_info)
            else:
                print("❌ 城市名称不能为空")
                
        elif choice == '2':
            city = input("请输入城市名称（中文或英文）: ").strip()
            if city:
                days = input("预报天数 (1-7，默认3天): ").strip()
                days = int(days) if days.isdigit() and 1 <= int(days) <= 7 else 3
                
                forecast = crawler.get_weather_forecast(city, days)
                crawler.display_forecast(forecast)
            else:
                print("❌ 城市名称不能为空")
                
        elif choice == '3':
            city = input("请输入城市名称（中文或英文）: ").strip()
            if city:
                weather_info = crawler.get_weather_by_city(city)
                if weather_info:
                    crawler.display_weather(weather_info)
                    filename = input("请输入保存的文件名 (默认: weather_data.json): ").strip()
                    filename = filename if filename else "weather_data.json"
                    crawler.save_to_json(weather_info, filename)
            else:
                print("❌ 城市名称不能为空")
                
        elif choice == '4':
            print("\n👋 感谢使用，再见！")
            break
            
        else:
            print("❌ 无效选项，请重新选择")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        sys.exit(1)
