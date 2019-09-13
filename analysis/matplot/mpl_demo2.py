import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


# 配置
#print(mpl.rcParams)
mpl.rcParams['font.family'] = 'SimHei' # 解决中文乱码
mpl.rcParams['axes.unicode_minus'] = False # 解决负号乱码
#mpl.rcParams['backend'] = 'TkAgg' # 解决Qt5平台错误
#print(mpl.matplotlib_fname())  # 获取配置文件路径

# 获取画布
figure = plt.figure()

# 创建一个坐标系，子图
x = [-2,-1,0,1,2]
y = [1,2,3,4,5]
y1 = np.sin(np.array(x))

axes1 = figure.add_subplot(2,4,1)
axes1.plot(x, y, 'c--s', label='直线')  # plot函数是画线图
axes1.set_title('成绩表')
axes1.set_xlabel('学科')
#axes1.set_xticks([0,1,2,3,4])
axes1.set_xlim(-2,2)
axes1.set_xticklabels(['英语','数学','英语','数学','语文'], rotation=45)
print(str(axes1.get_xticklabels()))
axes1.legend()
axes1.annotate('数学很重要', (-1, 2), (0,4) , arrowprops = {'arrowstyle':'->'})
axes1.text(0, 3, '上面是标注')

axes2 = figure.add_subplot(2,4,2)
item = np.array([0,1])
nvsheng = np.array([23,20])
nansheng = np.array([25,19])
w=0.3
#axes2.bar(item-w*0.5, nansheng, width=w, label='男')
axes2.bar(item+w*0.5, nvsheng, width=w, label='女', bottom=10)
axes2.set_xticks([0, 1])
axes2.set_xticklabels(['身高', '体重'])
axes2.set_title('男女数量表')
axes2.set_xlabel('项')
axes2.set_ylabel('数量')
for i in range(len(item)):
    x_ = item[i]
    y_ = nansheng[i]
    axes2.text(x_, y_+0.5, str(y_))
axes2.legend()

axes3 = figure.add_subplot(2,4,3)
axes3.scatter(x, y,color=['r','c','g'], alpha=0.5)

axes4 = figure.add_subplot(2,4,4)
axes4.hist(x, normed=False)
axes4.set_xticks([-2,-1.5,-1,-0.5])

axes5 = figure.add_subplot(2,4,5)
axes5.pie([1,2,3], explode=[0.1,0,0], autopct='%.1f')

axes6 = figure.add_subplot(2,4,6)
d = axes6.boxplot([1,2,3,4,5,6,7, 20])
print(d['fliers'][0].get_data())

# c = sqrt(a**2+b**2)
a = np.linspace(-2, 2, 100)
b = np.linspace(-2, 2, 100)
c = np.sqrt( a**2 + b**2 )  # > 100个数字
A, B = np.meshgrid(a, b)
C = np.sqrt( A**2 + B**2 )  # > 100个数字
print(a.shape)
print(A.shape)
axes7 = figure.add_subplot(111, projection = '3d')
#axes7.plot_surface(A,B,C,cmap=plt.cm.hot)
c = axes7.contourf(A,B,C,offset=0)
axes7.set_xlabel('x轴')
axes7.set_ylabel('y')
figure.colorbar(c)

plt.show()  # 显示
