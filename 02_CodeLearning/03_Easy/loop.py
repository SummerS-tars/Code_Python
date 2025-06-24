gpa_dict = { "高等数学": 1.0, "线性代数": 2.0, "程序设计": 4.0}

print(gpa_dict.keys())
print(gpa_dict.values())
print(gpa_dict.items())

for course, gpa in gpa_dict.items():
    if(gpa < 3.0):
        print(course + "取得绩点: " + str(gpa) + "，不嘻嘻")
    else:
        print(course + "取得绩点: " + str(gpa) + "，嘻嘻")
