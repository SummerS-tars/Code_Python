# Cleaner and Renamer 1

用于清理并重命名 `process_1` 目录中的图片与文本文件。

## 功能

- 以 `*_visualized.jpg` 为准，删除缺少任意一项（普通图片或 `.txt`）的文件组。
- 对保留下来的文件组重新编号：
    - 原始 `id` 在同一 `appname` 下收集后按顺序重新编号为 `new_id`。
    - 同一 `appname + 原始 id` 下的 `dul_times` 重新编号为 `new_dul_times`。
- 文件仍保留在原目录，仅改名。

> 假设：`id` 和 `dul_times` 不包含下划线，`appname` 可能包含下划线。

> 说明：脚本会自动忽略以 `.__tmp__` 开头的临时文件（可能来自上一次中断的重命名）。

## 使用方法

```bash
python cleaner_renamer1.py "path\to\process_1"
```

查看将要执行的操作：

```bash
python cleaner_renamer1.py "path\to\process_1" --dry-run
```

## 统计脚本

统计以下信息：

- 当前收集到的 app 列表
- 每个 app 的数据组数量（以完整三件套为准）
- 每个 app 内 duplicate times 最大为 1 的 id 占比
- 每个 app 的总数据量（duplicate times 全部计数）与所有 app 汇总

```bash
python dataset_stats.py "path\to\process_1"
```

递归扫描子目录并输出 CSV：

```bash
python dataset_stats.py "path\to\process_1" --recursive --output "stats.csv"
```

## 输出示例

```text
完成：删除 3 个文件，重命名 6 个文件，保留 2 组文件。
```

## 测试

```bash
python -m unittest discover -s tests
```
