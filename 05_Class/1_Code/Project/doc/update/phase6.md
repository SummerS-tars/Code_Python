#### 阶段六：数据生态闭环 (集成爬虫 & 数据浏览器)

**目标**：将 `fetch_data.py` 集成到主程序中，并提供一个可视化窗口供用户查看所有线路和站点数据。

* **涉及文件**:
* 新建 `src/services/data_fetcher.py` (重构自 `fetch_data.py`)
* `src/gui_app.py`
* `src/main.py`


* **技术点**: `ttk.Treeview`, `Toplevel` 窗口, 多线程(可选，防止界面卡死)

**Agent 指令提示词 (Phase 6):**

> **复制以下内容给 Agent：**
> 任务更新：我们需要增强系统的数据管理能力，包括“在线更新数据”和“查看所有数据”。
> 1. **新建 `src/services/data_fetcher.py**`:
> * 将原项目根目录下的 `fetch_data.py` 的逻辑迁移进来，封装为一个类 `DataFetcher`。
> * 提供 `fetch_and_save(output_path: str)` 方法。
> * **重要**: 确保它依赖的 `requests` 库如果不存在能优雅报错（提示用户安装），或者使用标准库 `urllib` 替代（如果为了减少依赖）。
> 
> 
> 2. **修改 `src/main.py**`:
> * 在 `MetroPathPlanner` 中增加 `update_data_online()` 方法，调用 `DataFetcher` 下载最新数据，成功后自动调用 `load_data()` 重新加载内存中的图结构。
> 
> 
> 3. **修改 `src/gui_app.py**`:
> * **新增功能区**: 在顶部增加一个菜单栏或在按钮区增加两个新按钮：“更新数据”和“查看线路图”。
> * **实现“更新数据”**: 点击后调用 `planner.update_data_online()`，并弹窗提示成功或失败。
> * **实现“查看线路图”**:
> * 点击后弹出一个新窗口 (`tk.Toplevel`)。
> * 窗口内放置一个 `ttk.Treeview` 组件。
> * **层级结构**: 根节点 -> 线路名 (如"1号线") -> 站点名 (如"莘庄")。
> * 遍历 `planner.network` 中的数据来填充这个树。
> * 添加滚动条以支持查看大量数据。
> 
> 
> 
> 
> 
> 

---
