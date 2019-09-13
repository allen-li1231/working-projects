# -*- coding: utf-8 -*-

import numpy as np
import matplotlib as mpl
# from matplorlib import pyplot as plt
import matplotlib.pyplot as plt

'''
Artist :
figure: 画布
axes : 坐标系
axis : 坐标轴
patch : 背景
lines : 所画的全部线
'''
#画图流程：
#1. 创建一个画布
figure = plt.figure() # plt.gcf() # 获取当前画布

#2. 创建一个坐标系
axes1 = figure.add_subplot(3, 3, 1) # (331)

#3. 在坐标系进行画图
# axes1.plot(...) # 绘制线图

# 4. 进行设置一些属性
# =============================================================================
# axes1.set_title(s) # 设置标题
# axes1.set_xlabel(s) # 设置坐标轴名称
# axes1.set_xticks(l) # 设置显示的刻度
# axes1.set_xticklabels(l) # 设置刻度标签
# axes1.set_xlim(l) # 设置显示的范围
# axes1.legend() # 显示图例
# axes1.annotate(s) # 设置注解
# axes1.text() # 绘制一些文字
# =============================================================================

# 5. 显示图形
plt.show()


# !!! 配置
print(mpl.rcParams) # 获取全部配置
print(mpl.rcParams['font.family']) # 获取字体
#mpl.rcParams['font.family'] = 'SimHei' # 设置字体

print(mpl.rcParams['backend'])
#mpl.rcParams['backend'] = 'TkAgg' # Qt5

print(mpl.rcParams['axes.unicode_minus'])
#mpl.rcParams['axes.unicode_minus'] = False

print(mpl.matplotlib_fname()) # 获取配置文件路径
mpl.rc_params() # 重新加载配置

# 折线图
# 创建画布
fig = plt.figure(figsize=(8, 6))
# 创建一个坐标系
axes1 = fig.add_subplot(1, 1, 1)
# 绘制图形
plot_x = np.linspace(-5, 5, 20)
plot_y = plot_x**2
#plot_x_2 = np.linspace(-5, 5, 100)
plot_y_2 = plot_x*2
axes1.plot(plot_x, plot_y, '--c', label='y')
axes1.plot(plot_x, plot_y_2, label='y=x*2')
axes1.set_title('曲线') # 设置标题
axes1.set_xlabel('x 轴') # 设置x轴名称
axes1.set_ylabel('y 轴') # 设置y轴的名称
axes1.legend() # 显示图例
axes1.set_xticks(range(-5, 6)) # 显示的刻度
axes1.set_xlim([-1, 1]) # 显示范围
axes1.set_xticklabels(['a', 'b'])

diff_1 = plot_y - plot_y_2
ret = np.logical_xor(diff_1[0:-1]>0, diff_1[1:]>0)
for index, r in enumerate(ret):
    if r:
        x = plot_x[index]
        y_1 = plot_y[index]
        axes1.annotate('(%.1f, %.1f)' % (x, y_1), (x, y_1), (x+1, y_1+20), arrowprops={'arrowstyle':'->'})
axes1.text(0, 15, '简单函数')
fig.savefig('simple.jpg', dpi=100)
plt.show()


plt.plot([1,2,3,4], [1,2,3,4])
fig = plt.gcf()
axes = plt.gca()
plt.title('标题')
plt.show()

######
fig, axes = plt.subplots(2, 3)
plt.gca()
print(type(axes))
axes[0, 0].plot([1,2,3,4],[1,2,3,4])
print(plt.gca() is axes[1,2])
plt.sca(axes[0,0])
plt.plot([1,2,3,4],[4,3,2,1])
lines = axes[0, 0].lines
print(lines)
for line in lines:
    print(line.get_xdata())
plt.show()


# 直方图
x = np.array([1,2,3,4,5,6])
y = np.array([3,2,5,2,1,2])

plt.bar(x, y, tick_label=['a','b','c','d','e','f'])
for index in range(0, len(x)): # for index, _ in enum...(x)
    x_ = x[index]
    y_ = y[index]
    #plt.text(x_-0.1, y_+0.1, y_)

scroe_type = np.array([1,2,3])
scroe_man = np.array([79, 98, 68])
scroe_women = np.array([99, 79, 88])
tick_label = ['英语', '数学', '语文']
width = 0.4
plt.bar(scroe_type-width*0.5, scroe_man, width=width, label='男生')
plt.bar(scroe_type+width*0.5, scroe_women, width=width, label='女生')
_axes = plt.gca()
_axes.set_xticks([1,2,3])
_axes.set_xticklabels(tick_label)
plt.legend(loc='center')
for index, _ in enumerate(scroe_type):
    x_man = scroe_type-width*0.5
    y_man = scroe_man[index]
    x_women = scroe_type+width*0.5
    y_women = scroe_women[index]
    plt.text(x_man[index], y_man, y_man)
    plt.text(x_women[index], y_women, y_women)
plt.show()


# 散点图
plt.scatter([2,3,1,9,4], [1,3,4,2,1],s=[10, 100], marker='o', edgecolor=['g', 'c'])
plt.show()

# 直方图
plt.hist([1,2,3,4,5,3,2,12,3,21,2,3,12,32], bins=5, normed=True)
plt.show()

#饼图
plt.pie([1,2,3,4], explode=[0.1, 0.1, 0.1, 0.1], labels=['a', 'b', 'c', 'd'], autopct='%.2f', pctdistance=0.5)
plt.show()

# 箱线图
x = np.random.randint(0, 10, size=200, dtype=np.int).reshape(50, 4)
x[10:13,3] = np.random.randint(20, 30, 3)
bp = plt.boxplot(x)
plt.yticks(range(-1, 11))
ycz = bp['fliers']
print(ycz[0].get_data())
plt.show()































