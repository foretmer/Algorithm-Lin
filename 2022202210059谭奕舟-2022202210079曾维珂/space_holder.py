from typing import Union

from box import Box
from coordinate import Coordinate
from dimension import Dimension

# holder is the descriptor of placed box
class Holder(Coordinate):
    def __init__(self, coordinate: Coordinate, box: Box, orientation:int = 0):
        
        Coordinate.__init__(self, coordinate.x, coordinate.y, coordinate.z)
        self.box = box
        self.orientation = orientation
    def get_width(self):
        if self.orientation == 0:
            return self.box.width
        else:
            return self.box.depth
    def get_depth(self):
        if self.orientation == 0:
            return self.box.depth
        else:
            return self.box.width
    def get_height(self):
        return self.box.height
    def __str__(self):
        return f'Holder [x = {self.x}, y = {self.y}, z={self.z}, width={self.get_width()}, depth={self.get_depth()}, ' \
               f'height={self.get_height()}]'
    
    def __repr__(self):
        return self.__str__()
        