import sys
import time
from itertools import product
import math
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import warnings
warnings.filterwarnings("ignore")

MAX_GAP = 0

# 绘图相关函数
def plot_linear_cube(ax, x, y, z, dx, dy, dz, color='red', linestyle=None):
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
        return "lx: {}, ly: {}, lz: {}, type: {}".format(self.lx, self.ly, self.lz,self.type)


# 块类
class Block:
    def __init__(self, lx, ly, lz, require_list=[], box_rotate=-1):
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
        return "lx: %s, ly: %s, lz: %s, volume: %s, require: %s,box_rotate: %a" % (self.lx, self.ly, self.lz, self.volume, self.require_list,self.box_rotate)

    def __eq__(self, other):
        return self.lx == other.lx and self.ly == other.ly and self.lz == other.lz and self.box_rotate == other.box_rotate and (np.array(self.require_list) == np.array(other.require_list)).all()


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
        return "x:{}, y:{}, z:{}, lx:{}, ly:{}, height_limit:{}".format(self.x, self.y, self.z, self.lx, self.ly, self.height_limit)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and self.lx == other.lx and self.ly == other.ly

    # 判断是否与另一个平面相邻（z坐标相同，至少有一个边平齐），并返回合并后的两个平面
    def adjacent_with(self, other):
        if self.z != other.z:
            return False, None, None
        # 矩形中心
        my_center = (self.x + self.lx / 2, self.y + self.ly / 2)
        other_center = (other.x + other.lx / 2, other.y + other.ly / 2)
        # 矩形相邻时的中心距离
        x_adjacent_measure = self.lx / 2 + other.lx / 2
        y_adjacent_measure = self.ly / 2 + other.ly / 2
        # 宽边相邻，长边对齐
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
                ms1 = Plane(min(self.x, other.x), max(self.y, other.y), self.z, self.lx + other.lx, min(self.ly, other.ly))
                if self.ly > other.ly:
                    ms2 = Plane(self.x, self.y, self.z, self.lx, self.ly - other.ly)
                else:
                    ms2 = Plane(other.x, other.y, self.z, other.lx, other.ly - self.ly)
                return True, ms1, ms2
        # 长边相邻，宽边对齐
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
                ms1 = Plane(max(self.x, other.x), min(self.y, other.y), self.z, min(self.lx, other.lx), self.ly + other.ly)
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
    # 选最低的平面
    min_z = min([p.z for p in ps.plane_list])
    temp_planes = [p for p in ps.plane_list if p.z == min_z]
    if len(temp_planes) == 1:
        return temp_planes[0]
    # 相同高度的平面有多个的话，选择面积最小的平面
    min_area = min([p.lx * p.ly for p in temp_planes])
    temp_planes = [p for p in temp_planes if p.lx * p.ly == min_area]
    if len(temp_planes) == 1:
        return temp_planes[0]
    # 较狭窄的
    min_narrow = min([p.lx/p.ly if p.lx <= p.ly else p.ly/p.lx for p in temp_planes])
    new_temp_planes = []
    for p in temp_planes:
        narrow = p.lx/p.ly if p.lx <= p.ly else p.ly/p.lx
        if narrow == min_narrow:
            new_temp_planes.append(p)
    if len(new_temp_planes) == 1:
        return new_temp_planes[0]
    # x坐标较小
    min_x = min([p.x for p in new_temp_planes])
    new_temp_planes = [p for p in new_temp_planes if p.x == min_x]
    if len(new_temp_planes) == 1:
        return new_temp_planes[0]
    # y坐标较小
    min_y = min([p.y for p in new_temp_planes])
    new_temp_planes = [p for p in new_temp_planes if p.y == min_y]
    return new_temp_planes[0]


# 将某平面从可用平面列表转移到备用平面列表
def disable_plane(ps: PackingState, plane: Plane):
    ps.plane_list.remove(plane)
    ps.spare_plane_list.append(plane)


