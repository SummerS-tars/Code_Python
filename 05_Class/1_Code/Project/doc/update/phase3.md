## 阶段三：站点模糊搜索与智能补全

**目标**：解决用户必须输入完整“线路名+站名”的痛点，允许仅输入站名，并处理重名站问题。

### 1. 设计逻辑

* **索引优化**：利用 `MetroNetwork.stations_by_name`。
* **模糊匹配**：如果用户输入 "复旦"，能匹配到 "复旦大学"。
* **歧义处理**：如果用户只输入 "西藏南路"，系统需识别出它既在4号线也在8号线。通常作为起点时，任选一个接入点即可（因为网络是连通的）；但为了严谨，可以优先选择换乘较少的线路，或者在 CLI 中列出选项让用户选（本阶段暂实现自动选择）。

### 2. 涉及文件

* `src/models/network.py`
* `src/main.py`

### 3. 给 IDE Agent 的指令提示词 (Phase 3)

> **复制以下内容给 Agent：**
> 现在的任务是增强搜索体验，支持模糊查询和纯站名输入。
> 1. **修改 `src/models/network.py**`：
> * 新增方法 `search_stations(keyword: str) -> List[Station]`。该方法遍历所有站点，返回名称包含 `keyword` 的所有站点列表。
> * 新增方法 `get_station_any_line(station_name: str) -> Optional[Station]`。如果用户没指定线路，返回该站名对应的任意一个 Station 对象（通常列表里的第一个即可）。
> 
> 
> 2. **修改 `src/main.py` 中的 `MetroPathPlanner` 类**：
> * 修改 `process_user_input` 逻辑。
> * 如果在 `parser` 解析时只有站名没有线路名，则调用 `network.get_station_any_line` 查找站点。
> * 如果找不到精确匹配，调用 `network.search_stations` 进行模糊搜索，如果找到唯一的模糊匹配结果，自动使用该结果；如果找到多个，抛出异常提示用户“您是指：A, B, C...?”。
> 
> 
> 
> 
> 这将允许用户直接输入 "复旦大学-交通大学" 进行查询。

---
