import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import pyreadstat as pr
import os

basePath = r'C:\Users\yst\Desktop\self-efficacy\data'
fileNames = ['train_test_data_standard.sav']
path = os.path.join(basePath, fileNames[0])

df, meta = pr.read_sav(path)

# sns.boxplot(data=df)
# sns.boxplot(data=df[df.columns[:20]])

fig, axes = plt.subplots(5, 4, figsize=(50,40))

# 遍历每一列，在对应的子图中绘制箱型图
for i, col in enumerate(df.columns[:20]):
    # 计算当前列对应的子图的行和列索引
    row = i // 4
    col_index = i % 4
    # 获取对应的子图对象
    ax = axes[row, col_index]
    sns.boxplot(data=df[col], ax=ax)
    ax.set_title(f'Box Plot of {col}')
    ax.set_xlabel(col)

# 调整子图之间的间距
plt.tight_layout()

# 显示图表
plt.show()

