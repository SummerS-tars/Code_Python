
"""
open() 传入文件（相对/绝对）路径，打开文件；
第二个参数是模式（只读等）；(默认为"r")
第三个是编码模式（例如utf-8）
返回一个文件指针对象

读写完毕后注意使用close()方法关闭文件

此外可以使用with语句，自动关闭文件
（类似于Java的try-with-resources）
with open(...) as f:

对于第二个参数，模式：
"r" 只读
"w" 只写（文件不存在则创建，存在则清空）
"a" 追加（文件不存在则创建，存在则追加）
"r+" 读写（文件不存在则报错）
"""


"""
文件指针可以调用read()等方法

read() 读取文件内容（且文件指针向后移动）
可以传入参数，指定读取的字节数

readline() 读取一行内容（换行符也会作为返回值的一部分）
没有则返回空字符串（注意与None区分）

readlines() 则直接读取所有行
返回由每行字符串组成的列表

write() 写入文件内容
可以传入参数，指定写入的字节数

writelines() 写入多行内容
可以传入参数，指定写入的列表
"""

# ! "w"模式下，文件不存在则创建，存在则清空（注意是清空）
with open("./test.txt", "w") as f:
    # ! 写入内容，不会自动换行
    f.write("Hello, World!")
    # ! 写入多行内容，也不会自动换行
    f.writelines(["test1","test2","test3"])

# ! "r"模式下，文件不存在则报错
with open("./test.txt", "r") as f:
    print(f.read())

# ! "a"模式下，文件不存在则创建，存在则追加
with open("./test.txt", "a") as f:
    f.write("test4")

# ! "r+"模式下，文件不存在则报错
with open("./test.txt", "r+") as f:
    print(f.read())
    f.write("test5")

with open("./test.txt", "r") as f:
    print(f.read())