"""路径查找器

使用广度优先搜索（BFS）查找最少经过站点的路径，并在跨线路时插入“换乘”标记。
"""

from collections import deque
from typing import Deque, Dict, List, Optional, Union
from models.station import Station


class PathNotFoundError(Exception):
    """路径未找到异常"""
    pass


class PathFinder:
    """路径查找器类
    
    使用迭代式 BFS 查找两个站点之间的最短（按站点数）路径。
    """
    
    def __init__(self):
        """初始化路径查找器"""
        pass
    
    def find_path(self, start: Station, end: Station) -> List[Union[Station, str]]:
        """查找从起点到终点的路径（最少站点）
        
        Args:
            start: 起始站点
            end: 目标站点
            
        Returns:
            路径列表，包含 Station 对象和 "换乘" 标记
            
        Raises:
            ValueError: 起点或终点为 None 时抛出
            PathNotFoundError: 无可达路径时抛出
        """
        if start is None or end is None:
            raise ValueError("起点和终点不能为None")
        
        if start == end:
            return [start]
        
        # BFS 队列与前驱记录
        queue: Deque[Station] = deque([start])
        visited = {start}
        came_from: Dict[Station, Optional[Station]] = {start: None}
        
        found = False
        while queue:
            current = queue.popleft()
            if current == end:
                found = True
                break
            
            for neighbor in self._get_neighbors(current):
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
        
        if not found:
            raise PathNotFoundError(f"未找到从 {start} 到 {end} 的路径")
        
        # 回溯路径（仅站点序列）
        station_path: List[Station] = []
        node = end
        while node is not None:
            station_path.append(node)
            node = came_from[node]
        station_path.reverse()
        
        # 插入换乘标记：相邻站点线路名变化时加入
        path_with_transfer: List[Union[Station, str]] = []
        for i, station in enumerate(station_path):
            if i > 0:
                prev_station = station_path[i - 1]
                if prev_station.line_name != station.line_name:
                    path_with_transfer.append("换乘")
            path_with_transfer.append(station)
        
        return path_with_transfer
    
    def _get_neighbors(self, station: Station) -> List[Station]:
        """获取当前站点的所有可达邻居（同线前后 + 换乘）"""
        neighbors: List[Station] = []
        if station.prev_station:
            neighbors.append(station.prev_station)
        if station.next_station:
            neighbors.append(station.next_station)
        neighbors.extend(station.transfer_stations)
        return neighbors
    
    def calculate_transfer_count(self, path: List[Union[Station, str]]) -> int:
        """计算路径中的换乘次数"""
        return sum(1 for item in path if item == "换乘")
    
    def calculate_station_count(self, path: List[Union[Station, str]]) -> int:
        """计算路径中经过的站点数（不含换乘标记）"""
        return sum(1 for item in path if isinstance(item, Station))
