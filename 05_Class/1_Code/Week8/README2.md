# Student Grade Manager（多模块说明）

这是一个小型的学生成绩管理系统，采用字典为主的内存模型并拆分为多个职责清晰的模块。此 README 侧重介绍多模块设计、模块职责、模块间契约和扩展建议，便于你在课程或后续开发中复用、测试或扩展代码。

## 项目结构概览

- `grade_manager.py` — 程序入口与菜单交互（CLI）。
- `gm_core.py` — 核心业务逻辑（校验、CRUD、统计等），纯函数/无副作用优先，方便单元测试。
- `gm_data.py` — 持久化与数据格式转换（load/save、兼容旧格式）。
- `gm_display.py` — 所有终端输出与表格/清屏/暂停逻辑，单独解耦以便将来替换为 GUI/网页前端。
- `grades_dict.json` — 默认的数据文件（JSON 字典结构）。
- `ref/` — 演示图片。

## 设计目标（与多模块相关）

- 单一职责：每个模块只负责一类任务（I/O、业务、显示），降低耦合。
- 明确定义模块接口：模块之间通过简单的数据结构（主要是字典）交互，避免隐式依赖。
- 易于测试：业务逻辑与 I/O/显示分离，便于对 `gm_core` 做纯粹的单元测试。
- 可替换性：只需实现相同输入/输出契约即可替换持久化或展示实现（例如替换为数据库或 Web 前端）。

## 模块契约（简要）

下面列出每个模块对外暴露的主要函数和约定（以便快速理解如何在代码内调用或替换）。

- gm_data.py
  - load_data() -> Dict[str, Dict[str, int]]
    - 从 `grades_dict.json` 读取并返回字典结构。
    - 对旧版列表结构有兼容转换逻辑。
  - save_data(records: Dict[str, Dict[str, int]]) -> None
    - 将字典写回 JSON 文件。
  - Contract: 抛出异常或返回空字典代替无法读取的情况（调用方可据此决定）。

- gm_core.py
  - valid_student_id(sid: str) -> bool
  - valid_subject(subject: str) -> bool
  - valid_score(score: int) -> bool
  - add_record(records, sid, subject, score) -> None
  - update_record(records, sid, subject, score) -> bool
  - delete_record(records, sid, subject) -> bool
  - list_student_subjects(records, sid) -> List[Tuple[str, int]]
  - subject_statistics(records) -> Dict[str, {avg,max,min,count}]
  - Contract: 不直接做 I/O；所有修改都发生在传入的 `records` 对象上（调用方负责持久化）。

- gm_display.py
  - print_records(records, sid_filter=None) -> None
  - print_statistics(statistics) -> None
  - pause(), clear_screen()
  - Contract: 仅负责格式化与输出；不修改 records。

## 运行与常用命令（Windows PowerShell）

- 运行交互界面：在项目目录下运行

  ```powershell
  python .\\grade_manager.py
  ```

- 演示模式（不读写文件，只演示流程）：

  ```powershell
  python .\\grade_manager.py --demo
  ```

  备注：在 VS Code 的 PowerShell 终端直接运行即可。

## 示例：如何在代码中复用模块

假设你想在另一个脚本中加载数据、对某个学生加分并保存：

```python
from gm_data import load_data, save_data
from gm_core import add_record

records = load_data()
add_record(records, 'S010', 'Math', 92)
save_data(records)
```

这种调用方式得益于模块间清晰的职责分离：`gm_core` 不关心文件，`gm_data` 不关心业务规则。

## 测试策略（建议）

- 单元测试：把重点放在 `gm_core.py`（业务规则）和 `gm_data.py` 的数据转换逻辑。
- 使用临时文件或 monkeypatch 模拟文件 I/O，以避免测试依赖真实文件。
- 对 `gm_display.py`，测试主要为格式化函数的输出（可捕获 stdout 断言字符串）。

示例 pytest 伪代码：

```python
def test_add_and_list(tmp_path):
    records = {}
    add_record(records, 'S100', 'English', 88)
    assert list_student_subjects(records, 'S100') == [('English', 88)]
```

## 扩展与替换建议

- 替换持久化：实现一个 `gm_data_sql.py`，提供同样的 `load_data`/`save_data` 接口，内部使用 SQLite。这样其余代码无需改动。
- 替换展示层：实现一个 `gm_web.py`，将 `gm_core` 暴露为 HTTP API；前端调用时只需满足相同数据约定。
- 增加认证/权限：在 `grade_manager.py` 或新的 `auth.py` 中实现。业务函数仍保持纯净（接受已经验证的输入）。

## 开发者备注（实现细节与约定）

- 内存数据结构：主键为学号的字典 -> 每个学号对应的值是科目到分数的字典（Dict[str, Dict[str,int]]）。
- 错误处理：I/O 错误应由 `gm_data` 层捕获并以明确异常或返回值告知调用方，调用方负责用户提示或回退策略。
- 国际化：目前 CLI 中文为主，若需要多语言支持，可以将字串集中到 `i18n.py` 并在 `gm_display` 中引用。

---

如果你希望，我可以：

- 为 `gm_core` 写一组基础 pytest 单元测试（覆盖 CRUD 与统计）；
- 提供一个示例 `gm_data_sql.py`，展示如何用 SQLite 替换 JSON，接口兼容；
- 或把 README 中的“示例代码”直接放到 `examples/` 目录并添加运行脚本。

告诉我你想要的下一步，我会继续实现。
