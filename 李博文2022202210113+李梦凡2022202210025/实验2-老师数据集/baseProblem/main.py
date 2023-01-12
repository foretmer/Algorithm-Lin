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
    # print(boxes)
    # for box in boxes:
    #     print(box)
    # 根据最大面降序排列（先放最大的）
    # def key(a):     
        # return -np.sum(a.getMaxSurface())
        
    # 根据最大高度排序（先放最高的）
    def key(a):
        return -np.sum(a.getMaxH())


    boxes.sort(key=key)

    container = Container()
    curUsedCapcity = 0
    for i in range(len(boxes)):
        box = boxes[i]
        print('当前第{}盒子'.format(i), box)
        # 剪枝条件
        if box.getVolumn()<container.getRemainingCapacity():
            if not container.putBox_Base(box):
                print("can't put this, get next")
            else:
                curUsedCapcity+=box.getVolumn()
                print('当前利用率', curUsedCapcity/container.getTotalCapacity())
    print('最终利用率', curUsedCapcity/container.getTotalCapacity())


if __name__ == '__main__':
    main()