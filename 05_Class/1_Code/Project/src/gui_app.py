"""地铁换乘路径规划系统 - Tkinter GUI入口

提供桌面界面：起终点输入、策略选择、结果展示，并复用 MetroPathPlanner 作为后端。
"""

import re
import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import BOTH, YES, LEFT, RIGHT, X, Y, VERTICAL
from typing import List, Optional, Tuple, Union, Any

from main import MetroPathPlanner
from config import LINE_COLORS


def _is_station(obj: Any) -> bool:
    return hasattr(obj, "station_name") and hasattr(obj, "line_name")


class MetroGUI:
    def __init__(self, root: tb.Window, planner: MetroPathPlanner):
        self.root = root
        self.root.title("上海地铁路径规划系统 v3.0")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.planner = planner
        self.all_station_options: List[str] = []

        # 样式设置
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            pass
        style.configure('.', font=('Microsoft YaHei', 10))
        style.configure('TButton', padding=6)
        style.configure('TLabel', padding=2)

        if self.planner.network:
            self.all_station_options = self.planner.network.get_all_station_names_with_line()
        # 主布局：左侧侧栏，右侧内容
        container = tb.Frame(root, padding=10)
        container.pack(fill=BOTH, expand=YES)

        sidebar = tb.Frame(container, width=300, padding=10, bootstyle="light")
        sidebar.pack(side=LEFT, fill=Y, padx=(0, 10))
        sidebar.pack_propagate(False)

        content = tb.Labelframe(container, text="规划结果", padding=10, bootstyle="default")
        content.pack(side=LEFT, fill=BOTH, expand=YES)

        # 输入区
        tb.Label(sidebar, text="起点站", bootstyle="secondary").pack(anchor="w")
        self.entry_start = ttk.Combobox(sidebar, width=30, values=self.all_station_options)
        self.entry_start.pack(fill=X, pady=(5, 12))
        self.entry_start.bind('<KeyRelease>', lambda e: self._on_filter(self.entry_start))

        tb.Label(sidebar, text="终点站", bootstyle="secondary").pack(anchor="w")
        self.entry_end = ttk.Combobox(sidebar, width=30, values=self.all_station_options)
        self.entry_end.pack(fill=X, pady=(5, 12))
        self.entry_end.bind('<KeyRelease>', lambda e: self._on_filter(self.entry_end))

        # 策略选择
        strategy_frame = tb.Frame(sidebar)
        strategy_frame.pack(fill=X, pady=8)
        self.strategy_var = tk.StringVar(value="min_station")
        tb.Radiobutton(strategy_frame, text="最少站点", variable=self.strategy_var, value="min_station",
                      bootstyle="toolbutton-outline").pack(side=LEFT, fill=X, expand=YES, padx=2)
        tb.Radiobutton(strategy_frame, text="最少换乘", variable=self.strategy_var, value="min_transfer",
                      bootstyle="toolbutton-outline").pack(side=LEFT, fill=X, expand=YES, padx=2)

        # 按钮组
        btn_frame = tb.Frame(sidebar)
        btn_frame.pack(fill=X, pady=12)
        tb.Button(btn_frame, text="查询路线", command=self.on_search, bootstyle="success").pack(fill=X, pady=4)
        tb.Separator(sidebar).pack(fill=X, pady=6)
        tb.Button(sidebar, text="更新数据", command=self.on_update_data, bootstyle="info-outline").pack(fill=X, pady=4)
        tb.Button(sidebar, text="查看线路图", command=self.on_view_network, bootstyle="info-outline").pack(fill=X, pady=4)

        # 结果区域：Canvas + Scrollbar
        result_frame = tb.Frame(content)
        result_frame.pack(fill=BOTH, expand=YES)
        self.canvas = tk.Canvas(result_frame, background='white', highlightthickness=0)
        self.v_scroll = tb.Scrollbar(result_frame, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        self.v_scroll.pack(side=RIGHT, fill=Y)
    def on_search(self):
        start = self.entry_start.get().strip()
        end = self.entry_end.get().strip()
        strategy = self.strategy_var.get()

        if not start or not end:
            messagebox.showwarning("提示", "请填写起点和终点")
            return

        # 解析输入：允许格式 “线路，站名-线路，站名” 或 仅“站名-站名”
        try:
            start_line, start_name = self._parse_input_text(start)
            end_line, end_name = self._parse_input_text(end)

            path = self.planner.get_route(start_line, start_name, end_line, end_name, strategy=strategy)
            self._draw_route(path)
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def on_update_data(self):
        result = self.planner.update_data_online()
        messagebox.showinfo("更新结果", result)
        # 更新下拉列表数据
        if self.planner.network:
            self.all_station_options = self.planner.network.get_all_station_names_with_line()
            self.entry_start['values'] = self.all_station_options
            self.entry_end['values'] = self.all_station_options

    def on_view_network(self):
        if not self.planner.network:
            messagebox.showwarning("提示", "请先加载数据")
            return
        win = tk.Toplevel(self.root)
        win.title("线路与站点")
        tree = ttk.Treeview(win)
        tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.heading('#0', text='线路 / 站点')
        for line_name, line in self.planner.network.lines.items():
            line_id = tree.insert('', 'end', text=line_name)
            for st in line.stations:
                tree.insert(line_id, 'end', text=st.station_name)

    def _draw_route(self, path: List[Any]):
        self.canvas.delete('all')
        if not path:
            return

        y_start = 40
        step = 70
        x_line = 120
        radius = 10
        text_offset = 20
        prev_pos = None
        prev_color = None

        for idx, item in enumerate(path):
            y = y_start + idx * step
            if _is_station(item):
                color = LINE_COLORS.get(getattr(item, "line_name", ""), '#888888')
                if prev_pos is not None:
                    self.canvas.create_line(x_line, prev_pos, x_line, y, fill=prev_color or color, width=4)
                self.canvas.create_oval(x_line - radius, y - radius, x_line + radius, y + radius, fill=color, outline=color)
                label = f"{getattr(item, 'station_name', '')} ({getattr(item, 'line_name', '')})"
                self.canvas.create_text(x_line + text_offset, y, text=label, anchor=tk.W, font=('Microsoft YaHei', 10))
                prev_color = color
                prev_pos = y
            else:  # 换乘
                self.canvas.create_line(x_line, prev_pos or y, x_line, y, fill='#666666', width=2, dash=(4,2))
                self.canvas.create_text(x_line + text_offset, y, text="换乘", anchor=tk.W, font=('Microsoft YaHei', 9, 'italic'), fill='#666666')
                prev_pos = y

        # scroll region
        self.canvas.configure(scrollregion=(0, 0, 800, y_start + len(path) * step))

    def _on_filter(self, combo: ttk.Combobox):
        keyword = combo.get().strip()
        if not self.planner.network:
            return

        if keyword:
            matches = self.planner.network.search_stations(keyword)
            values = [self._format_station_option(s) for s in matches]
        else:
            values = self.all_station_options
        combo['values'] = values

    @staticmethod
    def _format_station_option(station) -> str:
        return f"{station.station_name} ({station.line_name})"

    def _parse_input_text(self, text: str) -> Tuple[Optional[str], str]:
        """支持两种输入：
        1) "站名 (线路)" -> 返回 (线路, 站名)
        2) 纯文本 -> (None, 文本)
        """
        raw = text.strip()
        if not raw:
            return None, ""

        # FIX: 使用正则匹配，正确处理 "10号线(支线)" 这种带内部括号的情况
        # 匹配规则：以 " (" 开头，中间是线路名，以 ")" 结尾
        # ^(.*) 捕获前面的站名
        # \((.*)\)$ 捕获最后括号内的线路名
        match = re.match(r"^(.*) \((.*)\)$", raw)
        
        if match:
            station_name = match.group(1).strip()
            line_name = match.group(2).strip()
            return line_name, station_name

        # 旧逻辑（已废弃，无法处理嵌套括号）
        # if raw.endswith(')') and '(' in raw:
        #     try:
        #         name_part, line_part = raw.rsplit('(', 1)
        #         ...
        
        # 默认返回纯站名
        return None, raw

def main():
    planner = MetroPathPlanner()
    if not planner.load_data():
        messagebox.showerror("错误", "数据加载失败，无法启动应用")
        return

    root = tb.Window(themename="cosmo")
    app = MetroGUI(root, planner)
    root.mainloop()


if __name__ == "__main__":
    main()
