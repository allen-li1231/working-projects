#!/usr/bin/env python3
# coding:utf-8


import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


mpl.rcParams['figure.dpi'] = 50 # 设置fig的显示像素
mpl.rcParams['backend'] = 'Tkagg'   # 设置后端
figure0 = plt.figure(num=0, figsize=(8,4))
fig = plt.gcf()
fig.subplots_adjust()
plt.plot([1,2,3],[1,2,3],[1,2,3],[3,2,1])
axs = plt.gca()
axs.set_ylabel('测试')
print(axs.lines)
print(plt.getp(axs.lines[0], 'color'))
plt.xlabel('轴')
plt.show()


plt.plot([1,2,3,4], [1,2,3,4], 'go--', label='直线')
x = np.linspace(0,10,100)
y = np.sin(x)
#plt.plot(x, y, label='sin(x)')
#plt.legend(loc='best')
#plt.show()
figure0 = plt.figure(num=0, figsize=(8,4))
# print(figure0)
fig = plt.gcf()   # get current figure，获取当前画板
print(fig)
axes0 = figure0.add_subplot(1,2,1)
print(axes0)
ax0 = plt.gca()
print(ax0)   # get current axes，获取当前子图
axes0.plot(x, y, 'r--')
axes0.plot(x, x)
axes0.set_title('线性图')
axes0.set_xlim([-2, 5])
axes0.set_ylim([-1, 6])
#axes0.set_xlabel('x 轴')
axes0.set_ylabel("y 轴")
axes0.set_xticks([0,1,2,3,4])
axes0.set_xticklabels(['a','b','c','d'])

axes0.xaxis.set_label_ ('轴')

plt.show()


x = np.linspace(0,10,100)
y = np.sin(x)

plt.figure(0)
ax0 = plt.gcf().add_subplot(2,1,1)
plt.plot(x, y)
ax1 = plt.gcf().add_subplot(2,1,2)
plt.plot(x, y)
plt.sca(ax0)
plt.plot(x, x)

fig, axes = plt.subplots(2,3)
for axs in axes:
    for ax in axs:
        ax.plot([1,2,3,4],[1,2,3,4])
plt.show()
