"""
将需要的特征从PISA中提取出来
"""
import pyreadstat as pr
import os
from tqdm import tqdm
from utils.meta_process import *


def main(basePath, fileName, savePath, factorsPath):
    path = os.path.join(basePath, fileName)
    df, meta = pr.read_sav(path)

    # 需要的特征/变量
    with open(factorsPath, 'r', encoding='utf-8') as f:
        extract_factors = [line.strip() for line in f.readlines()]

    # 需要删除的特征名
    result_list = [x for x in df.columns if x not in extract_factors]

    # 删除的特征名对应的索引
    indices = []
    for col in tqdm(df.columns):
        if col in result_list:
            indices.append(df.columns.get_loc(col))

    new_df = df[extract_factors]

    meta_dict = meta_process(meta, result_list, indices)

    pr.write_sav(new_df, savePath,
                 column_labels=meta_dict['column_labels'],
                 variable_value_labels=meta_dict['variable_value_labels'],
                 variable_display_width=meta_dict['variable_display_width'],
                 variable_measure=meta_dict['variable_measure'],
                 variable_format=meta_dict['variable_format'],
                 row_compress=True
                 )
    print('successfully')


if __name__ == '__main__':
    # 数据文件的路径
    basePath = r'C:\Users\perper\Desktop\self-efficacy\data'
    # 数据文件名
    fileName = 'student_school.sav'
    savePath = r'C:\Users\perper\Desktop\self-efficacy\data\student_school_extraFactors.sav'
    factorsPath = r'./特征变量提取.txt'
    main(basePath, fileName, savePath, basePath, factorsPath)
