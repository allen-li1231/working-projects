# -*- coding: utf-8 -*-

# 数据预处理
import pandas as pd
from sklearn import datasets as dss
from numpy import nan as NA

iris = dss.load_iris() # 加载鸢尾花数据
iris.data # 获取鸢尾花特征数据
iris.feature_names # 获取鸢尾花
print(iris.DESCR) # 获取数据的描述
iris.target # 获取数据的标签
iris.target_names # 数据的标签名
iris_df = pd.DataFrame(iris.data, columns=iris.feature_names) # 创建DataFrame结构
iris_df 
iris_df.head() # 获取前几行数据
iris_df.describe() # 获取数据的大概信息
iris_df.isnull() # 获取数据是否是缺失值的bool型结构
iris_df.isnull().sum()

# 还原本来的数据
iris_df_cp = iris_df.copy()
# iris_df_cp.dropna() # axis=1, how='any'
# iris_df_cp.fillna(method='ffill')
iris_df_cp['iris_name'] = iris.target
iris_df_cp['iris_name'].map({k:v for k,v in enumerate(iris.target_names)})
iris_df_cp.iloc[[1, 3, 5], [1, 2, 3]] = NA
#iris_df0 = iris_df_cp.loc[iris_df_cp.iloc[:,4] == 0]
# 使用sklearn补全缺失值
from sklearn import preprocessing as ppc
ipt = ppc.Imputer() # 
ipt.fit(iris_df_cp.iloc[:, :-1])
ipt.transform(iris_df_cp.iloc[:, :-1])

info_df = pd.read_excel('info.xlsx', index_col=0)
print(info_df.head())
print(info_df.shape)

info_df['工作年限'] = ppc.Imputer().fit_transform(info_df['工作年限'].reshape(-1, 1))

def outlierprocessing(array_like, method='mean'):
    """
    异常值处理函数
    """
    #array_like = info_df['工作年限']
    import numpy as np
    import matplotlib.pyplot as plt
    
    tmp_array = np.array(array_like)
    
    boxplot = plt.boxplot(tmp_array, whis=8)
    dots = boxplot['fliers'][0].get_ydata()
    print(dots)
    m = np.mean
    if method == 'median':
        m = np.median
    mean = m(tmp_array)
    for d in dots:
        tmp_array[tmp_array == d] = mean
    return tmp_array
    
info_df['工作年限'] = outlierprocessing(info_df['工作年限'])

# 将类别特征转为数字特征
info_df['学历'] = info_df['学历'].map({'中技':0, '大专':1, '本科':2, '硕士':3})
info_df['学历'][info_df['学历'].isnull()] = info_df['学历'].mean()

info_df = pd.read_excel('info.xlsx', index_col=0)
info_df_cp = info_df.copy()
# 使用sklearn
info_df_cp['性别'] = ppc.LabelEncoder().fit_transform(info_df_cp['性别'])
info_df_cp['学历'] = ppc.LabelEncoder().fit_transform(info_df_cp['学历'])
# 哑编码
# 特征中只有 男 女两种标签  [1, 0]  [0, 1]
# 特征中有 红 蓝 青三种标签  [1 ,0, 0] [0,1,] [0,0,1]
pd.get_dummies(info_df['性别'])
pd.get_dummies(info_df['学历'])

info_df = pd.read_excel('info.xlsx', index_col=0)

# 将标签转为数值
def label_to_number(array_like, max_length = 3):
    """
    将标签转为数值
    """
    import pandas as pd
    tmp_array = pd.Series(array_like)
    unique_list = tmp_array.unique()
    if len(unique_list) > max_length:
        tmp = tmp_array.map({v:k for k,v in enumerate(unique_list)})
    else:
        tmp = pd.get_dummies(tmp_array)
    return tmp

info_df = info_df.reindex(columns=['性别', '出生日期', '居住地', '学历', '工作年限'])
# 使用哑编码将标签转为数字特征
info_df = pd.get_dummies(info_df, columns=['性别', '居住地'])
# 使用map进行转为数字特征
def op_1(arg):
    return int(''.join(arg.split('/')))
info_df['出生日期'] = info_df['出生日期'].apply(op_1)

info_df['学历'] = info_df['学历'].map({'中技':0, '大专':1, '本科':2, '硕士':3})
info_df['学历'] = ppc.Imputer().fit_transform(info_df['学历'].reshape(-1, 1))

info_df['工作年限'] = ppc.Imputer().fit_transform(info_df['工作年限'].reshape(-1, 1))
info_df['工作年限'] = outlierprocessing(info_df['工作年限'])

# 区间缩放进行无量纲化
tmp = ppc.MinMaxScaler().fit_transform(info_df)
# 使用的标准化进行无量纲化
tmp = ppc.StandardScaler().fit_transform(info_df)

# 使用方差选取特征
from sklearn import feature_selection as fs
fs.VarianceThreshold(threshold=1).fit_transform(info_df)

# 使用卡方检验进行特征选取
from sklearn.feature_selection import chi2
fs.SelectKBest(chi2, k=2).fit_transform(iris.data, iris.target)

# 降维
# PCA
from sklearn.decomposition import PCA

PCA(n_components=2).fit_transform(iris.data)

PCA(n_components=2).fit_transform(iris.data, iris.target)