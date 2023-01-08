import numpy as np
from functools import reduce
import copy
from .PctTools import AddNewEMSZ, maintainEventBottom


class Stack(object):
    def __init__(self, centre, mass):
        self.centre = centre
        self.mass = mass


def IsUsableEMS(xlow, ylow, zlow, x1, y1, z1, x2, y2, z2):
    xd = x2 - x1
    yd = y2 - y1
    zd = z2 - z1
    if ((xd >= xlow) and (yd >= ylow) and (zd >= zlow)):
        return True
    return False


class Box(object):
    def __init__(self, x, y, z, lx, ly, lz, density, virtual=False):
        self.x = x
        self.y = y
        self.z = z
        self.lx = lx
        self.ly = ly
        self.lz = lz

        self.centre = np.array([self.lx + self.x / 2, self.ly + self.y / 2, self.lz + self.z / 2])
        self.vertex_low = np.array([self.lx, self.ly, self.lz])
        self.vertex_high = np.array([self.lx + self.x, self.ly + self.y, self.lz + self.z])
        self.mass = x * y * z * density
        if virtual: self.mass *= 1.0
        self.bottom_edges = []
        self.bottom_whole_contact_area = None

        self.up_edges = {}
        self.up_virtual_edges = {}

        # 当前的stack
        self.thisStack = Stack(self.centre, self.mass)
        # 当前虚拟的stack
        self.thisVirtualStack = Stack(self.centre, self.mass)
        self.involved = False


