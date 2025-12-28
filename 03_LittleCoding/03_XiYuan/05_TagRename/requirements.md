# Requirements Documentation

经过处理，现已经对所有的图片进行了`_class_duplicate`后缀的标注  
现需要对图片的`tag`部分进行调整

## 文件结构基础

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

会提供`class_all`的根目录路径
需要递归对其下所有的`class`与`class_unknown`目录下的子目录进行处理  

- `pic`目录下为图片
- `txt`目录下为标注文件

## 命名规范基础

图片  

已知类别：  

```txt
tag_time-tag_train/val_class_duplicate.png
```

未知类别：  

```txt
time_hash-tag_train/val_class_duplicate.png
```

标注文件：  

```txt
tag_time-tag.txt
```

示例：  

```txt
Adobe_Acrobat_2024_2_2_16_36-8_val_1_1.png
对应
Adobe_Acrobat_2024_2_2_16_36-8.txt
```

或者  

```txt
time_hash-tag.txt
```

示例：  

```txt
2024_3_18_17_19_e8ba0101cbc74242b48af70a57dafdf5-5_train_1_1.png
对应
2024_3_18_17_19_e8ba0101cbc74242b48af70a57dafdf5-5.txt
```

## 需求细节

**重点：**不管对某图片`tag`要做什么更改，必须保证其`class`和`duplicate`部分不变，同时保证其对应的标注文件(.txt)的`tag`部分被做出相同的更改，保证此操作的一致性，以防止对应关系被破坏  

总共分为两步：  

### 重命名部分  

总共有几种情况：  

1. 发现某些unknown的图片，实际属于某些已知类别  
    此时会将其从`unknown`中的类别直接移动到对应的已知类别中  
    要求将其`tag`部分直接变为已知类别  

    示例：  

    ```txt
    E:\_WorkingTemp\XiYuanTotalProcess\class_all\class\APNews\pic\2024_3_24_12_4_61dde84214804fe8b05cac4394187a00-8_train_91_1.png
    ```

    由于属于`APNews`类别  
    将其直接变为  

    ```txt
    APNews_91_1.png
    ```

2. 对于已知类别的图片，调整简化其`tag`部分  
    例如：  

    ```txt
    E:\_WorkingTemp\XiYuanTotalProcess\class_all\class\Ada\pic\Ada_2024_3_8_20_45-30_train_1_1.png
    ```

    将其简化为  

    ```txt
    Ada_1_1.png
    ```

3. 对于unknown类别的图片  
    一般来说其`pic`所位于的目录命中`classX_class_tag`  
    将其`tag`部分直接变为`class_tag`  
    例如：  

    ```txt
    E:\_WorkingTemp\XiYuanTotalProcess\class_all\class_unknown\class1_ikea\pic\2024_3_18_17_19_e8ba0101cbc74242b48af70a57dafdf5-5_train_1_1.png
    ```

    改为

    ```txt
    ikea_1_1.png
    ```

标注文件重命名规则：  
保证每个图片其对应的标注文件最后与该图片命名一样(只有后缀不同)！  

### 移动部分

最后需要对所有的图片及其对应的标注文件进行汇总移动  

要求：

根据`train/val`进行分类  
分别放在`class_all/train`与`class_all/val`目录下  
如果没有则创建  
