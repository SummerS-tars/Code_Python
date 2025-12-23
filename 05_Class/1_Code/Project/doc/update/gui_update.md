这是一个非常典型的 Tkinter 开发阶段会遇到的问题组合。

1. **路线显示全变为“换乘”**：这通常是因为**类型检查失败**（`isinstance(item, Station)` 返回了 False），或者后端返回的数据已经被转换成了字符串。
2. **窗口太小/丑**：Tkinter 默认窗口确实比较原始（Windows 95 风格），且默认不会自动适应内容大小。

以下是针对这两个问题的修复方案，以及使用 `ttkbootstrap` 进行 UI 美化的建议。

---

### 第一步：修复“全显示为换乘”的 Bug

**原因分析**：
在 `gui_app.py` 中，你可能使用了 `isinstance(item, Station)` 来判断节点类型。在 Python 中，如果 `main.py` 和 `gui_app.py` 对 `Station` 类的导入路径不一致（例如一个用了 `src.models.station`，另一个用了 `models.station`），`isinstance` 就会判断失败，导致逻辑掉进 `else` 分支（即“换乘”分支）。

**修复代码**：
不要依赖 `isinstance`，改用**属性判断**（鸭子类型），这样更健壮。

请修改 `gui_app.py` 中绘制/显示路线的部分（假设在 `draw_route` 或类似方法中）：

```python
# 修改前 (可能长这样)
# if isinstance(item, Station):
#     ...
# else:
#     # 认为是换乘

# 修改后：使用 hasattr 判断是否为站点对象
for item in path:
    # 只要有 name 和 line_name 属性，就视为站点
    if hasattr(item, 'name') and hasattr(item, 'line_name'):
        # === 绘制站点逻辑 ===
        print(f"Drawing Station: {item.name}")  # Debug
        # ... 你的绘制代码 ...
    else:
        # === 绘制换乘逻辑 ===
        # 即使是换乘，也要检查它是不是字符串 "换乘"
        if str(item) == "换乘":
             # ... 你的绘制换乘代码 ...
             pass

```

---

### 第二步：解决窗口大小与美化 (引入 ttkbootstrap)

原生的 Tkinter 样式（CSS）修改非常痛苦。我强烈推荐引入 **`ttkbootstrap`**。它是一个基于 Tkinter 的皮肤库，只需**两行代码**就能让你的程序拥有现代化的扁平风格（类似 Bootstrap），自带深色模式，且组件尺寸更合理。

#### 1. 安装库

在终端运行：

```bash
pip install ttkbootstrap

```

#### 2. 修改 `src/gui_app.py`

我为你重写了 `gui_app.py` 的关键结构，整合了**窗口尺寸修复**、**ttkbootstrap 美化**以及**更稳健的路径绘制逻辑**。

请参考以下代码进行修改：

