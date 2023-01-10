from Common import *
from typing import Any, List, Tuple

def valid_axis(axises:Tuple[Axis, Axis, Axis]):
    assert len(axises) == 3
    valid = False
    if Axis.LENGTH in axises and Axis.WIDTH in axises and Axis.HEIGHT in axises:
        valid = True
    return valid

def lwh_to_axis_map(axises:Tuple[Axis, Axis, Axis]) -> List[int]:
    axis_map = []
    for axis in axises:
        if axis == Axis.LENGTH:
            axis_map.append(0)
        if axis == Axis.WIDTH:
            axis_map.append(1)
        if axis == Axis.HEIGHT:
            axis_map.append(2)
    return axis_map

def axis_to_lwh_map(axises:Tuple[Axis, Axis, Axis]) -> List[int]:
    lwh_map = [None, None, None]
    for idx, axis in enumerate(axises):
        if axis == Axis.LENGTH:
            lwh_map[0] = idx
        if axis == Axis.WIDTH:
            lwh_map[1] = idx
        if axis == Axis.HEIGHT:
            lwh_map[2] = idx
    return lwh_map

def lwh_to_axis(lwh:Tuple[int,int,int], axises:Tuple[Axis, Axis, Axis]):
    axis_map = lwh_to_axis_map(axises)
    axis = []
    for one_axis_map in axis_map:
        axis.append(lwh[one_axis_map])
    return axis

def axis_to_lwh(axis:Tuple[int,int,int], axises:Tuple[Axis, Axis, Axis]):
    lwh_map = axis_to_lwh_map(axises)
    lwh = []
    for one_lwh_map in lwh_map:
        if one_lwh_map != None:
            lwh.append(axis[one_lwh_map])
        else:
            lwh.append(None)
    return lwh

def full_axis_type():
    return [(Axis.LENGTH, Axis.WIDTH, Axis.HEIGHT),
            (Axis.LENGTH, Axis.HEIGHT, Axis.WIDTH),
            (Axis.WIDTH, Axis.LENGTH, Axis.HEIGHT),
            (Axis.WIDTH, Axis.HEIGHT, Axis.LENGTH),
            (Axis.HEIGHT, Axis.LENGTH, Axis.WIDTH),
            (Axis.HEIGHT, Axis.WIDTH, Axis.LENGTH)]

def lwh_sort(lwh:Tuple[int,int,int]) -> Tuple[Axis, Axis, Axis]:
    lwh_sorted = sorted(enumerate(lwh), key=lambda x:x[1])
    axis_list = []
    for axis in lwh_sorted:
        if axis[0] == 0:
            axis_list.append(Axis.LENGTH)
        elif axis[0] == 1:
            axis_list.append(Axis.WIDTH)
        elif axis[0] == 2:
            axis_list.append(Axis.HEIGHT)
    return axis_list