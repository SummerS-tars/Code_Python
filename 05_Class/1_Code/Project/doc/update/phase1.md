# 地铁换乘系统 v2.0 升级设计文档

## 阶段一：核心算法重构与基础优化

**目标**：将路径搜索算法从 DFS 升级为 BFS（广度优先搜索），确保找到的是“经过站点最少”的路径，并增强系统的健壮性。

### 1. 改进点分析

* **PathFinder**: 当前 DFS 无法保证最短路径，且容易陷入深层递归。改为 BFS 可以保证找到无权图的最短路径。
* **Parser**: 当前输入格式过于严格，需放宽限制，允许用户只输入站名。
* **DataLoader**: 增加对坏数据的容错处理。

### 2. 涉及文件

* `src/services/path_finder.py`
* `src/utils/parser.py`
* `src/services/data_loader.py`

### 3. 给 IDE Agent 的指令提示词 (Phase 1)

> **复制以下内容给 Agent：**
> 我们的任务是重构地铁线路规划系统的核心算法。请按以下步骤修改代码：
> 1. **修改 `src/services/path_finder.py**`：
> * 引入 `collections.deque`。
> * 重写 `find_path` 方法，移除递归 DFS，改为迭代式的 BFS（广度优先搜索）。
> * 在 BFS 中，使用一个 `came_from` 字典记录路径的前驱节点，以便找到终点后回溯完整路径。
> * 确保在回溯路径时，如果前后两站线路不同，自动插入 "换乘" 标记。
> 
> 
> 2. **修改 `src/utils/parser.py**`：
> * 修改 `parse_input` 和 `_parse_station_info`。
> * 放宽输入限制：如果用户没有输入线路名（例如输入 "复旦大学" 而不是 "18号线，复旦大学"），暂不报错，而是将线路名设为 `None`。我们将在后续逻辑中处理查找问题。
> 
> 
> 3. **修改 `src/services/data_loader.py**`：
> * 在 `_parse_transfer_ids` 方法中增加 `try-except` 块，如果某个 ID 解析失败，跳过该 ID 而不是让整个程序崩溃。
> 
> 
> 
> 
> 完成后，请运行 `src/main.py` 的测试用例，确保依然能输出结果，且路径应该比之前的更短。

---
