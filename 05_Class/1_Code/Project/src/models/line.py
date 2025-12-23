"""地铁线路类

该模块定义了地铁线路的数据结构，负责管理线路上的站点序列。
"""

from typing import List, Optional
from models.station import Station


class Line:
    """地铁线路类
    
    用于表示一条地铁线路，管理该线路上的所有站点。
    
    Attributes:
        line_name: 线路名称
        stations: 线路上的站点列表（按顺序排列）
    """
    
    def __init__(self, line_name: str):
        """初始化线路实例
        
        Args:
            line_name: 线路名称
        """
        self.line_name: str = line_name
        self.stations: List[Station] = []
    
    def add_station(self, station: Station) -> None:
        """按顺序添加站点到线路
        
        自动建立与前一个站点的前后关系。
        
        Args:
            station: 要添加的站点
        """
        if self.stations:
            # 建立双向链接
            last_station = self.stations[-1]
            last_station.next_station = station
            station.prev_station = last_station
        
        self.stations.append(station)
    
    def get_station(self, station_name: str) -> Optional[Station]:
        """根据站名查找站点
        
        Args:
            station_name: 站点名称
            
        Returns:
            找到的站点对象，如果不存在则返回None
        """
        for station in self.stations:
            if station.station_name == station_name:
                return station
        return None
    
    def get_station_count(self) -> int:
        """获取线路的站点数量
        
        Returns:
            站点数量
        """
        return len(self.stations)
    
    def __str__(self) -> str:
        """返回线路的字符串表示
        
        Returns:
            线路名称
        """
        return self.line_name
    
    def __repr__(self) -> str:
        """返回线路的详细表示
        
        Returns:
            包含线路名称和站点数量的字符串
        """
        return f"Line(name={self.line_name}, stations={len(self.stations)})"
