# -*- coding: utf-8 -*-

from sklearn.datasets import load_iris
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
## 建立神经网络
fnn = buildNetwork(4, 10, 5, 1, bias = True)
fnn.modules
print("建立数据集")
# 建立数据集
iris = load_iris()
train, test, train_label, test_label = train_test_split(iris.data, iris.target)
ds = SupervisedDataSet(4, 1)
for i in range(len(train)):
    ds.addSample(train[i], train_label[i])
len(ds)
for inpt, target in ds:
    print(inpt, target)
    
print("构造bp")
# 构造bp训练节
trainer = BackpropTrainer(fnn, ds, 
                          momentum = 0.1, 
                          verbose = True, 
                          weightdecay = 0.01)
print("开始训练")
trainer.trainEpochs(epochs = 50)

print("开始返回结果")
out = SupervisedDataSet(4, 1)
for i in range(len(test)):
    temp = 0
    out.addSample(test[i], temp)
pred = fnn.activateOnDataset(out)
pred_p = np.round(pred, 2)
print(test_label)
print(pred_p)
## 用均方误差评估模型预测性能
mean_squared_error(test_label, pred_p)
