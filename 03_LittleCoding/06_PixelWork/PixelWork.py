import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import sys

class BeadSelectorGUI:
    def __init__(self, master, image_path, bead_size):
        self.master = master
        self.bead_size = bead_size
        
        # 1. 加载并准备图片
        try:
            self.orig_img = Image.open(image_path).convert("RGB")
        except FileNotFoundError:
            print(f"找不到文件: {image_path}")
            sys.exit(1)

        self.width, self.height = self.orig_img.size
        self.cols = self.width // self.bead_size
        self.rows = self.height // self.bead_size
        
        # 放大显示以便于点击 (例如放大2倍)
        self.scale = 2.0 
        self.display_bead_size = int(self.bead_size * self.scale)
        display_width = int(self.width * self.scale)
        display_height = int(self.height * self.scale)
        
        # 使用最近邻插值放大，保持像素感
        self.display_img = self.orig_img.resize((display_width, display_height), Image.NEAREST)
        self.tk_img = ImageTk.PhotoImage(self.display_img)

        # 2. 初始化移除掩码 (False = 保留, True = 移除)
        self.removed_mask = np.zeros((self.rows, self.cols), dtype=bool)
        self.is_finished = False

        # 3. 设置 GUI 组件
        self.canvas = tk.Canvas(master, width=display_width, height=display_height, cursor="crosshair")
        self.canvas.pack(side=tk.TOP)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
        
        # 绘制辅助网格线
        self.draw_grid_lines(display_width, display_height)

        # 底部按钮栏
        self.btn_frame = tk.Frame(master, pady=10)
        self.btn_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        instruction_label = tk.Label(self.btn_frame, text="操作指南: 点击网格以标记/取消标记要移除的区域 (红色X表示移除)", font=("微软雅黑", 10))
        instruction_label.pack()

        btn_finish = tk.Button(self.btn_frame, text="完成选择并生成图纸", command=self.finish, bg="#4CAF50", fg="white", font=("微软雅黑", 12, "bold"), padx=20, pady=5)
        btn_finish.pack(pady=(5, 0))
        
        # 绑定鼠标点击事件
        self.canvas.bind("<Button-1>", self.on_click)
        

    def draw_grid_lines(self, w, h):
        # 绘制青色虚线网格
        for c in range(self.cols + 1):
            x = c * self.display_bead_size
            self.canvas.create_line(x, 0, x, h, fill="cyan", width=1, dash=(4, 4))
        for r in range(self.rows + 1):
            y = r * self.display_bead_size
            self.canvas.create_line(0, y, w, y, fill="cyan", width=1, dash=(4, 4))

    def on_click(self, event):
        # 将点击坐标映射到网格行列
        c = int(event.x // self.display_bead_size)
        r = int(event.y // self.display_bead_size)

        # 检查边界
        if 0 <= r < self.rows and 0 <= c < self.cols:
            # 切换状态
            self.removed_mask[r, c] = not self.removed_mask[r, c]
            self.redraw_block_overlay(r, c)

    def redraw_block_overlay(self, r, c):
        # 计算画布上的区块坐标
        x0 = c * self.display_bead_size
        y0 = r * self.display_bead_size
        x1 = x0 + self.display_bead_size
        y1 = y0 + self.display_bead_size
        
        # 使用唯一 tag 管理该区块的覆盖层
        tag = f"overlay_{r}_{c}"
        self.canvas.delete(tag)

        if self.removed_mask[r, c]:
            # 绘制半透明红色覆盖层和一个大X
            # stipple="gray50" 创建半透明效果
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="red", stipple="gray50", outline="", tags=tag)
            self.canvas.create_line(x0, y0, x1, y1, fill="white", width=2, tags=tag)
            self.canvas.create_line(x0, y1, x1, y0, fill="white", width=2, tags=tag)

    def finish(self):
        self.is_finished = True
        self.master.destroy()


def generate_bead_pattern_with_selection(image_path, bead_size=20, output_prefix="shinji"):
    # --- 第一步: 启动交互式选择界面 ---
    root = tk.Tk()
    root.title("拼豆区域选择器 - 点击不需要的背景")
    # 将窗口置顶
    root.attributes('-topmost', True) 
    root.update()
    root.attributes('-topmost', False)

    app = BeadSelectorGUI(root, image_path, bead_size)
    root.mainloop()

    if not app.is_finished:
        print("操作窗口已关闭，取消生成。")
        return

    print("区域选择完成，开始处理数据...")
    removed_mask = app.removed_mask
    rows, cols = app.rows, app.cols
    img = app.orig_img
    width, height = app.width, app.height

    # --- 第二步: 颜色采样与提取 ---
    # 使用一个特殊值标记透明/移除区域, 例如 [-1, -1, -1]
    grid_colors = np.full((rows, cols, 3), -1, dtype=int)
    
    print(f"正在采样 {rows}x{cols} 的网格...")
    for r in range(rows):
        for c in range(cols):
            # 如果该区域被标记为移除，则跳过采样
            if removed_mask[r, c]:
                continue 

            # 采样中心点像素
            center_x = c * bead_size + bead_size // 2
            center_y = r * bead_size + bead_size // 2
            
            if center_x < width and center_y < height:
                pixel_color = img.getpixel((center_x, center_y))
                grid_colors[r, c] = pixel_color

    # 过滤掉标记为 -1 的透明区域，只保留有效颜色用于生成色板
    valid_colors_mask = np.all(grid_colors != -1, axis=2)
    valid_colors = grid_colors[valid_colors_mask]
    
    if len(valid_colors) == 0:
         print("错误：所有区域都被移除了，无法生成图纸。")
         return

    unique_colors = np.unique(valid_colors, axis=0)
    
    # 创建 ID 映射表
    color_map = {}
    id_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    legend_info = []
    
    print(f"\n检测到 {len(unique_colors)} 种有效颜色 (已排除移除区域):")
    for i, color in enumerate(unique_colors):
        color_tuple = tuple(color)
        cid = id_chars[i] if i < len(id_chars) else str(i)
        color_map[color_tuple] = cid
        
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        print(f"ID: [{cid}] | RGB: {color_tuple} | Hex: {hex_color}")
        legend_info.append((cid, color_tuple, hex_color))

    # --- 第三步: 生成最终设计图 ---
    cell_size = 30 # 输出图纸的格子大小
    out_img_w = cols * cell_size
    out_img_h = rows * cell_size
    # 图纸背景设为白色
    out_img = Image.new("RGB", (out_img_w, out_img_h), "white")
    draw = ImageDraw.Draw(out_img)
    
    try:
        # 尝试加载一个更好看的字体
        font = ImageFont.truetype("arialbd.ttf", 14) #尝试粗体
    except IOError:
        font = ImageFont.load_default()

    for r in range(rows):
        for c in range(cols):
            x0 = c * cell_size
            y0 = r * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            # 检查是否是被移除的区域
            if removed_mask[r, c]:
                # 绘制一个淡淡的叉号表示透明/留空
                draw.rectangle([x0, y0, x1, y1], outline="#e0e0e0") # 极浅的灰色边框
                draw.line([x0+8, y0+8, x1-8, y1-8], fill="#f0f0f0", width=2)
                draw.line([x0+8, y1-8, x1-8, y0+8], fill="#f0f0f0", width=2)
                continue

            # 绘制有效拼豆区域
            color_arr = grid_colors[r, c]
            color = tuple(color_arr)
            cid = color_map.get(color, "?")
            
            # 填充颜色和深灰色边框
            draw.rectangle([x0, y0, x1, y1], fill=color, outline="#555555")
            
            # 根据亮度决定文字颜色
            brightness = (color[0]*0.299 + color[1]*0.587 + color[2]*0.114)
            text_color = "white" if brightness < 128 else "black"
            
            # 简单居中文字
            draw.text((x0 + cell_size/3, y0 + cell_size/4), cid, fill=text_color, font=font)

    save_path_chart = f"{output_prefix}_设计图纸.png"
    out_img.save(save_path_chart)
    print(f"\n>>> 成功: 设计图纸已保存至: {save_path_chart}")
    
    # --- 第四步: 生成色卡图例 ---
    if len(unique_colors) > 0:
        # 根据颜色数量动态调整图例高度
        fig_height = max(2, len(unique_colors) * 0.6)
        plt.figure(figsize=(6, fig_height))
        plt.axis('off')
        plt.title(f"Mard色卡对照表 (共{len(unique_colors)}色)", fontproperties="Microsoft YaHei")
        
        for idx, (cid, rgb, hex_c) in enumerate(legend_info):
            # 绘制色块
            rect = plt.Rectangle((0, len(unique_colors) - idx - 1), 0.8, 0.8, color=np.array(rgb)/255)
            plt.gca().add_patch(rect)
            # 绘制文字说明
            text = f"ID: [{cid}]  RGB:{rgb}"
            plt.text(1.0, len(unique_colors) - idx - 0.6, text, fontsize=12, va='center', fontproperties="Arial")
            plt.text(3.5, len(unique_colors) - idx - 0.6, "<- 对应你的Mard色卡", fontsize=10, color="gray", va='center', fontproperties="Microsoft YaHei")
            
        plt.xlim(0, 5)
        plt.ylim(0, len(unique_colors))
        plt.tight_layout()
        save_path_legend = f"{output_prefix}_色卡对照.png"
        plt.savefig(save_path_legend)
        print(f">>> 成功: 色卡对照表已保存至: {save_path_legend}")
    else:
        print("未检测到任何有效颜色，跳过生成图例。")

# --- 执行部分 ---
if __name__ == "__main__":
    # 请确保文件名正确
    image_file = "C:\\Users\\Sum\\Desktop\\Transport\\真嗣原图框选.jpg" 
    # 运行主函数，output_prefix 可以修改为你想要的文件名前缀
    generate_bead_pattern_with_selection(image_file, bead_size=20, output_prefix="真嗣拼豆")