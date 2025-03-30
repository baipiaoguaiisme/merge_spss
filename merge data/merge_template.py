import pandas as pd
import pyreadstat as pr
import os
import numpy as np

bashPath = r'C:\Users\yst\Desktop\self-efficacy\data'
# fileNames = ['student.sav', 'school.sav', 'teacher.sav']
fileNames = ['student.sav']

columns = []
dfs = []

for fileName in fileNames:
    filePath = os.path.join(bashPath, fileName)
    df, meta = pr.read_sav(filePath, user_missing=False)
    # print(meta.column_labels)  # ['Country code 3-character', 'Country Identifier', 'Intl. School ID']
    # print(meta.variable_value_labels) # {'CNT': {'FRA': 'France', 'USA': 'United States'},'CNTRYID': {8.0: 'Albania', 31.0: 'Baku (Azerbaijan)'}}
    # print(meta.variable_display_width)  # {'CNT': 3, 'CNTRYID': 8, 'CNTSCHID': 8, 'CNTSTUID': 8, 'CYC': 4}
    # print(meta.variable_measure) # {'CNT': 'nominal', 'CNTRYID': 'nominal', 'PV10MPRE': 'scale', 'SENWT': 'scale'}
    # print(meta.original_variable_types)  # {'CNT': 'A3', 'CNTRYID': 'F3.0'}

# pr.write_sav(df, '1.sav',
#              column_labels=meta.column_labels,
#              variable_value_labels=meta.variable_value_labels,
#              missing_ranges=meta.missing_ranges,
#              variable_display_width=meta.variable_display_width,
#              variable_measure=meta.variable_measure,
#              variable_format=meta.original_variable_types,
#              row_compress=True
#              )
