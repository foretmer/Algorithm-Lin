from Box import Box
from Coordinate import Coordinate


class Space:
    def __init__(self, x, y, z, l, w, h):
        self.position = Coordinate(x, y, z)
        self.l = l
        self.w = w
        self.h = h
        self.volume = l * w * h

    def fit(self, box: Box):
        if self.volume < box.volume:
            return -1, -1, -1

        # 6种姿势
        if box.l <= self.l and box.w <= self.w and box.h <= self.h:
            return box.l, box.w, box.h

        if box.l <= self.l and box.h <= self.w and box.w <= self.h:
            return box.l, box.h, box.w

        if box.h <= self.l and box.w <= self.w and box.l <= self.h:
            return box.h, box.w, box.l

        if box.h <= self.l and box.l <= self.w and box.w <= self.h:
            return box.h, box.l, box.w

        if box.w <= self.l and box.l <= self.w and box.h <= self.h:
            return box.w, box.l, box.h

        if box.w <= self.l and box.h <= self.w and box.l <= self.h:
            return box.w, box.h, box.l

        return -1, -1, -1
