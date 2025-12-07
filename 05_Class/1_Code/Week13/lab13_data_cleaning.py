import os
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------
# Lab 13: 数据清洗与可视化 - 示例脚本
# 数据集：Seaborn Titanic
# -----------------------------


def ensure_output_dir(dir_path: Path) -> None:
    dir_path.mkdir(parents=True, exist_ok=True)


def load_data() -> pd.DataFrame:
    """加载 Seaborn Titanic 数据集。"""
    df = sns.load_dataset('titanic')
    return df


def explore(df: pd.DataFrame) -> None:
    print("=== 原始数据维度 ===")
    print(df.shape)
    print("\n=== 数据基本信息 ===")
    print(df.info())
    print("\n=== 数值列统计描述 ===")
    print(df.describe())
    print("\n=== 缺失值统计（前10列） ===")
    print(df.isna().sum().sort_values(ascending=False).head(10))


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()

    # 缺失值处理
    # 数值列：用中位数填充；分类列：用众数或 Unknown 填充
    num_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df_clean.select_dtypes(exclude=[np.number]).columns.tolist()

    for col in num_cols:
        median_val = df_clean[col].median()
        df_clean[col] = df_clean[col].fillna(median_val)

    for col in cat_cols:
        mode_val = df_clean[col].mode().iloc[0] if not df_clean[col].mode().empty else 'Unknown'
        df_clean[col] = df_clean[col].fillna(mode_val)
        df_clean[col] = df_clean[col].astype(str)

    # 重复值处理
    dup_count_before = df_clean.duplicated().sum()
    df_clean = df_clean.drop_duplicates()
    dup_count_after = df_clean.duplicated().sum()

    print(f"重复值数量：清洗前 {dup_count_before}，清洗后 {dup_count_after}")

    # 异常值处理（以 fare 为例，使用 IQR 截断）
    if 'fare' in df_clean.columns:
        q1 = df_clean['fare'].quantile(0.25)
        q3 = df_clean['fare'].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        before_outliers = ((df_clean['fare'] < lower) | (df_clean['fare'] > upper)).sum()
        df_clean['fare'] = df_clean['fare'].clip(lower=lower, upper=upper)
        after_outliers = ((df_clean['fare'] < lower) | (df_clean['fare'] > upper)).sum()
        print(f"fare 异常值处理：IQR 下界 {lower:.2f} 上界 {upper:.2f}，处理前异常 {before_outliers}，处理后异常 {after_outliers}")

    return df_clean


def visualize(df: pd.DataFrame, out_dir: Path) -> None:
    """绘制至少三种图表并保存到 out_dir。"""
    sns.set(style="whitegrid", context="talk")

    # 1) age 分布图（直方图 + KDE）
    plt.figure(figsize=(8, 6))
    # 为了兼容类型检查（如 Pylance），改为传 data=DataFrame 与 x 列名
    sns.histplot(data=df, x='age', bins=30, kde=True, color='steelblue')
    plt.title('Age Distribution (Titanic)')
    plt.xlabel('Age')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(out_dir / '01_age_distribution.png')
    plt.close()

    # 2) 不同性别的存活率（条形图）
    plt.figure(figsize=(8, 6))
    survival_by_sex = df.groupby('sex')['survived'].mean().sort_values()
    # 避免 seaborn 0.14 的 FutureWarning（palette 需配合 hue），改用单色
    sns.barplot(x=survival_by_sex.index, y=survival_by_sex.values, color='steelblue')
    plt.title('Survival Rate by Sex')
    plt.xlabel('Sex')
    plt.ylabel('Survival Rate')
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(out_dir / '02_survival_rate_by_sex.png')
    plt.close()

    # 3) 不同舱位的票价分布（箱线图）
    plt.figure(figsize=(8, 6))
    # 避免 seaborn 0.14 的 FutureWarning，移除 palette（或使用 hue）
    sns.boxplot(x='class', y='fare', data=df)
    plt.title('Fare Distribution by Class')
    plt.xlabel('Class')
    plt.ylabel('Fare')
    plt.tight_layout()
    plt.savefig(out_dir / '03_fare_boxplot_by_class.png')
    plt.close()

    # 4) (可选) 数值列相关性热力图
    num_df = df.select_dtypes(include=[np.number])
    if not num_df.empty:
        plt.figure(figsize=(10, 8))
        corr = num_df.corr(numeric_only=True)
        sns.heatmap(corr, cmap='coolwarm', annot=False, linewidths=0.5)
        plt.title('Correlation Heatmap (Numeric Columns)')
        plt.tight_layout()
        plt.savefig(out_dir / '04_correlation_heatmap.png')
        plt.close()


def main():
    figures_dir = Path(__file__).parent / 'figures'
    ensure_output_dir(figures_dir)

    # 加载与探索
    df_raw = load_data()
    explore(df_raw)

    # 清洗
    print("\n=== 开始数据清洗 ===")
    df_clean = clean_data(df_raw)

    # 清洗后对比（缺失值）
    print("\n=== 清洗后缺失值统计（前10列） ===")
    print(df_clean.isna().sum().sort_values(ascending=False).head(10))

    # 可视化
    print("\n=== 开始绘图（保存到 figures/） ===")
    visualize(df_clean, figures_dir)
    print("绘图完成，文件已保存到:", figures_dir)


if __name__ == '__main__':
    main()
