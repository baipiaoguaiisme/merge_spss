## 第三方库：pyreadstat，安装命令：pip install pyreadstat，版本：1.2.8<br>

***
## 字段说明
![img.png](img.png)

|  列名  |         Description          |   note    |
|:----:|:----------------------------:|:---------:|
|  名称  |      meta.column_names       | type:list |
|  类型  | meta.readstat_variable_types | type:dict |
|  宽度  | meta.variable_display_width  | type:dict |
| 小数位数 | meta.original_variable_types | type:dict | 
|  标签  |        column_labels         | type:list |
|  值   |    variable_value_labels     | type:dict |
|  缺失  |        missing_ranges        | type:dict |
|  测量  |       variable_measure       | type:dict |

#### Note:<br>meta.original_variable_types形如：___{'CNT': 'A3', 'CNTRYID': 'F3.0'}___<br>A3中的A通常代表 “字符型（Character）”数据类型，3表示该字符变量的显示宽度为3个字符<br>F3.0的F一般代表 “数值型（Numeric）”数据。3表示整个数值的宽度为3个字符.0表示小数点后的小数位数为 0
***
## 读取文件：
    df, meta = pr.read_sav(filePath, user_missing=True) #user_missing默认为False，若设置为True，缺失值会用设定好的缺失值代替，如99，虽然meta.missing_ranges有数据，但会影响计算
***
## 写入文件：
    pr.write_sav(df, 'xxx.sav',
                 column_labels=meta.column_labels,
                 variable_value_labels=meta.variable_value_labels,
                 missing_ranges=meta.missing_ranges,
                 variable_display_width=meta.variable_display_width,
                 variable_measure=meta.variable_measure,
                 variable_format=meta.original_variable_types,
                 row_compress=True # 压缩方式有两种，一种是row_compress行压缩，另一种是compress文件压缩，只能选一种为True
                 )
### row_compress与compress
- compress的优劣
  - 优点：能显著减小文件大小，在存储和传输方面具有明显优势。如果需要将.sav文件存储在空间有限的设备上，或者通过网络传输给他人，使用compress=True可以节省大量空间和传输时间。
  - 缺点：压缩和解压缩过程可能会消耗更多的时间和计算资源。在读取.zsav文件时，需要先进行解压缩操作，这可能会比读取普通.sav文件慢一些，尤其是在处理大型文件时。
- row_compress的优劣
  - 优点：在不改变文件格式为.zsav的前提下，对数据进行行级压缩，也能在一定程度上减少文件大小。同时，由于没有对整个文件进行压缩，在读取和写入数据时，相对.zsav格式可能会更高效一些，因为不需要进行整体的压缩和解压缩操作，只是在行数据处理上有一定的额外开销。 
  - 缺点：压缩效果可能不如compress参数明显，对于一些数据特征不适合行压缩算法的文件，可能无法达到理想的压缩比。

