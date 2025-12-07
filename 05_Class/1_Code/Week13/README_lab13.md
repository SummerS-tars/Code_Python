# Lab Week 13 实施方案：数据清洗与可视化

## 目标

- 安装 pandas 等必要库
- 选择并获取公开数据集（无需注册）
- 编写代码完成数据清洗（缺失/重复/异常值）
- 至少绘制三种图表展示分析结果
- 撰写简短报告总结发现

---

## 数据集选择方案

可选数据集（均可直接获取）：

1. Seaborn Titanic（泰坦尼克号乘客数据）
   - 获取方式：`seaborn.load_dataset('titanic')`
   - 字段：性别、舱位、年龄、票价、是否存活等
   - 优点：分类/数值字段都较丰富，适合演示缺失、异常与多类图表
2. Our World in Data（OWID）CO2 排放数据
   - 获取方式：CSV 直链
     - [owid-co2-data.csv](https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv)
   - 字段：国家、年份、各类排放指标
   - 优点：时间序列丰富，适合趋势线、分布与对比
3. UCI Wine（葡萄酒质量）
   - 获取方式：CSV 直链
     - [winequality-red.csv](https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv)
   - 字段：化学理化指标与质量评分
   - 优点：连续变量较多，适合相关性热力图与箱线图

推荐选择：Seaborn Titanic

- 无需下载文件，直接内置加载
- 分类与数值特征兼备，图表类型更丰富
- 数据量适中，清洗与绘图速度快

---

## 环境与依赖

需要的 Python 包：

- pandas
- numpy
- seaborn
- matplotlib
- (可选) plotly

Windows PowerShell 安装命令（建议在虚拟环境中执行）：

```pwsh
# 进入 Week13 目录（按需调整路径）
cd "e:/_ComputerLearning/7_Programming_Python/Code_Python/05_Class/1_Code/Week13"

# 创建并激活虚拟环境（可选）
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements_lab13.txt
```

---

## 实施步骤（代码逻辑）

1. 数据获取
   - 使用 `seaborn.load_dataset('titanic')` 加载数据为 `DataFrame`。

2. 初步探索
   - 查看维度与基本信息：`df.shape`, `df.info()`, `df.describe()`。
   - 统计缺失值分布：`df.isna().sum()`。

3. 数据清洗
   - 缺失值处理：
     - 数值列（如 `age`, `fare`）：可用中位数填充。
     - 分类列（如 `embarked`, `sex`, `class`）：用众数或“Unknown”填充。
   - 重复值处理：
     - 使用 `df.drop_duplicates(inplace=True)` 去重。
   - 异常值处理（以 `fare` 为例）：
     - 使用 IQR（四分位距）法：
       - 计算 Q1/Q3 与 IQR，定义上下界，截断或标记异常值。

4. 可视化（至少三种）
   - 分布图（直方图/核密度）：`age`、`fare` 的分布。
   - 分类对比图（条形图）：不同 `class` 或 `sex` 下的存活率。
   - 箱线图：`fare` 在不同 `class` 下的分布情况。
   - (可选) 相关性热力图：数值列之间的相关系数矩阵。

5. 结果输出
   - 将图表保存到本地 `figures/` 目录：`png` 文件。
   - 输出清洗前后关键统计对比：缺失值计数、重复条目数量、异常值处理影响。

6. 报告撰写（简短）
   - 数据来源与字段说明
   - 清洗策略（缺失/重复/异常值的处理方式）
   - 图表与发现（至少三图）
   - 局限与下一步（如加入时间轴、更多特征工程）

---

## 运行示例代码

```pwsh
# 激活虚拟环境（如果已创建）
.\.venv\Scripts\Activate.ps1

# 运行示例脚本
python lab13_data_cleaning.py
```

脚本会在 `figures/` 目录生成多张图表，并在控制台打印清洗前后的统计信息。

---

## 报告撰写要点（模板见 `lab13_report.md`）

- 数据集与字段简介
- 清洗方法与理由（缺失、重复、异常）
- 关键图表与洞察（配图 & 简述）
- 结论与建议（可扩展方向）

---

## 扩展方向（可选加分）

- 使用 Plotly 交互式图表（折线/散点/箱线图）
- 增加更多特征工程（如年龄分箱、派生指标）
- 多模型对比（如逻辑回归/随机森林预测存活）
