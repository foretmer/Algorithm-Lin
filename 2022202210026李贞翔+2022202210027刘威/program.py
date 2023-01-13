# 使用python实现动态装箱问题
# 算法前提：1.在线算法，箱子是按照一定顺序到达，先到达先摆放，使用第16行的标志位标志箱子到来顺序，默认是按固定顺序到达
#         2.每个箱子有3种不同的摆放状态，优先大的面摆放
# Author: 2022202210027 刘威，2022202210026 李贞翔
# 算法效果：在箱子种类较少时，使用固定次序到达的空间使用率在80%左右，随机次序在75%左右
#         在箱子种类较多时，使用固定次序到达的空间使用率在70%左右，随机次序在65%左右
import random
from enum import Enum
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from time import time
from typing import List, Iterable
from copy import deepcopy

# 使用随机队列标志，0为固定顺序到达，1为随机顺序到达
random_flag = 0
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']
fig: Figure = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
ax.view_init(elev=20, azim=40)
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
color_dict = {0: plt.get_cmap("Purples"), 1: plt.get_cmap("Greys"), 2: plt.get_cmap("Blues"),
              3: plt.get_cmap("Greens"), 4: plt.get_cmap("Oranges"), 5: plt.get_cmap("Reds"),
              6: plt.get_cmap("BuGn"), 7: plt.get_cmap("BuPu"), 8: plt.get_cmap("OrRd"),
              9: plt.get_cmap("GnBu"), 10: plt.get_cmap("YlGnBu"), 11: plt.get_cmap("PuBuGn"),
              12: plt.get_cmap("YlOrBr"), 13: plt.get_cmap("YlOrRd"), 14: plt.get_cmap("PuRd"), }
norm = plt.Normalize(vmin=15, vmax=20)


class CargoPose(Enum):
    """货物六种摆放的方式"""
    tall_wide = 1
    tall_thin = 2
    mid_wide = 3
    mid_thin = 4
    short_wide = 5
    short_thin = 6






class Point(object):
    """货物最靠近原点的顶点坐标"""

    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"({self.x},{self.y},{self.z})"

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y and self.z == __o.z

    @property
    def is_valid(self) -> bool:
        return self.x >= 0 and self.y >= 0 and self.z >= 0

    @property
    def tuple(self) -> tuple:
        return self.x, self.y, self.z


class Cargo(object):
    """表示一个货物"""

    def __init__(self, length: int, width: int, height: int, type: int) -> None:
        self._point = Point(-1, -1, -1)
        self._shape = {length, width, height}
        self._pose = CargoPose.short_thin
        self._type = type

    def __repr__(self) -> str:
        return f"{self._point} {self.shape}"

    def type(self) -> int:
        return self._type

    @property
    def pose(self) -> CargoPose:
        return self._pose

    @pose.setter
    def pose(self, new_pose: CargoPose):
        self._pose = new_pose

    @property
    def _shape_switch(self) -> dict:
        edges = sorted(self._shape)
        return {
            CargoPose.tall_thin: (edges[1], edges[0], edges[-1]),
            CargoPose.tall_wide: (edges[0], edges[1], edges[-1]),
            CargoPose.mid_thin: (edges[-1], edges[0], edges[1]),
            CargoPose.mid_wide: (edges[0], edges[-1], edges[-1]),
            CargoPose.short_thin: (edges[-1], edges[1], edges[0]),
            CargoPose.short_wide: (edges[1], edges[-1], edges[0])
        }

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, new_point: Point):
        self._point = new_point

    @property
    def x(self) -> int:
        return self._point.x

    @x.setter
    def x(self, new_x: int):
        self._point = Point(new_x, self.y, self.z)

    @property
    def y(self) -> int:
        return self._point.y

    @y.setter
    def y(self, new_y: int):
        self._point = Point(self.x, new_y, self.z)

    @property
    def z(self) -> int:
        return self._point.z

    @z.setter
    def z(self, new_z: int):
        self._point = Point(self.z, self.y, new_z)

    @property
    def length(self) -> int:
        return self.shape[0]

    @property
    def width(self) -> int:
        return self.shape[1]

    @property
    def height(self) -> int:
        return self.shape[-1]

    def get_shadow_of(self, planar: str) -> tuple:
        if planar in ("xy", "yx"):
            x0, y0 = self.x, self.y
            x1, y1 = self.x + self.length, self.y + self.width
        elif planar in ("xz", "zx"):
            x0, y0 = self.x, self.z
            x1, y1 = self.x + self.length, self.z + self.height
        elif planar in ("yz", "zy"):
            x0, y0 = self.y, self.z
            x1, y1 = self.y + self.width, self.z + self.height
        return x0, y0, x1, y1

    @property
    def shape(self) -> tuple:
        return self._shape_switch[self._pose]

    @shape.setter
    def shape(self, length, width, height):
        self._shape = {length, width, height}

    @property
    def volume(self) -> int:
        result = 1
        for i in self._shape:
            result *= i
        return result


