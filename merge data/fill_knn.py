import pandas as pd
from sklearn.impute import KNNImputer
import pandas as pd
import pyreadstat as pr
import os
from tqdm import tqdm
from utils.meta_process import *
import numpy as np


def main(bashPath, fileName, savePath, num_splits=2, n_neighbors=200, missing_threshold=0.5, split=False,
         compress=True):
    filePath = os.path.join(bashPath, fileName)
    df, meta = pr.read_sav(filePath)

    # knn填充法在遇到全缺失的列时，会报错，常见处理方法是直接删除全缺失的列
    imputer = KNNImputer(n_neighbors=n_neighbors)

    # 对缺失超过阈值的列进行删除
    # 存储被删除的列的索引
    del_column_indices = []
    # 存储被删除的列的名字
    del_column_names = []
    for col in tqdm(df.columns, desc='drop column'):
        missing_percentage = df[col].isnull().mean()
        if missing_percentage > missing_threshold:
            del_column_indices.append(df.columns.get_loc(col))
            del_column_names.append(col)

    # 删除缺失率超出阈值的列
    df = df.drop(df.columns[del_column_indices], axis=1)
    print(f'全缺失的列的数目：{len(del_column_indices)}')

    # 缺失率超出阈值的列被删除后，需要对meta也进行相应列的删除
    meta_dict = meta_process(meta, del_column_names, del_column_indices)

    # 拆分dataframe
    if split:
        # 拆分 DataFrame
        split_dfs = np.array_split(df, num_splits)
        # 对每个拆分后的 DataFrame 进行 KNN 填充缺失值
        filled_dfs = []
        for split_df in tqdm(split_dfs, desc='split'):
            filled_arr = imputer.fit_transform(split_df)  # type numpy array
            filled_df = pd.DataFrame(filled_arr, columns=split_df.columns)
            filled_dfs.append(filled_df)
        df_filled = pd.concat(filled_dfs, ignore_index=True)
    else:
        # 填补缺失值
        df_filled = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

    pr.write_sav(df_filled, savePath,
                 column_labels=meta_dict['column_labels'],
                 variable_value_labels=meta_dict['variable_value_labels'],
                 variable_display_width=meta_dict['variable_display_width'],
                 variable_measure=meta_dict['variable_measure'],
                 variable_format=meta_dict['variable_format'],
                 row_compress=compress
                 )
    print('successfully')


if __name__ == '__main__':
    # 数据文件的路径
    bashPath = r'C:\Users\perper\Desktop\self-efficacy\data'
    # 数据文件名
    fileName = 'student_school_extraFactors.sav'
    savePath = 'student_school_filled_knn__.sav'
    n_neighbors = 200
    missing_threshold = 0.65
    num_splits = 2
    split = True
    compress = True
    main(bashPath, fileName, savePath, num_splits=num_splits, n_neighbors=n_neighbors,
         missing_threshold=missing_threshold,
         split=split, compress=compress)
