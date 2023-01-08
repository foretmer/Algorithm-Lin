from box import Box

import random

def if_could_place(b_min_x, b_min_y, b_min_z, b:Box, loaded_boxes_list, container):
  if_could_place = True
  b_max_x = b.x + b_min_x
  b_max_y = b.y + b_min_y
  b_max_z = b.z + b_min_z

  # 超出容器范围
  L, W, H = container[0], container[1], container[2]
  if b_max_x > L or b_max_y > W or b_max_z > H:
    return False
  
  # 与其他已经放置的物品相碰撞
  x_intersection, y_intersection, z_intersection = -1, -1, -1
  for (loaded_box, min_x, min_y, min_z) in loaded_boxes_list:
    max_x = loaded_box.x + min_x
    max_y = loaded_box.y + min_y
    max_z = loaded_box.z + min_z
    # 计算每个维度的重合的比例，若所有维度均有重合且比例大于0，那么认为碰撞
    # x-axis
    x_intersection = -1
    if b_min_x >= min_x and b_min_x <= max_x:
      x_intersection = min(max_x, b_max_x) - b_min_x
    elif min_x >= b_min_x and min_x <= b_max_x:
      x_intersection = min(max_x, b_max_x) - min_x
    # y-axis
    y_intersection = -1
    if b_min_y >= min_y and b_min_y <= max_y:
      y_intersection = min(max_y, b_max_y) - b_min_y
    elif min_y >= b_min_y and min_y <= b_max_y:
      y_intersection = min(max_y, b_max_y) - min_y
    # z-axis
    z_intersection = -1
    if b_min_z >= min_z and b_min_z <= max_z:
      z_intersection = min(max_z, b_max_z) - b_min_z
    elif min_z >= b_min_z and min_z <= b_max_z:
      z_intersection = min(max_z, b_max_z) - min_z
    if x_intersection > 0 and y_intersection > 0 and z_intersection > 0:
      if_could_place = False
  return if_could_place

def solve(container, boxes_list, time_limit):
  I = [(0, 0, 0)]
  loaded_boxes_list = []

  i = 0
  while i < len(boxes_list):
    b:Box = boxes_list[i]
    flag = False
    for (x, y, z) in I:
      if if_could_place(x, y, z, b, loaded_boxes_list, container):
        flag = True
        break
    if flag:
      I.remove((x, y, z))
      loaded_boxes_list.append((b, x, y, z))
      I.extend([(x + b.x, y, z), (x, y + b.y, z), (x, y, z + b.z)])
      random.shuffle(I)
    i += 1
  return loaded_boxes_list