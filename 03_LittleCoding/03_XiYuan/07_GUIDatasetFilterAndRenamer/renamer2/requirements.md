# 需求文档

数据清理与重命名脚本1
Cleaner and Renamer 1  

## 背景介绍

现有文件命名  

```txt
{appname}_{id}_{dul_times}.jpg  
{appname}_{id}_{dul_times}_visualized.jpg  
{appname}_{id}_{dul_times}.txt  
```

- appname：应用名称，如WeChat、QQ等
- id：唯一标识符  
- dul_times：重复次数标识符，从1开始递增，用于区分同一id下的多张图片  

源文件目录结构：  

```txt
process_1/
    {appname}_{id}_{dul_times}.jpg  
    {appname}_{id}_{dul_times}_visualized.jpg  
    {appname}_{id}_{dul_times}.txt  
```

## 需求说明

经过人工筛选  

- 以visualized图片为准，删除没有对应visualized图片的普通图片和txt文件  
- 可能存在部分visualized图片因为人工的更改找不到对应的普通图片和txt文件  
    将这些没有匹配的visualized图片也删除  

然后需要对剩余的文件进行重命名  
要求：  

收集原始id  
将其从新从1开始递增编号，作为new_id  
同一原始id下的多个dul_times也进行收集  
进行从1开始递增编号，作为new_dul_times  
文件保留在原目录下，只进行重命名  
