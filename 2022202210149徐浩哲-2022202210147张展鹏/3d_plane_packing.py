import copy
import sys
from itertools import product
import math
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import time

MAX_GAP = 0


# 绘图相关函数
def plot_linear_cube(ax, x, y, z, dx, dy, dz, color='red', linestyle=None):
    xx = [x, x, x + dx, x + dx, x]
    yy = [y, y + dy, y + dy, y, y]
    kwargs = {"alpha": 1, "color": color, "linewidth": 2.5, "zorder": 2}
    if linestyle:
        kwargs["linestyle"] = linestyle
    ax.plot3D(xx, yy, [z] * 5, **kwargs)
    ax.plot3D(xx, yy, [z + dz] * 5, **kwargs)
    ax.plot3D([x, x], [y, y], [z, z + dz], **kwargs)
    ax.plot3D([x, x], [y + dy, y + dy], [z, z + dz], **kwargs)
    ax.plot3D([x + dx, x + dx], [y + dy, y + dy], [z, z + dz], **kwargs)
    ax.plot3D([x + dx, x + dx], [y, y], [z, z + dz], **kwargs)


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


# 箱子类
class Box:
    def __init__(self, lx, ly, lz, type=0):
        # 长
        self.lx = lx
        # 宽
        self.ly = ly
        # 高
        self.lz = lz
        # 类型
        self.type = type

    def __str__(self):
        return "lx: {}, ly: {}, lz: {}, type: {}".format(self.lx, self.ly, self.lz, self.type)


# 块类
class Block:
    def __init__(self, lx, ly, lz, require_list=[], box_rotate=False):
        # 长
        self.lx = lx
        # 宽
        self.ly = ly
        # 高
        self.lz = lz
        # 需要的物品数量
        self.require_list = require_list
        # 体积
        self.volume = 0
        # 是否旋转
        self.box_rotate = box_rotate

    def __str__(self):
        return "lx: %s, ly: %s, lz: %s, volume: %s, require: %s, box_rotate: %a" % (
            self.lx, self.ly, self.lz, self.volume, self.require_list, self.box_rotate)

    def __eq__(self, other):
        return self.lx == other.lx and self.ly == other.ly and self.lz == other.lz and self.box_rotate == other.box_rotate and (
                np.array(self.require_list) == np.array(other.require_list)).all()


# 平面类
class Plane:
    def __init__(self, x, y, z, lx, ly, height_limit=0):
        # 坐标
        self.x = x
        self.y = y
        self.z = z
        # 长
        self.lx = lx
        # 宽
        self.ly = ly
        # 限高
        self.height_limit = height_limit
        self.origin = None

    def __str__(self):
        return "x:{}, y:{}, z:{}, lx:{}, ly:{}, height_limit:{}".format(self.x, self.y, self.z, self.lx, self.ly,
                                                                        self.height_limit)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and self.lx == other.lx and self.ly == other.ly

    # 判断是否与另一个平面相邻（z坐标相同，至少有一个边平齐），并返回合并后的两个平面
    def adjacent_with(self, other):
        if self.z != other.z:
            return False, None, None

        my_center = (self.x + self.lx / 2, self.y + self.ly / 2)
        other_center = (other.x + other.lx / 2, other.y + other.ly / 2)

        x_adjacent_measure = self.lx / 2 + other.lx / 2
        y_adjacent_measure = self.ly / 2 + other.ly / 2

        if x_adjacent_measure + MAX_GAP >= math.fabs(my_center[0] - other_center[0]) >= x_adjacent_measure:
            if self.y == other.y and self.ly == other.ly:
                ms1 = Plane(min(self.x, other.x), self.y, self.z, self.lx + other.lx, self.ly)
                return True, ms1, None
            if self.y == other.y:
                ms1 = Plane(min(self.x, other.x), self.y, self.z, self.lx + other.lx, min(self.ly, other.ly))
                if self.ly > other.ly:
                    ms2 = Plane(self.x, self.y + other.ly, self.z, self.lx, self.ly - other.ly)
                else:
                    ms2 = Plane(other.x, self.y + self.ly, self.z, other.lx, other.ly - self.ly)
                return True, ms1, ms2
            if self.y + self.ly == other.y + other.ly:
                ms1 = Plane(min(self.x, other.x), max(self.y, other.y), self.z, self.lx + other.lx,
                            min(self.ly, other.ly))
                if self.ly > other.ly:
                    ms2 = Plane(self.x, self.y, self.z, self.lx, self.ly - other.ly)
                else:
                    ms2 = Plane(other.x, other.y, self.z, other.lx, other.ly - self.ly)
                return True, ms1, ms2

        if y_adjacent_measure + MAX_GAP >= math.fabs(my_center[1] - other_center[1]) >= y_adjacent_measure:
            if self.x == other.x and self.lx == other.lx:
                ms1 = Plane(self.x, min(self.y, other.y), self.z, self.lx, self.ly + other.ly)
                return True, ms1, None
            if self.x == other.x:
                ms1 = Plane(self.x, min(self.y, other.y), self.z, min(self.lx, other.lx), self.ly + other.ly)
                if self.lx > other.lx:
                    ms2 = Plane(self.x + other.lx, self.y, self.z, self.lx - other.lx, self.ly)
                else:
                    ms2 = Plane(self.x + self.lx, other.y, self.z, other.lx - self.lx, other.ly)
                return True, ms1, ms2
            if self.x + self.lx == other.x + other.lx:
                ms1 = Plane(max(self.x, other.x), min(self.y, other.y), self.z, min(self.lx, other.lx),
                            self.ly + other.ly)
                if self.lx > other.lx:
                    ms2 = Plane(self.x, self.y, self.z, self.lx - other.lx, self.ly)
                else:
                    ms2 = Plane(other.x, other.y, self.z, other.lx - self.lx, other.ly)
                return True, ms1, ms2
        return False, None, None


