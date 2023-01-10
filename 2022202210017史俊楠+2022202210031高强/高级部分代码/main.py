from Initi_Car_box import *
import random
from packer import Packer
from bin import Bin
from item import Item
import time

def random_arrive_a_box(boxes):
    category = len(boxes)
    while True:
        index = random.randint(0, category - 1)
        if boxes[index][3] >= 1:
            boxes[index][3] -= 1
            return boxes[index]


if __name__ == '__main__':
    for j in range(1,25):
        car, boxes = init_car_box(j)
        packer = Packer()
        packer.add_bin(Bin('small-envelope', 587, 233, 220, 99999999))
        total_box_number = 0
        for box in boxes:
            total_box_number += box[3]
        print(total_box_number)
        for i in range(total_box_number):
            box = random_arrive_a_box(boxes)
            item = Item("hhhh"+str(i), box[0], box[1], box[2], 0)
            packer.add_item(item)
        tic = time.perf_counter()
        packer.pack()
        toc = time.perf_counter()
        print("第",j,f"该程序耗时: {toc - tic:0.4f} seconds","平均每个",(toc - tic)/total_box_number)
