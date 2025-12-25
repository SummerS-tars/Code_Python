"""
示例：Pandas 数据预处理演示

包含演示：
- 缺失值处理（isnull, dropna, fillna, ffill, bfill）
- 重复值处理（duplicated, drop_duplicates）
- 异常值处理（IQR法）
- 数据集成（merge, concat）
- 数据转换（标准化、离散化）
- 数据规约（PCA）

运行：
    python pandas_preprocessing_demo.py

依赖：
    pip install pandas numpy scikit-learn matplotlib seaborn

作者：自动生成示例（中文注释）
"""

try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except ImportError:
    print("警告：pandas 未安装，跳过数据预处理演示")
    PANDAS_AVAILABLE = False
    # 不设置 pd = None 和 np = None，避免 Pylance 类型推断问题

try:
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    from sklearn.decomposition import PCA
    SKLEARN_AVAILABLE = True
except ImportError:
    print("警告：scikit-learn 未安装，跳过相关演示")
    SKLEARN_AVAILABLE = False

import warnings
warnings.filterwarnings('ignore')


def parse_arguments():
    """解析命令行参数"""
    import argparse
    parser = argparse.ArgumentParser(description='Pandas 数据预处理演示')
    parser.add_argument('--save-images', action='store_true',
                       help='保存生成的图片文件（默认不保存）')
    return parser.parse_args()


def demo_missing_values():
    """演示缺失值处理"""
    print('--- 缺失值处理 ---')

    # 创建包含缺失值的数据
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, np.nan, 30, 35, np.nan],
        'salary': [50000, 60000, np.nan, 80000, 70000],
        'department': ['IT', 'HR', 'IT', np.nan, 'Finance']
    }

    df = pd.DataFrame(data)
    print('原始数据：')
    print(df)
    print()

    # 检测缺失值
    print('缺失值检测：')
    print(df.isnull())
    print(f'每列缺失值数量：\n{df.isnull().sum()}')
    print()

    # 删除缺失值
    print('删除包含缺失值的行：')
    df_dropna = df.dropna()
    print(df_dropna)
    print()

    # 填充缺失值
    print('填充缺失值：')
    df_fillna = df.copy()

    # 用均值填充数值列
    df_fillna['age'] = df_fillna['age'].fillna(df_fillna['age'].mean())
    df_fillna['salary'] = df_fillna['salary'].fillna(df_fillna['salary'].mean())

    # 用特定值填充分类列
    df_fillna['department'] = df_fillna['department'].fillna('Unknown')

    print(df_fillna)
    print()

    # 前向填充和后向填充
    print('前向填充（ffill）：')
    df_ffill = df.copy()
    df_ffill = df_ffill.ffill()
    print(df_ffill)
    print()

    print('后向填充（bfill）：')
    df_bfill = df.copy()
    df_bfill = df_bfill.bfill()
    print(df_bfill)
    print()


def demo_duplicates():
    """演示重复值处理"""
    print('--- 重复值处理 ---')

    # 创建包含重复值的数据
    data = {
        'name': ['Alice', 'Bob', 'Alice', 'Charlie', 'Bob', 'David'],
        'age': [25, 30, 25, 35, 30, 40],
        'department': ['IT', 'HR', 'IT', 'Finance', 'HR', 'IT']
    }

    df = pd.DataFrame(data)
    print('原始数据：')
    print(df)
    print()

    # 检测重复值
    print('检测重复行：')
    print(df.duplicated())
    print()

    # 删除重复值
    print('删除重复行（保留第一次出现）：')
    df_dedup = df.drop_duplicates()
    print(df_dedup)
    print()

    # 基于特定列删除重复值
    print('基于 name 列删除重复值：')
    df_dedup_name = df.drop_duplicates(subset=['name'])
    print(df_dedup_name)
    print()


def demo_outliers():
    """演示异常值处理（IQR法）"""
    print('--- 异常值处理（IQR法）---')

    # 创建包含异常值的数据
    np.random.seed(42)
    data = {
        'value': [10, 12, 11, 13, 12, 14, 100, 11, 13, 12, 15, 200, 13, 11, 12]
    }

    df = pd.DataFrame(data)
    print('原始数据：')
    print(df.describe())
    print()

    # 计算IQR
    Q1 = df['value'].quantile(0.25)
    Q3 = df['value'].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    print(f'Q1: {Q1}, Q3: {Q3}, IQR: {IQR}')
    print(f'下界: {lower_bound}, 上界: {upper_bound}')
    print()

    # 识别异常值
    outliers = df[(df['value'] < lower_bound) | (df['value'] > upper_bound)]
    print('异常值：')
    print(outliers)
    print()

    # 移除异常值
    df_clean = df[(df['value'] >= lower_bound) & (df['value'] <= upper_bound)]
    print('移除异常值后的数据：')
    print(df_clean.describe())
    print()


