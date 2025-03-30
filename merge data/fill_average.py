import pandas as pd
import pyreadstat as pr
import os
from tqdm import tqdm

# 数据文件的路径
bashPath = r'C:\Users\yst\Desktop\xxx'
# 数据文件名
fileName = 'xxx.sav'
saveFileName = 'xxx.sav'

filePath = os.path.join(bashPath, fileName)
df, meta = pr.read_sav(filePath)
# 创建一个结构与df新的dataframe，用于将计算好的案例进行填补
new_df = pd.DataFrame(columns=df.columns)
# 复制列的数据类型
for col in df.columns:
    new_df[col] = new_df[col].astype(df[col].dtype)
# 方便判断该变量是否是字符串或小数点数量
variable_types = meta.original_variable_types  # {'CNT': 'A3','CYC': 'A4', 'CNTRYID': 'F3.0', 'ATTCONFM': 'F7.4'}

for column in tqdm(df.columns,desc='filling data'):
    # 如果有缺失值则使用平均值填补
    if df[column].isna().any():
        # 变量的类型
        class_column_type = variable_types[column]  # 'A4','F3.0'...
        # 只有数值类型才进行填补
        if class_column_type.startswith('F'):
            point_num = class_column_type.split('.')[-1]
            mean = round(df[column].mean(), int(point_num))
            df[column] = df[column].fillna(mean)
        # 字符类型则使用第一个案例进行填补
        elif class_column_type.startswith('A'):
            aver = df[column].iloc[0]
            df[column] = df[column].fillna(aver)
# 对全缺失的列进行删除
# 存储被删除的列的索引
del_column_indices = []
# 存储被删除的列的名字
del_column_names = []
for column in tqdm(df.columns,desc='dropping column'):
    if df[column].isna().any():
        del_column_indices.append(df.columns.get_loc(column))
        del_column_names.append(column)
# 删除全缺失的列
df = df.drop(df.columns[del_column_indices], axis=1)

# 全缺失的列被删除后，需要对meta也进行相应列的删除
# 处理好的column_labels
meta_column_labels = [element for i, element in enumerate(meta.column_labels) if i not in del_column_indices]

# 处理好的variable_value_labels
meta_variable_value_labels = meta.variable_value_labels
for key in del_column_names:
    if key in meta.variable_value_labels:
        del meta_variable_value_labels[key]

# 处理好的variable_display_width
meta_variable_display_width = meta.variable_display_width
for key in del_column_names:
    if key in meta.variable_display_width:
        del meta_variable_display_width[key]

# 处理好的variable_measure
meta_variable_measure = meta.variable_measure
for key in del_column_names:
    if key in meta.variable_measure:
        del meta_variable_measure[key]

# 处理好的original_variable_types
meta_original_variable_types = meta.original_variable_types
for key in del_column_names:
    if key in meta.original_variable_types:
        del meta_original_variable_types[key]


# 保存文件
pr.write_sav(df, os.path.join(bashPath, saveFileName),
             column_labels=meta_column_labels,
             variable_value_labels=meta_variable_value_labels,
             variable_display_width=meta_variable_display_width,
             variable_measure=meta_variable_measure,
             variable_format=meta_original_variable_types,
             row_compress=True
             )
print('successfully')
