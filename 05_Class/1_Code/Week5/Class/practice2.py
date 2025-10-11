try:
    price = float(input("请输入消费总金额："))
    if price < 0:
        raise ValueError("金额不能为负数")
    if price >= 2000:
        discount = 0.8
    elif price >= 1000:
        discount = 0.85
    else:
        discount = 1
    final_price = price * discount
    print(f"""原始金额：{price:.2f} 元
折扣金额：{(price-final_price):.2f} 元
最终价格：{final_price:.2f} 元""")
except ValueError as ve:
    print(f"输入错误: {ve}")
except TypeError as te:
    print(f"类型错误: {te}")
