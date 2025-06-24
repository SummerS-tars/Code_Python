# 1 python简介

## 1.1 定义

Python是一种结合了**解释性、编译性、互动性and面向对象的脚本语言**  

p.s.
解释型:**开发过程中**没有编译环节  
交互式:可以在Python提示符`>>>`后直接执行代码  
面向对象:支持 面向对象的风格 and 将代码封装在对象 的编程技术  

## 1.2 编译 and 运行过程

虽然是解释型，到Python也不能直接解释源代码，需要有一个编译和运行的环节  

具体来说:需要从`.py`经过解释器转为`.pyc`(Python字节码)，后由PVM(Python虚拟机)执行，最后在终端输出结果  

因此，解释型语言具体指的是解释 **Python字节码** 而非 **Python源代码**  

*补充:此时我们肯定会好奇为什么要生成中间码？因为通过不同平台的解释器生成对应中间码，再交与虚拟机运行，可以降低语言对平台的依赖性，不过牺牲了一定的效率*  
*补充2:一般简单来说，和解释行相对应的就是编译型，这里我们分别用Python和C来理解，Python实际是一边翻译`.py`源程序一边运行(一行一行的)，C则必须先让源程序`.c`经过编译器处理为可执行文件才可以执行*  
*补充3:解释器由一个编译器和一个虚拟机构成，编译器负责将源代码转换成字节码文件，而虚拟机负责执行字节码* ([如何理解Python的解释性](https://blog.csdn.net/nb_zsy/article/details/110468714))  

### 1.2.1 Python解释器

**Python解释器**(*Interpreter*) 负责将Python语言翻译为CPU可以执行的指令  

### 1.2.2 Python解释器的种类

暂无需多了解，一下仅列举几个较重要的：  

1. Cpython  
2. Jpython  

### 1.2.3 PVM(Python Virtual Machine,Python虚拟机)

输入由编译器转换出的字节码，逐行解释执行

*可参考文章：[Python解释器](https://blog.csdn.net/qq_41813454/article/details/136645809)*  

### 1.2.4 Python字节码(.pyc)

Python中的字节码(bytecode)为一种数据类型，即Python编译后的结果  

假如有个test.py文件需要执行，那么它会先生成.pyc文件，一般可能的情况如下：

1. 执行 python test.py 会对test.py进行编译成字节码并解释执行，但不会生成test.pyc  
2. 如果test.py中加载了其他模块，如import urllib2，那么python会对urllib2.py进行编译成字节码，生成urllib2.pyc，然后对字节码解释执行  
3. 如果想生成test.pyc，可以使用python内置模块py_compile来编译，也可以执行命令 python -m py_compile test.py 这样，就生成了test.pyc  
4. 加载模块时，如果同时存在.py和.pyc，python会使用.pyc运行，如果.pyc的编译时间早于.py的时间，则重新编译 .py文件，并更新.pyc文件  
