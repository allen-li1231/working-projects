# -*- coding: utf-8 -*-

"""
支持向量机的核心：寻找分类中距离最近的点的距离，使其最大化，这些样本点即为支持向量，由支持向量建立超平面
"""

from sklearn.svm import SVC
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

# 加载数据
iris = datasets.load_iris()
X = iris.data[:, [2,3]]
y = iris.target

# 数据的分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# 数据处理, 标准化缩放
sc = StandardScaler()
X_train_std = sc.fit_transform(X_train)
X_test_std = sc.transform(X_test)

svm = SVC(kernel='linear')
svm.fit(X_train_std, y_train)
print('准确度：%.3f' % svm.score(X_test_std, y_test))

moons = datasets.make_moons(n_samples=500, noise=0.3, random_state=0)
# print(moons)
X, y = moons
plt.scatter(X[:, 0], X[:,1], c=y)
plt.show()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# 数据处理, 标准化缩放
sc = StandardScaler()
X_train_std = sc.fit_transform(X_train)
X_test_std = sc.transform(X_test)

svm = SVC(C=10)
svm.fit(X_train_std, y_train)
print('训练集准确度：%.3f' % svm.score(X_train_std, y_train))
print('测试集准确度：%.3f' % svm.score(X_test_std, y_test))















