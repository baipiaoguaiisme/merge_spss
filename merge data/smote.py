import numpy as np
from imblearn.over_sampling import SMOTE
import pandas as pd
import os
import pyreadstat as pr
from collections import Counter


# 数据文件的路径
bashPath = r'C:\Users\perper\Desktop\self-efficacy\data'
# 数据文件名
fileName = 'student_school_filled_knn_standard.sav'
savePath = 'student_school_filled_knn_standard_smote.sav'

df, meta = pr.read_sav(os.path.join(bashPath, fileName))
x = df[df.columns[:-1]]
columns = x.columns
y = df[df.columns[-1]]

# 使用 SMOTE 进行重采样
sm = SMOTE(random_state=42, k_neighbors=200)
x, y = sm.fit_resample(x, y)

# 将重采样后的结果转换回 DataFrame
resampled_df = pd.DataFrame(x, columns=columns)
resampled_df['ICTEFFIC'] = y

pr.write_sav(resampled_df, os.path.join(bashPath, savePath),
             column_labels=meta.column_labels,
             variable_value_labels=meta.variable_value_labels,
             variable_display_width=meta.variable_display_width,
             variable_measure=meta.variable_measure,
             variable_format=meta.original_variable_types,
             row_compress=True
             )