def gen_cargoes(cargo_list: list):
    """
    箱子序列生成函数
    :param cargo_list:
    :return:cargo_num为各类箱子数量，cargoes_list为箱子列表
    """
    cargo_num = []
    cargoes_list = [Cargo(cargo_list[0][0], cargo_list[0][1], cargo_list[0][2], 0, ) for _ in range(cargo_list[0][-1])]
    for i in range(1, len(cargo_list)):
        cargoes_list.extend(
            [Cargo(cargo_list[i][0], cargo_list[i][1], cargo_list[i][2], i) for _ in range(cargo_list[i][-1])])

    for k in range(len(cargo_list)):
        cargo_num.append(cargo_list[k][-1])
    return cargoes_list, cargo_num


class Container(object):
    def __init__(self, length: int, width: int, height: int) -> None:
        self._length = length
        self._width = width
        self._height = height
        self._refresh()

    def __repr__(self) -> str:
        return f"{self._length}, {self._width}, {self._height}"

    def _refresh(self):
        self._horizontal_planar = 0  # 水平放置参考面
        self._vertical_planar = 0  # 垂直放置参考面
        self._available_points = [Point(0, 0, 0)]  # 可放置点有序集合
        self._setted_cargoes: List[Cargo] = []

    def _sort_available_points(self):
        self._available_points.sort(key=lambda x: x.z)
        self._available_points.sort(key=lambda x: x.x)
        self._available_points.sort(key=lambda x: x.y)

    def is_encasable(self, site: Point, cargo: Cargo) -> bool:
        encasable = True
        temp = deepcopy(cargo)
        temp.point = site
        if (
                temp.x + temp.length > self.length or
                temp.y + temp.width > self.width or
                temp.z + temp.height > self.height
        ):
            encasable = False
        for setted_cargo in self._setted_cargoes:
            if _is_cargoes_collide(temp, setted_cargo):
                encasable = False
        return encasable

    def _encase(self, cargo: Cargo) -> Point:
        # flag存储放置位置, (-1, -1, 0)放置失败并调整参考面, (-1, -1, -1)放置失败.
        flag = Point(-1, -1, -1)
        # 用于记录执行前的参考面位置, 便于后续比较
        history = [self._horizontal_planar, self._vertical_planar]

        def __is_planar_changed() -> bool:
            return (
                    not flag.is_valid and  # 防止破坏已经确定可放置的点位, 即只能在(-1, -1, -1)基础上改
                    self._horizontal_planar == history[0] and
                    self._vertical_planar == history[-1]
            )

        for point in self._available_points:
            if (
                    self.is_encasable(point, cargo) and
                    point.x + cargo.length < self._horizontal_planar and
                    point.z + cargo.height < self._vertical_planar
            ):
                flag = point
                break
        if not flag.is_valid:
            if (
                    self._horizontal_planar == 0 or
                    self._horizontal_planar == self.length
            ):
                if self.is_encasable(Point(0, 0, self._vertical_planar), cargo):
                    flag = Point(0, 0, self._vertical_planar)
                    self._vertical_planar += cargo.height
                    self._horizontal_planar = cargo.length
                    # 放置了货物 不检测参考面改变
                elif self._vertical_planar < self.height:
                    self._vertical_planar = self.height
                    self._horizontal_planar = self.length
                    if __is_planar_changed():
                        flag.z == 0  # 放置失败并调整参考面
            else:
                for point in self._available_points:
                    if (
                            point.x == self._horizontal_planar and
                            point.y == 0 and
                            self.is_encasable(point, cargo) and
                            point.z + cargo.height <= self._vertical_planar
                    ):
                        flag = point
                        self._horizontal_planar += cargo.length
                        break
                        # 放置了货物 不检测参考面改变
                if not flag.is_valid:
                    self._horizontal_planar = self.length
                    if __is_planar_changed():
                        flag.z == 0  # 放置失败并调整参考面
        if flag.is_valid:
            cargo.point = flag
            if flag in self._available_points:
                self._available_points.remove(flag)
            self._adjust_setting_cargo(cargo)
            self._setted_cargoes.append(cargo)
            self._available_points.extend([
                Point(cargo.x + cargo.length, cargo.y, cargo.z),
                Point(cargo.x, cargo.y + cargo.width, cargo.z),
                Point(cargo.x, cargo.y, cargo.z + cargo.height)
            ])
            self._sort_available_points()
        return flag

    def _adjust_setting_cargo(self, cargo: Cargo):
        site = cargo.point
        temp = deepcopy(cargo)
        if not self.is_encasable(site, cargo):
            return None
        xyz = [site.x, site.y, site.z]
        # 序列化坐标以执行遍历递减操作, 减少冗余
        for i in range(3):  # 012 分别表示 xyz
            is_continue = True
            while xyz[i] > 1 and is_continue:
                xyz[i] -= 1
                temp.point = Point(xyz[0], xyz[1], xyz[2])
                for setted_cargo in self._setted_cargoes:
                    if not _is_cargoes_collide(setted_cargo, temp):
                        continue
                    xyz[i] += 1
                    is_continue = False
                    break
        cargo.point = Point(xyz[0], xyz[1], xyz[2])  # 反序列化

    def save_encasement_as_file(self):
        file = open(f"{int(time())}_encasement.csv", 'w', encoding='utf-8')
        file.write(f"index,x,y,z,length,width,height\n")
        i = 1
        for cargo in self._setted_cargoes:
            file.write(f"{i},{cargo.x},{cargo.y},{cargo.z},")
            file.write(f"{cargo.length},{cargo.width},{cargo.height}\n")
            i += 1
        file.write(f"container,,,,{self}\n")
        file.close()

    @property
    def length(self) -> int:
        return self._length

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def volume(self) -> int:
        return self.height * self.length * self.width

    @property
    def setted_cargoes(self):
        return self._setted_cargoes


