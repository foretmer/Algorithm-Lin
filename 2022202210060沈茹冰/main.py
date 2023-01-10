import copy
from plot import *
from dataset import *
from utils import *
from heuristic import *
import time
import warnings
import sys
warnings.filterwarnings('ignore')


class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


def main():

    # log = Logger('results/output.txt')  
    # sys.stdout = log

    test_data = read_data('data.txt')
    # 容器底面
    container = Plane(0,0,0,587,233)
    # 箱体列表
    for tid in test_data:
        start = time.time()
        box_list = []
        num_list = []
        for box in tid:
            box_list.append(Box(int(box['lx']), int(box['ly']), int(box['lz']), int(box['type'])))
            num_list.append(int(box['num']))
        # 问题
        problem = Problem(container=container, height_limit=220, box_list=box_list, num_list=copy.copy(num_list))
        # 启发式算法
        new_avail_list, used_ratio, used_high, box_pos_, _ = heuristic(problem, box['test_id'])
        end = time.time()
        # 打印测试样例、空间利用率
        print("%s  %s  %.2fs" % (box['test_id'], used_ratio, end-start))
        # 打印箱子坐标
        print(box_pos_)
        print('\n')



if __name__ == "__main__":
    main()

