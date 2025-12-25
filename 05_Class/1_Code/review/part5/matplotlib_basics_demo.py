"""
示例：Matplotlib 基础绘图演示

包含演示：
- 图表结构（Figure, Axes, Axis, Subplot）
- 绘图流程（准备数据、绘制、保存/显示）
- 基础图形：scatter, bar, hist, plot, pie
- 子图和多图布局

运行：
    python matplotlib_basics_demo.py

依赖：
    pip install matplotlib numpy pandas

注意：如果在无GUI环境中运行，可能需要设置后端：
    import matplotlib
    matplotlib.use('Agg')  # 使用非交互式后端

作者：自动生成示例（中文注释）
"""

try:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    print("警告：matplotlib 未安装，跳过绘图演示")
    MATPLOTLIB_AVAILABLE = False
    # 不设置 plt = None, np = None, pd = None，避免 Pylance 类型推断问题
import os

import os

# 设置中文字体支持（如果有中文字体的话）
if MATPLOTLIB_AVAILABLE:
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

# 如果在无GUI环境中，设置后端
try:
    if MATPLOTLIB_AVAILABLE:
        import matplotlib
        matplotlib.use('Agg')
    SAVE_ONLY = True
except:
    SAVE_ONLY = False


def parse_arguments():
    """解析命令行参数"""
    import argparse
    parser = argparse.ArgumentParser(description='Matplotlib 基础绘图演示')
    parser.add_argument('--save-images', action='store_true',
                       help='保存生成的图片文件（默认不保存）')
    return parser.parse_args()


