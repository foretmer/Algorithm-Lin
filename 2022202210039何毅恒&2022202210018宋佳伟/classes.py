from copy import deepcopy
from enum import Enum
from typing import List


class Point(object):
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    # 用于print实例
    def __repr__(self):
        return f"({self.x},{self.y},{self.z})"

    # 判断实例是否相等
    def __eq__(self, __o: object):
        return self.x == __o.x and self.y == __o.y and self.z == __o.z

    # 加了@property后，可以用调用属性的形式来调用方法,后面不需要加（）
    @property
    def is_valid(self):
        return self.x >= 0 and self.y >= 0 and self.z >= 0


class BoxPose(Enum):
    tall_wide = 0
    tall_narrow = 1
    normal_wide = 2
    normal_narrow = 3
    short_wide = 4
    short_narrow = 5


class Box(object):
    def __init__(self, length: int, width: int, height: int):
        self._point = Point(-1, -1, -1)
        self._shape = [length, width, height]
        self._pose = BoxPose.tall_wide
        self._current_pose_weight = [0, 0, 0, 0, 0, 0]

    def __repr__(self):
        return f"{self.shape}".replace(", ", "-")

    @property
    def pose(self):
        return self._pose

    @pose.setter
    def pose(self, new_pose: BoxPose):
        self._pose = new_pose

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, new_point: Point):
        self._point = new_point

    @property
    def x(self):
        return self._point.x

    @x.setter
    def x(self, new_x: int):
        self._point = Point(new_x, self.y, self.z)

    @property
    def y(self):
        return self._point.y

    @y.setter
    def y(self, new_y: int):
        self._point = Point(self.x, new_y, self.z)

    @property
    def z(self):
        return self._point.z

    @z.setter
    def z(self, new_z: int):
        self._point = Point(self.z, self.y, new_z)

    @property
    def current_pose_weight(self):
        return self._current_pose_weight

    @current_pose_weight.setter
    def current_pose_weight(self, new_pose_weight: list[int]):
        self._current_pose_weight = new_pose_weight

    @property
    def length(self):
        return self.shape[0]

    @property
    def width(self):
        return self.shape[1]

    @property
    def height(self):
        return self.shape[-1]

    @property
    def shape(self):
        return self.update_shape[self._pose]

    @shape.setter
    def shape(self, length, width, height):
        self._shape = [length, width, height]

    @property
    def volume(self):
        return self._shape[0] * self._shape[1] * self._shape[2]

    @property
    def update_shape(self):
        sorted_shape = sorted(self._shape)
        return {
            BoxPose.tall_wide: (sorted_shape[0], sorted_shape[1], sorted_shape[2]),
            BoxPose.tall_narrow: (sorted_shape[1], sorted_shape[0], sorted_shape[2]),
            BoxPose.normal_wide: (sorted_shape[0], sorted_shape[2], sorted_shape[1]),
            BoxPose.normal_narrow: (sorted_shape[2], sorted_shape[0], sorted_shape[1]),
            BoxPose.short_wide: (sorted_shape[1], sorted_shape[2], sorted_shape[0]),
            BoxPose.short_narrow: (sorted_shape[2], sorted_shape[1], sorted_shape[0])
        }

    def get_shadow(self, planar: str):
        x0, y0, x1, y1 = 0, 0, 0, 0
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


