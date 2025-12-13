"""
快速测试脚本 - 演示天气爬虫的基本功能
无需交互，直接运行查看结果
"""

from weather_crawler import WeatherCrawler


def test_basic_features():
    """测试基本功能"""
    print("="*60)
    print("🧪 天气爬虫系统 - 功能测试")
    print("="*60)
    
    # 创建爬虫实例
    crawler = WeatherCrawler()
    
    # 测试城市列表
    test_cities = ["北京", "上海", "London"]
    
    print("\n📍 测试 1: 查询多个城市的当前天气\n")
    for city in test_cities:
        print(f"\n正在查询 {city}...")
        weather_info = crawler.get_weather_by_city(city)
        if weather_info:
            crawler.display_weather(weather_info)
        else:
            print(f"❌ {city} 查询失败")
    
    print("\n📍 测试 2: 查询天气预报\n")
    city = "北京"
    print(f"正在获取 {city} 的3天天气预报...")
    forecast = crawler.get_weather_forecast(city, days=3)
    if forecast:
        crawler.display_forecast(forecast)
    else:
        print("❌ 天气预报获取失败")
    
    print("\n📍 测试 3: 保存数据到 JSON 文件\n")
    city = "上海"
    weather_info = crawler.get_weather_by_city(city)
    if weather_info:
        filename = "test_weather_data.json"
        success = crawler.save_to_json(weather_info, filename)
        if success:
            print(f"✅ 测试通过：数据已保存到 {filename}")
    
    print("\n" + "="*60)
    print("✅ 所有测试完成！")
    print("="*60)


if __name__ == "__main__":
    try:
        test_basic_features()
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