def ensure_dir(dir_name):
    """确保目录存在"""
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def demo_chart_structure():
    """演示图表结构"""
    print('--- 图表结构演示 ---')

    # 创建Figure和Axes
    fig, ax = plt.subplots(figsize=(8, 6))

    # 设置标题和标签
    ax.set_title('图表结构示例', fontsize=16, fontweight='bold')
    ax.set_xlabel('X轴标签')
    ax.set_ylabel('Y轴标签')

    # 添加网格
    ax.grid(True, alpha=0.3)

    # 添加文本注释
    ax.text(0.5, 0.5, '这是Axes区域', ha='center', va='center',
            transform=ax.transAxes, fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # 保存图表
    ensure_dir('matplotlib_basics')
    plt.savefig('matplotlib_basics/chart_structure.png', dpi=150, bbox_inches='tight')
    print('图表已保存为 matplotlib_basics/chart_structure.png')

    if not SAVE_ONLY:
        plt.show()
    plt.close()

    print('Figure: 整个图表容器')
    print('Axes: 坐标系区域')
    print('Axis: X轴和Y轴')
    print('Title: 图表标题')
    print('Labels: 轴标签')
    print()


def demo_scatter_plot():
    """演示散点图"""
    print('--- 散点图 (scatter) ---')

    # 生成随机数据
    np.random.seed(42)
    x = np.random.randn(100)
    y = 2 * x + np.random.randn(100) * 0.5
    sizes = np.random.randint(20, 200, 100)
    colors = np.random.rand(100)

    # 创建散点图
    fig, ax = plt.subplots(figsize=(10, 6))

    scatter = ax.scatter(x, y, s=sizes, c=colors, alpha=0.6, cmap='viridis')

    # 设置标题和标签
    ax.set_title('散点图示例', fontsize=16, fontweight='bold')
    ax.set_xlabel('X变量')
    ax.set_ylabel('Y变量')

    # 添加颜色条
    plt.colorbar(scatter, ax=ax, label='颜色值')

    # 添加网格
    ax.grid(True, alpha=0.3)

    plt.savefig('matplotlib_basics/scatter_plot.png', dpi=150, bbox_inches='tight')
    print('散点图已保存为 matplotlib_basics/scatter_plot.png')

    if not SAVE_ONLY:
        plt.show()
    plt.close()
    print()


def demo_bar_chart():
    """演示柱状图"""
    print('--- 柱状图 (bar) ---')

    # 准备数据
    categories = ['产品A', '产品B', '产品C', '产品D', '产品E']
    sales = [120, 150, 98, 175, 132]
    colors = ['skyblue', 'lightgreen', 'lightcoral', 'gold', 'violet']

    # 创建柱状图
    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(categories, sales, color=colors, alpha=0.8, width=0.6)

    # 添加数值标签
    for bar, value in zip(bars, sales):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{value}', ha='center', va='bottom', fontweight='bold')

    # 设置标题和标签
    ax.set_title('产品销售柱状图', fontsize=16, fontweight='bold')
    ax.set_xlabel('产品类别')
    ax.set_ylabel('销售额')

    # 设置Y轴范围
    ax.set_ylim(0, max(sales) * 1.1)

    # 添加网格
    ax.grid(True, axis='y', alpha=0.3)

    plt.savefig('matplotlib_basics/bar_chart.png', dpi=150, bbox_inches='tight')
    print('柱状图已保存为 matplotlib_basics/bar_chart.png')

    if not SAVE_ONLY:
        plt.show()
    plt.close()
    print()


def demo_histogram():
    """演示直方图"""
    print('--- 直方图 (hist) ---')

    # 生成正态分布数据
    np.random.seed(42)
    data1 = np.random.normal(50, 10, 1000)  # 均值50，标准差10
    data2 = np.random.normal(70, 15, 1000)  # 均值70，标准差15

    # 创建直方图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # 子图1：单个直方图
    ax1.hist(data1, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    ax1.set_title('单个数据集直方图', fontsize=14, fontweight='bold')
    ax1.set_xlabel('值')
    ax1.set_ylabel('频次')
    ax1.grid(True, alpha=0.3)

    # 子图2：多个数据集比较
    ax2.hist([data1, data2], bins=30, alpha=0.7, label=['数据集1', '数据集2'],
             color=['skyblue', 'lightgreen'], edgecolor='black')
    ax2.set_title('多个数据集直方图比较', fontsize=14, fontweight='bold')
    ax2.set_xlabel('值')
    ax2.set_ylabel('频次')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('matplotlib_basics/histogram.png', dpi=150, bbox_inches='tight')
    print('直方图已保存为 matplotlib_basics/histogram.png')

    if not SAVE_ONLY:
        plt.show()
    plt.close()
    print()


def demo_line_plot():
    """演示折线图"""
    print('--- 折线图 (plot) ---')

    # 准备时间序列数据
    months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
    sales_2023 = [120, 135, 148, 162, 175, 168, 185, 192, 178, 195, 210, 225]
    sales_2024 = [125, 142, 155, 168, 182, 175, 195, 205, 188, 202, 218, 235]

    # 创建折线图
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(months, sales_2023, marker='o', linestyle='-', linewidth=2,
            color='blue', label='2023年', markersize=6)
    ax.plot(months, sales_2024, marker='s', linestyle='--', linewidth=2,
            color='red', label='2024年', markersize=6)

    # 设置标题和标签
    ax.set_title('年度销售趋势对比', fontsize=16, fontweight='bold')
    ax.set_xlabel('月份')
    ax.set_ylabel('销售额（万元）')

    # 添加图例
    ax.legend()

    # 添加网格
    ax.grid(True, alpha=0.3)

    # 旋转X轴标签
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('matplotlib_basics/line_plot.png', dpi=150, bbox_inches='tight')
    print('折线图已保存为 matplotlib_basics/line_plot.png')

    if not SAVE_ONLY:
        plt.show()
    plt.close()
    print()


def demo_pie_chart():
    """演示饼图"""
    print('--- 饼图 (pie) ---')

    # 准备数据
    departments = ['技术部', '销售部', '市场部', '财务部', '人事部']
    budgets = [35, 25, 20, 12, 8]
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'gold', 'violet']
    explode = [0.1, 0, 0, 0, 0]  # 突出显示第一个扇形

    # 创建饼图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # 子图1：基础饼图
    wedges1, texts1, autotexts1 = ax1.pie(budgets, labels=departments, colors=colors,
                                         autopct='%1.1f%%', startangle=90, explode=explode)

    ax1.set_title('各部门预算分配（突出技术部）', fontsize=14, fontweight='bold')

    # 子图2：环形饼图
    wedges2, texts2, autotexts2 = ax2.pie(budgets, labels=departments, colors=colors,
                                         autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.3))

    ax2.set_title('各部门预算分配（环形图）', fontsize=14, fontweight='bold')

    # 调整字体大小
    for autotext in autotexts1 + autotexts2:
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')

    plt.tight_layout()
    plt.savefig('matplotlib_basics/pie_chart.png', dpi=150, bbox_inches='tight')
    print('饼图已保存为 matplotlib_basics/pie_chart.png')

    if not SAVE_ONLY:
        plt.show()
    plt.close()
    print()


