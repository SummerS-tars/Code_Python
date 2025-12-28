# Requirements Document

标注序号检查及纠正脚本  

## Overview

这个文档用于描述一个python脚本的功能需求  
主要用于一个对于图片类别的类别及重复序号的标注检查以及纠正  

## Specific Requirements

### Background

#### 文件结构

会给一个图片的目录  
其下有许多图片(.png)  

#### 文件命名

图片命名格式如下：  

```txt
tag_time-tag_train/val_class_duplicate.png
```

或者  

```txt
time_hash-tag_train/val_class_duplicate.png
```

示例：  
Ada_2024_3_8_20_45-30_train_2_3.png

前面的都不用管  
主要需要注意`class`和`duplicate`两个数字  
默认情况下  
`class`从1开始连续增长  
`duplicate`从1开始连续增长  

### Function Requirements

`class`由于标注时为了方便，中间可能有跳号  
以及`duplicate`可能有重复或者缺失的情况  
需要对这些进行检查和纠正  

具体来说：  

1. `class`要连续增长  
    - 如果发现跳号，则需要将后面的类别依次前移补齐  
    - 例如：1,2,4,5 → 1,2,3,4

2. `duplicate`要从1开始连续增长  
    - 如果发现缺失，则需要将后面的序号依次前移补齐
    - 如果是重复，将该类的序号告知用户，由人工进行检查
        - 可能是不同class误用了标成同一个class  
            这时候需要将用户指定的某个具体文件改成新的class
        - 也可能是同一个class误用了同一个duplicate
            这时候保证该class下的duplicate连续即可

## Extra Requirements

上述所需要处理的`class`都是属于某一类图片的情况之下  
现有多种类图片的情况  

文件结构参考：  

```txt
.../class_all
├──class
│  ├──Ada
│  │  ├──pic
│  │  ├──txt
│  │  └──unmatched
│  └──...
├──class_unknown
│  ├──class1_ikea
│  │  ├──pic
│  │  ├──txt
│  │  └──unmatched
│  └──...
└──labels
    ├──train
    └──val
```

现会提供`class_all`目录的路径  
需要递归地对其下所有的`pic`目录下的图片进行分别处理  
简单来说就是不必反复提供`pic`的路径  