# 问题类
class Problem:
    def __init__(self, container: Plane, height_limit=sys.maxsize, box_list=[], num_list=[], rotate=False):
        # 初始最低水平面
        self.container = container
        # 限高
        self.height_limit = height_limit
        # 箱体列表
        self.box_list = box_list
        # 箱体数量
        self.num_list = num_list
        # 是否考虑板材旋转
        self.rotate = rotate


# 放置类
class Place:
    def __init__(self, plane: Plane, block: Block):
        self.plane = plane
        self.block = block

    def __eq__(self, other):
        return self.plane == other.plane and self.block == other.block


# 装箱状态类
class PackingState:
    def __init__(self, plane_list=[], avail_list=[]):
        # 装箱计划
        self.plan_list = []
        # 可用箱体数量
        self.avail_list = avail_list
        # 可用平面列表
        self.plane_list = plane_list
        # 备用平面列表
        self.spare_plane_list = []
        # 当前排样体积
        self.volume = 0


# 选择平面
def select_plane(ps: PackingState):
    min_z = min([p.z for p in ps.plane_list])
    temp_planes = [p for p in ps.plane_list if p.z == min_z]
    if len(temp_planes) == 1:
        return temp_planes[0]
    min_area = min([p.lx * p.ly for p in temp_planes])
    temp_planes = [p for p in temp_planes if p.lx * p.ly == min_area]
    if len(temp_planes) == 1:
        return temp_planes[0]
    min_narrow = min([p.lx / p.ly if p.lx <= p.ly else p.ly / p.lx for p in temp_planes])
    new_temp_planes = []
    for p in temp_planes:
        narrow = p.lx / p.ly if p.lx <= p.ly else p.ly / p.lx
        if narrow == min_narrow:
            new_temp_planes.append(p)
    if len(new_temp_planes) == 1:
        return new_temp_planes[0]
    min_x = min([p.x for p in new_temp_planes])
    new_temp_planes = [p for p in new_temp_planes if p.x == min_x]
    if len(new_temp_planes) == 1:
        return new_temp_planes[0]
    min_y = min([p.y for p in new_temp_planes])
    new_temp_planes = [p for p in new_temp_planes if p.y == min_y]
    return new_temp_planes[0]


# 将某平面从可用平面列表转移到备用平面列表
def disable_plane(ps: PackingState, plane: Plane):
    ps.plane_list.remove(plane)
    ps.spare_plane_list.append(plane)


