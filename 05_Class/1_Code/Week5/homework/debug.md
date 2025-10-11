# Homework 4 Debug Log

## 1. Debugging Steps

### 1.1. First Try

```txt
╭─[MacbookSum] as thesumst in ~/ComputerLearning/Code_Python on (main)✘✘✘                                                                                              18:04:34
╰─(ﾉ˚Д˚)ﾉ (.venv)  cd /Users/thesumst/ComputerLearning/Code_Python ; /usr/bin/env /Users/thesumst/ComputerLearning/Code_Python/.venv/bin/python /Users/thesumst/.vscode/extensions/ms-python.debugpy-2025.10.0-darwin-arm64/bundled/libs/debugpy/adapter/../../debugpy/launcher 61218 -- /Users/thesumst/ComputerLearning/Code_Python/05_Class/1_Code/Week5/homework/buggy.py 
Traceback (most recent call last):
  ...
  File "/Users/thesumst/ComputerLearning/Code_Python/05_Class/1_Code/Week5/homework/buggy.py", line 4
    student_name = "小明
                   ^
SyntaxError: unterminated string literal (detected at line 4)
```

we can see the compiler told us that there is a syntax error in line 4 because of the unterminated string literal.  

#### 1.1.1. Fix 1

from

```python
student_name = "小明
```

to

```python
student_name = "小明"
```

### 1.2. Second Try

```txt
  File "/Users/thesumst/ComputerLearning/Code_Python/05_Class/1_Code/Week5/homework/buggy.py", line 9
    define calculate_scores(score_list)
           ^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax
```

we can see the compiler told us that there is a syntax error in line 9 because of the invalid syntax.

#### 1.2.1. Fix 2

this is because in python we use `def` to define a function, not `define`.

so we fix this from

```python
define calculate_scores(score_list)
```

to

```python
def calculate_scores(score_list):
```

### 1.3. Third Try

```txt
  File "/Users/thesumst/ComputerLearning/Code_Python/05_Class/1_Code/Week5/homework/buggy.py", line 10
    def calculate_scores(score_list)
                                    ^
SyntaxError: expected ':'
```

#### 1.3.1. Fix 3

the compiler told us all and how to fix it.  
not mentioned here.  

### 1.4. Fourth Try

```txt
发生异常: TypeError
unsupported operand type(s) for +=: 'int' and 'str'
```

we can find that in the test data list 1, there are both integers and strings.
as the requirements, we shouldn't modify the test data.  
so we need to add a step to convert the string to integer.  

#### 1.4.1. Fix 4

from

```python
    total_score = 0
    average_score = 0
    for score in score_list:
        total_score += score
```

to

```python
    total_score = 0
    average_score = 0
    for score in score_list:
        score = int(score) # bugfix 4: convert score to integer
        total_score += score
```

the conversion step is added  

### 1.5. Fifth Try

```txt
发生异常: NameError
name 'averge' is not defined
```

#### 1.5.1. Fix 5

normal error that type the wrong variable name.

from

```python
print(f"学生 {student_name} 的平均分是：{averge}")
```

to

```python
print(f"学生 {student_name} 的平均分是：{average}")
```

### 1.6. Sixth Try

```txt
发生异常: ZeroDivisionError
division by zero
  File "/Users/thesumst/ComputerLearning/Code_Python/05_Class/1_Code/Week5/homework/buggy.py", line 17, in calculate_scores
    average_score = total_score / len(score_list)
                    ~~~~~~~~~~~~^~~~~~~~~~~~~~~~~
  File "/Users/thesumst/ComputerLearning/Code_Python/05_Class/1_Code/Week5/homework/buggy.py", line 28, in <module>
    total, average = calculate_scores(scores2)
                     ~~~~~~~~~~~~~~~~^^^^^^^^^
ZeroDivisionError: division by zero
```

we can see that the test data list 2 is an empty list  
which means the length of the list is 0  
so when we calculate the average score, it will cause a division by zero error.

#### 1.6.1. Fix 6

from

```python
    average_score = total_score / len(score_list)
```

to

```python
    if len(score_list) == 0:
        average_score = 0
    else:
        average_score = total_score / len(score_list)
```
