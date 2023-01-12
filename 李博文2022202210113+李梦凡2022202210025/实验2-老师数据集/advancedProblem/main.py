import sys
sys.path.append("..")
from tools.container import Container
from tools.box import Box
from tools.generateBoxes import generateBoxes

import random
import numpy as np




def main():
    print("choose box type: ")
    print("type 1: 3种箱子")
    print("type 2: 5种箱子")
    print("type 3: 8种箱子")
    print("type 4: 10种箱子")
    print("type 5: 15种箱子")

    value = input('input a int:')
    # print(value)
    boxes = generateBoxes(int(value))
    
    totalBox = 0
    for box in boxes:
        totalBox += box.getVolumn()

    print('totalBox 体积', totalBox)
    container = Container()
    print('盒子总体积为容器总体积的多少倍', totalBox/container.getTotalCapacity())

    # 盒子随机顺序到达
    for i in range(len(boxes)):
        box = boxes[i]
        print('当前第{}盒子'.format(i)) #, box
        if box.getVolumn()<container.getRemainingCapacity():
            if not container.putBox_Advance(box):
                print("放置失败")
            else:
                print('放置成功，当前占用率', str(1- container.getRemainingCapacity()/container.getTotalCapacity()))

    print('最终占用率可以达到：', 1- container.getRemainingCapacity()/container.getTotalCapacity())

if __name__ == '__main__':
    main()