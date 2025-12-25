"""
示例：Seaborn 高级绘图演示

包含演示：
- 小提琴图（violinplot）：显示数据分布及其概率密度
- 箱线图（boxplot）：显示数据的分位数及异常值
- 回归模型图（lmplot）：显示变量间的线性关系及回归线
- 成对图（pairplot）：显示多变量间的两两关系
- Seaborn的优势：语法简洁，内置美观调色板

运行：
    python seaborn_advanced_demo.py

依赖：
    pip install seaborn matplotlib numpy pandas scikit-learn

作者：自动生成示例（中文注释）
"""

try:
    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.datasets import make_regression, load_iris
    SEABORN_AVAILABLE = True
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    print("警告：seaborn 或 scikit-learn 未安装，跳过相关演示")
    SEABORN_AVAILABLE = False
    # 尝试导入基础库
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        MATPLOTLIB_AVAILABLE = True
    except ImportError:
        MATPLOTLIB_AVAILABLE = False
        # 不设置 plt = None, np = None, pd = None，避免 Pylance 类型推断问题
import os

# 设置Seaborn样式
if SEABORN_AVAILABLE:
    sns.set_style("whitegrid")  # 设置背景样式
    sns.set_palette("husl")     # 设置颜色调色板

# 设置中文字体支持
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
    parser = argparse.ArgumentParser(description='Seaborn 高级绘图演示')
    parser.add_argument('--save-images', action='store_true',
                       help='保存生成的图片文件（默认不保存）')
    return parser.parse_args()


