from time import time
from typing import List
from _cargo import *
from copy import deepcopy


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
        self._setted_cargos : List[Cargo] = []
        self.plane_shadow = [[],[],[]] # 创建紧贴坐标面的cargo列表

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
        for setted_cargo in self._setted_cargos:
            if _is_cargos_collide(temp, setted_cargo):
                encasable = False
        return encasable

    def _encase(self, cargo: Cargo) -> Point:
        # flag存储放置位置, (-1, -1, 0)放置失败并调整参考面, (-1, -1, -1)放置失败.
        flag = Point(-1, -1, -1)  
        # 用于记录执行前的参考面位置, 便于后续比较
        history = [self._horizontal_planar, self._vertical_planar]
        def __is_planar_changed() -> bool:
            return (
                not flag.is_valid and # 防止破坏已经确定可放置的点位, 即只能在(-1, -1, -1)基础上改
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
                        flag.z == 0 # 放置失败并调整参考面
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
                        flag.z == 0 # 放置失败并调整参考面


        return flag

    def _extend_points(self,cargo,flag):
        if flag.is_valid:
            #print(flag)
            #print(cargo,'$$')
            cargo.point = flag
            #print(cargo,'^^')
            if flag in self._available_points:
                self._available_points.remove(flag)
            self._adjust_setting_cargo(cargo)
       #     self._setted_cargos.append(cargo)
            self._available_points.extend([
                Point(cargo.x + cargo.length, cargo.y, cargo.z),
                Point(cargo.x, cargo.y + cargo.width, cargo.z),
                Point(cargo.x, cargo.y, cargo.z + cargo.height)
            ])
            #若cargo贴着坐标面，则加入到各自的分组中
            if cargo.x == 0:
                self.plane_shadow[0].append(cargo) #yz面货物集合
            if cargo.y == 0:
                self.plane_shadow[1].append(cargo) #xz面货物集合
            if cargo.z == 0:
                self.plane_shadow[2].append(cargo) #xy面货物集合
            self._sort_available_points()

    def _adjust_setting_cargo(self, cargo: Cargo):
        site = cargo.point
        temp = deepcopy(cargo)
        if not self.is_encasable(site, cargo):
            return None
        xyz = [site.x, site.y, site.z] 
        # 序列化坐标以执行遍历递减操作, 减少冗余
        for i in range(3): # 012 分别表示 xyz
            is_continue = True
            while xyz[i] > 1 and is_continue:
                xyz[i] -= 1
                temp.point = Point(xyz[0], xyz[1], xyz[2])
                for setted_cargo in self._setted_cargos:
                    if not _is_cargos_collide(setted_cargo, temp):
                        continue
                    xyz[i] += 1
                    is_continue = False
                    break
        cargo.point = Point(xyz[0], xyz[1], xyz[2]) # 反序列化
    
    # 求出每一个cargo与三个平面投影面积重叠的和
    def rectangles_overlap_area_sum(self, cargo: Cargo):
        temp = deepcopy(cargo)
        area = 0
        for i in range(3):
            for j in range(len(self.plane_shadow[i])):
                plusarea = rectangles_overlap_area(self.plane_shadow[i][j], temp, i)
                area += plusarea
        return area



    def save_encasement_as_file(self):
        file = open(f"{int(time())}_encasement.csv",'w',encoding='utf-8')
        file.write(f"index,x,y,z,length,width,height\n")
        i = 1
        for cargo in self._setted_cargos:
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


def _is_rectangles_overlap(rec1:tuple, rec2:tuple) -> bool:
    return not (
        rec1[0] >= rec2[2] or rec1[1] >= rec2[3] or
        rec2[0] >= rec1[2] or rec2[1] >= rec1[3]
    )


def rectangles_overlap_area(cargo0:Cargo, cargo1:Cargo, opt):
    area = 0
    if opt == 0:
        rec0 = cargo0.get_shadow_of("yz")
        rec1 = cargo1.get_shadow_of("yz")
        if _is_rectangles_overlap(rec0, rec1):
            # 求重叠阴影面积
            area = area + min(abs(rec0[0]-rec1[2]),abs(rec0[2]-rec1[0])) * min(abs(rec0[1]-rec1[3]),abs(rec0[3]-rec1[1]))
    if opt == 1:
        rec0 = cargo0.get_shadow_of("xz")
        rec1 = cargo1.get_shadow_of("xz")
        if _is_rectangles_overlap(rec0, rec1):
            # 求重叠阴影面积
            area = area + min(abs(rec0[0]-rec1[2]),abs(rec0[2]-rec1[0])) * min(abs(rec0[1]-rec1[3]),abs(rec0[3]-rec1[1])) 
    if opt == 2:
        rec0 = cargo0.get_shadow_of("yz")
        rec1 = cargo1.get_shadow_of("yz")
        if _is_rectangles_overlap(rec0, rec1):
            # 求重叠阴影面积
            area = area + min(abs(rec0[0]-rec1[2]),abs(rec0[2]-rec1[0])) * min(abs(rec0[1]-rec1[3]),abs(rec0[3]-rec1[1]))   
    return area

    


def _is_cargos_collide(cargo0: Cargo, cargo1: Cargo) -> bool:
    return (
        _is_rectangles_overlap(cargo0.get_shadow_of("xy"), cargo1.get_shadow_of("xy")) and
        _is_rectangles_overlap(cargo0.get_shadow_of("yz"), cargo1.get_shadow_of("yz")) and
        _is_rectangles_overlap(cargo0.get_shadow_of("xz"), cargo1.get_shadow_of("xz"))
    )

