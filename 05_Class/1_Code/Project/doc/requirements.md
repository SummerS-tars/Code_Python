# 地铁换乘路径规划系统 - 技术需求文档

## 1. 项目概述

### 1.1 项目描述
开发一个基于Python的地铁换乘路径智能规划系统，通过读取CSV格式的地铁线路数据，采用递归搜索算法为用户提供从起始站到目标站的最优换乘方案。

### 1.2 技术栈
- **开发语言**：Python 3.11+
- **数据格式**：CSV
- **核心算法**：递归深度优先搜索（DFS）

### 1.3 参考文档
- 原始需求：[地铁换乘智能推荐系统.md](地铁换乘智能推荐系统.md)
- 测试数据：[线路.csv](线路.csv)

---

## 2. 项目架构

### 2.1 目录结构
```
Project/
├── doc/                          # 文档目录
│   ├── requirements.md           # 本需求文档
│   ├── 地铁换乘智能推荐系统.md      # 原始需求
│   └── 线路.csv                   # 示例数据
├── src/                          # 源代码目录
│   ├── main.py                   # 程序入口
│   ├── models/                   # 数据模型
│   │   ├── __init__.py
│   │   ├── station.py            # 站点类
│   │   ├── line.py               # 线路类
│   │   └── network.py            # 地铁网络图
│   ├── services/                 # 业务逻辑
│   │   ├── __init__.py
│   │   ├── data_loader.py        # 数据加载器
│   │   └── path_finder.py        # 路径查找器
│   ├── utils/                    # 工具函数
│   │   ├── __init__.py
│   │   ├── parser.py             # 输入解析
│   │   └── formatter.py          # 输出格式化
│   └── config.py                 # 配置文件
├── tests/                        # 测试目录
│   ├── __init__.py
│   ├── test_station.py
│   ├── test_line.py
│   ├── test_network.py
│   ├── test_data_loader.py
│   ├── test_path_finder.py
│   └── test_integration.py       # 集成测试
└── requirements.txt              # 依赖清单
```

### 2.2 模块职责划分

#### 2.2.1 数据模型层（models/）
- **Station**：站点实体，封装站点属性和邻接关系
- **Line**：线路实体，管理线路上的站点序列
- **Network**：地铁网络图，维护全局站点和线路关系

#### 2.2.2 业务逻辑层（services/）
- **DataLoader**：负责读取和解析CSV数据，构建网络图
- **PathFinder**：实现递归路径搜索算法，生成换乘方案

#### 2.2.3 工具层（utils/）
- **Parser**：解析用户输入，提取起点和终点信息
- **Formatter**：格式化路径输出，生成符合要求的结果

---

## 3. 功能需求

### 3.1 核心功能

#### 3.1.1 数据加载
- **输入**：CSV格式地铁线路数据
- **字段定义**：
  - `站点ID`：整数类型，唯一标识符，递增排序
  - `线路名`：字符串类型，地铁线路名称（如"10号线"）
  - `站名`：字符串类型，车站名称
  - `可换乘站点ID`：字符串类型，多个换乘站用"/"分隔
- **处理要求**：
  - 按序读取同线路站点，自动建立前后邻接关系
  - 解析换乘站点ID，建立跨线路连接
  - 验证数据完整性和一致性

#### 3.1.2 路径搜索
- **算法要求**：递归深度优先搜索（DFS）
- **搜索策略**：
  - 从起始站点开始，向前驱和后继站点扩展
  - 遇到换乘站时，可跳转至关联线路继续搜索
  - 维护访问标记集合，避免重复访问和死循环
  - 找到目标站点后返回完整路径
- **终止条件**：
  - 成功：找到目标站点
  - 失败：所有可达站点均已访问，无可行路径

#### 3.1.3 用户交互
- **输入格式**：`起始线路，起始站名-目标线路，目标站名`
  - 示例：`18号线，复旦大学-10号线，交通大学`
- **输出格式**：按访问顺序输出路径，换乘处标注"换乘"
  ```
  18号线，复旦大学
  18号线，国权路
  换乘
  10号线，国权路
  10号线，交通大学
  ```
- **异常处理**：
  - 输入格式错误
  - 站点或线路不存在
  - 无可达路径

### 3.2 数据示例

提供的测试数据（线路.csv）：

| 站点ID | 线路名 | 站名          | 可换乘站点ID |
| ------ | ------ | ------------- | ------------ |
| 1      | 18号线 | 上海财经大学  |              |
| 2      | 18号线 | 复旦大学      |              |
| 3      | 18号线 | 国权路        | 5            |
| 4      | 10号线 | 同济大学      |              |
| 5      | 10号线 | 国权路        | 3            |
| 6      | 10号线 | 交通大学      | 9            |
| 7      | 10号线 | 虹桥火车站    | 12           |
| 8      | 10号线 | 虹桥2号航站楼 | 13           |
| 9      | 11号线 | 交通大学      | 6            |
| 10     | 11号线 | 迪士尼        |              |
| 11     | 1号线  | 人民广场      | 14/17        |
| 12     | 2号线  | 虹桥火车站    | 7            |
| 13     | 2号线  | 虹桥2号航站楼 | 8            |
| 14     | 2号线  | 人民广场      | 11/17        |
| 15     | 2号线  | 浦东国际机场  |              |
| 16     | 8号线  | 东方体育中心  |              |
| 17     | 8号线  | 人民广场      | 11/14        |
| 18     | 8号线  | 虹口足球场    |              |

