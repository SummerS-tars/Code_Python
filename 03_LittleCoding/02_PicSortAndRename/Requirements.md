# Requirements

## 基础

提供一个路径指向一个目录，目录下有许多图像文件  
命名示范：  

```txt
tag_time-tag_train/val_class_duplicate.png
```

对于每个图像文件有对应的txt文件，命名示范：

```txt
tag_time-tag.txt
```

其中：  

- train/val表示训练集或验证集
- class表示图像在tag下的类别，是一个数字
- duplicate表示该类别下的第几个图像，是一个数字
- tag和time-tag可以参考下面实例

示例：  

1. `365Scores_2024_2_5_16_7-8_train_1_1.png`
2. `365Scores_2024_2_5_16_7-8.txt`

文件结构大概为：  

```txt
root
|-- pic
|   |-- ....png
|   |-- ....png
|   `-- ....png
`-- txt
    |-- ....txt
    |-- ....txt
    `-- ....txt
```

## 功能要求

将pic中的png图像文件按照train和val分别放入root下的train和val目录中  
然后将txt中与png图像`tag_time-tag`相同的txt文件放入对应的train和val目录中  

然后进行重命名  
重命名后的格式为：  

```txt
tag_class_duplicate.png
```

即需要去掉  

1. time-tag标签
2. train/val标签

```txt
tag_class_duplicate.txt
```

即需要根据对应的png文件进行重命名

如有异常，将异常的pic和txt分别放入一个root下的error/pic和root下的error/txt中  
并统计正常和异常的数量，输出到控制台  
