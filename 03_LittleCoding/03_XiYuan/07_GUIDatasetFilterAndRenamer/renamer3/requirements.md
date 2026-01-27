# requirements

命名格式更改脚本  
Renamer2  
负责将其他脚本梳理下来的中间命名改成最终命名格式  

## 背景介绍

经过前面的[filter1脚本](../filter1/README.md)处理  
我们的到的数据命名格式如下：  

```txt
`{appname}_{senary}_{new_id}_{dul_times}.jpg`
`{appname}_{senary}_{new_id}_{dul_times}_visualized.jpg`
`{appname}_{senary}_{new_id}_{dul_times}.txt`
```

字段解释：  

- `{appname}`：应用名称，例如：eleme、zhifubao、tencent_meeting 等  
- `{senary}`：场景名称，例如：main、personal 等  
- `{new_id}`：场景下唯一标号，从1开始递增  
- `{dul_times}`：类似重复次数，在同意场景下的同一new_id下，通过dul_times区分不同的图片和标注文件，也从1开始递增  

会分布在不同的 dataset_{appname} 文件夹下

## 最终命名格式要求

去掉{senary}字段，重排{new_id}字段  
将{senary}_{new_id}合并成新的{new_id}，从1开始递增  
保持{dul_times}字段不变  

最终命名格式如下：  

```txt
{appname}_{new_id}_{dul_times}.jpg
{appname}_{new_id}_{dul_times}_visualized.jpg
{appname}_{new_id}_{dul_times}.txt
```
