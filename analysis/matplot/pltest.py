import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np

pic = plt.figure()
axs = pic.add_subplot(1, 1, 1)
xh = np.linspace(-32,32,65)
yv = np.sin(xh*math.pi/16)
hline = np.zeros
axs.plot(list(range(-32,33)), np.linspace(0, 0, 65), 'k', linewidth = 0.5)

axs.plot(xh, yv, 'r', label='y = sin(x)')
#axs.set_xticks([-np.pi/2, 0, np.pi/2])
axs.legend()
axs.axis([-32,32,-1.5,1.5])