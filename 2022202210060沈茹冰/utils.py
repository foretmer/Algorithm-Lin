import sys
import math
import numpy as np

MAX_GAP = 0

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
        return "lx: %s, ly: %s, lz: %s, volume: %s, require: %s, box_rotate: %a" % (self.lx, self.ly, self.lz, self.volume, self.require_list, self.box_rotate)

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
        # 是否考虑旋转
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