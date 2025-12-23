#### 阶段五：智能输入体验 (Autocomplete)

**目标**：将输入框升级为“带搜索功能的下拉框”，利用后端数据实现实时联想，减少用户输入错误。

* **涉及文件**: `src/gui_app.py`, `src/models/network.py`
* **技术点**: `tkinter.ttk.Combobox`, 事件绑定

**Agent 指令提示词 (Phase 5):**

> **复制以下内容给 Agent：**
> 任务更新：我们需要大幅升级 GUI 的输入体验，实现“输入联想/自动补全”功能。
> 1. **修改 `src/models/network.py**`:
> * 新增方法 `get_all_station_names_with_line() -> List[str]`。
> * 返回一个格式化的字符串列表，例如 `["复旦大学 (18号线)", "交通大学 (10号线)", ...]`，包含网络中所有站点的精确描述。
> 
> 
> 2. **修改 `src/gui_app.py**`:
> * 引入 `tkinter.ttk` 模块。
> * **组件替换**: 将 `entry_start` 和 `entry_end` 从普通的 `tk.Entry` 替换为 `ttk.Combobox`。
> * **初始化数据**: 在 `__init__` 中调用 network 的新方法，将所有站点填入 Combobox 的 `values` 属性，作为默认下拉列表。
> * **动态过滤**: 绑定 `<KeyRelease>` 事件。当用户输入字符时，获取输入内容，调用 `network.search_stations(keyword)`，将结果格式化后更新到 `values` 列表中，实现实时联想。
> * **调整查询逻辑**: 在 `on_search` 中，如果用户选择的是 `“站名 (线路)”` 这种格式，需要解析出精确的线路名和站名传给后端；如果是纯文本，则保持原有的模糊搜索逻辑。
> 
> 
> 
> 

---
