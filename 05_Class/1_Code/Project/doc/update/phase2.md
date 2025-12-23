## 阶段二：多策略路径规划（最短路径 vs 最少换乘）

**目标**：引入 Dijkstra 算法，通过调整“权重”来实现两种不同的导航策略。

### 1. 设计逻辑

* **策略模式**：允许用户选择 "shortest" (最短路径/最少站点) 或 "min_transfer" (最少换乘)。
* **权重设计**：
* **同线路相邻站**：权重 = 1
* **换乘操作**：
* 策略为 "shortest" 时：权重 = 1 (视作普通一站) 或 0
* 策略为 "min_transfer" 时：权重 = 1000 (给予极高的惩罚值)




* **算法**：使用 `heapq` 实现 Dijkstra 算法。

### 2. 涉及文件

* `src/services/path_finder.py`
* `src/main.py` (增加策略参数)

### 3. 给 IDE Agent 的指令提示词 (Phase 2)

> **复制以下内容给 Agent：**
> 下一步任务是实现“最少换乘”优先的策略。请按以下步骤操作：
> 1. **修改 `src/services/path_finder.py**`：
> * 引入 `heapq` 模块。
> * 将 `PathFinder` 类重构为支持权重图搜索。
> * 新增方法 `find_path_dijkstra(start, end, strategy)`。
> * **权重逻辑**：
> * 如果 `strategy == 'min_station'`：邻居站点间权重为 1，换乘权重为 1。
> * 如果 `strategy == 'min_transfer'`：邻居站点间权重为 1，**换乘站点的权重设为 1000**（或者一个足够大的数）。
> 
> 
> * 保留原有的 `find_path` 接口，但内部调用新的 Dijkstra 逻辑，默认策略为 `min_station`。
> 
> 
> 2. **修改 `src/main.py**`：
> * 更新 `MetroPathPlanner.find_route` 方法，增加一个 `strategy` 参数（默认 'min_station'）。
> 
> 
> 
> 
> 请确保代码能够处理同一站点在不同线路上的权重计算（即换乘时的代价）。

---
