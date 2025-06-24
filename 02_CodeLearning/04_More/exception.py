"""
Python中的异常处理也类似于Java
使用try-except语句
使用raise语句抛出异常
使用finally语句执行清理操作
使用with语句自动关闭文件
使用assert语句断言
使用logging模块记录日志
使用traceback模块打印异常堆栈
使用pdb模块调试
使用logging模块记录日志
"""

try:
    print("calculate A / B")
    a = int(input("A: "))
    b = int(input("B: "))
    # ! 小插曲，python可以自动将两个整数相除的结果转为浮点数
    result = a / b
    print(f"result: {result}")
except ValueError:
    print("except说：我抓住了ValueError异常，请输入数字")
except ZeroDivisionError:
    print("except说：我抓住了ZeroDivisionError异常，除数不能为0")
except Exception as e:
    print(f"except说：我抓住了其他异常: {e}")
else:
    print("else说：没有异常，我也要执行")
finally:
    print("finally说：不管怎样，我都要执行")
