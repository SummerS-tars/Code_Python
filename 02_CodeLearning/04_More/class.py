class Wallet: # 类名用Pascal命名风格（大驼峰）
    def __init__(self, owner_name, balance):
        # * self 是默认必须带有的参数，用于表示对象自身
        # * 类似于Java中的this
        self.owner_name = owner_name
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

# * 默认也不需要传入self，其为默认自动传入的
wallet1 = Wallet("张三", 1000)
print(wallet1)
print(wallet1.owner_name)
print(wallet1.balance)

print("存了1000元")
wallet1.deposit(1000)
print(wallet1.balance)

print("取了200元")
wallet1.withdraw(200)
print(wallet1.balance)