# 生成简单块
def gen_simple_block(init_plane: Plane, box_list, num_list, max_height, can_rotate=False, rotate_num = 5):
    block_table = []
    for box in box_list:
        for nx in np.arange(num_list[box.type]) + 1:
            for ny in np.arange(num_list[box.type] / nx) + 1:
                for nz in np.arange(num_list[box.type] / nx / ny) + 1:
                    if box.lx * nx <= init_plane.lx and box.ly * ny <= init_plane.ly and box.lz * nz <= max_height - init_plane.z:
                        # 该简单块需要的立体箱子数量
                        requires = np.full_like(num_list, 0)
                        requires[box.type] = int(nx) * int(ny) * int(nz)
                        # 简单块
                        block = Block(lx=box.lx * nx, ly=box.ly * ny, lz=box.lz * nz, require_list=requires)
                        # 简单块填充体积
                        block.volume = box.lx * nx * box.ly * ny * box.lz * nz
                        block_table.append(block)
                    if can_rotate:
                        # 物品朝向选择90度进行堆叠, box_rotate = 1, x与y交换
                        if rotate_num >= 1 and box.ly * nx <= init_plane.lx and box.lx * ny <= init_plane.ly and box.lz * nz <= max_height - init_plane.z:
                            requires = np.full_like(num_list, 0)
                            requires[box.type] = int(nx) * int(ny) * int(nz)
                            # 简单块
                            block = Block(lx=box.ly * nx, ly=box.lx * ny, lz=box.lz * nz, require_list=requires, box_rotate=1)
                            # 简单块填充体积
                            block.volume = box.ly * nx * box.lx * ny * box.lz * nz
                            block_table.append(block)
                        # x与z交换
                        elif rotate_num >= 2 and box.lz * nx <= init_plane.lx and box.ly * ny <= init_plane.ly and box.lx * nz <= max_height - init_plane.z:
                            requires = np.full_like(num_list, 0)
                            requires[box.type] = int(nx) * int(ny) * int(nz)
                            # 简单块
                            block = Block(lx=box.lz * nx, ly=box.ly * ny, lz=box.lx * nz, require_list=requires, box_rotate=2)
                            # 简单块填充体积
                            block.volume = box.lz * nx * box.ly * ny * box.lx * nz
                            block_table.append(block)
                        # y与z交换
                        elif rotate_num >= 3 and box.lx * nx <= init_plane.lx and box.lz * ny <= init_plane.ly and box.ly * nz <= max_height - init_plane.z:
                            requires = np.full_like(num_list, 0)
                            requires[box.type] = int(nx) * int(ny) * int(nz)
                            # 简单块
                            block = Block(lx=box.lx * nx, ly=box.lz * ny, lz=box.ly * nz, require_list=requires, box_rotate=3)
                            # 简单块填充体积
                            block.volume = box.lx * nx * box.lz * ny * box.ly * nz
                            block_table.append(block)
                        # y z x
                        elif rotate_num >= 4 and box.ly * nx <= init_plane.lx and box.lz * ny <= init_plane.ly and box.lx * nz <= max_height - init_plane.z:
                            requires = np.full_like(num_list, 0)
                            requires[box.type] = int(nx) * int(ny) * int(nz)
                            # 简单块
                            block = Block(lx=box.ly * nx, ly=box.lz * ny, lz=box.lx * nz, require_list=requires, box_rotate=4)
                            # 简单块填充体积
                            block.volume = box.ly * nx * box.lz * ny * box.lx * nz
                            block_table.append(block)
                        # z x y
                        elif rotate_num >= 5 and box.lz * nx <= init_plane.lx and box.lx * ny <= init_plane.ly and box.ly * nz <= max_height - init_plane.z:
                            requires = np.full_like(num_list, 0)
                            requires[box.type] = int(nx) * int(ny) * int(nz)
                            # 简单块
                            block = Block(lx=box.lz * nx, ly=box.lx * ny, lz=box.ly * nz, require_list=requires, box_rotate=5)
                            # 简单块填充体积
                            block.volume = box.lz * nx * box.lx * ny * box.ly * nz
                            block_table.append(block)
    return block_table


# 生成可行块列表
def gen_block_list(plane: Plane, avail, block_table, max_height):
    block_list = []
    for block in block_table:
        # 块中需要的箱子数量必须小于最初的待装箱的箱子数量
        # 块的尺寸必须小于放置空间尺寸
        # 块的重量必须小于可放置重量
        if (np.array(block.require_list) <= np.array(avail)).all() and block.lx <= plane.lx and block.ly <= plane.ly \
                and block.lz <= max_height - plane.z:
            block_list.append(block)
    return block_list


