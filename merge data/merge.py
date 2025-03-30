"""
一次只能合并两个文件
"""

import pandas as pd
import os
from tqdm import tqdm
import pyreadstat as pr

basePath = r'C:\Users\yst\Desktop\self-efficacy\data'
fileName1 = 'student.sav'
fileName2 = 'school.sav'

df1, meta1 = pr.read_sav(os.path.join(basePath, fileName1))
df2, meta2 = pr.read_sav(os.path.join(basePath, fileName2))
df1_columns = df1.columns
df2_columns = df2.columns


# print(meta1.column_labels)
# print(meta2.column_labels)


def merge_data(d1: pd.DataFrame, d2: pd.DataFrame, index_column_name: str):
    """
    将d2合并至d1
    :param d1: 原数据
    :param d2: 被合并的数据
    :return: 返回一个合并好的dataframe
    """
    # 找出d1里没有，但d2里有的列
    unique_columns_sored = [col for col in d2.columns if col not in d1.columns]

    # 将unique_columns组成一个样本数和d1一样的dataframe
    new_columns_data = {col: [None] * len(d1) for col in unique_columns_sored}
    new_df = pd.DataFrame(new_columns_data)
    # 复制列的数据类型
    for col in unique_columns_sored:
        new_df[col] = new_df[col].astype(d2[col].dtype)

    d1 = pd.concat([d1, new_df], axis=1)  # 将新的dataframe和d1组合，这样d1就有了与d2相互没有的列

    unique_columns = list(unique_columns_sored)
    d2_index_column = d2[index_column_name]  # 将一列数据取出
    # d2_index_column = d2_index_column[:5] # 测试
    for step, column in tqdm(enumerate(d2_index_column), total=len(d2_index_column)):  # [34400001,34400002,34400003...]
        d2_target_row = d2[d2[index_column_name] == column]  # 取出d2对应列中的对应行,shape(1, 431)(index,column)
        d1_target_row = d1[d1[index_column_name] == column]  # 取出d1对应列中的对应行,shape(26, 1697) (index,column)
        for unique_column in unique_columns:  # [SC018Q10JA01,SC018Q10JA02...]
            for i in d1_target_row.index:  # [0,5,33,126...]
                d1.loc[i, unique_column] = d2_target_row.loc[step, unique_column]
    return d1


def save(df, path, filename, meta, compress=True):
    abs_path = os.path.join(path, filename)
    pr.write_sav(df, abs_path,
                 column_labels=meta.column_labels,
                 variable_value_labels=meta.variable_value_labels,
                 missing_ranges=meta.missing_ranges,
                 variable_display_width=meta.variable_display_width,
                 variable_measure=meta.variable_measure,
                 variable_format=meta.original_variable_types,
                 row_compress=compress
                 )


def find_common_elements_and_indices(a, b):
    # 找出共同元素
    common_elements = set(a).intersection(set(b))
    # 存储共同元素及其在b中的索引
    result = {}
    for element in common_elements:
        # 获取元素在b中的所有索引位置
        indices = [i for i, x in enumerate(b) if x == element]
        result[str(element)] = indices[0]
    return result


def remove_elements_by_indices(lst, indices):
    return [element for i, element in enumerate(lst) if i not in indices]


def process_meta(df1_columns, df2_columns, meta1, meta2):
    # 找到两列表相同的元素，并返回这些元素在第二个列表的下标
    column_labels = find_common_elements_and_indices(df1_columns, df2_columns)  # {'OECD': 8, 'CYC': 3}
    column_labels_keys = list(column_labels.keys())  # ['VER_DAT', 'STRATUM', 'OECD']
    column_labels_values = list(column_labels.values())  # [8, 3, 10, 1]

    # 处理好的column_labels
    meta2_column_labels = remove_elements_by_indices(meta2.column_labels, column_labels_values)

    # 处理好的variable_value_labels
    meta2_variable_value_labels = meta2.variable_value_labels
    for key in column_labels_keys:
        if key in meta2.variable_value_labels:
            del meta2_variable_value_labels[key]

    # 处理好的variable_display_width
    meta2_variable_display_width = meta2.variable_display_width
    for key in column_labels_keys:
        if key in meta2.variable_display_width:
            del meta2_variable_display_width[key]

    # 处理好的variable_measure
    meta2_variable_measure = meta2.variable_measure
    for key in column_labels_keys:
        if key in meta2.variable_measure:
            del meta2_variable_measure[key]

    # 处理好的original_variable_types
    meta2_original_variable_types = meta2.original_variable_types
    for key in column_labels_keys:
        if key in meta2.original_variable_types:
            del meta2_original_variable_types[key]

    # 将meta2合并到meta1中
    # 合并column_labels
    meta1.column_labels.extend(meta2_column_labels)
    # 合并variable_value_labels
    meta1.variable_value_labels = {**meta1.variable_value_labels, **meta2_variable_value_labels}
    # 合并variable_display_width
    meta1.variable_display_width = {**meta1.variable_display_width, **meta2_variable_display_width}
    # 合并variable_measure
    meta1.variable_measure = {**meta1.variable_measure, **meta2_variable_measure}
    # 合并variable_value_labels
    meta1.original_variable_types = {**meta1.original_variable_types, **meta2_original_variable_types}

    print('meta数据合并完成')
    return meta1


if __name__ == '__main__':
    df = merge_data(df1, df2, index_column_name='CNTSCHID')
    meta = process_meta(df1_columns, df2_columns, meta1, meta2)
    save(df, './', 'student_school.sav', meta, compress=True)