def demo_data_integration():
    """演示数据集成"""
    print('--- 数据集成 ---')

    # 创建两个数据集
    df1 = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['Alice', 'Bob', 'Charlie', 'David'],
        'department': ['IT', 'HR', 'Finance', 'IT']
    })

    df2 = pd.DataFrame({
        'id': [1, 2, 3, 5],
        'salary': [50000, 60000, 70000, 80000],
        'experience': [2, 3, 4, 5]
    })

    print('数据集1：')
    print(df1)
    print()
    print('数据集2：')
    print(df2)
    print()

    # 合并（merge）
    print('内连接合并（inner join）：')
    df_merged = pd.merge(df1, df2, on='id', how='inner')
    print(df_merged)
    print()

    print('左连接合并（left join）：')
    df_left = pd.merge(df1, df2, on='id', how='left')
    print(df_left)
    print()

    # 堆叠（concat）
    df3 = pd.DataFrame({
        'id': [6, 7],
        'name': ['Eve', 'Frank'],
        'department': ['Marketing', 'Sales']
    })

    print('原始数据集1：')
    print(df1)
    print()
    print('要堆叠的数据集3：')
    print(df3)
    print()

    print('垂直堆叠（concat）：')
    df_concat = pd.concat([df1, df3], ignore_index=True)
    print(df_concat)
    print()


def demo_data_transformation():
    """演示数据转换"""
    print('--- 数据转换 ---')

    if not SKLEARN_AVAILABLE:
        print('跳过标准化演示（需要 scikit-learn）')
        return

    # 创建数值数据
    data = {
        'feature1': [10, 20, 30, 40, 50],
        'feature2': [100, 200, 300, 400, 500],
        'age': [25, 30, 35, 40, 45]
    }

    df = pd.DataFrame(data)
    print('原始数据：')
    print(df)
    print()

    # Z-score 标准化
    print('Z-score 标准化：')
    scaler = StandardScaler()
    df_standardized = pd.DataFrame(
        scaler.fit_transform(df),
        columns=df.columns
    )
    print(df_standardized)
    print(f'均值: {df_standardized.mean().round(6).tolist()}')
    print(f'标准差: {df_standardized.std().round(6).tolist()}')
    print()

    # Min-Max 标准化
    print('Min-Max 标准化：')
    minmax_scaler = MinMaxScaler()
    df_normalized = pd.DataFrame(
        minmax_scaler.fit_transform(df),
        columns=df.columns
    )
    print(df_normalized)
    print()

    # 离散化（分箱）
    print('年龄离散化（pd.cut）：')
    age_bins = [0, 30, 40, 100]
    age_labels = ['青年', '中年', '老年']
    df['age_category'] = pd.cut(df['age'], bins=age_bins, labels=age_labels)
    print(df[['age', 'age_category']])
    print()

    print('年龄离散化（pd.qcut - 等频分箱）：')
    df['age_quartile'] = pd.qcut(df['age'], q=3, labels=['低', '中', '高'])
    print(df[['age', 'age_quartile']])
    print()


def demo_pca():
    """演示主成分分析（PCA）"""
    print('--- 数据规约：主成分分析（PCA）---')

    if not SKLEARN_AVAILABLE:
        print('跳过 PCA 演示（需要 scikit-learn）')
        return

    # 创建高维数据
    np.random.seed(42)
    data = np.random.randn(50, 4)  # 50个样本，4个特征
    df = pd.DataFrame(data, columns=['feature1', 'feature2', 'feature3', 'feature4'])

    print('原始数据形状：', df.shape)
    print('原始数据描述：')
    print(df.describe())
    print()

    # 应用PCA
    pca = PCA(n_components=2)  # 降维到2维
    principal_components = pca.fit_transform(df)

    df_pca = pd.DataFrame(
        principal_components,
        columns=['PC1', 'PC2']
    )

    print('PCA后数据形状：', df_pca.shape)
    print('主成分数据：')
    print(df_pca.head())
    print()

    # 解释方差比
    print('各主成分解释的方差比：')
    print(pca.explained_variance_ratio_)
    print(f'前2个主成分解释的总方差: {pca.explained_variance_ratio_.sum():.3f}')
    print()


def main():
    print('=' * 50)
    print('Pandas 数据预处理演示')
    print('=' * 50)
    print()

    # 解析命令行参数（保持与其他演示文件一致）
    args = parse_arguments()

    if not PANDAS_AVAILABLE:
        print('pandas 未安装，无法运行数据预处理演示')
        print('请运行：pip install pandas numpy')
        return

    try:
        demo_missing_values()
        demo_duplicates()
        demo_outliers()
        demo_data_integration()
        demo_data_transformation()
        demo_pca()

    except ImportError as e:
        print(f'导入错误：{e}')
        print('请安装必要的包：pip install pandas numpy scikit-learn matplotlib seaborn')
    except Exception as e:
        print(f'运行错误：{e}')


if __name__ == '__main__':
    main()