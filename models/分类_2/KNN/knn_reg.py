# 从sklearn.datasets导入波士顿房价数据读取器。
from sklearn.datasets import load_boston
# 从读取房价数据存储在变量boston中。
boston = load_boston()

from sklearn.model_selection import train_test_split

X = boston.data
X.shape
y = boston.target

# 随机采样25%的数据构建测试样本，其余作为训练样本。
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=33, test_size=0.25)

# 从sklearn.preprocessing导入数据标准化模块。
from sklearn.preprocessing import StandardScaler
# 分别初始化对特征和目标值的标准化器。
ss_X = StandardScaler()
#ss_y = StandardScaler()
# 分别对训练和测试数据的特征以及目标值进行标准化处理。
X_train = ss_X.fit_transform(X_train)
X_test = ss_X.fit_transform(X_test)


#y_train = ss_y.fit_transform(y_train)
#y_test = ss_y.fit_transform(y_test)

# 从sklearn.neighbors导入KNeighborRegressor（K近邻回归器）。
from sklearn.neighbors import KNeighborsRegressor
mse1 = [];mse2 = []
mae1 = [];mae2 = []
r21 = [];r22 = []
for i in range(4, 40):
    n_neighbors = i
    # 初始化K近邻回归器，并且调整配置，使得预测的方式为平均回归：weights='uniform'。
    uni_knr = KNeighborsRegressor(weights='uniform', n_neighbors = n_neighbors)
    uni_knr.fit(X_train, y_train)
    uni_knr_y_predict = uni_knr.predict(X_test)
    
    # 初始化K近邻回归器，并且调整配置，使得预测的方式为根据距离加权回归：weights='distance'。
    dis_knr = KNeighborsRegressor(weights='distance', n_neighbors = n_neighbors)
    dis_knr.fit(X_train, y_train)
    dis_knr_y_predict = dis_knr.predict(X_test)
    
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    # 使用R-squared、MSE以及MAE三种指标对平均回归配置的K近邻模型在测试集上进行性能评估。
    mse1.append(mean_squared_error(y_test, uni_knr_y_predict))
    mse2.append(mean_squared_error(y_test, dis_knr_y_predict))
    print('R-squared value of uniform-weighted KNeighorRegression:', uni_knr.score(X_test, y_test))     #此处是R^2
    print('The mean squared error of uniform-weighted KNeighorRegression:', mean_squared_error(y_test, uni_knr_y_predict))
    print('The mean absoluate error of uniform-weighted KNeighorRegression', mean_absolute_error(y_test, uni_knr_y_predict))
    
    print('R-squared value of uniform-weighted KNeighorRegression:', dis_knr.score(X_test, y_test))
    print('The mean squared error of uniform-weighted KNeighorRegression:', mean_squared_error(y_test, dis_knr_y_predict))
    print('The mean absoluate error of uniform-weighted KNeighorRegression', mean_absolute_error(y_test, dis_knr_y_predict))
mse1
mse2
import numpy as np
i = np.arange(4, 40, 1)
import matplotlib.pyplot as plt
plt.plot(i, mse1)
plt.plot(i, mse2)