# 生成简单块
def gen_simple_block(init_plane: Plane, box_list, num_list, max_height, can_rotate=False):
    block_table = []
    for box in box_list:
        for nx in np.arange(num_list[box.type]) + 1:
            for ny in np.arange(num_list[box.type] / nx) + 1:
                for nz in np.arange(num_list[box.type] / nx / ny) + 1:
                    if box.lx * nx <= init_plane.lx and box.ly * ny <= init_plane.ly and box.lz * nz <= max_height - init_plane.z:
                        requires = np.full_like(num_list, 0)
                        requires[box.type] = int(nx) * int(ny) * int(nz)
                        block = Block(lx=box.lx * nx, ly=box.ly * ny, lz=box.lz * nz, require_list=requires)
                        block.volume = box.lx * nx * box.ly * ny * box.lz * nz
                        block_table.append(block)
                    if can_rotate:
                        if box.ly * nx <= init_plane.lx and box.lx * ny <= init_plane.ly and box.lz * nz <= max_height - init_plane.z:
                            requires = np.full_like(num_list, 0)
                            requires[box.type] = int(nx) * int(ny) * int(nz)
                            block = Block(lx=box.ly * nx, ly=box.lx * ny, lz=box.lz * nz, require_list=requires,
                                          box_rotate=False)
                            block.volume = box.ly * nx * box.lx * ny * box.lz * nz
                            block_table.append(block)
    return block_table


# 生成可行块列表
def gen_block_list(plane: Plane, avail, block_table, max_height):
    block_list = []
    for block in block_table:
        if (np.array(block.require_list) <= np.array(avail)).all() and block.lx <= plane.lx and block.ly <= plane.ly \
                and block.lz <= max_height - plane.z:
            block_list.append(block)
    return block_list


# 查找下一个可行块
def find_block(plane: Plane, block_list, ps: PackingState):
    plane_area = plane.lx * plane.ly
    min_residual_area = min([plane_area - b.lx * b.ly for b in block_list])
    candidate = [b for b in block_list if plane_area - b.lx * b.ly == min_residual_area]
    max_plane_height = min([p.z for p in ps.plane_list])
    _candidate = sorted(candidate, key=lambda x: x.volume, reverse=True)
    return _candidate[0]


# 裁切出新的剩余空间（有稳定性约束）
def gen_new_plane(plane: Plane, block: Block):
    rs_top = Plane(plane.x, plane.y, plane.z + block.lz, block.lx, block.ly)
    if block.lx == plane.lx and block.ly == plane.ly:
        return rs_top, None, None
    if block.lx == plane.lx:
        return rs_top, Plane(plane.x, plane.y + block.ly, plane.z, plane.lx, plane.ly - block.ly), None
    if block.ly == plane.ly:
        return rs_top, Plane(plane.x + block.lx, plane.y, plane.z, plane.lx - block.lx, block.ly), None
    rsa1 = Plane(plane.x, plane.y + block.ly, plane.z, plane.lx, plane.ly - block.ly)
    rsa2 = Plane(plane.x + block.lx, plane.y, plane.z, plane.lx - block.lx, block.ly)
    rsa_bigger = rsa1 if rsa1.lx * rsa1.ly >= rsa2.lx * rsa2.ly else rsa2
    rsb1 = Plane(plane.x, plane.y + block.ly, plane.z, block.lx, plane.ly - block.ly)
    rsb2 = Plane(plane.x + block.lx, plane.y, plane.z, plane.lx - block.lx, plane.ly)
    rsb_bigger = rsb1 if rsb1.lx * rsb1.ly >= rsb2.lx * rsb2.ly else rsb2
    if rsa_bigger.lx * rsa_bigger.ly >= rsb_bigger.lx * rsb_bigger.ly:
        return rs_top, rsa1, rsa2
    else:
        return rs_top, rsb1, rsb2


# 计算平面浪费面积
def plane_waste(ps: PackingState, plane: Plane, block_table, max_height):
    waste = 0
    if plane:
        block_list = gen_block_list(plane, ps.avail_list, block_table, max_height)
        if len(block_list) > 0:
            block = find_block(plane, block_list, ps)
            waste = plane.lx * plane.ly - block.lx * block.ly
        else:
            waste = plane.lx * plane.ly
    return waste


