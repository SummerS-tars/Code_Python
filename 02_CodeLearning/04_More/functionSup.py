def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    return a / b

def get_calculator(operator):
    if(operator == "+"):
        return add
    elif(operator == "-"):
        return sub
    elif(operator == "*"):
        return mul
    elif(operator == "/"):
        return div
    else:
        raise ValueError("Invalid operator")

# * 类似于C中的函数指针，传入函数指针作为参数，用于调用函数
# * 可以被传入函数作为参数的函数称为高阶函数
def calculate(a, b, calculator):
    try:
        return calculator(a, b)
    except Exception as e:
        print(f"Error: {e}")
        return None

try:
    print("请输入运算符：(+ - * /)")
    operator = input()
except ValueError:
    print("非法运算符")
    exit()

try:
    print("请输入两个数字：")
    a = int(input("a = "))
    b = int(input("b = "))
except ValueError:
    print("非法数字")
    exit()

calculator = get_calculator(operator)
print("a",operator,"b =",calculate(a, b, calculator))

"""
Lambda表达式匿名函数语法
lambda 参数列表: 返回表达式

只适用于简单场景
不需要专门定义一个函数
"""
print("测试Lambda表达式匿名函数")
print(f"""(a + b) * (a - b) / (a * b) = {calculate(a, b,(lambda x, y: (x + y) * (x - y) / (x * y) ))}""")