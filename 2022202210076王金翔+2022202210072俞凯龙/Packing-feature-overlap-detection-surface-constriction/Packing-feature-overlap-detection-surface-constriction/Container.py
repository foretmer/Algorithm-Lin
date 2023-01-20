import time
from copy import deepcopy

from LayPoint import LayPoint
from VisualHelper import VisualHelper
from box.Box import Box


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
        self.local_fit_rate = 0

        self.boxes = []
        self.points = []

        # 限制面
        self.xy_plane = 0
        self.yz_plane = 0

        self.is_full = False

    def add_box_if_available(self, box: Box):
        lay_point = LayPoint()
        history_yz_plane = self.yz_plane
        history_xy_plane = self.xy_plane
        temp_box = deepcopy(box)

        def __is_plane_changed() -> bool:
            return (
                # 防止破坏已经确定可放置的点位, 即只能在(-1, -1, -1)基础上改
                not lay_point.is_valid and
                self.yz_plane == history_yz_plane and
                self.xy_plane == history_xy_plane
            )

        for point in self.points:
            # 同时满足xy，yz限制面约束
            if self._is_box_packable(temp_box, point) \
                    and point.x + temp_box.lay_l <= self.yz_plane \
                    and point.z + temp_box.lay_h <= self.xy_plane:
                lay_point = point
                break

        if not lay_point.is_valid:
            if len(self.boxes) == 0:
                lay_point = LayPoint(0, 0, 0)
                self.xy_plane = box.h
                self.yz_plane = box.l

            # 扩展xy限制面
            elif self.yz_plane == self.l or self.yz_plane == 0:
                # 可放置在xy限制面的原点
                if self._is_box_packable(temp_box, LayPoint(0, 0, self.xy_plane)):
                    lay_point = LayPoint(0, 0, self.xy_plane)
                    self.xy_plane += temp_box.lay_h
                    self.yz_plane = temp_box.lay_l
                # 箱子本身高度大于xy限制面
                elif self.xy_plane < temp_box.h:
                    self.xy_plane = self.h
                    self.yz_plane = self.l
                    # 调整限制面后待重装
                    if __is_plane_changed():
                        lay_point.z = 0
            else:
                for point in self.points:
                    # 扩展yz限制面
                    if self._is_box_packable(temp_box, point) \
                            and point.z + temp_box.lay_h <= self.xy_plane \
                            and point.x == self.yz_plane \
                            and point.y == 0:
                        lay_point = point
                        self.yz_plane += temp_box.lay_l
                        break

                if not lay_point.is_valid:
                    self.yz_plane = self.l
                    # 扩展yz限制面待重装
                    if __is_plane_changed():
                        lay_point.z = 0

        if lay_point.is_valid:
            box.pack(lay_point)
            self._move_box(box)
            self.boxes.append(box)

            # 更新放置点
            if box.lay_point in self.points:
                self.points.remove(box.lay_point)
            self.points.extend([LayPoint(box.lay_point.x + box.lay_l, box.lay_point.y, box.lay_point.z),
                                LayPoint(box.lay_point.x, box.lay_point.y + box.lay_w, box.lay_point.z),
                                LayPoint(box.lay_point.x, box.lay_point.y, box.lay_point.z + box.lay_h)])

            # 将放置点排序，优先选择z,x小的
            self.points.sort(key=lambda x: x.z)
            self.points.sort(key=lambda x: x.x)
            self.points.sort(key=lambda x: x.y)
            # 更新填充率
            self._update_used_volume(box)

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
        # if box.lay_point.x + box.lay_l > self.used_l:
        #     used_l = box.lay_point.x + box.lay_l
        # else:
        #     used_l = self.used_l
        #
        # if box.lay_point.y + box.lay_w > self.used_w:
        #     used_w = box.lay_point.y + box.lay_w
        # else:
        #     used_w = self.used_w
        #
        # if box.lay_point.z + box.lay_h > self.used_h:
        #     used_h = box.lay_point.z + box.lay_h
        # else:
        #     used_h = self.used_h

        self.used_volume += box.l * box.w * box.h

    def end(self, group="unknown", index="unknown"):
        print('fit rate: ' + str(self.used_volume / self.volume))
        # used_v = 0
        # for box in self.boxes:
        #     used_v += box.volume
        # print('fit rate: ' + str(used_v / self.volume)
        end_time = time.time()
        VisualHelper(self.boxes).display(group, index)
        return end_time
