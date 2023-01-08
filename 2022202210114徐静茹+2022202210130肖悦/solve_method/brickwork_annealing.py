from box import Box
from solve_method import brickwork

import random
import numpy as np
import time

# ref: http://www.jos.org.cn/1000-9825/18/2083.pdf（论文的算法2）

def get_scores(container, loaded_boxes):
  loaded_v = 0
  for (loaded_box, _, _, _) in loaded_boxes:
    loaded_v += loaded_box.l * loaded_box.w * loaded_box.h
  V = container[0] * container[1] * container[2]
  return loaded_v / V

def select(boxes_list):
  boxes_type_list = list(set([(b.x, b.y, b.z) for b in boxes_list]))
  boxes_type_list = sorted(boxes_type_list, key=lambda k: k[0]*k[1]*k[2], reverse=True)
  boxes_number_list = [0 for _ in boxes_type_list]
  for i in range(len(boxes_number_list)):
    for b in boxes_list:
      if (b.x, b.y, b.z) == (boxes_type_list[i][0], boxes_type_list[i][1], boxes_type_list[i][2]):
        boxes_number_list[i] += 1
  # 随机交换两类（注意不是个）盒子的顺序
  if random.random() >= 0.5:
    i, j = random.randint(0, len(boxes_type_list) - 1), random.randint(0, len(boxes_type_list) - 1)
    while i == j:
      i, j = random.randint(0, len(boxes_type_list) - 1), random.randint(0, len(boxes_type_list) - 1)
    boxes_type_list[i], boxes_type_list[j] = boxes_type_list[j], boxes_type_list[i]
    boxes_number_list[i], boxes_number_list[j] = boxes_number_list[j], boxes_number_list[i]
  # 交换某类箱子的任意两个尺寸
  else:
    i = random.randint(0, len(boxes_type_list) - 1)
    j = random.randint(0, 4) # 表示箱子的旋转次数，一定不会得到和目前相同的旋转方式
    b : Box = Box(boxes_type_list[i][0], boxes_type_list[i][1], boxes_type_list[i][2])
    for _ in range(j):
      b.revolve()
    boxes_type_list[i] = (b.x, b.y, b.z)
  boxes_list_neighbor = []
  for i in range(len(boxes_type_list)):
    (x, y, z) = boxes_type_list[i]
    number = boxes_number_list[i]
    for _ in range(number):
      boxes_list_neighbor.append(Box(x, y, z))
  assert(len(boxes_list_neighbor) == len(boxes_list))
  return boxes_list_neighbor


def solve(container, boxes_list, time_limit):
  # 预处理：按照体积大小排序，旋转满足z >= y >= x
  boxes_list = sorted(boxes_list, key=lambda b: b.x*b.y*b.z, reverse=True)
  boxes_list_t = list(boxes_list)
  b : Box
  for i, b in enumerate(boxes_list):
    while not (b.z >= b.y and b.y >= b.x):
      b.revolve()
    boxes_list_t[i] = b
  boxes_list = boxes_list_t

  # 
  setup_temperature = 1.0
  end_temperature = 0.01
  drop_rate = 0.9
  setup_domain_length = 0
  delta_domain_length = len(set([(b.x, b.y, b.z) for b in boxes_list]))
  boxes_list_best = boxes_list
  loaded_rate = get_scores(container, brickwork.solve(container, boxes_list, time_limit))
  f, f_best = loaded_rate, loaded_rate
  
  start_time = time.time()
  for i in range(1, 3):
    t, L_t = setup_temperature, setup_domain_length
    while t >= end_temperature and time.time() - start_time <= time_limit / 1000:
      for _ in range(L_t):
        if time.time() - start_time >= time_limit / 1000:
          break
        boxes_list_neighbor = select(boxes_list)
        f_neighor = get_scores(container, brickwork.solve(container, boxes_list_neighbor, time_limit))
        delta_f = f_neighor - f
        if delta_f > 0:
          f = f_neighor
          boxes_list = boxes_list_neighbor
          if f > f_best:
            f_best = f
            boxes_list_best = boxes_list
        else:
          x = random.random()
          if x < np.exp(10 * delta_f / t):
            f = f_neighor
            boxes_list = boxes_list_neighbor
      L_t += delta_domain_length
      t *= drop_rate
      drop_rate *= 0.8
  return brickwork.solve(container, boxes_list_best, time_limit)