# Renamer2

将中间格式 `{appname}_{senary}_{new_id}_{dul_times}` 重命名为最终格式 `{appname}_{new_id}_{dul_times}`。

## 功能

- 合并 `{senary}_{new_id}` 为新的 `new_id`，从 1 开始递增。
- 保留 `{dul_times}` 不变。
- 扫描 `dataset_*` 目录，支持递归处理。

> 假设：`senary` 和 `new_id` 不包含下划线，`appname` 可能包含下划线。

## 使用方法

在包含多个 `dataset_*` 子目录的根目录执行：

```bash
python renamer2.py "path\to\root"
```

只查看将要执行的操作：

```bash
python renamer2.py "path\to\root" --dry-run
```

递归扫描子目录：

```bash
python renamer2.py "path\to\root" --recursive
```

## 测试

```bash
python -m unittest discover -s tests
```