# 判断平面是否可以放置物品
def can_place(ps: PackingState, plane: Plane, block_table, max_height):
    if plane is None:
        return False
    block_list = gen_block_list(plane, ps.avail_list, block_table, max_height)
    return True if len(block_list) > 0 else False


# 用块填充平面
def fill_block(ps: PackingState, plane: Plane, block: Block):
    # 更新可用箱体数目
    ps.avail_list = (np.array(ps.avail_list) - np.array(block.require_list)).tolist()
    place = Place(plane, block)
    ps.plan_list.append(place)
    ps.volume = ps.volume + block.volume
    rs_top, rs1, rs2 = gen_new_plane(plane, block)
    ps.plane_list.remove(plane)
    if rs_top:
        ps.plane_list.append(rs_top)
    if rs1:
        ps.plane_list.append(rs1)
    if rs2:
        ps.plane_list.append(rs2)


# 合并平面
def merge_plane(ps: PackingState, plane: Plane, block_table, max_height):
    for ns in ps.plane_list + ps.spare_plane_list:
        if plane == ns:
            continue
        is_adjacent, ms1, ms2 = plane.adjacent_with(ns)
        if is_adjacent:
            block_list = gen_block_list(ns, ps.avail_list, block_table, max_height)
            if len(block_list) > 0:
                block = find_block(ns, block_list, ps)
                ws1 = ns.lx * ns.ly - block.lx * block.ly + plane.lx * plane.ly
                ws2 = plane_waste(ps, ms1, block_table, max_height) + plane_waste(ps, ms2, block_table, max_height)
                if ws1 > ws2:
                    ps.plane_list.remove(plane)
                    if ns in ps.plane_list:
                        ps.plane_list.remove(ns)
                    else:
                        ps.spare_plane_list.remove(ns)
                    if ms1:
                        ps.plane_list.append(ms1)
                    if ms2:
                        ps.plane_list.append(ms2)
                    return
                else:
                    continue
            else:
                if ms2 is None:
                    if can_place(ps, ms1, block_table, max_height):
                        ps.plane_list.remove(plane)
                        if ns in ps.plane_list:
                            ps.plane_list.remove(ns)
                        else:
                            ps.spare_plane_list.remove(ns)
                        ps.plane_list.append(ms1)
                        return
                    elif ms1.lx * ms1.ly > plane.lx * plane.ly and ms1.lx * ms1.ly > ns.lx * ns.ly:
                        ps.plane_list.remove(plane)
                        if ns in ps.plane_list:
                            ps.plane_list.remove(ns)
                        else:
                            ps.spare_plane_list.remove(ns)
                        ps.plane_list.append(ms1)
                        return
                    else:
                        continue
                else:
                    if (not can_place(ps, ms1, block_table, max_height)) and (
                            not can_place(ps, ms2, block_table, max_height)):
                        if (ms1.lx * ms1.ly > plane.lx * plane.ly and ms1.lx * ms1.ly > ns.lx * ns.ly) or (
                                ms2.lx * ms2.ly > plane.lx * plane.ly and ms2.lx * ms2.ly > ns.lx * ns.ly):
                            ps.plane_list.remove(plane)
                            if ns in ps.plane_list:
                                ps.plane_list.remove(ns)
                            else:
                                ps.spare_plane_list.remove(ns)
                            ps.spare_plane_list.append(ms1)
                            ps.spare_plane_list.append(ms2)
                            return
                        else:
                            continue
                    else:
                        ps.plane_list.remove(plane)
                        if ns in ps.plane_list:
                            ps.plane_list.remove(ns)
                        else:
                            ps.spare_plane_list.remove(ns)
                        if can_place(ps, ms1, block_table, max_height):
                            ps.plane_list.append(ms1)
                        else:
                            ps.spare_plane_list.append(ms1)

                        if can_place(ps, ms2, block_table, max_height):
                            ps.plane_list.append(ms2)
                        else:
                            ps.spare_plane_list.append(ms2)
                        return
    disable_plane(ps, plane)


