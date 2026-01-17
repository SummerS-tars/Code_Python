# GUI 数据集筛选与重命名

该脚本用于在 `dataset_*` 目录下：

1. 以 `*_visualized` 图片为基准过滤文件：
   - 删除没有对应 `*_visualized` 图片的普通图片与 `.txt` 文件。
2. 按规则重命名（不移动目录）：
   - `{appname}_{senary}_{new_id}_{dul_times}.jpg`
   - `{appname}_{senary}_{new_id}_{dul_times}_visualized.jpg`
   - `{appname}_{senary}_{new_id}_{dul_times}.txt`

## 命名规则说明

- `appname`：来自 `dataset_{appname}` 目录名。
- `senary`：来自原文件名中的场景。
- `new_id`：按 visualized 图片排序后，从 1 递增；同一 `orig_id` 共享同一 `new_id`。
- `dul_times`：同一 `senary + orig_id` 的重复次数，从 1 递增。

排序规则：`orig_id`、日期、时间、场景。

## 使用方式

### 1. 直接处理某个 `dataset_*` 目录

```powershell
python .\gui_dataset_filter_renamer.py .\dataset_wechat
```

### 2. 处理父目录下所有 `dataset_*` 目录

```powershell
python .\gui_dataset_filter_renamer.py .\ --all
```

### 3. 预览模式（不改动文件）

```powershell
python .\gui_dataset_filter_renamer.py .\dataset_wechat --dry-run
```

### 4. GUI 选择目录

直接运行：

```powershell
python .\gui_dataset_filter_renamer.py
```

## 注意事项

- 仅处理扩展名为 `.jpg/.jpeg/.png/.txt` 的文件。
- 文件名需符合：`<senary>_<id>_<YYYYMMDD>_<HHMMSS>[_visualized].ext`。
- 如需调整排序或 `new_id` 规则，可在 `gui_dataset_filter_renamer.py` 中修改 `ordered_keys` 排序逻辑。
