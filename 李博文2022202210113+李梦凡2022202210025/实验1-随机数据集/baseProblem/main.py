import sys
sys.path.append("..")
from tools.container import Container
from tools.box import Box
import random
import numpy as np



def generateBoxes(n):
    boxes = []
    for i in range(n):
        if random.random() < 0.6:
            MIN_SIZE, MAX_SIZE = 10, 50
        elif random.random() < 0.8:
            MIN_SIZE, MAX_SIZE = 50, 100
        elif random.random() < 0.9:
            MIN_SIZE, MAX_SIZE = 100, 150
        else:
            MIN_SIZE, MAX_SIZE = 150, 300

        boxes.append(Box(random.randint(MIN_SIZE, MAX_SIZE), random.randint(MIN_SIZE, MAX_SIZE),
                         random.randint(MIN_SIZE, MAX_SIZE)))

    return boxes


def main():
    boxes = generateBoxes(500)
    # 根据最大面降序排列（先放最大的）
    def key(a):
        return -np.sum(a.getMaxSurface())
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