# 构建箱体坐标，用于绘图
def build_box_position(block, init_pos, box_list):
    box_idx = (np.array(block.require_list) > 0).tolist().index(True)
    if box_idx > -1:
        box = box_list[box_idx]
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
        dimensions = (np.array([x for x in product(x_list, y_list, z_list)]) + np.array(
            [init_pos[0], init_pos[1], init_pos[2]])).tolist()
        if block.box_rotate:
            return sorted([d + [box.ly, box.lx, box.lz] for d in dimensions], key=lambda x: (x[0], x[1], x[2])), box_idx
        else:
            return sorted([d + [box.lx, box.ly, box.lz] for d in dimensions], key=lambda x: (x[0], x[1], x[2])), box_idx
    return None, None


# 绘制结果
def draw_packing_result(problem: Problem, ps: PackingState):
    fig = plt.figure()
    ax1 = fig.add_subplot(projection='3d')
    plot_linear_cube(ax1, 0, 0, 0, problem.container.lx, problem.container.ly, problem.height_limit)
    for p in ps.plan_list:
        box_pos, _ = build_box_position(p.block, (p.plane.x, p.plane.y, p.plane.z), problem.box_list)
        print(box_pos)
        positions = []
        sizes = []
        colors = ["yellow"] * len(box_pos)
        for bp in sorted(box_pos, key=lambda x: (x[0], x[1], x[2])):
            positions.append((bp[0], bp[1], bp[2]))
            sizes.append((bp[3], bp[4], bp[5]))

        pc = plotCubeAt(positions, sizes, colors=colors, edgecolor="k")
        ax1.add_collection3d(pc)
    plt.title('Cube{}'.format(0))
    plt.show()


# 基本启发式算法
def basic_heuristic(problem: Problem):
    # 生成简单块
    block_table = gen_simple_block(problem.container, problem.box_list, problem.num_list, problem.height_limit,
                                   problem.rotate)
    ps = PackingState(avail_list=problem.num_list)
    # 开始时，剩余空间堆栈中只有容器本身
    ps.plane_list.append(Plane(problem.container.x, problem.container.y, problem.container.z, problem.container.lx,
                               problem.container.ly))
    max_used_high = 0
    while ps.plane_list:
        plane = select_plane(ps)
        block_list = gen_block_list(plane, ps.avail_list, block_table, problem.height_limit)
        if block_list:
            block = find_block(plane, block_list, ps)
            # 填充平面
            fill_block(ps, plane, block)
            if plane.z + block.lz > max_used_high:
                max_used_high = plane.z + block.lz
        else:
            merge_plane(ps, plane, block_table, problem.height_limit)

    box_pos_info = [[] for _ in problem.num_list]
    for p in ps.plan_list:
        box_pos, box_idx = build_box_position(p.block, (p.plane.x, p.plane.y, p.plane.z), problem.box_list)
        for bp in box_pos:
            box_pos_info[box_idx].append((bp[0], bp[1], bp[2]))
    used_volume = problem.container.lx * problem.container.ly * max_used_high
    used_ratio = round(
        float(ps.volume) * 100 / float(problem.container.lx * problem.container.ly * problem.height_limit),
        3) if used_volume > 0 else 0
    return ps.avail_list, used_ratio, max_used_high, box_pos_info, ps


# 写入箱子位置
def write_box_pos(f_write, problem: Problem, ps: PackingState):
    f_write.write("boxes positions:\n")
    for p in ps.plan_list:
        box_pos, _ = build_box_position(p.block, (p.plane.x, p.plane.y, p.plane.z), problem.box_list)
        for box in box_pos:
            box = ", ".join([str(x) for x in box])
            f_write.write('[' + box + ']' + '\n')


