"""地铁网络图类

该模块定义了整个地铁网络的数据结构，负责管理所有线路和站点，
以及建立站点之间的换乘关系。
"""

from typing import Dict, List, Optional
from models.station import Station
from models.line import Line


class MetroNetwork:
    """地铁网络图类
    
    用于表示整个地铁网络，提供站点和线路的索引和查询功能。
    
    Attributes:
        stations_by_id: 按站点ID索引的字典
        lines: 按线路名称索引的字典
        stations_by_name: 按站点名称索引的字典（一个站名可能对应多个站点）
    """
    
    def __init__(self):
        """初始化地铁网络实例"""
        self.stations_by_id: Dict[int, Station] = {}
        self.lines: Dict[str, Line] = {}
        self.stations_by_name: Dict[str, List[Station]] = {}
    
    def add_line(self, line_name: str) -> Line:
        """添加或获取线路
        
        如果线路不存在则创建新线路，否则返回已存在的线路。
        
        Args:
            line_name: 线路名称
            
        Returns:
            线路对象
        """
        if line_name not in self.lines:
            self.lines[line_name] = Line(line_name)
        return self.lines[line_name]
    
    def add_station(self, station: Station) -> None:
        """添加站点到网络
        
        将站点添加到各个索引中，并自动添加到对应的线路。
        
        Args:
            station: 站点对象
        """
        # 添加到ID索引
        self.stations_by_id[station.id] = station
        
        # 添加到线路
        line = self.add_line(station.line_name)
        line.add_station(station)
        
        # 添加到站名索引
        if station.station_name not in self.stations_by_name:
            self.stations_by_name[station.station_name] = []
        self.stations_by_name[station.station_name].append(station)
    
    def get_station_by_id(self, station_id: int) -> Optional[Station]:
        """根据站点ID查找站点
        
        Args:
            station_id: 站点ID
            
        Returns:
            找到的站点对象，如果不存在则返回None
        """
        return self.stations_by_id.get(station_id)
    
    def build_transfer_links(self, transfer_data: Dict[int, List[int]]) -> None:
        """建立换乘站点之间的关联
        
        Args:
            transfer_data: 换乘数据字典，键为站点ID，值为可换乘的站点ID列表
        """
        for station_id, transfer_ids in transfer_data.items():
            station = self.get_station_by_id(station_id)
            if station:
                for transfer_id in transfer_ids:
                    transfer_station = self.get_station_by_id(transfer_id)
                    if transfer_station:
                        station.add_transfer_station(transfer_station)
    
    def find_station(self, line_name: str, station_name: str) -> Optional[Station]:
        """查找指定线路的站点
        
        Args:
            line_name: 线路名称
            station_name: 站点名称
            
        Returns:
            找到的站点对象，如果不存在则返回None
        """
        line = self.lines.get(line_name)
        if line:
            return line.get_station(station_name)
        return None
    
    def get_all_lines(self) -> List[str]:
        """获取所有线路名称
        
        Returns:
            线路名称列表
        """
        return list(self.lines.keys())
    
    def get_station_count(self) -> int:
        """获取网络中的站点总数
        
        Returns:
            站点总数
        """
        return len(self.stations_by_id)
    
    def __str__(self) -> str:
        """返回网络的字符串表示
        
        Returns:
            包含线路数和站点数的字符串
        """
        return f"MetroNetwork(lines={len(self.lines)}, stations={len(self.stations_by_id)})"
    
    def __repr__(self) -> str:
        """返回网络的详细表示
        
        Returns:
            包含所有线路名称的字符串
        """
        return f"MetroNetwork(lines={list(self.lines.keys())})"
