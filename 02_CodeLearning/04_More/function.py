import random

def ghost_howl():
    howl_list = ["冲刺", "握握手", "握握双手", "说的道理", "otto!",
    "oiiai", "啊啊啊啊啊啊啊啊啊爆爆", "那咋了", "勾勾构"]
    return howl_list[random.randint(0, len(howl_list) - 1)]

for i in range(15):
    print(ghost_howl())
