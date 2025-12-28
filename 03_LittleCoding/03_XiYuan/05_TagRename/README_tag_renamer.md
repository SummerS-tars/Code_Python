# Tag Renamer & Aggregator

基于 `requirements.md` 的实现，完成图片/标签的 tag 重命名与最终按 train/val 的汇总移动。

## 功能

- 递归扫描 `class_all/class/**/pic` 与 `class_all/class_unknown/**/pic`
- 解析图片名：`<descriptor>_(train|val)_<class>_<duplicate>.<ext>`
- 新 tag 规则：
  - 已知类别：使用 `class/<类别名>` 作为 tag
  - 未知类别：`class_unknown/classN_suffix` 使用 `suffix` 作为 tag（若不匹配则使用该目录名）
- 图片重命名为：`<tag>_<class>_<duplicate>.<ext>`（仅更改 tag）
- 标签（.txt）按 `<descriptor>-<tag>.txt` 匹配与重命名（仅更改 tag）
- 最终移动：
  - 图片 -> `root/train` 或 `root/val`
  - 标签 -> `root/labels/train` 或 `root/labels/val`

## 使用

Dry-run 预览（不会真正修改磁盘）：

```pwsh
python .\tag_renamer.py --root E:\_WorkingTemp\XiYuanTotalProcess\class_all
```

实际执行：

```pwsh
python .\tag_renamer.py --root E:\_WorkingTemp\XiYuanTotalProcess\class_all --execute
```

冲突策略：

- `--on-conflict skip`（默认）：遇到同名目标跳过
- `--on-conflict overwrite`：覆盖现有文件
- `--on-conflict rename`：在文件名后追加 `__dupN`

导出操作报告：

```pwsh
python .\tag_renamer.py --root E:\_...\class_all --execute --report E:\\_...\\reports\\tag_renamer.csv
```

## 假设与注意

- 图片名满足：`<descriptor>_(train|val)_<class>_<duplicate>.<ext>`；无法解析将被跳过。
- 标签名满足：`<descriptor>-<tag>.txt`；若找不到完全匹配，会尝试模糊匹配，仍找不到则仅移动图片。
- 支持图片扩展名：`.png .jpg .jpeg .webp .bmp`。
- 目录结构假设：
  - 已知：`root/class/<ClassName>/{pic,txt}`
  - 未知：`root/class_unknown/classN_suffix/{pic,txt}`
  - 最终汇总输出：`root/{train,val}` 与 `root/labels/{train,val}`

## 回滚建议

- 首次建议使用 `--report` 导出 CSV 并保留备份。
- `--on-conflict rename` 能最大限度避免覆盖风险。
