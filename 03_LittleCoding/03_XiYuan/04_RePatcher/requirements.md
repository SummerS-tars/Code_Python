# Requirement Documentation

在经过PicTxtPatcher处理之后，已经成功完成图片与相应的标注文件的配对  
具体处理结果结构请参考相关文档  
现在在处理过程中  
发现部分unknown的图片文件属于某些对应的已知类别文件  
同时发现部分class的图片实际属于错误归类，应属于其他class  
此时已经经过手动调整图片所属class而正确归类  

但是标注文件仍保留在了原class目录下的txt目录中  
请帮我找到移动过的图片文件，并重新帮他们将标注文件从原class目录下的txt目录中移动到正确class目录下的txt目录中  

此外注意：  
现在图片文件经过标注增加了`_class_duplicate`后缀  
请在匹配标注文件时忽略该后缀  

## 基础

新的命名规范：  

```txt
tag_train/val_class_duplicate.png
```

其中：  

`tag`分为两种  
一种是已知的类别，如`365Scores`、`XiYuan`等  
表现为`tag_time-tag`
另一种属于`unknown`类别  
表现为`time_hash-tag`  

所有的图片都有`_class_duplicate`后缀  
请在匹配时注意忽略该后缀（因为标注文件没有该后缀）  

## 示例

图片文件：  

```txt
2024_3_24_12_4_61dde84214804fe8b05cac4394187a00-8_train_91_1.png
```

从

```txt
E:\_WorkingTemp\XiYuanTotalProcess\class_all\class_unknown\class18_apnews\pic
```

移动到了

```txt
E:\_WorkingTemp\XiYuanTotalProcess\class_all\class\APNews\pic
```

而对应的标注文件

```txt
2024_3_24_12_4_61dde84214804fe8b05cac4394187a00-8.txt
```

则需要从

```txt
E:\_WorkingTemp\XiYuanTotalProcess\class_all\class_unknown\class18_apnews\txt
```

移动到

```txt
E:\_WorkingTemp\XiYuanTotalProcess\class_all\class\APNews\txt
```