def ensure_dir(dir_name):
    """确保目录存在"""
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def demo_violinplot():
    """演示小提琴图"""
    print('--- 小提琴图 (violinplot) ---')

    if not SEABORN_AVAILABLE:
        print('跳过小提琴图演示（需要 seaborn）')
        return

    # 创建示例数据：不同部门的员工薪资
    np.random.seed(42)
    data = {
        '部门': ['技术部'] * 50 + ['销售部'] * 50 + ['市场部'] * 50,
        '薪资': (
            np.random.normal(15000, 3000, 50).tolist() +  # 技术部：均值15000，标准差3000
            np.random.normal(12000, 2500, 50).tolist() +  # 销售部：均值12000，标准差2500
            np.random.normal(10000, 2000, 50).tolist()    # 市场部：均值10000，标准差2000
        )
    }

    df = pd.DataFrame(data)

    # 创建小提琴图
    plt.figure(figsize=(10, 6))

    ax = sns.violinplot(x='部门', y='薪资', data=df,
                       hue='部门', palette='Set3', inner='quartile', legend=False)

    # 设置标题和标签
    ax.set_title('各部门薪资分布小提琴图', fontsize=16, fontweight='bold')
    ax.set_xlabel('部门', fontsize=12)
    ax.set_ylabel('薪资（元）', fontsize=12)

    # 添加数值统计
    for i, dept in enumerate(['技术部', '销售部', '市场部']):
        dept_data = df[df['部门'] == dept]['薪资']
        mean_val = dept_data.mean()
        plt.text(i, mean_val + 500, f'均值: {mean_val:.0f}',
                ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    ensure_dir('seaborn_advanced')
    plt.savefig('seaborn_advanced/violinplot_demo.png', dpi=150, bbox_inches='tight')
    print('小提琴图已保存为 seaborn_advanced/violinplot_demo.png')

    if not SAVE_ONLY:
        plt.show()
    plt.close()

    print('小提琴图特点：')
    print('- 显示数据分布的形状和密度')
    print('- 白色箱子显示四分位数范围')
    print('- 黑色线条显示中位数')
    print('- 适合比较多个类别的分布')
    print()


def demo_boxplot():
    """演示箱线图"""
    print('--- 箱线图 (boxplot) ---')

    if not SEABORN_AVAILABLE:
        print('跳过箱线图演示（需要 seaborn 和 scikit-learn）')
        return

    # 使用模拟的iris数据集
    np.random.seed(42)
    # 模拟iris数据：3个品种，每个有4个特征
    data = []
    feature_names = ['sepal length', 'sepal width', 'petal length', 'petal width']
    species_names = ['setosa', 'versicolor', 'virginica']

    for species_idx, species in enumerate(species_names):
        for _ in range(50):
            if species == 'setosa':
                features = [
                    np.random.normal(5.0, 0.3),  # sepal length
                    np.random.normal(3.4, 0.3),  # sepal width
                    np.random.normal(1.5, 0.2),  # petal length
                    np.random.normal(0.2, 0.1)   # petal width
                ]
            elif species == 'versicolor':
                features = [
                    np.random.normal(5.9, 0.5),
                    np.random.normal(2.8, 0.3),
                    np.random.normal(4.3, 0.5),
                    np.random.normal(1.3, 0.2)
                ]
            else:  # virginica
                features = [
                    np.random.normal(6.6, 0.6),
                    np.random.normal(3.0, 0.3),
                    np.random.normal(5.6, 0.5),
                    np.random.normal(2.0, 0.3)
                ]
            data.append(features + [species])

    df = pd.DataFrame(data, columns=feature_names + ['species'])

    # 创建箱线图
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('鸢尾花数据集特征箱线图', fontsize=16, fontweight='bold')

    colors = ['lightblue', 'lightgreen', 'lightcoral', 'gold']

    for i, (feature, color) in enumerate(zip(feature_names, colors)):
        ax = axes[i//2, i%2]

        # 绘制箱线图
        sns.boxplot(x='species', y=feature, data=df, ax=ax,
                   hue='species', palette='Set2', width=0.6, legend=False)

        ax.set_title(f'{feature} by Species', fontsize=12, fontweight='bold')
        ax.set_xlabel('Species', fontsize=10)
        ax.set_ylabel(feature, fontsize=10)

        # 添加网格
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('seaborn_advanced/boxplot_demo.png', dpi=150, bbox_inches='tight')
    print('箱线图已保存为 seaborn_advanced/boxplot_demo.png')

    if not SAVE_ONLY:
        plt.show()
    plt.close()

    print('箱线图特点：')
    print('- 箱子显示四分位数范围（Q1-Q3）')
    print('- 中间线显示中位数（Q2）')
    print('- 须线显示数据范围')
    print('- 点显示异常值')
    print('- 适合检测异常值和比较分布')
    print()


def demo_lmplot():
    """演示回归模型图"""
    print('--- 回归模型图 (lmplot) ---')

    if not SEABORN_AVAILABLE:
        print('跳过回归模型图演示（需要 seaborn）')
        return

    # 生成模拟回归数据
    np.random.seed(42)
    n_samples = 200

    # 线性关系数据
    x_linear = np.random.uniform(0, 10, n_samples)
    y_linear = 2 * x_linear + 1 + np.random.normal(0, 2, n_samples)

    # 二次关系数据
    x_quad = np.random.uniform(0, 10, n_samples)
    y_quad = 0.5 * x_quad**2 - 2 * x_quad + 5 + np.random.normal(0, 3, n_samples)

    # 创建DataFrame
    df_linear = pd.DataFrame({'x': x_linear, 'y': y_linear})
    df_quad = pd.DataFrame({'x': x_quad, 'y': y_quad})

    # 创建回归图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('回归模型图示例', fontsize=16, fontweight='bold')

    # 线性回归
    sns.regplot(x='x', y='y', data=df_linear, ax=ax1,
                scatter_kws={'alpha':0.6, 'color':'blue'},
                line_kws={'color':'red', 'linewidth':2})

    ax1.set_title('线性回归', fontsize=14, fontweight='bold')
    ax1.set_xlabel('X变量')
    ax1.set_ylabel('Y变量')
    ax1.grid(True, alpha=0.3)

    # 多项式回归（二次）
    sns.regplot(x='x', y='y', data=df_quad, ax=ax2, order=2,
                scatter_kws={'alpha':0.6, 'color':'green'},
                line_kws={'color':'red', 'linewidth':2})

    ax2.set_title('多项式回归（二次）', fontsize=14, fontweight='bold')
    ax2.set_xlabel('X变量')
    ax2.set_ylabel('Y变量')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('seaborn_advanced/lmplot_demo.png', dpi=150, bbox_inches='tight')
    print('回归模型图已保存为 seaborn_advanced/lmplot_demo.png')

    if not SAVE_ONLY:
        plt.show()
    plt.close()

    print('回归模型图特点：')
    print('- 显示变量间的线性关系')
    print('- 自动拟合回归线')
    print('- 显示置信区间')
    print('- 支持多项式回归（order参数）')
    print()


def demo_pairplot():
    """演示成对图"""
    print('--- 成对图 (pairplot) ---')

    if not SEABORN_AVAILABLE:
        print('跳过成对图演示（需要 seaborn 和 scikit-learn）')
        return

    # 使用模拟的iris数据集
    np.random.seed(42)
    data = []
    feature_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    species_names = ['setosa', 'versicolor', 'virginica']

    for species_idx, species in enumerate(species_names):
        for _ in range(50):
            if species == 'setosa':
                features = [
                    np.random.normal(5.0, 0.3),  # sepal length
                    np.random.normal(3.4, 0.3),  # sepal width
                    np.random.normal(1.5, 0.2),  # petal length
                    np.random.normal(0.2, 0.1)   # petal width
                ]
            elif species == 'versicolor':
                features = [
                    np.random.normal(5.9, 0.5),
                    np.random.normal(2.8, 0.3),
                    np.random.normal(4.3, 0.5),
                    np.random.normal(1.3, 0.2)
                ]
            else:  # virginica
                features = [
                    np.random.normal(6.6, 0.6),
                    np.random.normal(3.0, 0.3),
                    np.random.normal(5.6, 0.5),
                    np.random.normal(2.0, 0.3)
                ]
            data.append(features + [species])

    df = pd.DataFrame(data, columns=feature_names + ['species'])

    # 创建成对图
    plt.figure(figsize=(12, 10))

    pair_plot = sns.pairplot(df, hue='species', palette='Set1',
                           diag_kind='kde',  # 对角线使用核密度估计
                           plot_kws={'alpha': 0.6},
                           diag_kws={'alpha': 0.7})

    pair_plot.fig.suptitle('鸢尾花数据集特征成对关系图', fontsize=16, fontweight='bold', y=1.02)

    plt.tight_layout()
    plt.savefig('seaborn_advanced/pairplot_demo.png', dpi=150, bbox_inches='tight')
    print('成对图已保存为 seaborn_advanced/pairplot_demo.png')

    if not SAVE_ONLY:
        plt.show()
    plt.close()

    print('成对图特点：')
    print('- 显示所有数值变量间的两两关系')
    print('- 对角线显示单变量分布')
    print('- 颜色编码不同类别')
    print('- 适合探索性数据分析')
    print('- 可以快速发现变量间的相关性和模式')
    print()


def demo_seaborn_advantages():
    """演示Seaborn的优势：语法简洁，美观调色板"""
    print('--- Seaborn 优势演示 ---')

    if not SEABORN_AVAILABLE:
        print('跳过 Seaborn 优势演示（需要 seaborn）')
        return

    # 创建比较数据
    np.random.seed(42)
    categories = ['A', 'B', 'C', 'D', 'E']
    values1 = np.random.randint(10, 50, 5)
    values2 = np.random.randint(15, 45, 5)

    df = pd.DataFrame({
        'category': categories * 2,
        'value': np.concatenate([values1, values2]),
        'group': ['Group1'] * 5 + ['Group2'] * 5
    })

    # Seaborn版本（简洁语法）
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    ax1 = sns.barplot(x='category', y='value', hue='group', data=df, palette='husl')
    ax1.set_title('Seaborn版本（简洁语法）', fontsize=12, fontweight='bold')
    ax1.set_xlabel('类别')
    ax1.set_ylabel('数值')
    ax1.legend(title='分组')

    # Matplotlib版本（繁琐语法）- 为了对比
    plt.subplot(1, 2, 2)

    x = np.arange(len(categories))
    width = 0.35

    bars1 = plt.bar(x - width/2, values1, width, label='Group1', alpha=0.8, color='skyblue')
    bars2 = plt.bar(x + width/2, values2, width, label='Group2', alpha=0.8, color='lightgreen')

    plt.xlabel('类别')
    plt.ylabel('数值')
    plt.title('Matplotlib版本（繁琐语法）', fontsize=12, fontweight='bold')
    plt.xticks(x, categories)
    plt.legend(title='分组')

    # 添加数值标签
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('seaborn_advanced/seaborn_advantages.png', dpi=150, bbox_inches='tight')
    print('Seaborn优势对比图已保存为 seaborn_advanced/seaborn_advantages.png')

    if not SAVE_ONLY:
        plt.show()
    plt.close()

    print('Seaborn优势：')
    print('1. 语法简洁：一行代码即可创建复杂图表')
    print('2. 自动美化：内置美观调色板和样式')
    print('3. 数据导向：直接使用DataFrame和列名')
    print('4. 统计功能：自动添加统计信息和置信区间')
    print('5. 集成Pandas：无缝配合数据处理')
    print()


def cleanup():
    """清理生成的图片文件"""
    image_dir = 'seaborn_advanced'
    if os.path.exists(image_dir):
        import shutil
        shutil.rmtree(image_dir)
        print('清理图片目录完成')


def main():
    print('=' * 50)
    print('Seaborn 高级绘图演示')
    print('=' * 50)
    print()

    # 解析命令行参数
    args = parse_arguments()

    if not SEABORN_AVAILABLE:
        print('seaborn 未安装，无法运行高级绘图演示')
        print('请运行：pip install seaborn matplotlib numpy pandas scikit-learn')
        return

    try:
        demo_violinplot()
        demo_boxplot()
        demo_lmplot()
        demo_pairplot()
        demo_seaborn_advantages()

        print('所有Seaborn图表已生成并保存为PNG文件')
        if SAVE_ONLY:
            print('注意：当前环境为无GUI模式，所有图表已保存为文件')

    except ImportError as e:
        print(f'导入错误：{e}')
        print('请安装必要的包：pip install seaborn matplotlib numpy pandas scikit-learn')
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