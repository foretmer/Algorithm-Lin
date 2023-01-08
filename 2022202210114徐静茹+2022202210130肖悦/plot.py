import matplotlib.pyplot as plt
import numpy as np

from main_int import eval
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(1,1,1,projection='3d')
# 调整三个坐标轴的缩放比例
ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([1.2, 0.8, 0.8, 1]))

loaded_rate, _, _, loaded_boxes  = eval("./dataset/E1-1.csv", "ourmethod_annealing", 1000000000)
print(loaded_rate)

def plot_opaque_cube(x=10, y=20, z=30, dx=40, dy=50, dz=60, color="red"):
  xx = np.linspace(x, x+dx, 2)
  yy = np.linspace(y, y+dy, 2)
  zz = np.linspace(z, z+dz, 2)

  xx2, yy2 = np.meshgrid(xx, yy)

  ax.plot_surface(xx2, yy2, np.full_like(xx2, z), color=color)
  ax.plot_surface(xx2, yy2, np.full_like(xx2, z+dz), color=color)
  

  yy2, zz2 = np.meshgrid(yy, zz)
  ax.plot_surface(np.full_like(yy2, x), yy2, zz2, color=color)
  ax.plot_surface(np.full_like(yy2, x+dx), yy2, zz2, color=color)

  xx2, zz2= np.meshgrid(xx, zz)
  ax.plot_surface(xx2, np.full_like(yy2, y), zz2, color=color)
  ax.plot_surface(xx2, np.full_like(yy2, y+dy), zz2, color=color)

colors = ["red", "green", "purple", "pink", "yellow", "gray"]
color_index = 0
boxes_type = list(set([(loaded_box.x, loaded_box.y, loaded_box.z) for (loaded_box, _, _, _) in loaded_boxes]))

for (loaded_box, x, y, z) in loaded_boxes:
  color_index = (boxes_type.index((loaded_box.x, loaded_box.y, loaded_box.z))) % len(colors)
  plot_opaque_cube(x,y,z,loaded_box.x, loaded_box.y, loaded_box.z, color=colors[color_index])

plt.show()


