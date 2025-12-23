"""地铁换乘路径规划系统 - Tkinter GUI入口

提供桌面界面：起终点输入、策略选择、结果展示，并复用 MetroPathPlanner 作为后端。
"""

import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from typing import List, Optional, Tuple

from main import MetroPathPlanner


class MetroGUI:
    def __init__(self, root: tk.Tk, planner: MetroPathPlanner):
        self.root = root
        self.root.title("地铁换乘路径规划系统")
        self.planner = planner
        self.all_station_options: List[str] = []

        if self.planner.network:
            self.all_station_options = self.planner.network.get_all_station_names_with_line()

        # 输入区
        input_frame = tk.Frame(root, padx=12, pady=10)
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="起点(可仅站名):").grid(row=0, column=0, sticky=tk.W, pady=4)
        self.entry_start = ttk.Combobox(input_frame, width=40, values=self.all_station_options)
        self.entry_start.grid(row=0, column=1, padx=6, pady=4)
        self.entry_start.bind('<KeyRelease>', lambda e: self._on_filter(self.entry_start))

        tk.Label(input_frame, text="终点(可仅站名):").grid(row=1, column=0, sticky=tk.W, pady=4)
        self.entry_end = ttk.Combobox(input_frame, width=40, values=self.all_station_options)
        self.entry_end.grid(row=1, column=1, padx=6, pady=4)
        self.entry_end.bind('<KeyRelease>', lambda e: self._on_filter(self.entry_end))

        # 策略选择
        strategy_frame = tk.LabelFrame(root, text="策略选择", padx=10, pady=8)
        strategy_frame.pack(fill=tk.X, padx=12, pady=6)
        self.strategy_var = tk.StringVar(value="min_station")
        tk.Radiobutton(strategy_frame, text="最短路径(最少站)", variable=self.strategy_var, value="min_station").pack(anchor=tk.W)
        tk.Radiobutton(strategy_frame, text="最少换乘", variable=self.strategy_var, value="min_transfer").pack(anchor=tk.W)

        # 查询按钮
        btn_frame = tk.Frame(root, padx=12, pady=6)
        btn_frame.pack(fill=tk.X)
        tk.Button(btn_frame, text="查询", command=self.on_search, width=12).pack(side=tk.LEFT)

        # 结果区
        result_frame = tk.LabelFrame(root, text="结果", padx=10, pady=8)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        self.result_text = ScrolledText(result_frame, height=16, width=60)
        self.result_text.pack(fill=tk.BOTH, expand=True)

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

            result = self.planner.find_route(start_line, start_name, end_line, end_name, strategy=strategy)
            self._set_result(result)
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def _set_result(self, text: str):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)

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

        if raw.endswith(')') and '(' in raw:
            try:
                name_part, line_part = raw.rsplit('(', 1)
                station_name = name_part.strip()
                line_name = line_part.rstrip(')').strip()
                if station_name and line_name:
                    return line_name, station_name
            except ValueError:
                pass

        # 默认返回纯站名，线路交由后端模糊/任意匹配
        return None, raw


def main():
    planner = MetroPathPlanner()
    if not planner.load_data():
        messagebox.showerror("错误", "数据加载失败，无法启动应用")
        return

    root = tk.Tk()
    app = MetroGUI(root, planner)
    root.mainloop()


if __name__ == "__main__":
    main()
