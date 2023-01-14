from enum import Enum

from LayPoint import LayPoint


class Posture(Enum):
    LWH = 0
    LHW = 1
    WLH = 2
    WHL = 3
    HLW = 4
    HWL = 5


class Box:
    def __init__(self, ID, type_id=-1, l=0, w=0, h=0):
        self.ID = ID
        self.type_id = type_id

        self.l = l
        self.w = w
        self.h = h
        self.volume = l * w * h
        # 初始保持原始姿势
        self.lay_l = l
        self.lay_w = w
        self.lay_h = h

        self.lay_point = LayPoint()
        self.is_packed = False

    def pack(self, point: LayPoint, posture: Posture):
        self.lay_point = point
        self.is_packed = True
        self.switch_posture(posture)

    def switch_posture(self, posture: Posture):
        if posture.value == Posture.LWH:
                self.lay_l, self.lay_w, self.lay_h = self.l, self.w, self.h
        if posture.value == Posture.LHW:
                self.lay_l, self.lay_w, self.lay_h = self.l, self.h, self.w
        if posture.value == Posture.WLH:
                self.lay_l, self.lay_w, self.lay_h = self.w, self.l, self.h
        if posture.value == Posture.WHL:
                self.lay_l, self.lay_w, self.lay_h = self.w, self.h, self.l
        if posture.value == Posture.HLW:
                self.lay_l, self.lay_w, self.lay_h = self.h, self.l, self.w
        if posture.value == Posture.HWL:
                self.lay_l, self.lay_w, self.lay_h = self.h, self.w, self.l

    def set_x(self, x):
        self.lay_point.x = x

    def set_y(self, y):
        self.lay_point.y = y

    def set_z(self, z):
        self.lay_point.z = z

    def is_overlap(self, other_box):
        return self._is_x_overlap(other_box) and self._is_y_overlap(other_box) and self._is_z_overlap(other_box)

    def is_xy_overlap(self, other_box):
        return self._is_x_overlap(other_box) and self._is_y_overlap(other_box)

    def is_xz_overlap(self, other_box):
        return self._is_x_overlap(other_box) and self._is_z_overlap(other_box)

    def is_yz_overlap(self, other_box):
        return self._is_y_overlap(other_box) and self._is_z_overlap(other_box)

    def _is_x_overlap(self, other_box):
        return other_box.lay_point.x + other_box.lay_l > self.lay_point.x \
               and other_box.lay_point.x < self.lay_point.x + self.lay_l

    def _is_y_overlap(self, other_box):
        return other_box.lay_point.y + other_box.lay_w > self.lay_point.y \
               and other_box.lay_point.y < self.lay_point.y + self.lay_w

    def _is_z_overlap(self, other_box):
        return other_box.lay_point.z + other_box.lay_h > self.lay_point.z \
               and other_box.lay_point.z < self.lay_point.z + self.lay_h

    def str(self):
        return str(self.ID) + "[" + str(self.type_id) + "]: " + "(" + str(self.l) + ',' + str(self.w) + ',' + str(
            self.h) + ')'