class Container(object):
    def __init__(self, length: int, width: int, height: int):
        self._length = length
        self._width = width
        self._height = height
        # 分别初始化水平和垂直参考面
        self._horizontal_planar = 0
        self._vertical_planar = 0
        # 可放置点的有序集合
        self._available_points = [Point(0, 0, 0)]
        # 已成功装入的boxes
        self._loaded_boxes: List[Box] = []

    def __repr__(self):
        return f"{self._length}, {self._width}, {self._height}"

    @property
    def length(self):
        return self._length

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def volume(self):
        return self.height * self.length * self.width

    @property
    def size_list(self):
        return [self.length, self.width, self.height]

    def sort_available_points(self):
        self._available_points.sort(key=lambda x: x.z)
        self._available_points.sort(key=lambda x: x.x)
        self._available_points.sort(key=lambda x: x.y)

    def is_loadable(self, site: Point, box: Box):
        loadable = True
        temp_box = deepcopy(box)
        temp_box.point = site
        if (temp_box.x + temp_box.length > self.length or temp_box.y + temp_box.width > self.width
                or temp_box.z + temp_box.height > self.height):
            loadable = False
        for loaded_box in self._loaded_boxes:
            if _is_boxes_collide(temp_box, loaded_box):
                loadable = False
        return loadable

    def load(self, box: Box):
        # 放置坐标, 其中(-1, -1, 0)表示放置失败但调整参考面, (-1, -1, -1)表示放置失败
        current_point = Point(-1, -1, -1)
        # 执行前的参考面位置
        planar_before = [self._horizontal_planar, self._vertical_planar]

        for point in self._available_points:
            if (self.is_loadable(point, box) and point.x + box.length < self._horizontal_planar
                    and point.z + box.height < self._vertical_planar):
                current_point = point
                break
        if not current_point.is_valid:
            if self._horizontal_planar == 0 or self._horizontal_planar == self.length:
                if self.is_loadable(Point(0, 0, self._vertical_planar), box):
                    current_point = Point(0, 0, self._vertical_planar)
                    self._vertical_planar += box.height
                    self._horizontal_planar = box.length
                elif self._vertical_planar < self.height:
                    self._vertical_planar = self.height
                    self._horizontal_planar = self.length
                    if not (current_point.is_valid and self._horizontal_planar == planar_before[0]
                            and self._vertical_planar == planar_before[-1]):
                        # 放置失败,调整参考面
                        current_point.z == 0
            else:
                for point in self._available_points:
                    if (point.x == self._horizontal_planar and point.y == 0 and self.is_loadable(point, box)
                            and point.z + box.height <= self._vertical_planar):
                        current_point = point
                        self._horizontal_planar += box.length
                        break
                if not current_point.is_valid:
                    self._horizontal_planar = self.length
                    if (not current_point.is_valid and self._horizontal_planar == planar_before[0]
                            and self._vertical_planar == planar_before[-1]):
                        # 放置失败,调整参考面
                        current_point.z == 0
        if current_point.is_valid:
            box.point = current_point
            if current_point in self._available_points:
                self._available_points.remove(current_point)
            self.move_box(box)
            self._loaded_boxes.append(box)
            self._available_points.extend([Point(box.x + box.length, box.y, box.z),
                                           Point(box.x, box.y + box.width, box.z),
                                           Point(box.x, box.y, box.z + box.height)])
            self.sort_available_points()
        return current_point

    def move_box(self, box: Box):
        site = box.point
        temp_box = deepcopy(box)
        if not self.is_loadable(site, box):
            return
        site_list = [site.x, site.y, site.z]
        for site_idx in range(3):
            break_while = True
            while site_list[site_idx] > 1 and break_while:
                site_list[site_idx] -= 1
                temp_box.point = Point(site_list[0], site_list[1], site_list[2])
                for loaded_box in self._loaded_boxes:
                    if _is_boxes_collide(loaded_box, temp_box):
                        site_list[site_idx] += 1
                        break_while = False
                        break
        box.point = Point(site_list[0], site_list[1], site_list[2])

    def save_csv(self, boxes_list_name: str, boxes_list: str, occ_rate: str):
        with open(f"output.csv", 'a', encoding='utf-8') as csv_f:
            idx = 1
            csv_f.write(f"{boxes_list_name}_list,{boxes_list}\n")
            csv_f.write(f"{boxes_list_name}_occ_rate,{occ_rate}\n")
            for box in self._loaded_boxes:
                csv_f.write(f"{boxes_list_name},{idx},{box.x},{box.y},{box.z},")
                csv_f.write(f"{box.length},{box.width},{box.height},{box.pose}")
                pose_w = box.current_pose_weight
                for weight in pose_w:
                    csv_f.write(f",{weight}")
                csv_f.write(f"\n")
                idx += 1

    @property
    def loaded_boxes(self):
        return self._loaded_boxes


def _is_rectangles_overlap(rec1: tuple, rec2: tuple):
    return not (rec1[0] >= rec2[2] or rec1[1] >= rec2[3]
                or rec2[0] >= rec1[2] or rec2[1] >= rec1[3])


def _is_boxes_collide(box0: Box, box1: Box):
    return (_is_rectangles_overlap(box0.get_shadow("xy"), box1.get_shadow("xy"))
            and _is_rectangles_overlap(box0.get_shadow("yz"), box1.get_shadow("yz"))
            and _is_rectangles_overlap(box0.get_shadow("xz"), box1.get_shadow("xz")))