# 查找下一个可行块
def find_block(plane: Plane, block_list, ps: PackingState):
    # 平面的面积
    plane_area = plane.lx * plane.ly
    # 放入块后，剩余的最小面积
    min_residual_area = min([plane_area - b.lx * b.ly for b in block_list])
    # 剩余面积相同，保留最大体积的块
    candidate = [b for b in block_list if plane_area - b.lx * b.ly == min_residual_area]
    # 可用平面最大高度
    max_plane_height = min([p.z for p in ps.plane_list])
    _candidate = sorted(candidate, key=lambda x: x.volume, reverse=True)
    # if max_plane_height == 0:
    #     # 第一次放置体积最大的块
    #     _candidate = sorted(candidate, key=lambda x: x.volume, reverse=True)
    # else:
    #     # 选择平面时尽量使放置物品后与已经放置的物品平齐
    #     _candidate = sorted(candidate, key=lambda x: x.lz + plane.z - max_plane_height)
    #     _candidate = sorted(candidate, key=lambda x: x.volume + ps.volume - 2440*1220*1000)
    return _candidate[0]


# 裁切出新的剩余空间（有稳定性约束）
def gen_new_plane(plane: Plane, block: Block):
    # 块顶部的新平面
    rs_top = Plane(plane.x, plane.y, plane.z + block.lz, block.lx, block.ly)
    # 底部平面裁切
    if block.lx == plane.lx and block.ly == plane.ly:
        return rs_top, None, None
    if block.lx == plane.lx:
        return rs_top, Plane(plane.x, plane.y + block.ly, plane.z, plane.lx, plane.ly - block.ly), None
    if block.ly == plane.ly:
        return rs_top, Plane(plane.x + block.lx, plane.y, plane.z, plane.lx - block.lx, block.ly), None
    # 比较两种方式中面积较大的两个子平面，选择有最大面积子平面的生成方式
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
    # 浪费面积
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
    # 更新放置计划
    place = Place(plane, block)
    ps.plan_list.append(place)
    # 更新体积利用率
    ps.volume = ps.volume + block.volume
    # 产生三个新的平面
    rs_top, rs1, rs2 = gen_new_plane(plane, block)
    # 移除裁切前的平面
    ps.plane_list.remove(plane)
    # 装入新的可用平面
    if rs_top:
        ps.plane_list.append(rs_top)
    if rs1:
        ps.plane_list.append(rs1)
    if rs2:
        ps.plane_list.append(rs2)


# 合并平面
def merge_plane(ps: PackingState, plane: Plane, block_table, max_height):
    # print("合并平面开始了")
    for ns in ps.plane_list + ps.spare_plane_list:
        # 不和自己合并
        if plane == ns:
            continue
        # 找相邻平面
        is_adjacent, ms1, ms2 = plane.adjacent_with(ns)
        if is_adjacent:
            # print("有相邻平面呦")
            block_list = gen_block_list(ns, ps.avail_list, block_table, max_height)
            # 相邻平面本身能放入至少一个剩余物品
            if len(block_list) > 0:
                block = find_block(ns, block_list, ps)
                # 计算相邻平面和原平面浪费面积的总和
                ws1 = ns.lx * ns.ly - block.lx * block.ly + plane.lx * plane.ly
                # 计算合并后平面的总浪费面积
                ws2 = plane_waste(ps, ms1, block_table, max_height) + plane_waste(ps, ms2, block_table, max_height)
                # 合并后，浪费更小，则保留合并
                if ws1 > ws2:
                    # 保留平面合并
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
                    # 放弃平面合并，寻找其他相邻平面
                    continue
            # 相邻平面本身无法放入剩余物品
            else:
                # 合共后产生一个平面
                if ms2 is None:
                    # 能放物品，则保留平面合并
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
                        # ps.spare_plane_list.append(ms1)
                        ps.plane_list.append(ms1)
                        return
                    else:
                        continue
                # 合并后产生两个平面
                else:
                    if (not can_place(ps, ms1, block_table, max_height)) and (not can_place(ps, ms2, block_table, max_height)):
                        if (ms1.lx * ms1.ly > plane.lx * plane.ly and ms1.lx * ms1.ly > ns.lx * ns.ly) or (ms2.lx * ms2.ly > plane.lx * plane.ly and ms2.lx * ms2.ly > ns.lx * ns.ly):
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

    # 若对平面列表和备用平面列表搜索完毕后，最终仍没有找到可合并的平面，则将目标平面从平面列表移入备用平面列表
    disable_plane(ps, plane)


