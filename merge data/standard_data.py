from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import pyreadstat as pr
import os

basePath = r'C:\Users\perper\Desktop\self-efficacy\data'
fileNames = ['student_school_filled_knn.sav']
saveName = 'student_school_filled_knn_standard.sav'
path = os.path.join(basePath, fileNames[0])

df, meta = pr.read_sav(path)

z_score_scaler = StandardScaler()
new_df = pd.DataFrame(z_score_scaler.fit_transform(df), columns=df.columns)

for key, value in meta.original_variable_types.items():
    if value.startswith('F'):
        res = value.split('.')[0] + '.4'
        meta.original_variable_types[key] = res

pr.write_sav(new_df, os.path.join(basePath, saveName),
             column_labels=meta.column_labels,
             variable_value_labels=meta.variable_value_labels,
             missing_ranges=meta.missing_ranges,
             variable_display_width=meta.variable_display_width,
             variable_measure=meta.variable_measure,
             variable_format=meta.original_variable_types,
             row_compress=True
             )
print('successful')
