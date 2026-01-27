import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import json
import os
import sys

class BeadSelectorGUI:
    def __init__(self, master, image_path, bead_size):
        self.master = master
        self.bead_size = bead_size
        
        # 1. 加载并准备图片
        try:
            # 保留透明通道，避免透明区域被当作黑色
            self.orig_img = Image.open(image_path).convert("RGBA")
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
        resampling_enum = getattr(Image, "Resampling", None)
        if resampling_enum is not None:
            resample = resampling_enum.NEAREST  # Pillow>=9
        else:
            resample = getattr(Image, "NEAREST", 0)
        display_img = self.orig_img.resize((display_width, display_height), resample)
        # 将透明背景合成到白色底上进行显示
        display_bg = Image.new("RGBA", display_img.size, (255, 255, 255, 255))
        display_img = Image.alpha_composite(display_bg, display_img)
        self.tk_img = ImageTk.PhotoImage(display_img.convert("RGB"))

        # 2. 初始化移除掩码 (False = 保留, True = 移除)
        self.removed_mask = np.zeros((self.rows, self.cols), dtype=bool)
        self.is_finished = False

        # 3. 设置 GUI 组件
        # 允许窗口调整大小，并为大图提供滚动查看
        master.resizable(True, True)

        # 计算画布初始尺寸（不超过屏幕大小）
        screen_w = master.winfo_screenwidth()
        screen_h = master.winfo_screenheight()
        canvas_w = min(display_width, screen_w - 120)
        canvas_h = min(display_height, screen_h - 220)

        canvas_frame = tk.Frame(master)
        canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            canvas_frame,
            width=canvas_w,
            height=canvas_h,
            cursor="crosshair",
            highlightthickness=0
        )

        v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
        self.canvas.config(scrollregion=(0, 0, display_width, display_height))
        
        # 绘制辅助网格线
        self.draw_grid_lines(display_width, display_height)

        # 底部按钮栏
        self.btn_frame = tk.Frame(master, pady=10)
        self.btn_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        instruction_label = tk.Label(
            self.btn_frame,
            text="操作指南: 点击网格以标记/取消标记要移除的区域 (红色X表示移除)\n下一步: 完成筛选后点击“完成选择并生成图纸”进入生成阶段",
            font=("微软雅黑", 10),
            justify="center"
        )
        instruction_label.pack()

        btn_finish = tk.Button(self.btn_frame, text="完成选择并生成图纸", command=self.finish, bg="#4CAF50", fg="white", font=("微软雅黑", 12, "bold"), padx=20, pady=5)
        btn_finish.pack(pady=(5, 0))
        
        # 绑定鼠标点击事件
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Button-4>", self.on_mousewheel)
        self.canvas.bind("<Button-5>", self.on_mousewheel)
        

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
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        c = int(canvas_x // self.display_bead_size)
        r = int(canvas_y // self.display_bead_size)

        # 检查边界
        if 0 <= r < self.rows and 0 <= c < self.cols:
            # 切换状态
            self.removed_mask[r, c] = not self.removed_mask[r, c]
            self.redraw_block_overlay(r, c)

    def on_mousewheel(self, event):
        # Windows: event.delta 正/负；Linux: Button-4/5
        if hasattr(event, "delta") and event.delta:
            direction = -1 if event.delta > 0 else 1
        else:
            direction = -1 if event.num == 4 else 1
        self.canvas.yview_scroll(direction, "units")

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


def generate_bead_pattern_with_selection(image_path, bead_size=20, output_prefix="shinji", color_tolerance=8):
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
                if isinstance(pixel_color, tuple) and len(pixel_color) == 4:
                    r_c, g_c, b_c, a_c = pixel_color
                    if a_c <= 0:
                        removed_mask[r, c] = True
                        continue
                    pixel_color = (r_c, g_c, b_c)
                grid_colors[r, c] = pixel_color

    # 过滤掉标记为 -1 的透明区域，只保留有效颜色用于生成色板
    valid_colors_mask = np.all(grid_colors != -1, axis=2)
    valid_colors = grid_colors[valid_colors_mask]
    
    if len(valid_colors) == 0:
         print("错误：所有区域都被移除了，无法生成图纸。")
         return

    unique_colors = np.unique(valid_colors, axis=0)

    def merge_similar_colors(colors, tolerance):
        clusters = []
        color_to_cluster = {}

        for color in colors:
            color_arr = np.array(color, dtype=float)
            assigned = None
            for idx, cluster in enumerate(clusters):
                if np.linalg.norm(color_arr - cluster["mean"]) <= tolerance:
                    assigned = idx
                    break
            if assigned is None:
                clusters.append({"mean": color_arr, "count": 1})
                assigned = len(clusters) - 1
            else:
                cluster = clusters[assigned]
                cluster["mean"] = (cluster["mean"] * cluster["count"] + color_arr) / (cluster["count"] + 1)
                cluster["count"] += 1

            color_to_cluster[tuple(int(x) for x in color)] = assigned

        merged_colors = [tuple(int(round(x)) for x in cluster["mean"]) for cluster in clusters]
        return merged_colors, color_to_cluster

    if color_tolerance and color_tolerance > 0:
        merged_colors, color_to_cluster = merge_similar_colors(unique_colors, color_tolerance)
        print(f"\n颜色合并阈值: {color_tolerance}，合并后颜色数: {len(merged_colors)} (原始: {len(unique_colors)})")
    else:
        merged_colors = [tuple(int(x) for x in color) for color in unique_colors]
        color_to_cluster = {tuple(int(x) for x in color): idx for idx, color in enumerate(unique_colors)}
    
    # 创建 ID 映射表
    color_map = {}
    id_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    legend_info = []
    
    print(f"\n检测到 {len(merged_colors)} 种有效颜色 (已排除移除区域):")
    for i, color in enumerate(merged_colors):
        color_tuple = tuple(int(x) for x in color)
        cid = id_chars[i] if i < len(id_chars) else str(i)
        color_map[color_tuple] = cid
        
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        print(f"ID: [{cid}] | RGB: {color_tuple} | Hex: {hex_color}")
        legend_info.append((cid, color_tuple, hex_color))

    # --- 额外输出: 保存去除背景后的图片 ---
    removed_img = img.convert("RGBA")
    removed_draw = ImageDraw.Draw(removed_img)
    for r in range(rows):
        for c in range(cols):
            if removed_mask[r, c]:
                x0 = c * bead_size
                y0 = r * bead_size
                x1 = x0 + bead_size - 1
                y1 = y0 + bead_size - 1
                removed_draw.rectangle([x0, y0, x1, y1], fill=(0, 0, 0, 0))

    save_path_removed = f"{output_prefix}_去背景.png"
    removed_img.save(save_path_removed)
    print(f">>> 成功: 去背景图片已保存至: {save_path_removed}")

    # --- 额外输出: 生成融合后的 JSON 像素文件 ---
    def rgba_hex(color_rgb, alpha=255):
        return "#{:02X}{:02X}{:02X}{:02X}".format(color_rgb[0], color_rgb[1], color_rgb[2], alpha)

    pixels = []
    for r in range(rows):
        for c in range(cols):
            if removed_mask[r, c]:
                pixels.append("#00000000")
                continue

            color_arr = grid_colors[r, c]
            color_tuple = tuple(int(x) for x in color_arr)
            cluster_idx = color_to_cluster.get(color_tuple)
            color = merged_colors[cluster_idx] if cluster_idx is not None else color_tuple
            pixels.append(rgba_hex(color, 255))

    json_data = {
        "width": cols,
        "height": rows,
        "pixels": pixels
    }

    save_path_json = f"{output_prefix}_融合像素.json"
    with open(save_path_json, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False)
    print(f">>> 成功: 融合像素 JSON 已保存至: {save_path_json}")

    # --- 额外输出: 将 JSON 像素映射到色号并生成最终图纸 ---
    def hex_to_rgba(hex_color):
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 6:
            r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]
            a = "FF"
        else:
            r, g, b, a = hex_color[0:2], hex_color[2:4], hex_color[4:6], hex_color[6:8]
        return tuple(int(x, 16) for x in (r, g, b, a))

    def load_palette(palette_path):
        palette = []
        with open(palette_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if len(parts) < 2:
                    continue
                code, hex_color = parts[0], parts[1]
                rgb = hex_to_rgba(hex_color + "FF")[:3]
                palette.append((code, hex_color.lower(), rgb))
        return palette

    def nearest_palette_color(rgb, palette, cache):
        if rgb in cache:
            return cache[rgb]
        best = None
        best_dist = float("inf")
        for code, hex_color, pal_rgb in palette:
            dist = np.linalg.norm(np.array(rgb) - np.array(pal_rgb))
            if dist < best_dist:
                best_dist = dist
                best = (code, hex_color, pal_rgb)
        cache[rgb] = best
        return best

    palette_path = os.path.join(os.path.dirname(__file__), "list.txt")
    if os.path.exists(palette_path):
        palette = load_palette(palette_path)
        if not palette:
            print(f"色卡清单为空: {palette_path}，跳过色号映射。")
        else:
            try:
                font = ImageFont.truetype("arialbd.ttf", 14)
            except IOError:
                font = ImageFont.load_default()
            palette_cache = {}
            mapped_cells = []
            used_palette = {}

            for pix in json_data["pixels"]:
                r_c, g_c, b_c, a_c = hex_to_rgba(pix)
                if a_c == 0:
                    mapped_cells.append(None)
                    continue
                nearest = nearest_palette_color((r_c, g_c, b_c), palette, palette_cache)
                if nearest is None:
                    mapped_cells.append(None)
                    continue
                code, hex_color, pal_rgb = nearest
                mapped_cells.append((code, hex_color, pal_rgb))
                used_palette[code] = (hex_color, pal_rgb)

            final_cell_size = 30
            final_w = cols * final_cell_size
            final_h = rows * final_cell_size
            final_img = Image.new("RGB", (final_w, final_h), "white")
            final_draw = ImageDraw.Draw(final_img)

            for r in range(rows):
                for c in range(cols):
                    idx = r * cols + c
                    x0 = c * final_cell_size
                    y0 = r * final_cell_size
                    x1 = x0 + final_cell_size
                    y1 = y0 + final_cell_size

                    cell = mapped_cells[idx]
                    if cell is None:
                        final_draw.rectangle([x0, y0, x1, y1], outline="#e0e0e0")
                        continue

                    code, hex_color, pal_rgb = cell
                    final_draw.rectangle([x0, y0, x1, y1], fill=tuple(pal_rgb), outline="#555555")
                    brightness = (pal_rgb[0] * 0.299 + pal_rgb[1] * 0.587 + pal_rgb[2] * 0.114)
                    text_color = "white" if brightness < 128 else "black"
                    final_draw.text((x0 + final_cell_size / 4, y0 + final_cell_size / 4), code, fill=text_color, font=font)

            save_path_final_chart = f"{output_prefix}_最终图纸.png"
            final_img.save(save_path_final_chart)
            print(f">>> 成功: 最终图纸已保存至: {save_path_final_chart}")

            used_items = [(code, *used_palette[code]) for code in sorted(used_palette.keys())]
            if used_items:
                fig_height = max(2, len(used_items) * 0.7)
                plt.figure(figsize=(7, fig_height))
                ax = plt.gca()
                ax.axis("off")
                ax.set_title(f"色号对照表 (共{len(used_items)}色)", fontproperties="Microsoft YaHei")

                for idx, (code, hex_color, pal_rgb) in enumerate(used_items):
                    y = len(used_items) - idx - 1
                    rect = Rectangle((0, y), 0.8, 0.8, color=np.array(pal_rgb) / 255)
                    ax.add_patch(rect)
                    text = f"{code}  {hex_color}"
                    ax.text(1.0, y + 0.4, text, fontsize=11, va="center", fontproperties="Arial")

                ax.set_xlim(0, 4.5)
                ax.set_ylim(-0.1, len(used_items) - 0.1)
                plt.tight_layout()
                save_path_final_legend = f"{output_prefix}_最终色号对照.png"
                plt.savefig(save_path_final_legend)
                print(f">>> 成功: 最终色号对照已保存至: {save_path_final_legend}")
    else:
        print(f"未找到色卡清单文件: {palette_path}，跳过色号映射。")

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
            color_tuple = tuple(int(x) for x in color_arr)
            cluster_idx = color_to_cluster.get(color_tuple)
            color = merged_colors[cluster_idx] if cluster_idx is not None else color_tuple
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
    if len(merged_colors) > 0:
        # 根据颜色数量动态调整图例高度
        fig_height = max(2, len(merged_colors) * 0.7)
        plt.figure(figsize=(7, fig_height))
        ax = plt.gca()
        ax.axis('off')
        ax.set_title(f"Mard色卡对照表 (共{len(merged_colors)}色)", fontproperties="Microsoft YaHei")
        
        for idx, (cid, rgb, hex_c) in enumerate(legend_info):
            y = len(merged_colors) - idx - 1
            # 绘制色块
            rect = Rectangle((0, y), 0.8, 0.8, color=np.array(rgb) / 255)
            ax.add_patch(rect)
            # 绘制文字说明
            text = f"ID: [{cid}]  RGB: {rgb}"
            ax.text(1.0, y + 0.4, text, fontsize=11, va='center', fontproperties="Arial")
            ax.text(3.9, y + 0.4, "<- 对应你的Mard色卡", fontsize=9, color="gray", va='center', fontproperties="Microsoft YaHei")
            
        ax.set_xlim(0, 5.2)
        ax.set_ylim(-0.1, len(merged_colors) - 0.1)
        plt.tight_layout()
        save_path_legend = f"{output_prefix}_色卡对照.png"
        plt.savefig(save_path_legend)
        print(f">>> 成功: 色卡对照表已保存至: {save_path_legend}")
    else:
        print("未检测到任何有效颜色，跳过生成图例。")

# --- 执行部分 ---
if __name__ == "__main__":
    # 请确保文件名正确
    image_file = "E:\\_ComputerLearning\\7_Programming_Python\\Code_Python\\03_LittleCoding\\06_PixelWork\\真嗣拼豆_去背景.png"
    # 运行主函数，output_prefix 可以修改为你想要的文件名前缀
    generate_bead_pattern_with_selection(image_file, bead_size=20, output_prefix="真嗣拼豆", color_tolerance=8)