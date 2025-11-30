import random

REDBALL_COUNT = 5
BLUEBALL_COUNT = 1
REDBALL_RANGE = range(1, 33)
BLUEBALL_RANGE = range(1, 16)

def generate_double_color_ball():
    """生成一注双色球号码"""
    red_balls = random.sample(REDBALL_RANGE, REDBALL_COUNT)
    red_balls.sort()
    blue_balls = random.sample(BLUEBALL_RANGE, BLUEBALL_COUNT)
    blue_balls.sort()
    return red_balls + blue_balls


if __name__ == "__main__":
    """主函数，生成并打印双色球号码"""
    ticket = generate_double_color_ball()
    red_balls = ticket[:REDBALL_COUNT]
    blue_balls = ticket[REDBALL_COUNT:]
    print("Red: ", ' '.join(f"{num:02d}" for num in red_balls))
    print("Blue: ", ' '.join(f"{num:02d}" for num in blue_balls))