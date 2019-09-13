import os
os.chdir("E:\\working\\Python\\\神经网络")
############
# 打开图片
from PIL import Image
img=Image.open('单层网络.png')
img.show()
##################
# matplotlib显示图片
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as im # im 用于读取图片
lena = im.imread('单层网络.png') # 
# 此时lena就已经是一个 np.array 
lena.shape 
plt.imshow(lena) # 显示图片
plt.axis('off') # 不显示坐标轴
plt.show()
######################################################
#多层神经网络
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib
train = pd.read_csv("mnist_train.csv")
test = pd.read_csv("mnist_test.csv")
train.shape
train.columns
X_train = train.iloc[:, 1:]
y_train = train.loc[:, 'label']
X_test = test.iloc[:, 1:]
y_test = test.loc[:, 'label']
print('Rows: %d, columns: %d' % (X_train.shape[0], X_train.shape[1]))
print('Rows: %d, columns: %d' % (X_test.shape[0], X_test.shape[1]))

import matplotlib.pyplot as plt

fig, ax = plt.subplots(nrows=2, ncols=5, sharex=True, sharey=True,)
ax = ax.flatten()
for i in range(10):
    #i = 0
    img = X_train[y_train == i].iloc[0].reshape(28, 28)
    ax[i].imshow(img, cmap='Greys', interpolation='nearest')

ax[0].set_xticks([])
ax[0].set_yticks([])
plt.tight_layout()
plt.savefig('mnist_all.png', dpi=300)
plt.show()
###########################
# 使用多层感知器进行手写数字的分析
mlp = MLPClassifier()
mlp.fit(X_train, y_train)
print('默认参数的多层感知器精度为 %.3f' % mlp.score(X_test, y_test))
joblib.dump(mlp, 'mlp.m')