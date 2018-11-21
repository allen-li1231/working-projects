import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#饼图
x = [1, 2, 3, 4]
plt.pie(x, explode=[0.1, 0, 0, 0], labels=['a','b','c','d'], colors=['r', 'b', 'c'], autopct='%.1f', pctdistance=0.9, shadow=True, labeldistance=1.5, startangle=90, radius=0.5, counterclock=False, )
plt.legend(loc='upper left')
#箱线图
x = np.random.random(size=(20,))
x[0] = 5
print(x.shape)
print(pd.DataFrame(x).describe())
f = plt.boxplot(x, sym='s', labels=['a'])
print(f['medians'][0].get_ydata())
plt.savefig('boxplot.png', dpi=120)
plt.show()
#3d散点图
fig = plt.figure()
axes3d = fig.add_subplot(1, 1, 1, projection='3d')
x = np.arange(-4, 4, 0.25)
y = np.arange(-4, 4, 0.25)
z = np.sqrt(x**2 + y**2)
axes3d.scatter3D(x, y, z)
axes3d.set_xlabel('x')   
axes3d.set_ylabel('y')
axes3d.set_zlabel('z')
#3d图
names = mpl.projections.get_projection_names()
print(names)
from mpl_toolkits.mplot3d import Axes3D # Axes3D必须写入
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
fig = plt.figure()
ax = fig.gca(projection='3d')
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()
################
# 等高线图
fig = plt.figure()
axes3d = fig.add_subplot(1, 1, 1, projection='3d')
X = np.arange(-4, 4, 0.25)
Y = np.arange(-4, 4, 0.25)
x, y = np.meshgrid(X, Y)
z = np.sqrt(x**2 + y**2)
#cont = axes3d.contour(x, y, z, cmap=plt.cm.hot)
cont = axes3d.contourf(x, y, z, offset=-1, cmap=plt.cm.hot)
fig.colorbar(cont)
plt.show()
