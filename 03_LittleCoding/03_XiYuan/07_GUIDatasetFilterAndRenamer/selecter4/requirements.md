# requirements

数据分类选择器  
用于将数据集分为训练集data和验证集val  

## 背景介绍

经过前面脚本链的处理  
最终得到数据命名格式如下  

```txt
{appname}_{new_id}_{dul_times}.jpg
{appname}_{new_id}_{dul_times}_visualized.jpg
{appname}_{new_id}_{dul_times}.txt
```

其中根据dul_times最大是否超过1来区分数据类型：  

- 如果最大就为1，说明该appname_new_id下只有一张图片和标注文件，直接划入数据集（不要放入验证集）  
- 如果最大大于1，说明该appname_new_id下有多张图片和标注文件，需要从中选择一部分划入验证集  

## 具体功能

- 扫描 dataset_* 目录，支持递归处理。  
- 根据 dul_times 最大值是否大于1 来区分数据类型。  
- 对于 dul_times 最大值大于1 的数据，直接划入数据集  
- 对于 dul_times 最大值等于1 的数据，按比例划分为训练集和验证集  
    比例方法：  
    - 提供验证集合占总数据集的比例参数，例如0.1  
    - 据此从 dul_times 最大值等于1 的数据中随机选择相应比例的数据划入验证集，其余划入训练集  
    - 此外由于可能有一些 appname_new_id 下的 dul_times 的值虽然大于1但比较小，例如2或3，此时考虑以一定概率选取1张图片划入验证集  
- 上述参数实现为一个参数配置文件 config.json，用户可根据需要自行修改  
- 源文件保留不变  
- 提供dry-run模式，仅查看将要执行的操作，不实际执行  

### 可能的特殊问题

不同的 dataset 下有可能出现同名文件的情况  
例如 dataset_elemee 和 dataset_zhifubao 下均有 eleme_1_1.jpg 文件  
此时统一处理方法为重排 new_id  
即将所有数据按 appname 分类后，重新为每个 appname 下的文件  
这可以作为单独的一个脚本在分类之前尝试执行  
要求支持仅检测同名文件而不实际重命名的 dry-run 模式  

### 目标目标结构

```txt
dataset
├── images
│   ├── data
│   └── val
├── labels
│   ├── data
│   └── val
└── visualized
    ├── data
    └── val
```

- images/data：训练集图片  
- images/val：验证集图片
- labels/data：训练集标注文件
- labels/val：验证集标注文件
- visualized/data：训练集可视化图片
- visualized/val：验证集可视化图片

数据图片为不带visualized后缀的jpg文件  
数据标注文件为txt文件  
可视化图片为带visualized后缀的jpg文件  