def _is_rectangles_overlap(rec1: tuple, rec2: tuple) -> bool:
    return not (
            rec1[0] >= rec2[2] or rec1[1] >= rec2[3] or
            rec2[0] >= rec1[2] or rec2[1] >= rec1[3]
    )


def _is_cargoes_collide(cargo0: Cargo, cargo1: Cargo) -> bool:
    return (
            _is_rectangles_overlap(cargo0.get_shadow_of("xy"), cargo1.get_shadow_of("xy")) and
            _is_rectangles_overlap(cargo0.get_shadow_of("yz"), cargo1.get_shadow_of("yz")) and
            _is_rectangles_overlap(cargo0.get_shadow_of(
                "xz"), cargo1.get_shadow_of("xz"))
    )


def draw_result(setted_container: Container):
    plt.gca().set_box_aspect((
        setted_container.length,
        setted_container.width,
        setted_container.height
    ))
    _draw_container(setted_container)
    for cargo in setted_container.setted_cargoes:
        _draw_cargo(cargo)
    plt.title('PackingResult')
    plt.show()


def _draw_container(container: Container):
    _plot_linear_cube(
        0, 0, 0,
        container.length,
        container.width,
        container.height
    )


def _draw_cargo(cargo: Cargo):
    _plot_opaque_cube(
        cargo.x, cargo.y, cargo.z,
        cargo.length, cargo.width, cargo.height, cargo
    )


