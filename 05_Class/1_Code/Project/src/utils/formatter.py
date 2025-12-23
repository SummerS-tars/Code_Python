"""输出格式化器

该模块负责将路径结果格式化为指定的输出格式。
"""

from typing import List, Union
from models.station import Station


class Formatter:
    """输出格式化器类
    
    负责将路径列表格式化为符合要求的输出字符串。
    
    输出格式：
        线路名，站名
        线路名，站名
        换乘
        线路名，站名
        ...
    """
    
    @staticmethod
    def format_path(path: List[Union[Station, str]]) -> str:
        """格式化路径为输出字符串
        
        Args:
            path: 路径列表，包含Station对象和"换乘"字符串
            
        Returns:
            格式化后的路径字符串
        """
        if not path:
            return "未找到路径"
        
        lines = []
        for item in path:
            if isinstance(item, Station):
                # 格式化站点：线路名，站名
                lines.append(f"{item.line_name}，{item.station_name}")
            elif item == "换乘":
                # 换乘标记
                lines.append("换乘")
        
        return '\n'.join(lines)
    
    @staticmethod
    def format_path_summary(
        path: List[Union[Station, str]],
        transfer_count: int,
        station_count: int
    ) -> str:
        """格式化路径摘要信息
        
        Args:
            path: 路径列表
            transfer_count: 换乘次数
            station_count: 站点数
            
        Returns:
            包含路径和摘要信息的字符串
        """
        path_str = Formatter.format_path(path)
        summary = f"\n\n路径摘要：\n经过站点数：{station_count}\n换乘次数：{transfer_count}"
        return path_str + summary
    
    @staticmethod
    def format_error(error_message: str) -> str:
        """格式化错误消息
        
        Args:
            error_message: 错误消息
            
        Returns:
            格式化后的错误消息
        """
        return f"错误: {error_message}"

    @staticmethod
    def format_info(message: str) -> str:
        """格式化提示消息"""
        return f"提示: {message}"
    
    @staticmethod
    def format_welcome() -> str:
        """返回欢迎信息
        
        Returns:
            欢迎信息字符串
        """
        return """
========================================
    地铁换乘路径规划系统
========================================
请输入起点和终点（格式：起始线路，起始站名-目标线路，目标站名）
示例：18号线，复旦大学-10号线，交通大学
输入 'q' 或 'quit' 退出程序
========================================
"""
