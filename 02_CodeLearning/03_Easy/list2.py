
# * here we will use some other functions

from decimal import MAX_PREC


price_list = []

price_list.append(100)
price_list.append(300)
price_list.append(200)

print(price_list)

max_price = max(price_list)
min_price = min(price_list)

print("max price: ", max_price)
print("min price: ", min_price)

price_list.sort()

print(price_list)