def _plot_opaque_cube(x, y, z, dx, dy, dz, cargo):
    xx = np.linspace(x, x + dx, 2)
    yy = np.linspace(y, y + dy, 2)
    zz = np.linspace(z, z + dz, 2)
    xx2, yy2 = np.meshgrid(xx, yy)
    ax.plot_surface(xx2, yy2, np.full_like(xx2, z), cmap=color_dict[cargo.type()], norm=norm)
    ax.plot_surface(xx2, yy2, np.full_like(xx2, z + dz), cmap=color_dict[cargo.type()], norm=norm)
    yy2, zz2 = np.meshgrid(yy, zz)
    ax.plot_surface(np.full_like(yy2, x), yy2, zz2, cmap=color_dict[cargo.type()], norm=norm)
    ax.plot_surface(np.full_like(yy2, x + dx), yy2, zz2, cmap=color_dict[cargo.type()], norm=norm)
    xx2, zz2 = np.meshgrid(xx, zz)
    ax.plot_surface(xx2, np.full_like(yy2, y), zz2, cmap=color_dict[cargo.type()], norm=norm)
    ax.plot_surface(xx2, np.full_like(yy2, y + dy), zz2, cmap=color_dict[cargo.type()], norm=norm)


def _plot_linear_cube(x, y, z, dx, dy, dz, color='red'):
    # ax = Axes3D(fig)
    xx = [x, x, x + dx, x + dx, x]
    yy = [y, y + dy, y + dy, y, y]
    kwargs = {'alpha': 1, 'color': color}
    ax.plot3D(xx, yy, [z] * 5, **kwargs)
    ax.plot3D(xx, yy, [z + dz] * 5, **kwargs)
    ax.plot3D([x, x], [y, y], [z, z + dz], **kwargs)
    ax.plot3D([x, x], [y + dy, y + dy], [z, z + dz], **kwargs)
    ax.plot3D([x + dx, x + dx], [y + dy, y + dy], [z, z + dz], **kwargs)
    ax.plot3D([x + dx, x + dx], [y, y], [z, z + dz], **kwargs)


def encase_cargoes(
        cargoes: Iterable,
        container: Container,
        num: list
) -> float:
    random_cargoes = cargoes
    if random_flag == 1:
        random.shuffle(random_cargoes)
    sorted_cargoes: List[Cargo] = random_cargoes
    i = 0  # 记录发当前货物
    while i < len(sorted_cargoes):
        j = 0  # 记录当前摆放方式
        cargo = sorted_cargoes[i]
        poses = list(CargoPose)
        while j < len(poses):
            cargo.pose = poses[j]
            is_encased = container._encase(cargo)
            if is_encased.is_valid:
                break  # 可以装入 不在考虑后续摆放方式
            j += 1  # 不可装入 查看下一个摆放方式
        if is_encased.is_valid:
            num[cargo.type()] -= 1
            i += 1  # 成功放入 继续装箱
        elif is_encased == Point(-1, -1, 0):
            continue  # 没放进去但是修改了参考面位置 重装
        else:
            i += 1  # 跳过看下一个箱子
    print("""------------各类箱子剩余数量----------""")
    print(num)
    return sum(list(map(
        lambda cargo: cargo.volume, container.setted_cargoes
    ))) / container.volume