### 3.3 测试用例

#### 用例1：单次换乘
- **输入**：`18号线，复旦大学-10号线，交通大学`
- **预期输出**：
  ```
  18号线，复旦大学
  18号线，国权路
  换乘
  10号线，国权路
  10号线，交通大学
  ```

#### 用例2：多次换乘
- **输入**：`18号线，上海财经大学-8号线，东方体育中心`
- **预期输出**：
  ```
  18号线，上海财经大学
  18号线，复旦大学
  18号线，国权路
  换乘
  10号线，国权路
  10号线，交通大学
  10号线，虹桥火车站
  10号线，虹桥2号航站楼
  换乘
  2号线，虹桥2号航站楼
  2号线，人民广场
  换乘
  8号线，人民广场
  8号线，东方体育中心
  ```

---

## 4. 数据结构设计

### 4.1 Station（站点类）

```python
class Station:
    """地铁站点实体类"""
    
    def __init__(self, station_id: int, line_name: str, station_name: str):
        self.id: int = station_id                    # 站点ID
        self.line_name: str = line_name              # 所属线路
        self.station_name: str = station_name        # 站点名称
        self.prev_station: Optional[Station] = None  # 前驱站点
        self.next_station: Optional[Station] = None  # 后继站点
        self.transfer_stations: List[Station] = []   # 换乘站点列表
```

**关键属性说明**：
- `prev_station` 和 `next_station`：构成双向链表，表示同线路的前后关系
- `transfer_stations`：存储可换乘的其他线路站点引用

### 4.2 Line（线路类）

```python
class Line:
    """地铁线路类"""
    
    def __init__(self, line_name: str):
        self.line_name: str = line_name              # 线路名称
        self.stations: List[Station] = []            # 站点列表（有序）
    
    def add_station(self, station: Station) -> None:
        """按顺序添加站点"""
        pass
    
    def get_station(self, station_name: str) -> Optional[Station]:
        """根据站名查找站点"""
        pass
```

### 4.3 MetroNetwork（地铁网络类）

```python
class MetroNetwork:
    """地铁网络图"""
    
    def __init__(self):
        self.stations_by_id: Dict[int, Station] = {}      # ID索引
        self.lines: Dict[str, Line] = {}                   # 线路索引
        self.stations_by_name: Dict[str, List[Station]] = {}  # 站名索引（支持同名站）
    
    def add_station(self, station: Station) -> None:
        """添加站点到网络"""
        pass
    
    def build_transfer_links(self, transfer_data: Dict[int, List[int]]) -> None:
        """建立换乘关联"""
        pass
    
    def find_station(self, line_name: str, station_name: str) -> Optional[Station]:
        """查找指定线路的站点"""
        pass
```

---

## 5. 算法设计

### 5.1 递归路径搜索伪代码

```
function find_path(current_station, target_station, visited, path):
    # 标记当前站点为已访问
    visited.add(current_station)
    path.append(current_station)
    
    # 终止条件：到达目标
    if current_station == target_station:
        return True
    
    # 递归探索相邻站点（同线路前后站）
    for neighbor in [current_station.prev, current_station.next]:
        if neighbor not in visited:
            if find_path(neighbor, target_station, visited, path):
                return True
    
    # 递归探索换乘站点（跨线路）
    for transfer_station in current_station.transfer_stations:
        if transfer_station not in visited:
            path.append("换乘")
            if find_path(transfer_station, target_station, visited, path):
                return True
            path.pop()  # 回溯
    
    # 回溯：当前路径不通
    path.pop()
    return False
```

### 5.2 算法复杂度分析
- **时间复杂度**：O(V + E)，V为站点数，E为边数（邻接+换乘）
- **空间复杂度**：O(V)，用于visited集合和递归栈

---

## 6. 编码规范

### 6.1 Python代码风格
遵循 **PEP 8** 规范：
- 使用4个空格缩进（禁用Tab）
- 类名采用 `PascalCase`
- 函数和变量名采用 `snake_case`
- 常量采用 `UPPER_SNAKE_CASE`
- 每行代码不超过100字符

### 6.2 类型注解
强制使用类型提示（Type Hints）：
```python
from typing import List, Optional, Dict

def find_station(line_name: str, station_name: str) -> Optional[Station]:
    pass
```

### 6.3 文档字符串
使用Google风格的docstring：
```python
def find_path(start: Station, end: Station) -> List[Station]:
    """查找两个站点之间的路径
    
    Args:
        start: 起始站点
        end: 目标站点
    
    Returns:
        包含完整路径的站点列表，若无路径则返回空列表
    
    Raises:
        ValueError: 起点或终点为None时抛出
    """
    pass
```

