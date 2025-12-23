"""地铁站点实体类

该模块定义了地铁站点的数据结构，包括站点基本信息、
同线路前后站点关系以及换乘站点关系。
"""

from typing import Optional, List


class Station:
    """地铁站点实体类
    
    用于表示地铁网络中的单个站点，包含站点的基本属性和邻接关系。
    
    Attributes:
        id: 站点唯一标识符
        line_name: 所属线路名称
        station_name: 站点名称
        prev_station: 同线路的前驱站点
        next_station: 同线路的后继站点
        transfer_stations: 可换乘的其他线路站点列表
    """
    
    def __init__(self, station_id: int, line_name: str, station_name: str):
        """初始化站点实例
        
        Args:
            station_id: 站点ID
            line_name: 线路名称
            station_name: 站点名称
        """
        self.id: int = station_id
        self.line_name: str = line_name
        self.station_name: str = station_name
        self.prev_station: Optional[Station] = None
        self.next_station: Optional[Station] = None
        self.transfer_stations: List[Station] = []
    
    def add_transfer_station(self, station: 'Station') -> None:
        """添加换乘站点
        
        Args:
            station: 可换乘的其他线路站点
        """
        if station not in self.transfer_stations:
            self.transfer_stations.append(station)
    
    def __str__(self) -> str:
        """返回站点的字符串表示
        
        Returns:
            格式为"线路名，站名"的字符串
        """
        return f"{self.line_name}，{self.station_name}"
    
    def __repr__(self) -> str:
        """返回站点的详细表示
        
        Returns:
            包含站点ID和名称的字符串
        """
        return f"Station(id={self.id}, line={self.line_name}, name={self.station_name})"
    
    def __eq__(self, other: object) -> bool:
        """判断两个站点是否相等
        
        Args:
            other: 另一个对象
            
        Returns:
            如果是同一个站点（ID相同）则返回True
        """
        if not isinstance(other, Station):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        """返回站点的哈希值
        
        Returns:
            基于站点ID的哈希值
        """
        return hash(self.id)
