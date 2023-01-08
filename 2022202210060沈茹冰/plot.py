from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from itertools import product
import numpy as np
from utils import *


def plot_linear_cube(ax, x, y, z, dx, dy, dz, color='yellow', linestyle=None):
    xx = [x, x, x+dx, x+dx, x]
    yy = [y, y+dy, y+dy, y, y]
    kwargs = {"alpha": 1, "color": color, "linewidth":2.5, "zorder":2}
    if linestyle:
        kwargs["linestyle"] = linestyle
    ax.plot3D(xx, yy, [z]*5, **kwargs)
    ax.plot3D(xx, yy, [z+dz]*5, **kwargs)
    ax.plot3D([x, x], [y, y], [z, z+dz], **kwargs)
    ax.plot3D([x, x], [y+dy, y+dy], [z, z+dz], **kwargs)
    ax.plot3D([x+dx, x+dx], [y+dy, y+dy], [z, z+dz], **kwargs)
    ax.plot3D([x+dx, x+dx], [y, y], [z, z+dz], **kwargs)


def cuboid_data(o, size=(1, 1, 1)):
    X = [[[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 0]],
         [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],
         [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
         [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
         [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
         [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]]
    X = np.array(X).astype(float)
    for i in range(3):
        X[:, :, i] *= size[i]
    X += np.array(o)
    return X


def plotCubeAt(positions, sizes=None, colors=None, **kwargs):
    if not isinstance(colors, (list, np.ndarray)):
        colors = ["C0"] * len(positions)
    if not isinstance(sizes, (list, np.ndarray)):
        sizes = [(1, 1, 1)] * len(positions)
    g = []
    for p, s, c in zip(positions, sizes, colors):
        g.append(cuboid_data(p, size=s))
    return Poly3DCollection(np.concatenate(g), facecolors=np.repeat(colors, 6), **kwargs)



# 构建箱体坐标，用于绘图
def build_box_position(block, init_pos, box_list):
    # 箱体类型索引
    box_idx = (np.array(block.require_list) > 0).tolist().index(True)
    if box_idx > -1:
        # 所需箱体
        box = box_list[box_idx]
        # 箱体的相对坐标
        if block.box_rotate:
            nx = block.lx / box.ly
            ny = block.ly / box.lx
            x_list = (np.arange(0, nx) * box.ly).tolist()
            y_list = (np.arange(0, ny) * box.lx).tolist()
        else:
            nx = block.lx / box.lx
            ny = block.ly / box.ly
            x_list = (np.arange(0, nx) * box.lx).tolist()
            y_list = (np.arange(0, ny) * box.ly).tolist()
        nz = block.lz / box.lz
        z_list = (np.arange(0, nz) * box.lz).tolist()
        # 箱体的绝对坐标
        dimensions = (np.array([x for x in product(x_list, y_list, z_list)]) + np.array([init_pos[0], init_pos[1], init_pos[2]])).tolist()
        # 箱体的坐标及尺寸
        if block.box_rotate:
            return sorted([d + [box.ly, box.lx, box.lz] for d in dimensions], key=lambda x: (x[0], x[1], x[2])), box_idx
        else:
            return sorted([d + [box.lx, box.ly, box.lz] for d in dimensions], key=lambda x: (x[0], x[1], x[2])), box_idx
    return None, None


# 绘制结果
def draw_packing_result(problem: Problem, ps: PackingState, test_id):
    fig = plt.figure()
    ax1 = fig.add_subplot(projection = '3d')
    # 绘制容器
    plot_linear_cube(ax1, 0, 0, 0, problem.container.lx, problem.container.ly, problem.height_limit)
    for p in ps.plan_list:
        # 绘制箱子
        box_pos, _ = build_box_position(p.block, (p.plane.x, p.plane.y, p.plane.z), problem.box_list)
        positions = []
        sizes = []
        colors = ["violet"] * len(box_pos)
        for bp in sorted(box_pos, key=lambda x: (x[0], x[1], x[2])):
            positions.append((bp[0], bp[1], bp[2]))
            sizes.append((bp[3], bp[4], bp[5]))

        pc = plotCubeAt(positions, sizes, colors=colors, edgecolor="k")
        ax1.add_collection3d(pc)
    # plt.show()
    plt.savefig('./results_2/{}.png'.format(test_id), dpi=300)