# 构建箱体坐标，用于绘图
def build_box_position(block, init_pos, box_list):
    # 箱体类型索引
    box_idx = (np.array(block.require_list) > 0).tolist().index(True)
    if box_idx > -1:
        # 所需箱体
        box = box_list[box_idx]

        x_list = []
        y_list = []
        z_list = []
        # 箱体的相对坐标
        if block.box_rotate != -1:
            if block.box_rotate == 1:
                nx = block.lx / box.ly
                ny = block.ly / box.lx
                nz = block.lz / box.lz
                x_list = (np.arange(0, nx) * box.ly).tolist()
                y_list = (np.arange(0, ny) * box.lx).tolist()
                z_list = (np.arange(0, nz) * box.lz).tolist()
            if block.box_rotate == 2:
                nx = block.lx / box.lz
                ny = block.ly / box.ly
                nz = block.lz / box.lx
                x_list = (np.arange(0, nx) * box.lz).tolist()
                y_list = (np.arange(0, ny) * box.ly).tolist()
                z_list = (np.arange(0, nz) * box.lx).tolist()
            if block.box_rotate == 3:
                nx = block.lx / box.lx
                ny = block.ly / box.lz
                nz = block.lz / box.ly
                x_list = (np.arange(0, nx) * box.lx).tolist()
                y_list = (np.arange(0, ny) * box.lz).tolist()
                z_list = (np.arange(0, nz) * box.ly).tolist()
            if block.box_rotate == 4:
                nx = block.lx / box.ly
                ny = block.ly / box.lz
                nz = block.lz / box.lx
                x_list = (np.arange(0, nx) * box.ly).tolist()
                y_list = (np.arange(0, ny) * box.lz).tolist()
                z_list = (np.arange(0, nz) * box.lx).tolist()
            if block.box_rotate == 5:
                nx = block.lx / box.lz
                ny = block.ly / box.lx
                nz = block.lx / box.ly
                x_list = (np.arange(0, nx) * box.lz).tolist()
                y_list = (np.arange(0, ny) * box.lx).tolist()
                z_list = (np.arange(0, nz) * box.ly).tolist()
        else:
            nx = block.lx / box.lx
            ny = block.ly / box.ly
            nz = block.lz / box.lz
            x_list = (np.arange(0, nx) * box.lx).tolist()
            y_list = (np.arange(0, ny) * box.ly).tolist()
            z_list = (np.arange(0, nz) * box.lz).tolist()
        # 箱体的绝对坐标
        dimensions = (np.array([x for x in product(x_list, y_list, z_list)]) + np.array([init_pos[0], init_pos[1], init_pos[2]])).tolist()
        # 箱体的坐标及尺寸
        if block.box_rotate != -1:
            if block.box_rotate == 1:
                return sorted([d + [box.ly, box.lx, box.lz] for d in dimensions], key=lambda x: (x[0], x[1], x[2])), box_idx
            elif block.box_rotate == 2:
                return sorted([d + [box.lz, box.ly, box.lx] for d in dimensions], key=lambda x: (x[0], x[1], x[2])), box_idx
            elif block.box_rotate == 3:
                return sorted([d + [box.lx, box.lz, box.ly] for d in dimensions], key=lambda x: (x[0], x[1], x[2])), box_idx
            elif block.box_rotate == 4:
                return sorted([d + [box.ly, box.lz, box.lx] for d in dimensions], key=lambda x: (x[0], x[1], x[2])), box_idx
            elif block.box_rotate == 5:
                return sorted([d + [box.lz, box.lx, box.ly] for d in dimensions], key=lambda x: (x[0], x[1], x[2])), box_idx
        else:
            return sorted([d + [box.lx, box.ly, box.lz] for d in dimensions], key=lambda x: (x[0], x[1], x[2])), box_idx
    return None, None


# 绘制排样结果
def draw_packing_result(problem: Problem, ps: PackingState):
    # 绘制结果
    fig = plt.figure()
    ax1 = fig.gca(projection='3d')
    # 绘制容器
    plot_linear_cube(ax1, 0, 0, 0, problem.container.lx, problem.container.ly, problem.height_limit)
    for p in ps.plan_list:
        # 绘制箱子
        #print(p.plane.x, p.plane.y, p.plane.z)
        box_pos, _ = build_box_position(p.block, (p.plane.x, p.plane.y, p.plane.z), problem.box_list)
        positions = []
        sizes = []
        colors = ["yellow"] * len(box_pos)
        for bp in sorted(box_pos, key=lambda x: (x[0], x[1], x[2])):
            positions.append((bp[0], bp[1], bp[2]))
            sizes.append((bp[3], bp[4], bp[5]))

        pc = plotCubeAt(positions, sizes, colors=colors, edgecolor="k")
        ax1.add_collection3d(pc)
    # plt.title('Cube{}'.format(0))

    plt.show()
    # plt.savefig('3d_lowest_plane_packing.png', dpi=800)


