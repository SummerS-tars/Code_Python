import json

INPUT_FILE = 'users.json'
OUTPUT_FILE = 'active_users.txt'

def filter_active_users(data): # fix 1 语法错误
    """筛选活跃用户并返回姓名列表"""
    active_user_names = []
    for user in data:
        # 筛选年龄大于30且活跃的用户
        try:
            if user['is_active'] and user['age'] > 30:
                active_user_names.append(user['name'])
        except KeyError as e:   # fix 4 错误处理
            print(f"缺少键 {e}，跳过用户: {user}")
    
    # 将所有符合条件的名字写入文件（只打开一次）
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f: # fix 2 语法错误 # fix 5 逻辑错误（重复使用w打开）
        for name in active_user_names:
            f.write(name + '\n')
    
    return active_user_names

# 主程序
try:
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        if not content.strip():
            print(f"错误: {INPUT_FILE} 是空文件")
        else:
            users_data = json.loads(content)
            
            if not isinstance(users_data, list):
                print(f"错误: JSON 应该是用户列表，但获得了 {type(users_data)}")
            else:
                filtered_names = filter_active_users(users_data) # fix 3 标识符错误
                print(f"已找到 {len(filtered_names)} 位符合条件的活跃用户。")
                print(f"名单已写入 {OUTPUT_FILE}")

except json.JSONDecodeError as e:
    print(f"JSON 格式错误: {e}")
    print(f"请检查 {INPUT_FILE} 的格式是否正确")
except FileNotFoundError:
    print(f"错误: 找不到文件 {INPUT_FILE}")
except Exception as e:
    print(f"程序运行出错: {e}")