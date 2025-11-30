import csv

def process_sales_data(filepath): # fix 1 语法错误
    """处理销售数据并计算高价商品的总销售额"""
    total_revenue = 0.0
    try:
        with open(filepath, 'r', encoding='utf-8') as f: # fix 3 逻辑错误
            reader = csv.reader(f)
            header = next(reader) # 跳过表头

            for row in reader:
                try:
                    # 检查列数是否足够
                    if len(row) < 4:    # fix 5 索引错误避免
                        print(f"列数不足，跳过行: {row}")
                        continue
                    
                    # 获取数量和价格
                    quantity = int(row[2])
                    price = float(row[3])

                    # 筛选出价格低于500的产品并累加销售额
                    if price < 500:
                        total_revenue += quantity * price
                except ValueError:  # fix 4 逻辑错误
                    print(f"数据格式错误，跳过行: {row}")

    except Exception as e:
        print(f"处理文件时发生错误: {e}")

    print(f"单价高于500元的产品总销售额为: {total_revenue}") # fix 2 标识符错误

# 主程序
process_sales_data('sales_data.csv')