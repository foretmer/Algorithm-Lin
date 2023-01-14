import time
from copy import deepcopy

from LayPoint import LayPoint
from VisualHelper import VisualHelper
from box.Box import Box, Posture


class Container:
    def __init__(self, l, w, h):
        self.l = l
        self.w = w
        self.h = h
        self.volume = l * w * h

        self.used_l = 0
        self.used_w = 0
        self.used_h = 0
        self.used_volume = 0

        self.boxes = []
        self.points = [LayPoint(0, 0, 0)]

        self.is_full = False

    def add_box_if_available(self, box: Box):
        lay_point = LayPoint()
        lay_posture = Posture.LWH
        best_local_fit_rate = 0

        for point in self.points:
            for name, member in Posture.__members__.items():
                temp_box = deepcopy(box)
                temp_box.switch_posture(member)
                if self._is_box_packable(temp_box, point):
                    # 挪动后比较局部填充率
                    temp_box.lay_point = point
                    moved_box = self._move_box(temp_box)
                    used_l, used_w, used_h, used_volume = self._update_used_volume(moved_box)
                    local_fit_rate = used_volume / (used_l * used_w * used_h)
                    if local_fit_rate > best_local_fit_rate:
                        lay_point = moved_box.lay_point
                        lay_posture = member
                        best_local_fit_rate = local_fit_rate

        if lay_point.is_valid:
            box.pack(lay_point, lay_posture)
            self.boxes.append(box)

            # 更新放置点
            if box.lay_point in self.points:
                self.points.remove(box.lay_point)
            self.points.extend([LayPoint(box.lay_point.x + box.lay_l, box.lay_point.y, box.lay_point.z),
                                LayPoint(box.lay_point.x, box.lay_point.y + box.lay_w, box.lay_point.z),
                                LayPoint(box.lay_point.x, box.lay_point.y, box.lay_point.z + box.lay_h)])

            # 更新填充率
            self.used_l, self.used_w, self.used_h, self.used_volume = self._update_used_volume(box)

        return lay_point

    # todo 挪动顺序可优化
    def _move_box(self, box: Box):
        nearest_box_x_edge, nearest_box_y_edge, nearest_box_z_edge = 0, 0, 0
        temp_box = deepcopy(box)

        # 尝试向x轴负方向挪动
        for packed_box in self.boxes:
            if temp_box.is_yz_overlap(packed_box):
                packed_box_x_edge = packed_box.lay_point.x + packed_box.lay_l
                if packed_box_x_edge == temp_box.lay_point.x:
                    nearest_box_x_edge = packed_box_x_edge
                    break
                elif temp_box.lay_point.x > packed_box_x_edge > nearest_box_x_edge:
                    nearest_box_x_edge = packed_box_x_edge

        temp_box.set_x(nearest_box_x_edge)

        # 尝试向y轴负方向挪动
        for packed_box in self.boxes:
            if temp_box.is_xz_overlap(packed_box):
                packed_box_y_edge = packed_box.lay_point.y + packed_box.lay_w
                if packed_box_y_edge == temp_box.lay_point.y:
                    nearest_box_y_edge = packed_box_y_edge
                    break
                elif temp_box.lay_point.y > packed_box_y_edge > nearest_box_y_edge:
                    nearest_box_y_edge = packed_box_y_edge

        temp_box.set_y(nearest_box_y_edge)

        # 尝试向z轴负方向挪动
        for packed_box in self.boxes:
            if temp_box.is_xy_overlap(packed_box):
                packed_box_z_edge = packed_box.lay_point.z + packed_box.lay_h
                if packed_box_z_edge == temp_box.lay_point.z:
                    nearest_box_z_edge = packed_box_z_edge
                    break
                elif temp_box.lay_point.z > packed_box_z_edge > nearest_box_z_edge:
                    nearest_box_z_edge = packed_box_z_edge

        box.lay_point = LayPoint(nearest_box_x_edge, nearest_box_y_edge, nearest_box_z_edge)
        return box

    def _is_box_packable(self, box: Box, point: LayPoint):
        temp_box = deepcopy(box)
        temp_box.lay_point = point

        # 检测是否和已有箱子重叠
        for packed_box in self.boxes:
            if temp_box.is_overlap(packed_box):
                return False

        # 检测是否满足容器约束
        if temp_box.lay_point.x + temp_box.lay_l <= self.l \
                and temp_box.lay_point.z + temp_box.lay_h <= self.h \
                and temp_box.lay_point.y + temp_box.lay_w <= self.w:
            return True

        return False

    def _update_used_volume(self, box):
        if box.lay_point.x + box.lay_l > self.used_l:
            used_l = box.lay_point.x + box.lay_l
        else:
            used_l = self.used_l

        if box.lay_point.y + box.lay_w > self.used_w:
            used_w = box.lay_point.y + box.lay_w
        else:
            used_w = self.used_w

        if box.lay_point.z + box.lay_h > self.used_h:
            used_h = box.lay_point.z + box.lay_h
        else:
            used_h = self.used_h

        used_volume = self.used_volume + box.l * box.w * box.h
        return used_l, used_w, used_h, used_volume

    def end(self, group="unknown", index="unknown"):
        print('fit rate: ' + str(self.used_volume / self.volume))
        # used_v = 0
        # for box in self.boxes:
        #     used_v += box.volume
        # print('fit rate: ' + str(used_v / self.volume)
        end_time = time.time()
        VisualHelper(self.boxes).display(group, index)
        return end_time
