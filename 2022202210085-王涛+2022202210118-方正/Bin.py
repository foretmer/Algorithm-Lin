from Common import *
from typing import Any, List, Tuple

import utils.axis_utils
import utils.math_utils

class Bin:
    def __init__(self, l:float, w:float, h:float, precision:int=PRECISION):
        self.l = l
        self.w = w
        self.h = h
        self.precision = precision
        self.priority = None

    def __str__(self):
        format_ctrl = "({{0:.{0}f}},{{1:.{0}f}},{{2:.{0}f}})".format(self.precision)
        return format_ctrl.format(self.l, self.w, self.h)

    def __repr__(self):
        format_ctrl = "[{{0:.{0}f}}({{3:d}}),{{1:.{0}f}}({{4:d}}),{{2:.{0}f}}({{5:d}})]".format(self.precision)
        return format_ctrl.format(self.l, self.w, self.h,
                                  self.length, self.width, self.height)

    @property
    def length(self):
        return utils.math_utils.to_precision(self.l, self.precision)

    @property 
    def width(self):
        return utils.math_utils.to_precision(self.w, self.precision)

    @property
    def height(self):
        return utils.math_utils.to_precision(self.h, self.precision)

    @property
    def size_list(self):
        return [self.length, self.width, self.height]
    
    @property
    def volume(self):
        return self.length * self.width * self.height

    def copy(self):
        return Bin(self.l, self.w, self.h, self.precision)
    
    def axis_sort(self, axises:Tuple[Axis, Axis, Axis], ascending:bool=True) -> bool:
        utils.axis_utils.valid_axis(axises)
        sorted_axises = sorted([self.l, self.w, self.h], reverse=(not ascending))
        self.l, self.w, self.h = utils.axis_utils.axis_to_lwh(sorted_axises, axises)

    def axis_transform(self, axises:Tuple[Axis, Axis, Axis]) -> bool:
        self.l, self.w, self.h = utils.axis_utils.lwh_to_axis([self.l, self.w, self.h], axises)

    def set_priority(self, priority:float) -> None:
        self.priority = priority
                
def sort_bins_by_priority(bins:List[Bin]) -> List[Bin]:
    bins.sort(key=lambda x: x.priority, reverse=True)
    return bins

       