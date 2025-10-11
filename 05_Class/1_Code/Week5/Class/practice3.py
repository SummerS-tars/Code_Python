try:
    american_cnt = int(input("请输入美式咖啡的数量："))
    latte_cnt = int(input("请输入拿铁的数量："))
    if american_cnt < 0 or latte_cnt < 0:
        raise ValueError("数量不能为负数")
except ValueError as ve:
    print(f"输入错误: {ve}")
except TypeError as te:
    print(f"类型错误: {te}")
else:
    american_price = 28
    latte_price = 31
    total_price = american_cnt * american_price + latte_cnt * latte_price
    if american_cnt + latte_cnt >= 3:
        minus = -10
    else:
        minus = 0
    final_price = total_price + minus
    print(f"""---订单详情---\n小计金额：{total_price:.2f} 元\n促销折扣：{minus:.2f} 元\n最终总计：{final_price:.2f} 元""")
