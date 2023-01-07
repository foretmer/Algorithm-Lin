from typing import Union


class Dimension:
    def __init__(self,w: int=None, d: int=None, h: int=None):
        
        self.width = w
        self.depth = d
        self.height = h

        if d is None or w is None or h is None:
            self.volume = 0
        else:
            self.volume = d * w * h

    @staticmethod
    def cmp_floorspace(a, b):
        if a.get_floor_space() < b.get_floor_space():
            return 1
        elif a.get_floor_space() > b.get_floor_space():
            return -1
        return 0

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_depth(self):
        return self.depth

    def get_floor_space(self):
        return self.width * self.depth

    def get_volume(self):
        return self.volume

    def is_empty(self):
        return self.width <= 0 or self.depth <= 0 or self.height <= 0

    def __str__(self):
        return (f'Dimension [width={self.width}, depth={self.depth}, '
                f'height={self.height}, volume={self.volume}]')

    def __repr__(self):
        return self.__str__()




Dimension.EMPTY = Dimension(0, 0, 0)
