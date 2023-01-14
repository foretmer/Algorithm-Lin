from Coordinate import Coordinate
from Posture import Posture
from box.Box import Box


class Space:
    def __init__(self, x, y, z, l, w, h):
        self.position = Coordinate(x, y, z)
        self.l = l
        self.w = w
        self.h = h
        self.volume = l * w * h

        self.postures = []

    def find_available_postures(self, box: Box):
        self.postures = []
        if self.volume < box.volume:
            return []

        # 6种姿势
        self._add_posture_if_available(box.l, box.w, box.h) \
            ._add_posture_if_available(box.l, box.h, box.w) \
            ._add_posture_if_available(box.w, box.l, box.h) \
            ._add_posture_if_available(box.w, box.h, box.l) \
            ._add_posture_if_available(box.h, box.l, box.w) \
            ._add_posture_if_available(box.h, box.w, box.l)

        return self.postures

    def _add_posture_if_available(self, lay_l, lay_w, lay_h):
        if lay_l <= self.l and lay_w <= self.w and lay_h <= self.h:
            self.postures.append(Posture(lay_l, lay_w, lay_h))

        return self
