from matplotlib import pyplot as plt
import numpy as np
from classes import *


def draw(loaded_container: Container):
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = ['SimHei']

    ax = plt.figure().add_subplot(1, 1, 1, projection='3d')
    ax.view_init(elev=25, azim=45)

    def plot_opaque_cube(x=10, y=20, z=30, dx=40, dy=50, dz=60):
        xx = np.linspace(x, x + dx, 2)
        yy = np.linspace(y, y + dy, 2)
        zz = np.linspace(z, z + dz, 2)
        xx2, yy2 = np.meshgrid(xx, yy)
        ax.plot_surface(xx2, yy2, np.full_like(xx2, z))
        ax.plot_surface(xx2, yy2, np.full_like(xx2, z + dz))
        yy2, zz2 = np.meshgrid(yy, zz)
        ax.plot_surface(np.full_like(yy2, x), yy2, zz2)
        ax.plot_surface(np.full_like(yy2, x + dx), yy2, zz2)
        xx2, zz2 = np.meshgrid(xx, zz)
        ax.plot_surface(xx2, np.full_like(yy2, y), zz2)
        ax.plot_surface(xx2, np.full_like(yy2, y + dy), zz2)

    def plot_linear_cube(x, y, z, dx, dy, dz):
        xx = [x, x, x + dx, x + dx, x]
        yy = [y, y + dy, y + dy, y, y]
        kwargs = {'alpha': 1, 'color': 'blue'}
        ax.plot3D(xx, yy, [z] * 5, **kwargs)
        ax.plot3D(xx, yy, [z + dz] * 5, **kwargs)
        ax.plot3D([x, x], [y, y], [z, z + dz], **kwargs)
        ax.plot3D([x, x], [y + dy, y + dy], [z, z + dz], **kwargs)
        ax.plot3D([x + dx, x + dx], [y + dy, y + dy], [z, z + dz], **kwargs)
        ax.plot3D([x + dx, x + dx], [y, y], [z, z + dz], **kwargs)

    plt.gca().set_box_aspect((loaded_container.length, loaded_container.width, loaded_container.height))
    plot_linear_cube(0, 0, 0, loaded_container.length, loaded_container.width, loaded_container.height)
    for box in loaded_container.loaded_boxes:
        plot_opaque_cube(box.x, box.y, box.z, box.length, box.width, box.height)
    plt.savefig("img.png")
    plt.show()



