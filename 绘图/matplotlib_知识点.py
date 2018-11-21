# 导入库
import matplotlib as mpl
import matplotlib.pyplot as plt

# 1. matplotlib 概念
'''
Artist : 艺术家
figure : 人物, 面板
figure = plt.gcf()   # 获取当前画图面板
figure = plt.figure()   # 生成画图面板
figure, axes = plt.subplots(2, 3)
axes : 轴，子图
axes = plt.gca()   # 获取当前画图坐标系
axes = figure.add_subplot(1, 2, 1)   # 生成画图坐标系

# axis : 轴，坐标轴
axis = axes.xaxis   # 获取 axes 坐标系的 x 轴
axis = axes.yaxis   # 获取 axes 坐标系的 y 轴
# lines : 线
lines = axes.lines   # 获取 axes 坐标系的线图
# patch : 背景
patch = axes.patch   # 获取 axes 坐标系的背景
'''
# 2. matplotlib 配置
'''
matplotlib.rcParams   # 用字典获取所有配置
matplotlibmpl.rcParams['backend'] = 'TkAgg'   # 修改后端，解决Qt5平台错误
matplotlibmpl.rcParams['font.family'] = 'SimHei'   # 修改字体支持中文，解决中文乱码
matplotlib.get_backends()  # 获取正在使用的后端
matplotlib.get_configdir()   # 获取配置文件夹
matplotlib.matplotlib_fname()   # 获取当前使用的配置文件路径
'''
'''
# Anaconda3\Lib\site-packages\matplotlib\mpl-data\matplotlibrc   # matplotlib默认配置文件，修改配置后永久有效
font.family : SimHei   # 解决中文乱码
backend : TkAgg   # 解决 Qt5 平台报错
axes.unicode_minus : False   # 解决负号是方块
matplotlib.rc_params()   # 重新读取配置，以字典形式返回
'''
# 3. 图像设置
# 使用 plt 设置图像属性
'''
figure, axes = plt.subplots(m, n)   # 创建面板及子视图
plt.title(string)   # 创建标题
plt.xlable(string)   # 创建 x 轴名称
plt.xticks(ticks, labels)   # 添加 x 轴刻度及可选刻度标签
plt.xlim(x_0, x_1)   # 刻度范围
plt.axis(x_0, x_1, y_0, y_2)   # 刻度范围
plt.legend(loc)   # 显示图例
plt.annotate(string, xy, xytext, textcoords)   # 添加注解
plt.text(x, y, string)   # 添加文字
# 使用 axes 坐标轴添加图像属性
axes.set_title(string)   # 创建标题
axes.set_xlable(string)   # 创建轴名称
axes.set_xticks(ticks)   # 添加刻度
axes.set_xticklabels(labels, rotation='旋转角度', fontsize=字体大小)   # 添加刻度标签
axes.set_xlim(x_0, x_1)   # 刻度 x 轴范围
axes.legend(loc)   # 显示图例
axes.annotate(string, xy, xytext, textcoords)   # 添加注解
axes.text(x, y, string)   # 添加文字
'''
# 4. 折线图 plot
'''
# plt.plot(x1, y1, 'r-s' x2, y2, 'b--o', ..., label, linestyle, linewidth, color, marker, markerfacecolor, markersize)
label : 图例
linestyle : 线型 -实线 --虚线 -.点画线 .点线
linewidth : 线宽
color : 颜色 r红 b蓝 y黄 w白 k黑 g绿 c青 RGB颜色#00ff00绿 RGB颜色(255, 0, 0)红 灰度颜色(1,0,0)红
marker : 标记 o实心圆 s方形 *星 +加号
markerfacecolor : 标记颜色
markersize : 标记大小
axes.plot(...)
'''

# 5. 条形图(柱形图) bar垂直 barh水平
'''
plt.bar(left, height, width, bottom, tick_label, align)   # 颜色等设置同 plot
left : x 轴数据
height : y 轴数据
width : 条形宽度
bottom : y 坐标开始位置
tick_label : 条形图标签
align : 条形图对其方式 center居中对其 x 刻度, edge左对齐 x 刻度
axes.bar(...)
'''

# 6. 散点图 scatter
'''
plt.scatter(x, y, s, c, cmap, norm, vmin, vmax, alpha, edgecolors)  # c = [2,4,5,2,3]  (2-2)/(5-2) 
s : 点的大小
c : 点的颜色
cmap : 当 c 参数是数字序列时，norm 将 c 进行归一化，cmap 将其映射为颜色
norm : 将 c 参数归一化
vmin : norm 进行归一化的最小值，不设置时取 c 的最小值
vmax : norm 进行归一化的最大值，不设置时取 c 的最大值
alpha : 透明度
edgecolors : 标记边缘颜色
axes.scatter(...)
'''

# 7. 直方图 hist
'''
plt.hist(x, bins, range, normed, weights, cumulative, bottom, histtype, align)
bins : 条数
range : 仅计算范围内的数据
normed : 归一化，形成概率密度计数 默认False
weights : x 的权重
cumulative : 是否累积 默认False
bottom : 同bar
histtype : 默认bar传统直方图 barstacked多个数据堆叠在一起的条形直方图 step不填充的直方图
align : left左对齐 默认mid居中对齐 right右对齐
axes.hist(...)
'''

# 8. 饼图 pie
'''
plt.pie(x, explode, labels, colors, autopct, pctdistance, labeldistance, shadow, startangle, radius, counterclock, center, frame)
explode : 楔形间隔
lables : 楔形标签
colors : 颜色
autopct : 信息
pctdistance : 信息距原点距离
labeldistance : 标签距原点距离
shadow : 是否阴影
startangle : 开始角度
radius : 饼图半径
counterclock : 是否逆时针
center : 原点位置
frame : 是否显示坐标系
axes.pie(...)
'''

# 9. 箱线图 boxplot
'''
plt.boxplot(x, sym, whis, labels)
sym : 异常值的标记样式，marker
whis : 上边缘=上四分位+whis*四分位差 下边缘=下四分位+whis*四分位差 四分位差=Q3-Q1
labels : 当 x 有多组值画多个箱线图时，设置标签
axes.boxplot(...)
'''

# 10. 三维图 plot_surface

mpl.projections.get_projection_names()   # 获取当前画布支持的作图类型
# import mpl_toolkits.mplot3d
# from mpl_toolkits.mplot3d import Axes3D   # 导入 3D 库
import numpy as np
figure = plt.figure()
axes = figure.add_subplot(111, projection='3d')
X = np.arange(-4, 4, 0.25)
Y = np.arange(-4, 4, 0.25)
x, y = np.meshgrid(X, Y)
r = np.sqrt(x**2 + y**2)
z = np.sin(r)
axes.plot_surface(x, y, z, rstride=1, cstride=1, cmap='rainbow')
# axes.plot_surface(x, y, z, rstride, rstride, rcount, ccount, color, cmap, facecolors, norm, vmin, vmax, shadow)

# 11. 等高线与等高面
# plt.contour(x, y, z, stride, zdir, offset)

