"""输入解析器

该模块负责解析用户输入，提取起点和终点信息。
"""

from typing import Tuple


class InvalidInputError(Exception):
    """输入格式错误异常"""
    pass


class Parser:
    """输入解析器类
    
    负责解析用户输入的起点和终点信息。
    
    输入格式：起始线路，起始站名-目标线路，目标站名
    示例：18号线，复旦大学-10号线，交通大学
    """
    
    @staticmethod
    def parse_input(user_input: str) -> Tuple[Tuple[str, str], Tuple[str, str]]:
        """解析用户输入
        
        Args:
            user_input: 用户输入字符串
            
        Returns:
            包含起点和终点信息的元组：
            ((起始线路, 起始站名), (目标线路, 目标站名))
            
        Raises:
            InvalidInputError: 输入格式错误时抛出
        """
        try:
            # 去除首尾空格
            user_input = user_input.strip()
            
            # 按"-"分割起点和终点
            if '-' not in user_input:
                raise InvalidInputError("输入格式错误，应包含'-'分隔符")
            
            parts = user_input.split('-')
            if len(parts) != 2:
                raise InvalidInputError("输入格式错误，应为：起始线路，起始站名-目标线路，目标站名")
            
            start_part = parts[0].strip()
            end_part = parts[1].strip()
            
            # 解析起点
            start_line, start_station = Parser._parse_station_info(start_part)
            
            # 解析终点
            end_line, end_station = Parser._parse_station_info(end_part)
            
            return (start_line, start_station), (end_line, end_station)
            
        except Exception as e:
            if isinstance(e, InvalidInputError):
                raise
            raise InvalidInputError(f"解析输入时出错: {str(e)}")
    
    @staticmethod
    def _parse_station_info(station_info: str) -> Tuple[str, str]:
        """解析站点信息
        
        Args:
            station_info: 站点信息字符串，格式为"线路名，站名"
            
        Returns:
            (线路名, 站名)元组
            
        Raises:
            InvalidInputError: 格式错误时抛出
        """
        # 按"，"或","分割
        if '，' in station_info:
            parts = station_info.split('，')
        elif ',' in station_info:
            parts = station_info.split(',')
        else:
            raise InvalidInputError(f"站点信息格式错误: {station_info}，应包含'，'或','分隔符")
        
        if len(parts) != 2:
            raise InvalidInputError(f"站点信息格式错误: {station_info}，应为：线路名，站名")
        
        line_name = parts[0].strip()
        station_name = parts[1].strip()
        
        if not line_name or not station_name:
            raise InvalidInputError(f"线路名和站名不能为空: {station_info}")
        
        return line_name, station_name
    
    @staticmethod
    def validate_input(user_input: str) -> bool:
        """验证用户输入格式是否正确
        
        Args:
            user_input: 用户输入字符串
            
        Returns:
            格式正确返回True，否则返回False
        """
        try:
            Parser.parse_input(user_input)
            return True
        except InvalidInputError:
            return False
