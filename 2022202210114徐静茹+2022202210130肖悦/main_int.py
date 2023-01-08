import pandas as pd
import numpy as np
import random
import os
import time
import argparse
from box import Box
from solve_method import brickwork, brickwork_annealing, ourmethod, ourmethod_annealing, random_place

def eval(file_path, method, time_limit):
  # 数据输入
  data = pd.read_csv(file_path)
  
  # 箱与盒
  container = data[data["label"] == "C"].loc[0, ["length", "width", "height"]].values
  boxes_list = []
  for _, row in data[data["label"] == "B"].iterrows():
    (l, w, h) = row[["length", "width", "height"]].values
    boxes_list.extend([Box(l, w, h) for _ in range(row["count"])])
  assert(len(boxes_list) == np.sum(data["count"].values) - 1)

  # 解题方法
  solve_time = time.time()
  # random.shuffle(boxes_list)
  if method == "brickwork":
    loaded_boxes = brickwork.solve(container, boxes_list, time_limit)
  elif method == "brickwork_annealing":
    loaded_boxes = brickwork_annealing.solve(container, boxes_list, time_limit)
  elif method == "ourmethod":
    loaded_boxes = ourmethod.solve(container, boxes_list, time_limit)
  elif method == "ourmethod_annealing":
    loaded_boxes = ourmethod_annealing.solve(container, boxes_list, time_limit)
  elif method == "random_place":
    loaded_boxes = random_place.solve(container, boxes_list, time_limit)
  solve_time = 1000 * (time.time() - solve_time)
  
  # 合法性检查
  # 将箱子看做一个三位数组，有盒子的地方则加1，查看是否存在大于1的地方，即发生碰撞
  container_array = np.zeros([container[0], container[1], container[2]])
  for (loaded_box, x, y, z) in loaded_boxes:
    assert(x >= 0 and loaded_box.x + x <= container[0])
    assert(y >= 0 and loaded_box.y + y <= container[1])
    assert(z >= 0 and loaded_box.z + z <= container[2])
    container_array[x:loaded_box.x+x, y:loaded_box.y+y, z:loaded_box.z+z] += 1
  assert(np.sum(container_array > 1) <= 0)

  # 结果评价
  loaded_v = 0
  for (loaded_box, _, _, _) in loaded_boxes:
    loaded_v += loaded_box.l * loaded_box.w * loaded_box.h
  V = container[0] * container[1] * container[2]
  return loaded_v / V, len(loaded_boxes) / len(boxes_list), solve_time, loaded_boxes

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--method", type=str, default="brickwork")
  parser.add_argument("--time_limit", type=float, default=10000000)
  args = parser.parse_args()

  method = args.method
  time_limit = args.time_limit

  for file_name in os.listdir("./dataset/"):
    if "-" in file_name and "E" in file_name and ".csv" in file_name:
      load_rate, _, solve_time, loaded_boxes = eval("./dataset/" + file_name, method, time_limit)
      f = open("result/" + method + "_" + str(time_limit) + ".txt", "a+")
      f.write("{}, {:.4f}, {:.0f}\n".format(file_name, load_rate, solve_time))
      f.close
      print("{}, {:.4f}, {:.0f}ms".format(file_name, load_rate, solve_time))
      # break # debug用的，只跑一个测例