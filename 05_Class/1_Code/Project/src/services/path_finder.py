"""路径查找器

该模块实现了基于递归深度优先搜索的路径查找算法。
"""

from typing import List, Set, Optional, Union
from models.station import Station


class PathNotFoundError(Exception):
    """路径未找到异常"""
    pass


class PathFinder:
    """路径查找器类
    
    使用递归深度优先搜索（DFS）算法查找两个站点之间的路径。
    """
    
    def __init__(self):
        """初始化路径查找器"""
        pass
    
    def find_path(self, start: Station, end: Station) -> List[Union[Station, str]]:
        """查找从起点到终点的路径
        
        Args:
            start: 起始站点
            end: 目标站点
            
        Returns:
            路径列表，包含Station对象和"换乘"标记
            
        Raises:
            ValueError: 起点或终点为None时抛出
            PathNotFoundError: 无可达路径时抛出
        """
        if start is None or end is None:
            raise ValueError("起点和终点不能为None")
        
        # 如果起点就是终点
        if start == end:
            return [start]
        
        # 初始化访问集合和路径
        visited: Set[Station] = set()
        path: List[Union[Station, str]] = []
        
        # 执行递归搜索
        if self._dfs(start, end, visited, path):
            return path
        else:
            raise PathNotFoundError(f"未找到从 {start} 到 {end} 的路径")
    
    def _dfs(
        self,
        current: Station,
        target: Station,
        visited: Set[Station],
        path: List[Union[Station, str]]
    ) -> bool:
        """递归深度优先搜索
        
        Args:
            current: 当前站点
            target: 目标站点
            visited: 已访问站点集合
            path: 当前路径
            
        Returns:
            如果找到路径返回True，否则返回False
        """
        # 标记当前站点为已访问
        visited.add(current)
        path.append(current)
        
        # 终止条件：到达目标
        if current == target:
            return True
        
        # 1. 探索同线路的前驱和后继站点
        neighbors = self._get_line_neighbors(current)
        for neighbor in neighbors:
            if neighbor not in visited:
                if self._dfs(neighbor, target, visited, path):
                    return True
        
        # 2. 探索换乘站点
        for transfer_station in current.transfer_stations:
            if transfer_station not in visited:
                # 添加换乘标记
                path.append("换乘")
                
                if self._dfs(transfer_station, target, visited, path):
                    return True
                
                # 回溯：移除换乘标记
                path.pop()
        
        # 回溯：当前路径不通，移除当前站点
        path.pop()
        return False
    
    def _get_line_neighbors(self, station: Station) -> List[Station]:
        """获取同线路的相邻站点
        
        Args:
            station: 当前站点
            
        Returns:
            相邻站点列表（前驱和后继）
        """
        neighbors = []
        if station.prev_station:
            neighbors.append(station.prev_station)
        if station.next_station:
            neighbors.append(station.next_station)
        return neighbors
    
    def calculate_transfer_count(self, path: List[Union[Station, str]]) -> int:
        """计算路径中的换乘次数
        
        Args:
            path: 路径列表
            
        Returns:
            换乘次数
        """
        return sum(1 for item in path if item == "换乘")
    
    def calculate_station_count(self, path: List[Union[Station, str]]) -> int:
        """计算路径中经过的站点数（不含换乘标记）
        
        Args:
            path: 路径列表
            
        Returns:
            站点数
        """
        return sum(1 for item in path if isinstance(item, Station))