class Space(object):
    def __init__(self, width=10, length=10, height=10, size_minimum=1, holder=200):
        self.plain_size = np.array([width, length, height])
        self.max_axis = max(width, length)
        self.height = height
        self.low_bound = size_minimum

        # 底面grid
        self.plain = np.zeros(shape=(self.max_axis, self.max_axis), dtype=np.int32)
        # 底面占据的grid
        self.space_mask = np.zeros(shape=(self.max_axis, self.max_axis), dtype=np.int32)
        # 底面剩余的grid
        self.left_space = np.zeros(shape=(self.max_axis, self.max_axis), dtype=np.int32)
        # 中间节点（已经装好的item）的相关信息
        self.box_vec = np.zeros((holder, 9))
        self.box_vec[0][-1] = 1

        self.reset()
        self.alleps = []

        # 保存ems的相关信息
        self.EMS3D = dict()
        # 初始的EMS: DBL, OUR, serial number
        self.EMS3D[0] = np.array([0, 0, 0, width, length, height, self.serial_number])

    def reset(self):
        self.plain[:] = 0
        self.space_mask[:] = 0
        self.left_space[:] = 0
        self.box_vec[:] = 0
        self.box_vec[0][-1] = 1

        self.NOEMS = 1
        self.EMS = [np.array([0, 0, 0, *self.plain_size])]

        # 装好的box
        self.boxes = []
        self.box_idx = 0
        self.serial_number = 0

        self.ZMAP = dict()
        self.ZMAP[0] = dict()

        r = self.ZMAP[0]
        r['x_up'] = [0]
        r['y_left'] = [0]
        r['x_bottom'] = [self.plain_size[0]]
        r['y_right'] = [self.plain_size[1]]

        self.EMS3D = dict()
        self.EMS3D[0] = np.array(
            [0, 0, 0, self.plain_size[0], self.plain_size[1], self.plain_size[2], self.serial_number])

    @staticmethod
    def update_height_graph(plain, box):
        plain = copy.deepcopy(plain)
        le = box.lx
        ri = box.lx + box.x
        up = box.ly
        do = box.ly + box.y
        max_h = np.max(plain[le:ri, up:do])
        max_h = max(max_h, box.lz + box.z)
        plain[le:ri, up:do] = max_h
        return plain

    def get_ratio(self):
        vo = reduce(lambda x, y: x + y, [box.x * box.y * box.z for box in self.boxes], 0.0)
        mx = self.plain_size[0] * self.plain_size[1] * self.plain_size[2]
        ratio = vo / mx
        assert ratio <= 1.0
        return ratio

    def drop_box(self, box_size, idx, flag, density):
        if not flag:
            x, y, z = box_size
        else:
            y, x, z = box_size

        lx, ly = idx
        # 放置区域内的最高点
        rec = self.plain[lx:lx + x, ly:ly + y]
        max_h = np.max(rec)
        box_now = Box(x, y, z, lx, ly, max_h, density)

        sta_flag = self.check_box(x, y, lx, ly, z, max_h)
        if sta_flag:
            # 更新bin中放入的box列表
            self.boxes.append(box_now)  # record rotated box
            # 更新等高线
            self.plain = self.update_height_graph(self.plain, self.boxes[-1])
            # 更新中间节点的状态信息，包括DBL，OUR等
            self.box_vec[self.box_idx] = np.array(
                [lx, ly, max_h, lx + x, ly + y, max_h + z, density, 0, 1])
            self.box_idx += 1
            return True
        return False

    # Virtually place an item into the bin,
    # this function is used to check whether the placement is feasible for the current item
    def drop_box_virtual(self, box_size, idx, flag, density, returnH=False, returnMap=False):
        if not flag:
            # 该rot下item的x,y,z大小
            x, y, z = box_size
        else:
            y, x, z = box_size

        # 放置位置底面的左下点
        lx, ly = idx
        rec = self.plain[lx:lx + x, ly:ly + y]
        max_h = np.max(rec)

        box_now = Box(x, y, z, lx, ly, max_h, density, True)

        if returnH:
            return self.check_box(x, y, lx, ly, z, max_h), max_h
        elif returnMap:
            return self.check_box(x, y, lx, ly, z, max_h), self.update_height_graph(self.plain,
                                                                                    box_now)
        else:
            return self.check_box(x, y, lx, ly, z, max_h)

    # 对放置的位置做边缘检测
    def check_box(self, x, y, lx, ly, z, max_h):
        if lx + x > self.plain_size[0] or ly + y > self.plain_size[1]:
            return False
        if lx < 0 or ly < 0:
            return False
        if max_h + z > self.height:
            return False

        return True

    # Calculate the incrementally generated empty maximal spaces during the packing.
    def GENEMS(self, itemLocation):
        numofemss = len(self.EMS)
        delflag = []
        for emsIdx in range(numofemss):
            xems1, yems1, zems1, xems2, yems2, zems2 = self.EMS[emsIdx]
            xtmp1, ytmp1, ztmp1, xtmp2, ytmp2, ztmp2 = itemLocation

            if (xems1 > xtmp1): xtmp1 = xems1
            if (yems1 > ytmp1): ytmp1 = yems1
            if (zems1 > ztmp1): ztmp1 = zems1
            if (xems2 < xtmp2): xtmp2 = xems2
            if (yems2 < ytmp2): ytmp2 = yems2
            if (zems2 < ztmp2): ztmp2 = zems2

            if (xtmp1 > xtmp2): xtmp1 = xtmp2
            if (ytmp1 > ytmp2): ytmp1 = ytmp2
            if (ztmp1 > ztmp2): ztmp1 = ztmp2
            if (xtmp1 == xtmp2 or ytmp1 == ytmp2 or ztmp1 == ztmp2):
                continue

            self.Difference(emsIdx, (xtmp1, ytmp1, ztmp1, xtmp2, ytmp2, ztmp2))
            delflag.append(emsIdx)

        if len(delflag) != 0:
            NOEMS = len(self.EMS)
            self.EMS = [self.EMS[i] for i in range(NOEMS) if i not in delflag]
        # 去掉冗余的EMS
        self.EliminateInscribedEMS()

        # maintain the event point by the way
        cx_min, cy_min, cz_min, cx_max, cy_max, cz_max = itemLocation
        # bottom
        if cz_min < self.plain_size[2]:
            bottomRecorder = self.ZMAP[cz_min]
            cbox2d = [cx_min, cy_min, cx_max, cy_max]
            maintainEventBottom(cbox2d, bottomRecorder['x_up'], bottomRecorder['y_left'], bottomRecorder['x_bottom'],
                                bottomRecorder['y_right'], self.plain_size)

        if cz_max < self.plain_size[2]:
            AddNewEMSZ(itemLocation, self)

    # Split an EMS when it intersects a placed item
    def Difference(self, emsID, intersection):
        x1, y1, z1, x2, y2, z2 = self.EMS[emsID]
        x3, y3, z3, x4, y4, z4, = intersection
        if self.low_bound == 0:
            self.low_bound = 0.1
        if IsUsableEMS(self.low_bound, self.low_bound, self.low_bound, x1, y1, z1, x3, y2, z2):
            self.AddNewEMS(x1, y1, z1, x3, y2, z2)
        if IsUsableEMS(self.low_bound, self.low_bound, self.low_bound, x4, y1, z1, x2, y2, z2):
            self.AddNewEMS(x4, y1, z1, x2, y2, z2)
        if IsUsableEMS(self.low_bound, self.low_bound, self.low_bound, x1, y1, z1, x2, y3, z2):
            self.AddNewEMS(x1, y1, z1, x2, y3, z2)
        if IsUsableEMS(self.low_bound, self.low_bound, self.low_bound, x1, y4, z1, x2, y2, z2):
            self.AddNewEMS(x1, y4, z1, x2, y2, z2)
        if IsUsableEMS(self.low_bound, self.low_bound, self.low_bound, x1, y1, z4, x2, y2, z2):
            self.AddNewEMS(x1, y1, z4, x2, y2, z2)

    def AddNewEMS(self, a, b, c, x, y, z):
        self.EMS.append(np.array([a, b, c, x, y, z]))

    # Eliminate redundant ems
    def EliminateInscribedEMS(self):
        NOEMS = len(self.EMS)
        delflags = np.zeros(NOEMS)
        for i in range(NOEMS):
            for j in range(NOEMS):
                if i == j:
                    continue
                # 如果EMS[i]被EMS[j]包含，则删掉EMS[i]
                if (self.EMS[i][0] >= self.EMS[j][0] and self.EMS[i][1] >= self.EMS[j][1]
                        and self.EMS[i][2] >= self.EMS[j][2] and self.EMS[i][3] <= self.EMS[j][3]
                        and self.EMS[i][4] <= self.EMS[j][4] and self.EMS[i][5] <= self.EMS[j][5]):
                    delflags[i] = 1
                    break
        self.EMS = [self.EMS[i] for i in range(NOEMS) if delflags[i] != 1]
        return len(self.EMS)

    # Convert EMS to placement (leaf node) for the current item.
    def EMSPoint(self, next_box):
        posVec = set()
        orientation = 6

        for ems in self.EMS:
            for rot in range(orientation):  # 0 x y z, 1 y x z, 2 x z y, 3 y z x, 4 z x y, 5 z y x
                if rot == 0:
                    sizex, sizey, sizez = next_box[0], next_box[1], next_box[2]
                elif rot == 1:
                    sizex, sizey, sizez = next_box[1], next_box[0], next_box[2]
                    if sizex == sizey:
                        continue
                elif rot == 2:
                    sizex, sizey, sizez = next_box[0], next_box[2], next_box[1]
                    if sizey == sizez:
                        continue
                elif rot == 3:
                    sizex, sizey, sizez = next_box[1], next_box[2], next_box[0]
                    if sizey == sizez or sizex == sizez:
                        continue
                elif rot == 4:
                    sizex, sizey, sizez = next_box[2], next_box[0], next_box[1]
                    if sizex == sizey or sizex == sizez:
                        continue
                elif rot == 5:
                    sizex, sizey, sizez = next_box[2], next_box[1], next_box[0]
                    if sizex == sizey or sizey == sizez or sizex == sizez:
                        continue

                # 如果当前EMS能容纳该item，则对每个rot就有4种放置位置
                if ems[3] - ems[0] >= sizex and ems[4] - ems[1] >= sizey and ems[5] - ems[2] >= sizez:
                    posVec.add((ems[0], ems[1], ems[2], ems[0] + sizex, ems[1] + sizey, ems[2] + sizez))
                    posVec.add((ems[3] - sizex, ems[1], ems[2], ems[3], ems[1] + sizey, ems[2] + sizez))
                    posVec.add((ems[0], ems[4] - sizey, ems[2], ems[0] + sizex, ems[4], ems[2] + sizez))
                    posVec.add((ems[3] - sizex, ems[4] - sizey, ems[2], ems[3], ems[4], ems[2] + sizez))
        # 每个posvec是包括了放置的DBL点和OUR点
        posVec = np.array(list(posVec))
        return posVec

    # Convert EMS to placement (leaf node) for the current item.
    def EMSUtilization(self, next_box,next_den):
        orientation = 6
        EMS_utilization = dict()
        EMS_posvec = dict()

        for ems in self.EMS:
            EMS_posvec[tuple(ems)] = []
            EMS_utilization[tuple(ems)] = 0
            for rot in range(orientation):  # 0 x y z, 1 y x z, 2 x z y, 3 y z x, 4 z x y, 5 z y x
                if rot == 0:
                    sizex, sizey, sizez = next_box[0], next_box[1], next_box[2]
                elif rot == 1:
                    sizex, sizey, sizez = next_box[1], next_box[0], next_box[2]
                    if sizex == sizey:
                        continue
                elif rot == 2:
                    sizex, sizey, sizez = next_box[0], next_box[2], next_box[1]
                    if sizey == sizez:
                        continue
                elif rot == 3:
                    sizex, sizey, sizez = next_box[1], next_box[2], next_box[0]
                    if sizey == sizez or sizex == sizez:
                        continue
                elif rot == 4:
                    sizex, sizey, sizez = next_box[2], next_box[0], next_box[1]
                    if sizex == sizey or sizex == sizez:
                        continue
                elif rot == 5:
                    sizex, sizey, sizez = next_box[2], next_box[1], next_box[0]
                    if sizex == sizey or sizey == sizez or sizex == sizez:
                        continue

                # 如果当前EMS能容纳该item，则对每个rot就有4种放置位置
                if ems[3] - ems[0] >= sizex and ems[4] - ems[1] >= sizey and ems[5] - ems[2] >= sizez:
                    if self.drop_box_virtual([sizex, sizey, sizez], (ems[0], ems[1]), False, next_den):
                        EMS_posvec[tuple(ems)].append((ems[0], ems[1], ems[2], ems[0] + sizex, ems[1] + sizey, ems[2] + sizez))
                    if self.drop_box_virtual([sizex, sizey, sizez], (ems[3] - sizex, ems[1]), False, next_den):
                        EMS_posvec[tuple(ems)].append((ems[3] - sizex, ems[1], ems[2], ems[3], ems[1] + sizey, ems[2] + sizez))
                    if self.drop_box_virtual([sizex, sizey, sizez], (ems[0], ems[4] - sizey), False, next_den):
                        EMS_posvec[tuple(ems)].append((ems[0], ems[4] - sizey, ems[2], ems[0] + sizex, ems[4], ems[2]+ sizez))
                    if self.drop_box_virtual([sizex, sizey, sizez], (ems[3] - sizex, ems[4] - sizey), False, next_den):
                        EMS_posvec[tuple(ems)].append((ems[3] - sizex, ems[4] - sizey, ems[2], ems[3], ems[4], ems[2] + sizez))
            if len(EMS_posvec[tuple(ems)]) >= 1:
                ems_x = ems[3] - ems[0]
                ems_y = ems[4] - ems[1]
                ems_z = ems[5] - ems[2]
                EMS_utilization[tuple(ems)] = (next_box[0] * next_box[1] * next_box[2]) / (ems_x * ems_y * ems_z)
        # 每个posvec是包括了放置的DBL点和OUR点
        return EMS_utilization, EMS_posvec
