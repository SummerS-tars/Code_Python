# Requirements Document

图片与参数文件匹配处理脚本  

## Overview

这个文档用于处理项目中图片(.png)与对应参数文件(.txt)的匹配  
依据为图片文件命名中的部分与参数文件命名中的部分  
需要根据需要调整相关的文件结构  
并统计处理正常以及异常的结果  

## Specific Requirements

### Background

#### 文件结构

```txt
E:\_WorkingTemp\XiYuanTotalProcess\class_all
├──class
│  ├──Ada
│  └──...
├──class_unknown
│  ├──class1_ikea
│  └──...
└──labels
   ├──train
   └──val
```

具体解释：  

- class_all: 总目录
- class: 已知类别目录
- class_unknown: 未知类别目录
- labels: 参数文件目录

class与class_unknown目录下的子目录分别都对应一个类别  
每个类别目录下有大量的图片文件(.png)  

label下的train与val目录分别存放训练集与验证集的参数文件(.txt)  

#### 文件命名

class目录下各个类别的图片命名格式：  

```txt
tag_time-tag_train/val.png
```

示例：  
Ada_2024_3_8_20_45-30_train  

class_unknown目录下各个类别的图片命名格式：  

```txt
time_hash-tag_train/val.png
```

示例：  
2024_3_18_17_19_e8ba0101cbc74242b48af70a57dafdf5-5_train.png  

labels目录下train和val目录下参数文件命名格式：  

```txt
tag_time-tag.txt
```

```txt
time_hash-tag.txt
```

简单来说就是对应的图片命名去掉了`_train/val`后缀，并且将`.png`改为了`.txt`  

#### 对应关系

一般来说  
每张图片文件都有且仅有一个对应的参数文件  

可能存在部分异常情况：  

1. 图片文件找不到对应的参数文件
2. 参数文件找不到对应图片文件

### Function Requirements

1. 遍历class与class_unknown目录下的所有图片文件

2. 根据图片文件名提取对应的参数文件名

3. 在labels目录下的train与val目录中查找对应的参数文件

4. 整理文件结构为  

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

所有的图片文件都要放入对应类别目录下的pic子目录中  
所有的参数文件都要放入对应类别目录下的txt子目录中  
所有找不到对应参数文件的图片文件都要放入对应类别目录下的unmatched子目录中  
考虑到无法找到对应图片的参数文件无法知道类别，留在labels目录下不动  
