
#### 阶段七：富文本结果展示 (UI 美化)

**目标**：让路径规划的结果不再是枯燥的纯文本，通过颜色区分线路、高亮换乘信息，提升阅读体验。

* **涉及文件**: `src/gui_app.py`, `src/main.py`
* **技术点**: `Tkinter.Text` 的 `tag` 功能

**Agent 指令提示词 (Phase 7):**

> **复制以下内容给 Agent：**
> 最后一个阶段任务：美化查询结果的显示。
> 1. **修改 `src/main.py**`:
> * 给 `MetroPathPlanner` 增加 `get_route_object(...)` 方法。
> * 该方法与 `find_route` 逻辑一致，但**不返回字符串**，而是直接返回结构化的 `List[Union[Station, str]]`（即原始的 path 对象）。
> 
> 
> 2. **修改 `src/gui_app.py**`:
> * 修改 `on_search` 方法，调用新的 `get_route_object` 获取原始数据。
> * **重构 `_set_result` 方法**:
> * 清空文本框。
> * 定义样式 Tags:
> * `tag_line`: 蓝色粗体（用于显示线路名）。
> * `tag_station`: 黑色（用于站名）。
> * `tag_transfer`: 红色背景或红色粗体（用于高亮 "换乘" 字样）。
> * `tag_arrow`: 灰色（用于显示 "->" 箭头）。
> 
> 
> * **渲染逻辑**:
> * 遍历 path 列表。
> * 如果是 Station 对象：插入 `[线路名]` (应用 `tag_line`) + `站名` (应用 `tag_station`)。
> * 如果是 "换乘" 字符串：插入文本 `[ 换乘 ]` (应用 `tag_transfer`)。
> * 在元素之间插入箭头 `->`。
> 
> 
> * 这样用户一眼就能看出在哪里换乘，坐哪条线。
> 
> 
> 
> 
> 
> 
