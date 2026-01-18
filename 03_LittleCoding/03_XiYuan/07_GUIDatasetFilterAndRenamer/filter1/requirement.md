# requirements

用于对获取的GUI数据集进行过滤和重命名的工具

## 功能需求

分app配合人工筛选进行数据集的过滤  

然后进行相应的重命名  

## 具体背景

### 存储结构

数据集目录结构：

```txt
dataset_{appname}/
    <senary>_[id]_{timestamp}.jpg
    <senary>_[id]_{timestamp}_visualized.jpg
    <senary>_[id]_{timestamp}.txt

```

community_1_20260115_213121.txt

- appname：应用名称，如WeChat、QQ等
- senary：应用场景，如mainpage、detail、setting、personal_page等
- id：唯一标识符
- timestamp：时间戳，格式为YYYYMMDD_HHMMSS
- visualized：后缀，标识该图片为框选结果可视化版本

### 要求

id一般来说应该从1开始递增  
可能会出现重复的，这是故意取出来，用于辅助构成验证集的  

人工筛选是基于visualized图片进行的  
因此可能出现的漏号一般会出现在visualized图片中  
需要以visualized图片有的id序列为准  
删掉没有对应visualized图片的普通图片和txt文件  

重命名要求：  

{appname}_{senary}_{new_id}_{dul_times}.jpg  
{appname}_{senary}_{new_id}_{dul_times}_visualized.jpg  
{appname}_{senary}_{new_id}_{dul_times}.txt  

- new_id：从1开始递增的唯一标识符  
- dul_times：重复次数标识符，从1开始递增，用于区分同一new_id下的多张图片  
- 其他参数来自于原文件名  

文件不需要移动位置，只需要在原目录下进行重命名即可  