def demo_subplots():
    """演示子图布局"""
    print('--- 子图和多图布局 ---')

    # 创建2x2的子图布局
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('多图布局示例', fontsize=16, fontweight='bold')

    # 子图1：散点图
    np.random.seed(42)
    x = np.random.randn(50)
    y = 2 * x + np.random.randn(50)
    ax1.scatter(x, y, alpha=0.6, color='blue')
    ax1.set_title('散点图')
    ax1.grid(True, alpha=0.3)

    # 子图2：柱状图
    categories = ['A', 'B', 'C', 'D']
    values = [10, 15, 7, 12]
    ax2.bar(categories, values, color='lightgreen', alpha=0.7)
    ax2.set_title('柱状图')
    ax2.grid(True, axis='y', alpha=0.3)

    # 子图3：直方图
    data = np.random.normal(0, 1, 200)
    ax3.hist(data, bins=20, alpha=0.7, color='lightcoral', edgecolor='black')
    ax3.set_title('直方图')
    ax3.grid(True, alpha=0.3)

    # 子图4：饼图
    sizes = [30, 25, 20, 15, 10]
    labels = ['A', 'B', 'C', 'D', 'E']
    ax4.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=90)
    ax4.set_title('饼图')

    plt.tight_layout()
    plt.savefig('matplotlib_basics/subplots_demo.png', dpi=150, bbox_inches='tight')
    print('子图布局已保存为 matplotlib_basics/subplots_demo.png')

    if not SAVE_ONLY:
        plt.show()
    plt.close()
    print()


def cleanup():
    """清理生成的图片文件"""
    image_dir = 'matplotlib_basics'
    if os.path.exists(image_dir):
        import shutil
        shutil.rmtree(image_dir)
        print('清理图片目录完成')


def main():
    print('=' * 50)
    print('Matplotlib 基础绘图演示')
    print('=' * 50)
    print()

    # 解析命令行参数
    args = parse_arguments()

    if not MATPLOTLIB_AVAILABLE:
        print('matplotlib 未安装，无法运行绘图演示')
        print('请运行：pip install matplotlib numpy pandas')
        return

    try:
        demo_chart_structure()
        demo_scatter_plot()
        demo_bar_chart()
        demo_histogram()
        demo_line_plot()
        demo_pie_chart()
        demo_subplots()

        print('所有图表已生成并保存为PNG文件')
        if SAVE_ONLY:
            print('注意：当前环境为无GUI模式，所有图表已保存为文件')

    except ImportError as e:
        print(f'导入错误：{e}')
        print('请安装必要的包：pip install matplotlib numpy pandas')
    except Exception as e:
        print(f'运行错误：{e}')
    finally:
        # 根据命令行参数决定是否清理图片
        if not args.save_images:
            cleanup()
        else:
            print('图片文件已保存，可在当前目录查看')
            print('下次运行时如需清理，请不使用 --save-images 参数')


if __name__ == '__main__':
    main()