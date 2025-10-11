# buggy.py

# 学生姓名和他的分数列表
student_name = "小明"  # bugfix 1 unterminated string literal
scores1 = [95, 88, '76', 92, 85] #测试数据1，此行不得修改
scores2 = [] #测试数据2，此行不得修改

# 函数目标：计算总分和平均分
# bugfix 2: error syntax that 'define' a function
def calculate_scores(score_list): # bugfix 3: missing colon
    total_score = 0
    average_score = 0
    for score in score_list:
        score = int(score) # bugfix 4: convert score to integer
        total_score += score
    
    if len(score_list) > 0:  # bugfix 5: avoid division by zero
        average_score = total_score / len(score_list)
    else:
        average_score = 0  # If no scores, average is 0
    
    return total_score, average_score

# 主程序部分
print('第一组测试')
total, average = calculate_scores(scores1)
print(f"学生 {student_name} 的总分是：{total}")
print(f"学生 {student_name} 的平均分是：{average}") 

print('第二组测试')
total, average = calculate_scores(scores2)
print(f"学生 {student_name} 的总分是：{total}")
print(f"学生 {student_name} 的平均分是：{average}") 