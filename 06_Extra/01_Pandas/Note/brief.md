# Pandas 学习

Pandas，Python中非常重要和流行的数据分析和处理库  

以下用于总结入门学习的经历及要点  

## 1. 工具

- venv环境  
- Jupyter Notebook：交互式笔记本  
    将Code、Output、Markdown三者进行了结合  

### 1.1. Jupyter Notebook 补充

Jupyter Notebook运行过程中  
相当于一个大内存状态机，所有Cell共享同一个内存空间  
请在充分理解这一点的基础上使用它  

Jupyter Notebook 最佳实践范式 (The Golden Standard)  
把你的 Notebook 想象成一篇技术文章,而不是一个草稿纸。

#### 1.1.1. 结构化布局 (The Standard Layout)

一个标准的 Notebook 应该严格遵守以下顺序：

- **Cell 1: 全局引用 (Imports & Config)**  
    - 把所有需要的库 (pandas, numpy, matplotlib) 都放在第一个格子里  
    - 把全局设置也放在这里（比如设置中文字体、设置显示的最大行数）  
    - 理由：任何读你代码的人（包括未来的你自己），看一眼开头就知道这个项目依赖什么环境  
    - C++ 类比：这就是你的 `#include` 和 `#define` 区域  

- **Cell 2: 全局常量 (Constants)**  
    - 定义文件路径、固定的阈值、硬编码的参数  
    - 示例：`FILE_PATH = "./data/dirty_coffee_sales.csv"`  

- **Cell 3: 数据加载 (Data Loading)**  
    - 读取文件这一步通常比较慢（如果文件很大的话），所以单独放在一个 Cell  
    - 读取完后，立刻在同一个 Cell 做简单的检查（如 `df.head()`）  

- **Cell 4+: 具体的逻辑/分析**  
    - 一个 Cell 只做一件事（原子化）

#### 1.1.2. 其他范式

- 函数式编程：  
    - 又称为"幂等性"  
    - 一个Cell无论运行多少次，结果都应该是一样的  

- "Restart & Run All" 测试：  
    - 完成工作提交或者关闭前，点击"Restart Kernel and Run All Cells"  
    - 防止乱序执行导致的隐藏的状态问题未被发现

- 善用富文本输出：  
    - 不要滥用 `print()`  
    - 直接把变量放在 Cell 的最后一行，Jupyter 会自动渲染输出  

## 2. 实践学习路径

### 2.1. 规划

根据一个小型项目进行分析开始学习：  
**连锁咖啡店的"故障"订单分析**  

### 2.2. Step 0: 准备流程

生成脏数据  

### 2.3. Step 1: 基础了解

理解数据基本形态

- **任务 A**：不要直接读取 CSV，先看上面的 `data` 字典。尝试手动创建一个 `Series`，只包含 `Product` 列的数据。
- **任务 B (索引实战)**：
    - 使用 `.loc` 找出标签（索引）为 3 的那行数据（看看是哪家店买了什么）。
    - 使用 `.iloc` 找出前 5 行、前 2 列的数据。

#### 2.3.1. 关键点

两个核心概念： **Series** 和 **DataFrame**  
可以认为是Pandas数据处理中的"原子"单位  

- **Series（序列）**：  
    - 实质：一维数组，每个数据点有一个 **标签（Label）**，也就是索引（Index）  
    - 特征：Series里的数据必须是同一类型的  
- **DataFrame（数据框）**：  
    - 实质：二维表格  
    - 关键点：DataFrame由多个Series拼接而成，每一列是一个Series，共享同一个 **Index（行索引）**  
    - 理解：类似于C++中的`std::vector<Series>`，或者说更像是一个结构体数组的视图  

### 2.4. Step 2: 数据加载与预览

将csv加载到DataFrame中成为可操作对象  

- **任务**：
    - 使用 `pd.read_csv()` 读取 `dirty_coffee_sales.csv` 并赋值给变量 `df`。
    - 运行 `df.head()` 看看前 5 行长什么样。
    - 关键步骤：运行 `df.info()`。
    - 观察点：看 `Price` 这一列，Non-Null Count 是多少？是不是少于总行数？（这就是你需要清洗的地方）。

### 2.5. Step 3: 数据清洗与处理

目标：把数据修好，否则无法计算收入。

**任务 A (处理重复值)**：

系统故障导致 Transaction_ID 为 102 的订单被记录了两次。

- 使用 `df.duplicated()` 检查重复项。
- 使用 `df.drop_duplicates()` 删除重复行，并更新 `df`。

**任务 B (处理缺失值)**：

你会发现 Mocha (摩卡) 的 Price 是 NaN (空值)。

- 假设摩卡的价格固定是 35.0 元。请使用 `df.fillna(35.0)` 填充缺失的价格。
- 进阶挑战：确认清洗后 `df.info()` 中所有列都没有缺失值。

**任务 C (数据转换)**：

老板不仅想要单价，还想知道每单的总价。

- 创建一个新列 `Total_Amount`，计算公式为：`df['Price'] * df['Quantity']`。

#### 2.5.1. 细节分析

这里在更新`df`时，使用了链式赋值（chained assignment）。  

以及我们会发现，删除重复值后，DataFrame的索引变得不连续了。  
实践中我们分两种情况处理：  

- 行号索引：  
    只是行号，那么一般在过滤、去重后重置索引  
    使用`df.reset_index(drop=True)`（或者在去重时后面直接加上`.reset_index(drop=True)`）  

- 标签索引：  
    如果索引有实际意义（比如用户ID、订单ID），那就保留原来的索引，不要重置。  

### 2.6. Step 4: 数据聚合与分析

回答老板的业务问题。

**任务 A (Groupby)**：

老板问："哪个分店（Branch）今天的总销售额最高？"

- 使用 `df.groupby('Branch')['Total_Amount'].sum()` 来计算。

**任务 B (数据透视)**：

老板问："每个分店卖得最好的产品是什么？"

- 使用 `pivot_table` 或 `groupby` 统计每个分店、每种产品的销量 (Quantity) 总和。

#### 补充

对于链式赋值（chained assignment）  
可能会导致代码比较长  
我们可以通过括号把它们包起来，分多行写  

```python
(
    df.groupby(['Branch', 'Product'], as_index=False)
      .agg(Total_Amount=('Total_Amount', 'sum'))
      .sort_values(by=['Branch', 'Total_Amount'], ascending=[True, False])
)
```