# 基本启发式算法
def basic_heuristic(problem: Problem, f):
    ps_final = None
    used_radio_max = 0
    show_picture = False

    time1 = time.perf_counter()

    for i in range(6):
        # 生成简单块
        block_table = gen_simple_block(problem.container, problem.box_list, problem.num_list, problem.height_limit, problem.rotate, i)
        # 初始化排样状态
        ps = PackingState(avail_list=problem.num_list)
        # 开始时，剩余空间堆栈中只有容器本身
        ps.plane_list.append(Plane(problem.container.x, problem.container.y, problem.container.z, problem.container.lx,problem.container.ly))
        max_used_high = 0

        # 循环直到所有平面使用完毕
        while ps.plane_list:
            # 选择平面
            plane = select_plane(ps)
            # 查找可用块
            block_list = gen_block_list(plane, ps.avail_list, block_table, problem.height_limit)
            if block_list:
                # 查找下一个近似最优块
                block = find_block(plane, block_list, ps)
                # 填充平面
                fill_block(ps, plane, block)
                # 更新最大使用高度
                if plane.z + block.lz > max_used_high:
                    max_used_high = plane.z + block.lz
            else:
                # 合并相邻平面
                merge_plane(ps, plane, block_table, problem.height_limit)
        used_volume = problem.container.lx * problem.container.ly * max_used_high
        used_ratio = round(float(ps.volume) * 100 / float(used_volume), 3) if used_volume > 0 else 0
        if used_ratio > used_radio_max:
            used_radio_max = used_ratio
            ps_final = ps
    time2 = time.perf_counter()
    # 板材的位置信息
    box_pos_info = [[] for _ in problem.num_list]
    for p in ps_final.plan_list:
        box_pos, box_idx = build_box_position(p.block, (p.plane.x, p.plane.y, p.plane.z), problem.box_list)
        for bp in box_pos:
            box_pos_info[box_idx].append([bp[0], bp[1], bp[2]])
            f.write('{:.2f}'.format(bp[0]) + ' ' + '{:.2f}'.format(bp[1])  + ' ' + '{:.2f}'.format(bp[2]) + '\n')
            # print(bp[0],bp[1],bp[2])
    f.write('used ratio:' + str(used_radio_max) + '%\n\n')
    print('Used Radio:{:.3f}% '.format(used_radio_max), 'Time:{:.3f}s'.format(round(time2 - time1, 3)))

    # # 绘制排样结果图
    if show_picture:
        draw_packing_result(problem, ps_final)

    return ps_final.avail_list, used_radio_max, box_pos_info, ps_final



def import_data():
    box_list, num_list, container_list, filepath, length, width, height = [], [], [], './data.txt', 0, 0, 0
    with open(filepath, 'r', encoding='utf-8') as f:
        ff, series, num_L, idx, num, flag = f.read(), '', [], 0, 0, 0
        for le in ff:
            if le == 'C':
                series = 'C'
            elif le == 'B':
                series = 'B'
                box_list.append([])
                num_list.append([])
            elif le in ['[', ',', '，', '\n']:
                continue
            elif le == ']':
                idx = 0
                container_list.append([Plane(0, 0, 0, length, width, height)])
            elif le == '(':
                num_L.clear()
            elif le == ')':
                if num != 0:
                    if flag == 0:
                        flag = 1
                    num_L.append(num / flag)
                if series == 'C':
                    length, width, height = num_L[0], num_L[1], num_L[2]
                else:
                    box_list[-1].append(Box(num_L[0], num_L[1], num_L[2], type=idx))
                    idx += 1
                    num_list[-1].append(num_L[3])
                num_L.clear()
                num, flag = 0, 0
            elif le == ' ':
                if num != 0:
                    if flag == 0:
                        flag = 1
                    num_L.append(num / flag)
                    num, flag = 0, 0
            elif le == '.':
                flag = 1
            else:
                num = num * 10 + int(le)
                flag *= 10
    return container_list, box_list, num_list

# 主算法
def simple_test(container_lists, box_lists, num_lists):
    f = open('output.txt', 'w')
    for i in range(len(container_lists)):
    # for i in range(3):
        # 容器底面
        container = container_lists[i][0]
        # 箱体列表
        box_list = box_lists[i]
        num_list = num_lists[i]
        # 问题
        problem = Problem(container=container, height_limit=container.height_limit, box_list=box_list, num_list=num_list, rotate=True)
        # 具体计算
        f.write('Case ' + str(i+1) + '\n')
        new_avail_list, used_ratio, box_pos_, _ = basic_heuristic(problem, f)
    f.close()



if __name__ == "__main__":
    container_list, box_list, num_list = import_data()
    simple_test(container_list, box_list, num_list)