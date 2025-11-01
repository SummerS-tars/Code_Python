# Student Grade Manager: 学生成绩管理系统

## Overview: 功能概述

- 存储学生成绩记录  
- 新增学生成绩记录  
- 支持按学号查询并打印匹配的成绩记录  
- 支持按学号定位学生，并修改单科成绩  
- 支持按学号匹配删除学生单科记录  
- 统计数据：  
    - 班级科目平均分（按总分）  
    - 科目最高分/最低分（注明学生）  

补充：  
持久化存储（使用文件保存和加载数据）  

## Running Instructions: 运行说明

Environment： Python 3.7+  

Start the program:  

```sh
python grade_manager.py
```

## Details Design: 详细设计

### Data Structure: 数据结构

学生成绩记录：  
列表  

```py
records = [
    {"student_id": "S001", "subject": "Math", "score": 95},
    {"student_id": "S002", "subject": "English", "score": 88},
    ...
]
```

### Functions: 功能实现

1. Add Record: 添加成绩记录  
    input: student_id, subject, score  
    one record every time  
2. Query Records: 查询成绩记录  
    input: student_id  
    output: list of matching records  
3. Update Record: 修改成绩记录  
    interaction: locate the matching record(s)  
    and let user choose which to update  
    then input new score  
4. Delete Record: 删除成绩记录  
    interaction: locate the matching record(s)  
    and let user choose which to delete  
5. Statistics: 统计数据  
    - Average Score: 计算班级科目平均分（按总分）  
    - Highest/Lowest Score: 计算科目最高分/最低分（注明学生）  
6. Persistence: 数据持久化  
    - Save to File: 保存数据到文件  
    - Load from File: 从文件加载数据
    - File Format: 存储文件格式  
        使用csv或json格式  

### User Interaction: 用户交互  

#### Main Menu: 主菜单

use Chinese prompts for user interaction  

user selects options listed in main menu  
e.g. use numbers to select options  

main menu keeps running until user chooses to exit or the program aborts  

#### Input Prompts: 输入提示  

all the CRUD operations should prompt user for every required input member  
every time only one data should be inputted  
(e.g. student_id, subject, score take three separate prompts and inputs)  

#### Output Display: 输出显示

every time after choose an operation, before print the prompts, clear the screen to improve user experience  

before returning the output, also clear the screen to improve the readability  

beautify the output display of the queried records or statistics  

after displaying the output, prompt user the press Enter to return to main menu(and also clear the screen after that)  

#### Input Validation: 输入校验

- Student ID: non-empty string  
- Subject: preset list of subjects  
- Score: Integer between 0 and 100  

#### Error Handling: 错误处理  

- Invalid Input: prompt user to re-enter  
- Record Not Found: notify user and return to main menu  
- File I/O Errors: handle exceptions and notify user  
- Duplicate Records: notify user when adding duplicate records  
- Empty Dataset: handle gracefully during queries and statistics  

besides:  
when reading from file, when encountering malformed data, skip those records and notify user about the count of skipped records  
and no matter what, before the program exits, try to ask user whether to save current data to file  

### Code Quality: 代码质量

use proper modularization and functions to realize different functionalities  
use standard naming conventions and add necessary comments for clarity  
