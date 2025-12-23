#### 阶段六（重制版）：高级数据清洗与拓扑修复

**目标**：在爬虫层彻底修复“环线断开”和“分叉线混淆”的问题，为算法提供完美的图数据。

* **涉及文件**: `src/services/data_fetcher.py`, `src/services/path_finder.py`

**Agent 指令提示词 (Phase 6 - Refined):**

> **复制以下内容给 Agent：**
> 这是一个关键的任务更新，我们需要增强数据爬虫的逻辑来处理复杂的地铁拓扑，并调整算法适配这种拓扑。
> 1. **重构 `src/services/data_fetcher.py**`:
> * 在类中增加配置：`LOOP_LINES = ['4号线']`。
> * **实现 `_fix_topology` 逻辑**（在生成 CSV 行之前调用）：
> * **处理环线**：检查当前线路名是否在 `LOOP_LINES` 中。如果是，且 `stations[0]['n'] != stations[-1]['n']`，则将 `stations[0]` 的副本 append 到 `stations` 列表末尾。
> * **处理分叉**：维护一个 `seen_lines = {}` (key=line_name, value=stations_list)。
> * 如果当前 `line_name` 已存在，且站点列表不同（说明是支线）：
> * 将当前线路名修改为 `f"{line_name}(支线)"`（如果已有支线，可叠加后缀）。
> * **重要**：确保修改后的名字能通过 `process_data` 后续的逻辑。
> 
> 
> * **去重**：应用之前的 `(line_name, station_name)` 去重逻辑，防止 API 返回完全重复的数据段。
> 
> 
> 
> 
> 2. **修改 `src/services/path_finder.py**`:
> * 修改 `_get_neighbors_with_weight` 方法。
> * **实现“零代价换乘”逻辑**：
> * 当计算换乘权重时（即 `current_station.name == neighbor.name` 但 `line_name` 不同）：
> * 判定是否为“同系线路”：
> * 如果 `line_A` 包含 `line_B`（如 "10号线" 包含 "10号线(支线)"），或者它们属于同一个主线编号。
> * **或者**，如果这是“同线同名换乘”（针对环线首尾相接的情况，line_name 完全相同，但 ID 不同）。
> 
> 
> * 如果满足上述任一条件，**将换乘权重设为 0**（或者一个极小值 0.1，以防死循环）。
> * 否则，维持标准的换乘惩罚（如 1000）。
> 
> 
> 
> 
> 
> 
> 完成后，请运行爬虫更新数据，并测试“4号线环线搜索”和“10号线主支线搜索”，确保路径连通且没有奇怪的绕路。

---
