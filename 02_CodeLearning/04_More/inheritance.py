class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    # * 类似Java的toString方法
    def __str__(self):
        return f"Person(name={self.name}, age={self.age})"
    
    def breathe(self):
        print(self.name,"is breathing...")

# * Python继承语法：class 子类(父类)
class Otto(Person):
    def __init__(self, name, age):
        # * 此处也类似Java，super()调用父类构造方法
        super().__init__(name, age)
    
    def breathe(self):
        print(self.name,"is breathing...冲刺！！")

class WildAnimalSenbai(Person):
    def __init__(self, name, age):
        super().__init__(name, age)
    
    def breathe(self):
        print(self.name,"is breathing...嗯嗯嗯啊啊啊啊啊啊啊")

normal_person = Person("normal", 20)
normal_person.breathe()

otto = Otto("Otto", 20)
otto.breathe()

senbai = WildAnimalSenbai("senbai", 20)
senbai.breathe()