```python
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb  # 引入美化库
from ttkbootstrap.constants import *
from typing import List, Tuple, Optional

# 确保导入路径一致
from src.main import MetroPathPlanner
# 如果你没有 models.__init__ 里的导出，可能需要直接导
from src.models.station import Station 
from src.config import LINE_COLORS

class MetroGUI:
    def __init__(self, root: tb.Window, planner: MetroPathPlanner):
        self.root = root
        self.planner = planner
        
        # 1. 窗口设置：设定初始大小和最小尺寸
        self.root.title("上海地铁路径规划系统 v3.0")
        self.root.geometry("1000x700")  # 初始宽x高
        self.root.minsize(800, 600)     # 最小尺寸防止内容遮挡

        # 2. 布局初始化 (使用 ttkbootstrap 的 Frame)
        # main_container 用于左右分栏
        main_container = tb.Frame(self.root, padding=10)
        main_container.pack(fill=BOTH, expand=YES)

        # === 左侧控制栏 ===
        sidebar = tb.Frame(main_container, width=300, padding=10, bootstyle="light")
        sidebar.pack(side=LEFT, fill=Y, padx=(0, 10))
        
        # 标题
        tb.Label(sidebar, text="行程设置", font=("微软雅黑", 16, "bold"), bootstyle="primary").pack(pady=(0, 20), anchor="w")

        # 起点输入
        tb.Label(sidebar, text="起点站", bootstyle="secondary").pack(anchor="w")
        self.combo_start = ttk.Combobox(sidebar, height=10)
        self.combo_start.pack(fill=X, pady=(5, 15))
        
        # 终点输入
        tb.Label(sidebar, text="终点站", bootstyle="secondary").pack(anchor="w")
        self.combo_end = ttk.Combobox(sidebar, height=10)
        self.combo_end.pack(fill=X, pady=(5, 15))

        # 策略选择 (使用 Toolbutton 样式更好看)
        tb.Label(sidebar, text="偏好策略", bootstyle="secondary").pack(anchor="w")
        self.strategy_var = tk.StringVar(value="min_station")
        strategy_frame = tb.Frame(sidebar)
        strategy_frame.pack(fill=X, pady=5)
        
        tb.Radiobutton(strategy_frame, text="最少站点", variable=self.strategy_var, 
                      value="min_station", bootstyle="toolbutton-outline").pack(side=LEFT, fill=X, expand=YES, padx=2)
        tb.Radiobutton(strategy_frame, text="最少换乘", variable=self.strategy_var, 
                      value="min_transfer", bootstyle="toolbutton-outline").pack(side=LEFT, fill=X, expand=YES, padx=2)

        # 按钮区
        tb.Button(sidebar, text="查询路线", command=self.on_search, bootstyle="success").pack(fill=X, pady=20)
        
        tb.Separator(sidebar).pack(fill=X, pady=10)
        
        # 数据管理按钮
        tb.Button(sidebar, text="更新数据", command=self.on_update_data, bootstyle="info-outline").pack(fill=X, pady=5)
        tb.Button(sidebar, text="查看线路图", command=self.on_view_map, bootstyle="info-outline").pack(fill=X, pady=5)

        # === 右侧结果展示区 (Canvas) ===
        content_frame = tb.Labelframe(main_container, text="规划结果", padding=10, bootstyle="default")
        content_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        # 滚动条与 Canvas
        self.canvas = tk.Canvas(content_frame, bg="white", highlightthickness=0)
        scrollbar = tb.Scrollbar(content_frame, orient=VERTICAL, command=self.canvas.yview)
        
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # 初始化联想输入
        self._init_combobox_events()

    def _init_combobox_events(self):
        # ... (保留你之前的联想逻辑) ...
        pass

    def on_search(self):
        # 模拟获取结果
        start_txt = self.combo_start.get()
        end_txt = self.combo_end.get()
        strategy = self.strategy_var.get()
        
        try:
            # 1. 解析输入 (复用你之前的逻辑)
            # ...
            
            # 2. 获取路径对象 (注意：是 get_route_object)
            # 假设后端返回: path_list, fare, time_cost
            # 这里请根据你实际的 Phase 7 修改适配
            path_list = self.planner.find_path_object_mock(start_txt, end_txt) # 替换为你真实的方法调用

            # 3. 绘制
            self.draw_route_on_canvas(path_list)

        except Exception as e:
            messagebox.showerror("错误", str(e))

    def draw_route_on_canvas(self, path_list):
        """核心修复：绘制逻辑"""
        self.canvas.delete("all")
        
        x_base = 100
        y_current = 50
        y_step = 60  # 站点垂直间距
        
        # 用于动态调整滚动区域
        max_width = 400 

        for i, item in enumerate(path_list):
            # === BUG FIX: 使用 hasattr 代替 isinstance ===
            is_station = hasattr(item, 'name') and hasattr(item, 'line_name')
            
            if is_station:
                # 获取颜色
                line_color = LINE_COLORS.get(item.line_name, '#999999')
                
                # 1. 绘制连接线 (如果不是最后一个)
                if i < len(path_list) - 1:
                    # 检查下一个是不是换乘，如果是换乘，画虚线或保持颜色
                    self.canvas.create_line(x_base, y_current, x_base, y_current + y_step, 
                                          width=4, fill=line_color, tags="route")

                # 2. 绘制站点圆点
                r = 8
                self.canvas.create_oval(x_base-r, y_current-r, x_base+r, y_current+r, 
                                      fill="white", outline=line_color, width=3, tags="station")
                
                # 3. 绘制文字
                # 站名
                self.canvas.create_text(x_base + 30, y_current - 5, 
                                      text=item.name, anchor="w", 
                                      font=("微软雅黑", 12, "bold"), fill="#333")
                # 线路标签
                self.canvas.create_text(x_base + 30, y_current + 15, 
                                      text=item.line_name, anchor="w", 
                                      font=("Arial", 9), fill=line_color)

                y_current += y_step

            else:
                # === 处理换乘/其他字符串 ===
                # 这里只在两个站点之间标记“换乘”
                # 通常换乘站的 Station 对象本身已经包含了线路变化，
                # 所以 path_list 里如果插入了 "换乘" 字符串，我们可以在这里画一个图标
                
                # 绘制一个“换乘”小胶囊背景
                self.canvas.create_rectangle(x_base - 20, y_current - 40, x_base + 20, y_current - 20,
                                           fill="#f0ad4e", outline="", tags="transfer_badge")
                self.canvas.create_text(x_base, y_current - 30, text="换乘", 
                                      font=("微软雅黑", 8, "bold"), fill="white")
                # 不增加 y_current，让它浮在连线上
                pass

        # 更新滚动区域
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # ... 其他回调方法 ...

# 启动代码修改
if __name__ == "__main__":
    # 使用 ttkbootstrap 的 Window 代替 tk.Tk
    app = tb.Window(themename="cosmo") # 主题可选: cosmo, flatly, journal, darkly...
    # ... 初始化逻辑 ...
    # gui = MetroGUI(app, planner)
    app.mainloop()

```

### 总结修改点

1. **Bug 修复**：在 `draw_route_on_canvas` 中使用 `hasattr(item, 'name')` 而不是 `isinstance`，彻底解决跨文件导入导致的类型失配问题。
2. **窗口修复**：在 `__init__` 中添加 `self.root.geometry("1000x700")`。
3. **UI 美化**：引入 `ttkbootstrap`，并在创建窗口时使用 `tb.Window(themename="cosmo")`。左侧栏使用 `bootstyle="light"`，按钮使用 `bootstyle="success"` 等预设样式，瞬间提升颜值。
4. **绘图逻辑**：使用 `Canvas` 绘制时间轴式的路线图（圆点+连线），比纯文本列表直观得多。