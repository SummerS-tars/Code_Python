# Selector4

数据分类选择器：按规则将数据集划分为训练集与验证集，并保持源文件不变。

## 功能

- 扫描 `dataset_*` 目录，支持递归处理。
- 根据 `dul_times` 最大值区分数据类型。
    - 单张（最大值 = 1）：全部进入训练集。
    - 多张（最大值 > 1）：
        - 当数量 $\le$ `small_group_threshold`：按概率抽取一张进入验证集。
        - 当数量 $>$ `small_group_threshold`：按比例划分进验证集（至少一张）。
- 输出标准目录结构（images/labels/visualized + data/val）。
- 提供 `dry-run` 模式。
- 提供同名文件检测与重排脚本（可选）。

## 目录结构

```txt
dataset
├── images
│   ├── data
│   └── val
├── labels
│   ├── data
│   └── val
└── visualized
    ├── data
    └── val
```

## 配置文件

`config.json` 示例：

```json
{
  "val_ratio": 0.1,
  "prob_pick_single_from_small_multi": 0.2,
  "small_group_threshold": 3,
  "random_seed": 42
}
```

- `val_ratio`: 大样本组（数量 $>$ `small_group_threshold`）划入验证集的比例。
- `prob_pick_single_from_small_multi`: 2~`small_group_threshold` 张样本中抽取一张进入验证集的概率。
- `small_group_threshold`: 小样本分界值，默认 3。
- `random_seed`: 随机种子，保证可复现。

## 使用方法

划分训练/验证集：

```bash
python selector4.py "path\to\root"
```

指定输出目录：

```bash
python selector4.py "path\to\root" --output "path\to\dataset"
```

递归扫描：

```bash
python selector4.py "path\to\root" --recursive
```

只预览：

```bash
python selector4.py "path\to\root" --dry-run
```

## 预处理：大小写统一 + new_id 重排

当不同数据集出现大小写不一致（如 `TaoBao` / `taobao`）时，
请先使用预处理脚本生成中间备份目录（源目录不改动）：

```bash
python preprocess_case_renumber.py "path\to\root" --recursive --output "path\to\backup"
```

预处理完成后，请使用备份目录作为 `selector4.py` 的输入。

## 同名文件检测/重排（可选）

仅检测同名文件：

```bash
python check_collision_renumber.py "path\to\root" --recursive
```

执行重排 new_id：

```bash
python check_collision_renumber.py "path\to\root" --recursive --fix --dry-run
```

## 测试

```bash
python -m unittest discover -s tests
```
