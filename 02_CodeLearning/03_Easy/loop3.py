import random

times = random.randint(1, 100) # ! attention that here the range is [1, 100]

while(times >= 0):
    print("还剩下" + str(times) + "次机会")
    times -= 1

print("结束")
