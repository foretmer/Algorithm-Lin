import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']
fig: Figure = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
ax.view_init(elev=20, azim=40)
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)


class Cargo:
    def __init__(self, x, y, z, dx, dy, dz) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.dz = dz


def draw_reslut(path="test.txt"):
    with open(path, "r") as f:
        s = f.readlines()
    x, y, z = [float(i) for i in s[0].split(" ")]

    plt.gca().set_box_aspect((
        x, y, z
    ))
    _draw_container(x, y, z)

    s = [i.split(" ") for i in s[1:]]
    s = [Cargo(float(x), float(y), float(z), float(dx), float(dy), float(dz))
         for [x, y, z, dx, dy, dz] in s]
    for c in s:
        _draw_cargo(c)
        print(c.x, c.y, c.z, c.dx, c.dy, c.dz)
    plt.show()


def _draw_container(x, y, z):
    _plot_linear_cube(
        0, 0, 0,
        x, y, z
    )


def _draw_cargo(ca: Cargo):
    _plot_opaque_cube(
        ca.x, ca.y, ca.z,
        ca.dx, ca.dy, ca.dz
    )


def _plot_opaque_cube(x, y, z, dx, dy, dz):
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


def _plot_linear_cube(x, y, z, dx, dy, dz, color='red'):
    xx = [x, x, x + dx, x + dx, x]
    yy = [y, y + dy, y + dy, y, y]
    kwargs = {'alpha': 1, 'color': color}
    ax.plot3D(xx, yy, [z] * 5, **kwargs)
    ax.plot3D(xx, yy, [z + dz] * 5, **kwargs)
    ax.plot3D([x, x], [y, y], [z, z + dz], **kwargs)
    ax.plot3D([x, x], [y + dy, y + dy], [z, z + dz], **kwargs)
    ax.plot3D([x + dx, x + dx], [y + dy, y + dy], [z, z + dz], **kwargs)
    ax.plot3D([x + dx, x + dx], [y, y], [z, z + dz], **kwargs)


if __name__ == "__main__":
    draw_reslut()
