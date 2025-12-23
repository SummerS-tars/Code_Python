"""路径查找器

使用可配置权重的最短路径搜索（Dijkstra），支持“最少站点”和“最少换乘”策略，并在跨线路时插入“换乘”标记。
"""

import heapq
from typing import Dict, List, Optional, Tuple, Union
from models.station import Station


class PathNotFoundError(Exception):
    """路径未找到异常"""
    pass


class PathFinder:
    """路径查找器类
    
    使用 Dijkstra 算法查找两个站点之间的路径，支持不同权重策略。
    """
    
    def __init__(self):
        """初始化路径查找器"""
        pass
    
    def find_path(self, start: Station, end: Station, strategy: str = "min_station") -> List[Union[Station, str]]:
        """查找从起点到终点的路径
        
        Args:
            start: 起始站点
            end: 目标站点
            strategy: 路径策略，"min_station"（默认，最少站点）或 "min_transfer"（最少换乘）
            
        Returns:
            路径列表，包含 Station 对象和 "换乘" 标记
            
        Raises:
            ValueError: 起点/终点为 None 或策略非法时抛出
            PathNotFoundError: 无可达路径时抛出
        """
        if start is None or end is None:
            raise ValueError("起点和终点不能为None")
        if strategy not in {"min_station", "min_transfer"}:
            raise ValueError(f"不支持的策略: {strategy}")
        if start == end:
            return [start]
        
        # Dijkstra
        dist: Dict[Station, float] = {start: 0.0}
        came_from: Dict[Station, Optional[Station]] = {start: None}
        heap: List[Tuple[float, int, Station]] = []
        counter = 0
        heapq.heappush(heap, (0.0, counter, start))
        visited: set[Station] = set()
        
        found = False
        while heap:
            cost, _, current = heapq.heappop(heap)
            if current in visited:
                continue
            visited.add(current)
            if current == end:
                found = True
                break
            
            for neighbor, weight in self._get_neighbors_with_weight(current, strategy):
                if neighbor in visited:
                    continue
                new_cost = cost + weight
                if new_cost < dist.get(neighbor, float('inf')):
                    dist[neighbor] = new_cost
                    came_from[neighbor] = current
                    counter += 1
                    heapq.heappush(heap, (new_cost, counter, neighbor))
        
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
    
    def _get_neighbors_with_weight(self, station: Station, strategy: str) -> List[Tuple[Station, float]]:
        """获取邻居及权重"""
        neighbors: List[Tuple[Station, float]] = []
        # 同线路相邻站，权重始终为1
        if station.prev_station:
            neighbors.append((station.prev_station, 1.0))
        if station.next_station:
            neighbors.append((station.next_station, 1.0))
        # 换乘站
        for transfer in station.transfer_stations:
            weight = self._calc_transfer_weight(station, transfer, strategy)
            neighbors.append((transfer, weight))
        return neighbors

    def _extract_main_line(self, line_name: str) -> str:
        """提取主线名称（去掉支线后缀）"""
        return line_name.split("(")[0].strip()

    def _is_same_family(self, line_a: str, line_b: str) -> bool:
        """判定是否属于同一线路族（主线/支线/包含关系）"""
        if line_a == line_b:
            return True
        if line_a in line_b or line_b in line_a:
            return True
        return self._extract_main_line(line_a) == self._extract_main_line(line_b)

    def _calc_transfer_weight(self, current: Station, neighbor: Station, strategy: str) -> float:
        """计算换乘权重，支持同线/同系零代价换乘"""
        base_weight = 1.0 if strategy == "min_station" else 1000.0

        # 同名换乘（含环线闭合、主线-支线换乘）
        if current.station_name == neighbor.station_name:
            if current.line_name == neighbor.line_name:
                return 0.1
            if self._is_same_family(current.line_name, neighbor.line_name):
                return 0.1

        return base_weight
    
    def calculate_transfer_count(self, path: List[Union[Station, str]]) -> int:
        """计算路径中的换乘次数"""
        return sum(1 for item in path if item == "换乘")
    
    def calculate_station_count(self, path: List[Union[Station, str]]) -> int:
        """计算路径中经过的站点数（不含换乘标记）"""
        return sum(1 for item in path if isinstance(item, Station))
