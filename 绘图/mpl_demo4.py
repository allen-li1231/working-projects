# -*- coding: utf-8 -*-
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

'''
figure # 画布
axes : 轴，坐标系
axis # 轴，坐标轴
lable # 标签
tick # 刻度
'''

# 配置
#print(mpl.rcParams)
mpl.rcParams['font.family'] = 'SimHei' # 解决中文乱码
mpl.rcParams['axes.unicode_minus'] = False # 解决负号乱码
#mpl.rcParams['backend'] = 'TkAgg' # 解决Qt5平台错误
#print(mpl.matplotlib_fname())  # 获取配置文件路径
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
## 绘图
x = np.arange(-4, 4, 0.01)
y = 2 * x + 3
plt.plot(x, y, '--ok',label='直线')
plt.legend() # 显示图例
plt.xlabel('x 轴') # 设置 x 轴的名称
plt.ylabel('y 轴') # 设置 x 轴的名称
plt.xlim(-5, 5) # 设置 x 轴显示的范围
plt.ylim(-10, 20)
plt.text(3.5, 4, '直线')
plt.annotate('2 * x + 3',(1,4),(3,3), arrowprops={"arrowstyle":'->'})
plt.show()


# 获取画布
figure = plt.figure()
axes_plot = figure.add_subplot(2, 3, 1)
axes_plot.plot([1,2,3,4,5],[1,2,3,4,5])
axes_plot.set_xlim(1,5)
axes_plot.set_xticks([1,3,5])
axes_plot.set_xticklabels(['数学','英语','语文'])
axes_plot.set_title('直线')
plot1 = axes_plot.lines[0]
print(plot1.get_data())
plt.show()
##########################################
# 绘制多张图
x = np.linspace(0, 2*np.pi, 100)
y = np.cos(x)
fig = plt.figure()
axes_cos = fig.add_subplot(231)
axes_cos.plot(x, y, color='r')
axes_cos.plot(x, np.zeros_like(x), '--k')
axes_scatter = fig.add_subplot(232)
axes_scatter.scatter([1,2,3,4],[3,7,2,9],s=[3,7,2,9], color=['r','b'])
nvs = [170,168,180]
nans = [169,180,178]
x_label = np.array([1,2,3])
axes_bar = fig.add_subplot(233)
axes_bar.bar(x_label-0.3/2, nvs, width=0.3, color='r', label='女')
axes_bar.bar(x_label+0.3/2, nans, width=0.3, color='b', label='男')
#axes_bar.legend()
for i in x_label:
    x1 = i-0.4
    x2 = i-0.1
    y1 = nvs[i-1]
    y2 = nans[i-1]
    axes_bar.text(x1, y1, str(y1))
    axes_bar.text(x2, y2, str(y2))

rand = np.random.randn(1000)
axes_hist = fig.add_subplot(234)
axes_hist.hist(rand, bins=50, normed=True)
axes_3d = fig.add_subplot(235, projection='3d')
x_3d = np.linspace(-2, 2, 300)
y_3d = np.linspace(-2, 2, 300)
x_3d, y_3d = np.meshgrid(x_3d, y_3d)
z_3d = np.sqrt(x_3d**2 + y_3d**2)
axes_3d.plot_surface(x_3d, y_3d, z_3d, cmap=plt.cm.hot)
axes_3d.set_xlabel('x')
# 等高线图
c = axes_3d.contourf(x_3d, y_3d, z_3d, offset=0, cmap=plt.cm.hot)
fig.colorbar(c)
plt.show()


































