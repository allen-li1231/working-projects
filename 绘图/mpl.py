#/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# 1.直接使用pyplot创建图形
plt.plot([1,2,3,4,5],[1,2,3,4,5])
plt.show()


# 2.使用figure创建子axes
fig = plt.figure()
ax1 = fig.add_subplot(1,2,1)	#fig.add_subplot(121)
ax2 = fig.add_subplot(1,2,2)
ax1.plot(x, y1)
ax2.plot(x, y2)
plt.show()


# 3.快捷创建figure和axes
fig, axes = plt.subplots(1, 2, sharex=True, sharey=True)
print(axes)
axes[0].plot(x, y1, x, y2, x, np.linspace(0, 0, 100))
#axes[0].plot(x, np.linspace(0, 0, 100), color='r', linestyle='--')
axes[1].plot(x, y2)
fig.subplots_adjust(wspace=0, hspace=0)
plt.show()


figure = plt.figure()

# 4.使用plot创建正弦和余弦函数
axes1 = figure.add_subplot(1, 1, 1)
axes1.plot(x, y1, 'r--', label='y=sin(x)')
axes1.plot(x, y2, linestyle=':', color='g', label='y=cos(x)')
axes1.legend(loc='upper right')
axes1.set_title('plot')
def pi_formatter(x, pos):
    """将数值转换为以pi/2为单位的刻度文本"""
    m = round(x / (np.pi/2))
    if m == 0:
        return "0"
    if m%2 == 0:
        return r"${%d} \pi$" % int(m/2)
    return r"$\frac{%d \pi}{%d}$" % (m, 2)   # latex
from matplotlib.ticker import MultipleLocator, FuncFormatter
axes1.xaxis.set_major_locator(MultipleLocator(np.pi/2))     #设置单位跨度
axes1.xaxis.set_major_formatter(FuncFormatter(pi_formatter))#设置格式
for tick in axes1.xaxis.get_major_ticks():                  #设置大小
    tick.label.set_fontsize(6)
axes1.axis([-2*np.pi, 2*np.pi, -1, 2])                      #设置x轴，y轴范围


# 5.使用scatter创建散点图
x_scatter = np.random.randn(20)
y_scatter = np.random.randn(20)
axes2 = figure.add_subplot(2, 3, 2)
axes2.scatter(x_scatter, y_scatter, marker='o', c=['r', 'b', 'k'], cmap=plt.cm.hot)
axes2.set_title('scatter')
axes2.annotate('annotate_10', xy=[x_scatter[10], y_scatter[10]], xytext=[0.2,0.2], arrowprops=dict(facecolor='g'))


# 6.使用bar创建条形图
axes3 = figure.add_subplot(2,3,3)
x_bar = np.linspace(1,5,5)
y_bar = np.linspace(1,5,5)
axes3.bar(x_bar, y_bar, align='center')
for x_t, y_t in zip(x_bar, y_bar):
    axes3.text(x=x_t, y=y_t+0.01, s='%.0f' % y_t, ha='center', va= 'bottom')
axes3.set_title('bar')
#

# 7.使用hist创建直方图
axes4 = figure.add_subplot(2,3,4)
x_hist = np.random.randn(1000)
axes4.hist(x_hist, bins=50, normed=True)
axes4.set_title('hist')
#"""

# 8.使用plot_surface创建3d
figure = plt.figure()
axes5 = figure.add_subplot(1,1,1,projection='3d')
x_sf = np.linspace(-2, 2, 101)
y_sf = np.linspace(-2, 2, 101)
X_sf, Y_sf = np.meshgrid(x_sf, y_sf)
z = np.sin(np.sqrt(X_sf**2+Y_sf**2))
#axes5.plot_surface(X_sf, Y_sf, z, cmap=plt.cm.hot)
axes5.contour(X_sf, Y_sf, z, zdir='z', offset=-1, cmap=plt.cm.hot)
axes5.set_zlim(-1, 2)
axes5.set_title('surface')
#
#axes5 = figure.add_subplot(1,1,1)
#axes5.scatter(x_sf, z[1], marker='o')
#plt.show()
#

# 9.使用contourf创建等高面
figure = plt.figure()
axes6 = figure.add_subplot(2,3,6,projection='3d')
axes6.contourf(X_sf, Y_sf, z, zdir='z', offset=0, cmap=plt.cm.hot)
axes6.set_title('contourf')
#

figure.subplots_adjust(wspace=0.1,hspace=0.5)
figure.savefig("1.png", dpi=300)
plt.show()