### 6.4 异常处理
- 使用具体的异常类型（避免裸except）
- 自定义业务异常类：
  ```python
  class StationNotFoundError(Exception):
      """站点不存在异常"""
      pass
  
  class InvalidInputError(Exception):
      """输入格式错误异常"""
      pass
  ```

### 6.5 代码组织
- 每个模块顶部添加模块说明
- 导入语句按标准库、第三方库、本地模块分组
- 每个类和函数前留一个空行

---

## 7. 测试要求

### 7.1 单元测试

#### 7.1.1 测试框架
使用 `pytest` 进行单元测试

#### 7.1.2 测试覆盖率
- **最低要求**：80%代码覆盖率
- **推荐目标**：90%以上
- 使用 `pytest-cov` 生成覆盖率报告

#### 7.1.3 测试用例设计

**Station类测试（test_station.py）**：
- 测试站点创建和属性访问
- 测试前后站点关联
- 测试换乘站点添加

**Line类测试（test_line.py）**：
- 测试站点添加和顺序维护
- 测试站点查询功能
- 测试边界情况（空线路、单站线路）

**MetroNetwork类测试（test_network.py）**：
- 测试网络构建
- 测试站点索引查询
- 测试换乘关系建立

**DataLoader测试（test_data_loader.py）**：
- 测试CSV文件读取
- 测试数据解析正确性
- 测试异常数据处理（格式错误、缺失字段）

**PathFinder测试（test_path_finder.py）**：
- 测试单线路路径查找
- 测试单次换乘场景
- 测试多次换乘场景
- 测试无路径情况
- 测试起点即终点
- 测试环路处理

### 7.2 集成测试

**test_integration.py**：
- 端到端测试：从读取CSV到输出结果的完整流程
- 使用示例数据验证所有测试用例
- 测试用户输入解析和输出格式化

### 7.3 测试命令

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=src --cov-report=html

# 运行特定测试文件
pytest tests/test_path_finder.py

# 运行特定测试用例
pytest tests/test_path_finder.py::test_single_transfer -v
```

### 7.4 测试数据
- 在 `tests/` 目录下创建 `fixtures/` 子目录存放测试数据
- 提供最小化测试CSV文件
- 使用pytest的fixture管理测试数据

---

## 8. 开发流程

### 8.1 开发阶段

1. **阶段1：数据模型实现**（优先级：高）
   - 实现Station、Line、MetroNetwork类
   - 编写对应单元测试
   - 确保测试通过

2. **阶段2：数据加载器**（优先级：高）
   - 实现CSV读取和解析
   - 构建网络图
   - 编写单元测试

3. **阶段3：路径查找器**（优先级：高）
   - 实现递归搜索算法
   - 处理换乘逻辑
   - 编写单元测试

4. **阶段4：用户接口**（优先级：中）
   - 实现输入解析
   - 实现输出格式化
   - 集成main.py入口

5. **阶段5：完善优化**（优先级：低）
   - 异常处理增强
   - 性能优化
   - 代码重构

### 8.2 质量保证
- 每个阶段完成后进行代码审查
- 持续运行测试确保回归
- 使用 `black` 进行代码格式化
- 使用 `pylint` 或 `flake8` 进行静态检查

---

## 9. 依赖清单

### 9.1 核心依赖
```txt
# requirements.txt
# Python标准库足以完成核心功能，无需外部依赖
```

### 9.2 开发依赖
```txt
# requirements-dev.txt
pytest>=7.4.0           # 测试框架
pytest-cov>=4.1.0       # 覆盖率工具
black>=23.0.0           # 代码格式化
flake8>=6.0.0           # 代码检查
mypy>=1.5.0             # 类型检查
```

---

## 10. 验收标准

### 10.1 功能验收
- [ ] 能够正确读取并解析CSV数据
- [ ] 能够处理示例文档中的所有测试用例
- [ ] 输出格式完全符合要求
- [ ] 能够正确处理无路径情况
- [ ] 输入验证和异常处理完善

### 10.2 代码质量
- [ ] 代码覆盖率达到80%以上
- [ ] 所有单元测试通过
- [ ] 集成测试通过
- [ ] 符合PEP 8规范（flake8检查通过）
- [ ] 类型检查通过（mypy检查通过）
- [ ] 代码包含完整的文档字符串

### 10.3 性能要求
- [ ] 在示例数据上，路径查找耗时 < 100ms
- [ ] 支持至少100个站点规模的网络

---

## 11. 后续扩展（可选）

### 11.1 功能增强
- 支持多条路径查询，选择最短路径
- 支持最少换乘、最少站点等不同优化目标
- 支持时间预估和票价计算
- 提供GUI界面

### 11.2 技术优化
- 使用Dijkstra或A*算法优化路径搜索
- 支持并发查询
- 数据持久化（数据库）
- RESTful API接口
