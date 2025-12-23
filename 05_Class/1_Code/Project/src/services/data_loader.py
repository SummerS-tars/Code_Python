"""数据加载器

该模块负责从CSV文件读取地铁线路数据，并构建地铁网络图。
"""

import csv
from typing import Dict, List
from models.station import Station
from models.network import MetroNetwork


class DataLoadError(Exception):
    """数据加载异常"""
    pass


class DataLoader:
    """数据加载器类
    
    负责读取CSV格式的地铁线路数据，解析并构建完整的地铁网络图。
    
    CSV文件格式：
        站点ID,线路名,站名,可换乘站点ID
    """
    
    def __init__(self):
        """初始化数据加载器"""
        self.network = MetroNetwork()
        self.transfer_data: Dict[int, List[int]] = {}
    
    def load_from_csv(self, file_path: str) -> MetroNetwork:
        """从CSV文件加载数据
        
        Args:
            file_path: CSV文件路径
            
        Returns:
            构建完成的地铁网络对象
            
        Raises:
            DataLoadError: 文件不存在或格式错误时抛出
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # 验证CSV文件头
                required_fields = {'站点ID', '线路名', '站名', '可换乘站点ID'}
                if not required_fields.issubset(set(reader.fieldnames or [])):
                    raise DataLoadError(f"CSV文件缺少必要字段，需要: {required_fields}")
                
                # 第一遍：创建所有站点
                for row in reader:
                    self._process_station_row(row)
                
                # 第二遍：建立换乘关系
                self.network.build_transfer_links(self.transfer_data)
                
                return self.network
                
        except FileNotFoundError:
            raise DataLoadError(f"文件未找到: {file_path}")
        except Exception as e:
            raise DataLoadError(f"加载数据时出错: {str(e)}")
    
    def _process_station_row(self, row: Dict[str, str]) -> None:
        """处理CSV文件中的一行数据
        
        Args:
            row: CSV行数据字典
            
        Raises:
            DataLoadError: 数据格式错误时抛出
        """
        try:
            # 解析基本信息
            station_id = int(row['站点ID'].strip())
            line_name = row['线路名'].strip()
            station_name = row['站名'].strip()
            transfer_ids_str = row['可换乘站点ID'].strip()
            
            # 创建站点
            station = Station(station_id, line_name, station_name)
            self.network.add_station(station)
            
            # 解析换乘信息
            if transfer_ids_str:
                transfer_ids = self._parse_transfer_ids(transfer_ids_str)
                self.transfer_data[station_id] = transfer_ids
                
        except ValueError as e:
            raise DataLoadError(f"数据格式错误: {str(e)}")
        except KeyError as e:
            raise DataLoadError(f"缺少必要字段: {str(e)}")
    
    def _parse_transfer_ids(self, transfer_ids_str: str) -> List[int]:
        """解析换乘站点ID字符串
        
        Args:
            transfer_ids_str: 换乘站点ID字符串，多个ID用"/"分隔
            
        Returns:
            换乘站点ID列表
            
        Raises:
            ValueError: ID格式错误时抛出
        """
        if not transfer_ids_str:
            return []
        
        ids: List[int] = []
        for id_str in transfer_ids_str.split('/'):
            token = id_str.strip()
            if not token:
                continue
            try:
                ids.append(int(token))
            except ValueError:
                # 跳过解析失败的ID，避免中断加载
                continue
        return ids
    
    def get_network(self) -> MetroNetwork:
        """获取构建的地铁网络
        
        Returns:
            地铁网络对象
        """
        return self.network
