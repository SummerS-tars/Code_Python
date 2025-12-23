"""地铁换乘路径规划系统 - 主程序

该程序实现了地铁换乘路径的智能规划功能。
"""

import sys
import os
from typing import Optional

# 添加src目录到路径，以便导入模块
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from models.station import Station
from models.network import MetroNetwork
from services.data_loader import DataLoader, DataLoadError
from services.path_finder import PathFinder, PathNotFoundError
from utils.parser import Parser, InvalidInputError
from utils.formatter import Formatter
from config import DEFAULT_DATA_FILE


class MetroPathPlanner:
    """地铁换乘路径规划系统主类"""
    
    def __init__(self, data_file: str = DEFAULT_DATA_FILE):
        """初始化系统
        
        Args:
            data_file: CSV数据文件路径
        """
        self.data_file = data_file
        self.network: Optional[MetroNetwork] = None
        self.path_finder = PathFinder()
        self.parser = Parser()
        self.formatter = Formatter()
    
    def load_data(self) -> bool:
        """加载地铁数据
        
        Returns:
            加载成功返回True，否则返回False
        """
        try:
            loader = DataLoader()
            self.network = loader.load_from_csv(self.data_file)
            print(f"✓ 成功加载数据: {self.network}")
            return True
        except DataLoadError as e:
            print(self.formatter.format_error(f"加载数据失败: {str(e)}"))
            return False
    
    def find_route(self, start_line: Optional[str], start_station: str, 
                   end_line: Optional[str], end_station: str, strategy: str = "min_station") -> str:
        """查找路径
        
        Args:
            start_line: 起始线路
            start_station: 起始站名
            end_line: 目标线路
            end_station: 目标站名
            strategy: 路径策略（"min_station" 最少站点 / "min_transfer" 最少换乘）
            
        Returns:
            格式化的路径字符串
        """
        try:
            if self.network is None:
                return self.formatter.format_error("系统未初始化，请先加载数据")
            
            # 起点处理
            start = None
            if start_line:
                start = self.network.find_station(start_line, start_station)
            else:
                # 无线路名时，尝试精确站名匹配任意线路
                start = self.network.get_station_any_line(start_station)
                if start is None:
                    # 尝试模糊搜索
                    candidates = self.network.search_stations(start_station)
                    if len(candidates) == 1:
                        start = candidates[0]
                    elif len(candidates) > 1:
                        options = '，'.join(str(s) for s in candidates)
                        return self.formatter.format_error(
                            f"起点存在多个匹配，请指定线路或更精确站名：{options}")
            if start is None:
                return self.formatter.format_error(
                    f"未找到起点站: {start_station}"
                )

            # 终点处理
            end = None
            if end_line:
                end = self.network.find_station(end_line, end_station)
            else:
                end = self.network.get_station_any_line(end_station)
                if end is None:
                    candidates = self.network.search_stations(end_station)
                    if len(candidates) == 1:
                        end = candidates[0]
                    elif len(candidates) > 1:
                        options = '，'.join(str(s) for s in candidates)
                        return self.formatter.format_error(
                            f"终点存在多个匹配，请指定线路或更精确站名：{options}")
            if end is None:
                return self.formatter.format_error(
                    f"未找到终点站: {end_station}"
                )
            
            # 查找路径
            path = self.path_finder.find_path(start, end, strategy=strategy)
            
            # 格式化输出
            return self.formatter.format_path(path)
            
        except PathNotFoundError as e:
            return self.formatter.format_error(str(e))
        except Exception as e:
            return self.formatter.format_error(f"查找路径时出错: {str(e)}")
    
    def process_user_input(self, user_input: str) -> str:
        """处理用户输入
        
        Args:
            user_input: 用户输入字符串
            
        Returns:
            处理结果字符串
        """
        try:
            # 解析输入
            (start_line, start_station), (end_line, end_station) = \
                self.parser.parse_input(user_input)
            
            # 查找路径
            result = self.find_route(start_line, start_station, 
                                    end_line, end_station)
            return result
            
        except InvalidInputError as e:
            return self.formatter.format_error(str(e))
    
    def run_interactive(self):
        """运行交互式模式"""
        print(self.formatter.format_welcome())
        
        while True:
            try:
                user_input = input("\n请输入查询（或输入q退出）: ").strip()
                
                # 检查退出命令
                if user_input.lower() in ['q', 'quit', 'exit']:
                    print("\n感谢使用，再见！")
                    break
                
                if not user_input:
                    continue
                
                # 处理查询
                print("\n查询结果：")
                print("=" * 40)
                result = self.process_user_input(user_input)
                print(result)
                print("=" * 40)
                
            except KeyboardInterrupt:
                print("\n\n程序被中断，再见！")
                break
            except Exception as e:
                print(self.formatter.format_error(f"程序错误: {str(e)}"))
    
    def run_test_cases(self):
        """运行测试用例"""
        print("\n" + "=" * 50)
        print("运行测试用例")
        print("=" * 50)
        
        test_cases = [
            "18号线，复旦大学-10号线，交通大学",
            "18号线，上海财经大学-8号线，东方体育中心"
        ]
        
        for i, test_input in enumerate(test_cases, 1):
            print(f"\n【测试用例 {i}】")
            print(f"输入: {test_input}")
            print("\n输出:")
            print("-" * 40)
            result = self.process_user_input(test_input)
            print(result)
            print("-" * 40)


def main():
    """主函数"""
    # 创建系统实例
    planner = MetroPathPlanner()
    
    # 加载数据
    if not planner.load_data():
        print("系统初始化失败，程序退出。")
        sys.exit(1)
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test':
            # 运行测试用例
            planner.run_test_cases()
        else:
            # 处理单个查询
            query = ' '.join(sys.argv[1:])
            result = planner.process_user_input(query)
            print("\n查询结果：")
            print(result)
    else:
        # 交互式模式
        planner.run_interactive()


if __name__ == "__main__":
    main()
