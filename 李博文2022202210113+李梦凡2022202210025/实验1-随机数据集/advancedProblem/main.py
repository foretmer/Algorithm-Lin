import sys
import time
sys.path.append("..")
from tools.container import Container
from tools.box import Box
import random
import numpy as np

def generateBoxes(n):
    boxes = []
    for i in range(n):
        if random.random()<0.4:
            MIN_SIZE, MAX_SIZE = 10, 50
        elif random.random()<0.8:
            MIN_SIZE, MAX_SIZE = 50, 100
        elif random.random()<0.9:
            MIN_SIZE, MAX_SIZE = 100, 150
        else:
            MIN_SIZE, MAX_SIZE = 150, 300

        boxes.append(Box(random.randint(MIN_SIZE, MAX_SIZE), random.randint(MIN_SIZE, MAX_SIZE), random.randint(MIN_SIZE, MAX_SIZE)))

    return boxes


def main():


    # 盒子随机顺序到达
    sum = 0
    count = 0
    for j in range(0, 5):
        start = time.perf_counter()
        boxes = generateBoxes(500)
        totalBox = 0
        for box in boxes:
            totalBox += box.getVolumn()

        print('totalBox', totalBox)
        container = Container()
        print('盒子总体积为容器总体积的多少倍', totalBox / container.getTotalCapacity())
        for i in range(len(boxes)):
            box = boxes[i]
            print('当前第{}盒子'.format(i), box)
            if box.getVolumn() < container.getRemainingCapacity():
                container.putBox_Advance(box)

        rate = 1 - container.getRemainingCapacity() / container.getTotalCapacity()
        print('最终占用率可以达到：', rate)
        sum = sum + rate
        count = count + 1
        end = time.perf_counter()
        print('本次用时：', end - start)
    print('装箱实验次数：', count)
    print('平均占用率：', sum / count)


if __name__ == '__main__':
    main()