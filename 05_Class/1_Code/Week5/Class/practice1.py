try:
    dollar = float(input("请输入美元金额："))
    if dollar < 0:
        raise ValueError("金额不能为负数")
except ValueError as ve:
    print(f"输入错误: {ve}")
except TypeError as te:
    print(f"类型错误: {te}")
else:
    exchange_rate = 0.14  # 假设当前汇率为1人民币=0.14人民币
    rmb = dollar / exchange_rate
    print(f"{dollar:.1f} 美元等值于 {rmb:.2f} 人民币")
