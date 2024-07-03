# 4 Python基础语法

## 4.1 编码(见2.3.1中)

## 4.2 标识符

1. 第一个字符必须为 字母表中字母 or 下划线`_`  
2. 标识符其他部分由 字母、数字 and 下划线`_` 组成  
3. 大小写敏感

注：在Python3中，支持中文作为变量名，非ASCII标识符也被允许  

## 4.3 Python保留字

可以通过

```py
>>> import keyword
>>> keyword.kwlist
# ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
```

输出当前版本的所有关键字  

## 4.4 注释(见2.3.5)

## 4.5 行与缩进(见2.3.6)

Python特色：使用缩进代表代码块，而非使用`{}`  
缩进空格数可变，但同一代码块的语句必须包含相同缩进空格数  

## 4.6 多行语句

Python通常一行写完一条语句，过长可用`\`分割  
注：`[]` `{}` `()` 中不需要使用  

## 4.7 数字类型

Python中只有四种：整形、布尔型、浮点数 and 复数  

1. int  
    注意只有一种整数类型，表长整型  
2. bool  
3. float
4. complex(复数)  
    如 `1+2j` `1.1+2.2j`  

## 4.8 字符串

1. Python中`'` `"`的使用一致  
2. 使用三引号指定一个多行字符串  
3. 转义符`\`，同时可以在字符串前加`r`阻止转化  
4. 字符换可以用`+`串联，用`*`重复  
5. Python中字符串不可以改变  
6. Python中无单独的字符类型，单个字符就是长度为1的字符串  
7. 