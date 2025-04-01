import pandas as pd
from sklearn.impute import KNNImputer
import pandas as pd
import pyreadstat as pr
import os
from tqdm import tqdm
from utils.meta_process import *

# 数据文件的路径
bashPath = r'C:\Users\perper\Desktop\self-efficacy\data'
# 数据文件名
fileName = 'student_school_extraFactors.sav'
saveFileName = 'student_school_filled_knn.sav'

filePath = os.path.join(bashPath, fileName)
df, meta = pr.read_sav(filePath)

imputer = KNNImputer(n_neighbors=200)

# 对全缺失的列进行删除
# 存储被删除的列的索引
del_column_indices = []
# 存储被删除的列的名字
del_column_names = []
for column in tqdm(df.columns, desc='dropping column'):
    if df[column].isna().all():
        del_column_indices.append(df.columns.get_loc(column))
        del_column_names.append(column)
# 删除全缺失的列
df = df.drop(df.columns[del_column_indices], axis=1)
print(f'全缺失的列的数目：{len(del_column_indices)}')

# 全缺失的列被删除后，需要对meta也进行相应列的删除
meta_dict = meta_process(meta, del_column_names, del_column_indices)

# 填补缺失值
df_filled = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

pr.write_sav(df_filled, os.path.join(bashPath, saveFileName),
             column_labels=meta_dict['column_labels'],
             variable_value_labels=meta_dict['variable_value_labels'],
             variable_display_width=meta_dict['variable_display_width'],
             variable_measure=meta_dict['variable_measure'],
             variable_format=meta_dict['variable_format'],
             row_compress=True
             )
print('successfully')
