from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from _cargo import *
from _container import *

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']
fig:Figure = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
ax.view_init(elev=20, azim=40)
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)

def draw_reslut(setted_container:Container,string):
    plt.gca().set_box_aspect((
        setted_container.length,
        setted_container.width,
        setted_container.height
    )) 
    _draw_container(setted_container)
    for cargo in setted_container._setted_cargos:
        _draw_cargo(cargo)
    #plt.show()
    plt.savefig("/Users/admire/Desktop/算法"+string+".jpg")

def _draw_container(container:Container):
    _plot_linear_cube(
        0,0,0,
        container.length,
        container.width,
        container.height
    )

def _draw_cargo(cargo:Cargo):
    _plot_opaque_cube(
        cargo.x, cargo.y, cargo.z,
        cargo.length, cargo.width, cargo.height
    )

def _plot_opaque_cube(x=10, y=20, z=30, dx=40, dy=50, dz=60):
    xx = np.linspace(x, x+dx, 2)
    yy = np.linspace(y, y+dy, 2)
    zz = np.linspace(z, z+dz, 2)
    xx2, yy2 = np.meshgrid(xx, yy)
    ax.plot_surface(xx2, yy2, np.full_like(xx2, z))
    ax.plot_surface(xx2, yy2, np.full_like(xx2, z+dz))
    yy2, zz2 = np.meshgrid(yy, zz)
    ax.plot_surface(np.full_like(yy2, x), yy2, zz2)
    ax.plot_surface(np.full_like(yy2, x+dx), yy2, zz2)
    xx2, zz2= np.meshgrid(xx, zz)
    ax.plot_surface(xx2, np.full_like(yy2, y), zz2)
    ax.plot_surface(xx2, np.full_like(yy2, y+dy), zz2)

def _plot_linear_cube(x, y, z, dx, dy, dz, color='red'):
    # ax = Axes3D(fig)
    xx = [x, x, x+dx, x+dx, x]
    yy = [y, y+dy, y+dy, y, y]
    kwargs = {'alpha': 1, 'color': color}
    ax.plot3D(xx, yy, [z]*5, **kwargs)
    ax.plot3D(xx, yy, [z+dz]*5, **kwargs)
    ax.plot3D([x, x], [y, y], [z, z+dz], **kwargs)
    ax.plot3D([x, x], [y+dy, y+dy], [z, z+dz], **kwargs)
    ax.plot3D([x+dx, x+dx], [y+dy, y+dy], [z, z+dz], **kwargs)
    ax.plot3D([x+dx, x+dx], [y, y], [z, z+dz], **kwargs)
