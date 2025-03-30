import pandas as pd
import pyreadstat as pr
import os
from tqdm import tqdm

# 数据文件的路径
bashPath = r'C:\Users\yst\Desktop\self-efficacy\data'
# 数据文件名
fileNames = ['teacher.sav']

# 根据flag，将相同flag的变量/列平均成一条案例
flag = 'CNTSCHID'

for fileName in fileNames:
    filePath = os.path.join(bashPath, fileName)
    df, meta = pr.read_sav(filePath)
    # 创建一个结构与df新的dataframe，用于将计算好的案例进行填补
    new_df = pd.DataFrame(columns=df.columns)
    # 复制列的数据类型
    for col in df.columns:
        new_df[col] = new_df[col].astype(df[col].dtype)
    # 方便判断该变量是否是字符串或小数点数量
    variable_types = meta.original_variable_types  # {'CNT': 'A3','CYC': 'A4', 'CNTRYID': 'F3.0', 'ATTCONFM': 'F7.4'}

    # 将重复的flag数值去掉
    flag_values = list(dict.fromkeys(df[flag].tolist()))  # [34400001.0, 34400002.0, 34400003.0...]

    index = 0

    for flag_value in tqdm(flag_values):  # [34400001.0, 34400002.0, 34400003.0...]
        # 将相同flag value的选出
        class_df = df[df[flag] == flag_value]
        # class dataframe的列名
        class_df_columns = class_df.columns
        for class_column in class_df_columns:
            # 变量的类型
            class_column_type = variable_types[class_column]  # 'A4','F3.0'...
            # 如果该变量为字符串，直接选取该class的该变量的第一个数值为变量的值
            if class_column_type.startswith('A'):
                # 不能写成aver = class_df.loc[0,class_column],因为有些class df第一行数据可能是原始df的第30个元素,所以就得用class_df.loc[29,class_column]来取,因此采取下述写法可解决此问题
                aver = class_df[class_column].iloc[0]
                new_df.loc[index, class_column] = aver
            # 如果该变量为数值型，则选取该class的该变量的平均值为变量的值
            elif class_column_type.startswith('F'):
                # 查看该变量的小数点
                point_num = class_column_type.split('.')[-1]
                # 一般使用pandas或pyreadstat读取sav文件时，文件中的数值型数值一般会转换为float64类型，因此round(mean,0)仍然会残留一个小数点
                # 计算均值并四舍五入到该小数点位
                mean = round(class_df[class_column].mean(), int(point_num))
                new_df.loc[index, class_column] = mean
        index += 1
    # 过滤掉非数值型变量的缺失值范围
    numeric_columns = [col for col, var_type in variable_types.items() if var_type.startswith('F')]
    filtered_missing_ranges = {col: meta.missing_ranges[col] for col in meta.missing_ranges if col in numeric_columns}
    # 保存文件
    pr.write_sav(new_df, 'teacher_average.sav',
                 column_labels=meta.column_labels,
                 variable_value_labels=meta.variable_value_labels,
                 missing_ranges=filtered_missing_ranges,
                 variable_display_width=meta.variable_display_width,
                 variable_measure=meta.variable_measure,
                 variable_format=meta.original_variable_types,
                 row_compress=True
                 )
