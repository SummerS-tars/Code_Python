# 薪资计算器（Week10 作业）

说明：这是为课程作业实现的一个基础薪资计算器示例，包含交互式与命令行运行两种模式，并提供简单的分级税率计算示例。

主要文件：  

- `salary_calculator.py`：主程序，支持交互与命令行参数运行。
- `ai_dialogue.txt`：保存与 AI 的对话摘要（用于作业提交）。
- `ai_report.md`：AI 生成代码的分析与审查报告。

示例运行（非交互）：

在 PowerShell 中运行（示例）：

python "pathTo/salary_calculator.py" --name TestUser --base 8000 --bonus 1200

交互运行：
python "pathTo/salary_calculator.py"

说明：脚本默认免征点（月）为 5000，默认税率为示例性分级税率，请根据课程要求替换税率表与单位（年/月）。

使用配置文件：
脚本支持通过 `--config` 指定税率配置 JSON 文件；如果不指定，脚本会尝试读取与脚本同目录下的 `tax_config.json`（如果存在）。配置文件示例在同目录下提供为 `tax_config.json`。