# 文件数据输入
def file_data_input():
    f_read = open("./input_data.txt", 'r')
    f_write = open("./output_data.txt", 'w')
    for line in f_read.readlines():
        if line[0] == 'E':
            type_case = line
            f_write.write(type_case)
        elif line[0] == 'C':
            continue
        elif line[0] == 'B':
            line = line[2:]
            line = line.replace('[', ' ')
            line = line.replace(']', ' ')
            line = line.replace('(', ' ')
            line = line.replace(')', ' ')
            box_size_list = line.split(',')
            box_num = len(box_size_list)
            bx = []
            by = []
            bz = []
            bn = []
            for box_size in box_size_list:
                box_size = box_size.split()
                bx.append(int(box_size[0]))
                by.append(int(box_size[1]))
                bz.append(int(box_size[2]))
                bn.append(int(box_size[3]))
            num_list = bn
            box_list = []
            for i in range(box_num):
                box_list.append(Box(lx=bx[i], ly=by[i], lz=bz[i], type=i))
            container = Plane(0, 0, 0, 587, 233)
            problem = Problem(container=container, height_limit=220, box_list=box_list, num_list=copy.copy(num_list),
                              rotate=True)
            start_time = time.perf_counter()
            new_avail_list, used_ratio, used_high, box_pos_, packing_state = basic_heuristic(problem)
            end_time = time.perf_counter()
            operate_time = '%.3f' % (end_time - start_time)
            f_write.write("time: " + operate_time + 's\n')
            print(num_list)
            print(new_avail_list)
            new_avail_list = ",".join([str(x) for x in new_avail_list])
            f_write.write("left boxes: " + '[' + new_avail_list + ']' + '\n')
            print(used_ratio)
            used_ratio = str(used_ratio)
            f_write.write("used rate: " + used_ratio + '%\n')
            write_box_pos(f_write, problem, packing_state)
    f_read.close()
    f_write.close()


# 单个数据输入
def single_data_input():
    container = Plane(0, 0, 0, 10, 10)
    height_limit = 10
    box_list = [Box(lx=1, ly=2, lz=3, type=0)]
    num_list = [10000]
    box_min_edge = box_list[0].lx
    for box in box_list:
        box_min_edge = min(box_min_edge, min(box.lx, min(box.ly, box.lz)))
    problem = Problem(container=container, height_limit=height_limit, box_list=copy.copy(box_list),
                      num_list=copy.copy(num_list))
    new_avail_list, used_ratio, used_height, box_pos_, packing_state = basic_heuristic(problem)
    print(num_list)
    print(new_avail_list)
    print(used_ratio)
    while height_limit - used_height >= box_min_edge & len(new_avail_list) != 0:
        used_height_former = used_height
        height_limit = height_limit - used_height
        num_list = copy.copy(new_avail_list)
        box_list_tmp = copy.deepcopy(box_list)
        for box in box_list_tmp:
            box_min_tmp = min(box.lx, min(box.ly, box.lz))
            if box.lz == box_min_tmp:
                continue
            elif box.lx == box_min_tmp:
                box.lx = box.lz
                box.lz = box_min_tmp
            elif box.ly == box_min_tmp:
                box.ly = box.lz
                box.lz = box_min_tmp
        problem_tmp = Problem(container=container, height_limit=height_limit, box_list=copy.copy(box_list_tmp),
                              num_list=copy.copy(num_list))
        new_avail_list, used_ratio, used_height, box_pos_, packing_state_tmp = basic_heuristic(problem_tmp)
        for p in packing_state_tmp.plan_list:
            p.plane.z = p.plane.z + used_height_former
        print(num_list)
        print(new_avail_list)
        print(used_ratio)
        print(packing_state_tmp.volume)
        origin_type_num = len(problem.box_list)
        fill_list = np.zeros((origin_type_num,), dtype=int)
        print(fill_list)
        for p1 in packing_state.plan_list:
            p1.block.require_list = np.append(p1.block.require_list, fill_list)
            print(p1.block.require_list)
        fill_list = np.zeros((origin_type_num,), dtype=int)
        for p2 in packing_state_tmp.plan_list:
            p2.block.require_list = np.append(fill_list, p2.block.require_list)
            print(p2.block.require_list)
        packing_state.plan_list = packing_state.plan_list + packing_state_tmp.plan_list
        problem.box_list = problem.box_list + problem_tmp.box_list

        for i in range(len(problem.box_list)):
            problem.box_list[i].type = i
        for i in range(len(problem.box_list)):
            print(problem.box_list[i])
        for p in packing_state.plan_list:
            print(p.block)
            print(p.plane)
    draw_packing_result(problem, packing_state)


if __name__ == "__main__":
    file_data_input()
    # single_data_input()
