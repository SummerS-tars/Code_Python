## Debug实战赛题目 (20分钟)
### 任务说明
- 请在20分钟内，尽力完成以下两道“代码修复”任务；
- 每个任务都提供了一个目标、所需的输入文件内容，以及一份有问题的Python脚本；
- 你的目标是找出并修复脚本中所有的Bug，让程序能够成功运行并达成预定目标；
- 挑战: 每个脚本中都隐藏了不少于5个不同类型的Bug！
- 提交要求：请上传改正后的代码。代码最前方添加注释：说明你所发现的每一处错误及错误类型，如：“IndexError：错误说明”，或“逻辑错误：错误说明”。并在下面代码相应地方使用注释进行标记，如：#此处为对第1个错误的修正。

### 任务一：销售数据处理器
#### 目标:
读取一个包含产品销售数据的CSV文件 sales_data.csv，计算其中单价高于500元的产品的总销售额 (即 数量 * 单价 的总和)，并将最终结果打印出来。
所需输入文件 (sales_data.csv):
请在你的项目文件夹中创建这个文件，并将以下内容复制进去。
```text
ProductID,ProductName,Quantity,Price
P001,Laptop,10,8000
P002,Mouse,100,150.50
P003,Keyboard,50,'300'
P004,Monitor,20
P005,Webcam,N/A,450
```

#### 有问题的脚本 (task1_buggy.py):
```python
import csv

def process_sales_data(filepath)
    """处理销售数据并计算高价商品的总销售额"""
    total_revenue = 0.0
    try:
        with open('sales.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader) # 跳过表头

            for row in reader:
                # 获取数量和价格
                quantity = int(row[2])
                price = float(row[3])

                # 筛选出价格低于500的产品并累加销售额
                if price < 500:
                    total_revenue += quantity * price
    
    except Exception as e:
        print(f"处理文件时发生错误: {e}")

    print(f"单价高于500元的产品总销售额为: {total_revnue}")

# 主程序
process_sales_data('sales_data.csv')
```


### 任务二：活跃用户筛选器
#### 目标:
读取一个包含用户信息的JSON文件 users.json，筛选出其中所有年龄大于30岁且状态为活跃 (is_active为true) 的用户，并将他们的姓名写入到一个名为 active_users.txt 的文件中，每行一个名字。
所需输入文件 (users.json):
请创建这个文件并复制以下内容。
```json
[
  {"id": 1, "name": "Alice", "age": 32, "is_active": true},
  {"id": 2, "name": "Bob", "age": "25", "is_active": false},
  {"id": 3, "name": "Charlie", "is_active": true},
  {"id": 4, "name": "Diana", "age": 45, "is_active": true}
]
```

#### 有问题的脚本 (task2_buggy.py):
```python
import json

INPUT_FILE = 'users.json'
OUTPUT_FILE = 'active_users.txt'

def filter_active_users(data)
    """筛选活跃用户并返回姓名列表"""
    active_user_names = []
    for user in data:
        # 筛选年龄大于30且活跃的用户
        if user['is_active'] and user['age'] > 30:
            active_user_names.append(user['name'])
            
            # 将名字写入文件
            with open(OUTPUT_FILE, 'w' as f:
                f.write(user['name'] + '\n')
    
    return active_user_names

# 主程序
try:
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        users_data = json.load(f)
        
    filtered_names = filter_user(users_data)
    print(f"已找到 {len(filtered_names)} 位符合条件的活跃用户。")
    print(f"名单已写入 {OUTPUT_FILE}")

except Exception as e:
    print(f"程序运行出错: {e}")
```