if __name__ == "__main__":
    # 测试集E1-1
    ls1 = [(108, 76, 30, 40), (110, 43, 25, 33), (92, 81, 55, 39)]
    # 测试集E1-2
    ls2 = [(91, 54, 45, 32), (105, 77, 72, 24), (79, 78, 48, 30)]
    # 测试集E1-3
    ls3 = [(91, 54, 45, 32), (105, 77, 72, 24), (79, 78, 48, 30)]
    # 测试集E1-4
    ls4 = [(60, 40, 32, 64), (98, 75, 55, 40), (60, 59, 39, 64)]
    # 测试集E1-5
    ls5 = [(78, 37, 27, 63), (89, 70, 25, 52), (90, 84, 41, 55)]
    # 测试集E2-1
    ls6 = [(108, 76, 30, 24), (110, 43, 25, 7), (92, 81, 55, 22), (81, 33, 28, 13), (120, 99, 73, 15)]
    # 测试集E2-2
    ls7 = [(49, 25, 21, 22), (60, 51, 41, 22), (103, 76, 64, 28), (95, 70, 62, 25), (111, 49, 26, 17)]
    # 测试集E2-3
    ls8 = [(88, 54, 39, 25), (94, 54, 36, 27), (87, 77, 43, 21), (100, 80, 72, 20), (83, 40, 36, 24)]
    # 测试集E2-4
    ls9 = [(90, 70, 63, 16), (84, 78, 28, 28), (94, 85, 39, 20), (80, 76, 54, 23), (69, 50, 45, 31)]
    # 测试集E2-5
    ls10 = [(74, 63, 61, 22), (71, 60, 25, 12), (106, 80, 59, 25), (109, 76, 42, 24), (118, 56, 22, 11)]
    # 测试集E3-1
    ls11 = [(108, 76, 30, 24), (110, 43, 25, 9), (92, 81, 55, 8), (81, 33, 28, 11),
            (120, 99, 73, 11), (111, 70, 48, 10), (98, 72, 46, 12), (95, 66, 31, 9)]
    # 测试集E3-2
    ls12 = [(97, 81, 27, 10), (102, 78, 39, 20), (113, 46, 36, 18), (66, 50, 42, 21),
            (101, 30, 26, 16), (100, 56, 35, 17), (91, 50, 40, 22), (106, 61, 56, 19)]
    # 测试集E3-3
    ls13 = [(88, 54, 39, 16), (94, 54, 36, 14), (87, 77, 43, 20), (100, 80, 72, 16),
            (83, 40, 36, 6), (91, 54, 22, 15), (109, 58, 54, 17), (94, 55, 30, 9)]
    # 测试集E3-4
    ls14 = [(49, 25, 21, 16), (60, 51, 41, 8), (103, 76, 64, 16), (95, 70, 62, 18),
            (111, 49, 26, 18), (85, 84, 72, 16), (48, 36, 31, 17), (86, 76, 38, 6)]
    # 测试集E3-5
    ls15 = [(113, 92, 33, 23), (52, 37, 28, 22), (57, 33, 29, 26), (99, 37, 30, 17),
            (92, 64, 33, 23), (119, 59, 39, 26), (54, 52, 49, 18), (75, 45, 35, 30)]
    # 测试集E4-1
    ls16 = [(49, 25, 21, 13), (60, 51, 41, 9), (103, 76, 64, 11), (95, 70, 62, 14), (111, 49, 26, 13),
            (85, 84, 72, 16), (48, 36, 31, 12), (86, 76, 38, 11), (71, 48, 47, 16), (90, 43, 33, 8)]
    # 测试集E4-2
    ls17 = [(97, 81, 27, 8), (102, 78, 39, 16), (113, 46, 36, 12), (66, 50, 42, 12), (101, 30, 26, 18),
            (100, 56, 35, 13), (91, 50, 40, 14), (106, 61, 56, 17), (103, 63, 58, 12), (75, 57, 41, 13)]
    # 测试集E4-3
    ls18 = [(86, 84, 45, 18), (81, 45, 34, 19), (70, 54, 37, 13), (71, 61, 52, 16), (78, 73, 40, 10),
            (69, 63, 46, 13), (72, 67, 56, 10), (75, 75, 36, 8), (94, 88, 50, 12), (65, 51, 50, 13)]
    # 测试集E4-4
    ls19 = [(113, 92, 33, 15), (52, 37, 28, 17), (57, 33, 29, 17), (99, 37, 30, 19), (92, 64, 33, 13),
            (119, 59, 39, 19), (54, 52, 49, 13), (75, 45, 35, 21), (79, 68, 44, 13), (116, 49, 47, 22)]
    # 测试集E4-5
    ls20 = [(118, 79, 51, 16), (86, 32, 31, 8), (64, 58, 52, 14), (42, 42, 32, 14), (64, 55, 43, 16), (84, 70, 35, 10),
            (76, 57, 36, 14), (95, 60, 55, 14), (80, 66, 52, 14), (109, 73, 23, 18)]
    # 测试集E5-1
    ls21 = [(98, 73, 44, 6), (60, 60, 38, 7), (105, 73, 60, 10), (90, 77, 52, 3), (66, 58, 24, 5), (106, 76, 55, 10),
            (55, 44, 36, 12), (82, 58, 23, 7), (74, 61, 58, 6), (81, 39, 24, 8), (71, 65, 39, 11), (105, 97, 47, 4),
            (114, 97, 69, 5), (103, 78, 55, 6), (93, 66, 55, 6)]
    # 测试集E5-2
    ls22 = [(108, 76, 30, 12), (110, 43, 25, 12), (92, 81, 55, 6), (81, 33, 28, 9), (120, 99, 73, 5), (111, 70, 48, 12),
            (98, 72, 46, 9), (95, 66, 31, 10), (85, 84, 30, 8), (71, 32, 25, 3), (36, 34, 25, 10), (97, 67, 62, 7),
            (33, 25, 23, 7), (95, 27, 26, 10), (94, 81, 44, 9)]
    # 测试集E5-3
    ls23 = [(49, 25, 21, 13), (60, 51, 41, 9), (103, 76, 64, 8), (95, 70, 62, 6), (111, 49, 26, 10), (74, 42, 40, 4),
            (85, 84, 72, 10), (48, 36, 31, 10), (86, 76, 38, 12), (71, 48, 47, 14), (90, 43, 33, 9), (98, 52, 44, 9),
            (73, 37, 23, 10), (61, 48, 39, 14), (75, 75, 63, 11)]
    # 测试集E5-4
    ls24 = [(97, 81, 27, 6), (102, 78, 39, 6), (113, 46, 36, 15), (66, 50, 42, 8), (101, 30, 26, 6), (100, 56, 35, 7),
            (91, 50, 40, 12), (106, 61, 56, 10), (103, 63, 58, 8), (75, 57, 41, 11), (71, 68, 64, 6), (85, 67, 39, 14),
            (97, 63, 56, 9), (61, 48, 30, 11), (80, 54, 35, 9)]
    # 测试集E5-5
    ls25 = [(113, 92, 33, 8), (52, 37, 28, 12), (57, 33, 29, 5), (99, 37, 30, 12), (92, 64, 33, 9), (119, 59, 39, 12),
            (54, 52, 49, 8), (75, 45, 35, 6), (79, 68, 44, 12), (116, 49, 47, 9), (83, 44, 23, 11), (98, 96, 56, 10),
            (78, 72, 57, 8), (98, 88, 47, 9), (41, 33, 31, 13)]

    cargoes, num = gen_cargoes(ls4)
    print("现有各类箱子数量\n{}".format(num))
    case = Container(587, 233, 220)
    final_result = encase_cargoes(cargoes, case, num)
    print("the space usage is:")
    print('{:.4%}'.format(final_result))
    case.save_encasement_as_file()
    draw_result(case)
