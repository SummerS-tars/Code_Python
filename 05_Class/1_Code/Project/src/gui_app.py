"""地铁换乘路径规划系统 - Tkinter GUI入口

提供桌面界面：起终点输入、策略选择、结果展示，并复用 MetroPathPlanner 作为后端。
"""

import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from typing import Optional

from main import MetroPathPlanner


class MetroGUI:
    def __init__(self, root: tk.Tk, planner: MetroPathPlanner):
        self.root = root
        self.root.title("地铁换乘路径规划系统")
        self.planner = planner

        # 输入区
        input_frame = tk.Frame(root, padx=12, pady=10)
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="起点(可仅站名):").grid(row=0, column=0, sticky=tk.W, pady=4)
        self.entry_start = tk.Entry(input_frame, width=40)
        self.entry_start.grid(row=0, column=1, padx=6, pady=4)

        tk.Label(input_frame, text="终点(可仅站名):").grid(row=1, column=0, sticky=tk.W, pady=4)
        self.entry_end = tk.Entry(input_frame, width=40)
        self.entry_end.grid(row=1, column=1, padx=6, pady=4)

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
        user_input = f"{start}-{end}"
        try:
            result = self.planner.process_user_input(user_input if "-" in user_input else user_input)
            # 由于 process_user_input 已包含 formatter，直接输出
            self._set_result(result)
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def _set_result(self, text: str):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)


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
