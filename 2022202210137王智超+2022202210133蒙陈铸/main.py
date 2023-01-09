import random
import numpy as np
import copy
from tqdm import tqdm
import sys
import os


def init_box(l, w, h):
    return np.zeros((l, w, h), dtype=np.int)


def modify_space(box, pos, l, w, h):
    x, y, z = pos[0], pos[1], pos[2]
    box[x:x + l, y:y + w, z:z + h] = 1


def judge_item(box, pos, l, w, h):
    max_l, max_w, max_h = box.shape  # 箱子的参数
    x, y, z = pos[0], pos[1], pos[2]  # 当前摆放的位置

    if l + x > max_l or w + y > max_w or z + 1 > max_h:
        return False, 0

    for i in range(x, x + l):  # 如果放进去的箱子超过了车厢的长和宽，则失败
        for j in range(y, y + w):
            if box[i, j, z]:
                return False, 0

    min_h = z
    for k in range(z - 1, -1, -1):  # 找到可以放进去的车厢的最大高度
        flag = True
        for i in range(x, x + l):
            for j in range(y, y + w):
                if box[i, j, k]:
                    flag = False
                    break
            if not flag:
                break
        if not flag:
            break
        min_h -= 1

    if min_h + h > max_h:
        return False, z - min_h

    for k in range(1, h - z + min_h):
        for i in range(x, x + l):
            for j in range(y, y + w):
                if box[i, j, z + k]:
                    return False, z - min_h

    return True, z - min_h

def pack_item_into_box(list_item, box_para, seq):  # 查看DNA（装车顺序及姿势)的空间利用率和装车结果
    max_l, max_w, max_h = box_para['dimensions']
    box = init_box(max_l, max_w, max_h)  # 将车厢划分为小空间
    pos_list = [[0, 0, 0]]  # 可选放置点
    info = []

    total_space = max_w * max_l * max_h
    used_space = 0

    dir_list = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]
    for i in range(len(list_item)):
        pos_list.sort(key=lambda x: (x[2], x[1], x[0]))  # 放置点列表更新后，为保证约定的放置顺序，排序放置点
        item = list_item[seq[i][0]]
        seq_dir = seq[i][1]
        l, w, h = item['size'][dir_list[seq_dir][0]], item['size'][dir_list[seq_dir][1]], item['size'][
            dir_list[seq_dir][2]]
        if l > max_l or w > max_w or h > max_h or (used_space + l * w * h) > total_space:
            continue
        for index, pos in enumerate(pos_list):
            flag, min_h = judge_item(box, pos, l, w, h)  # 依次实验在每个放置点放置箱子，如果箱子在这个位置能放成功，装入车厢
            if flag:
                new_pos = [pos[0], pos[1], pos[2] - min_h]
                modify_space(box, new_pos, l, w, h)
                info.append("{}-shape({}, {}, {})-location:{}".format(item['id'], l, w, h, new_pos))
                pos_list.pop(index)

                pos_list.append([new_pos[0] + l, new_pos[1], new_pos[2]])
                pos_list.append([new_pos[0], new_pos[1] + w, new_pos[2]])
                pos_list.append([new_pos[0], new_pos[1], new_pos[2] + h])

                used_space += l * w * h
                break

    space_ratio = used_space / total_space

    return space_ratio, info


def exchange_item(list_item):  # 随机交换两个箱子装车顺序
    count = len(list_item)
    if count > 1:
        s1, s2 = random.randint(0, count - 1), random.randint(0, count - 1)
        while s1 == s2:
            s2 = random.randint(0, count - 1)
        list_item[s1], list_item[s2] = list_item[s2], list_item[s1]


def exchange_direction(list_item):  # 随机交换某个箱子的装车姿势
    count = len(list_item)
    s = random.randint(0, count - 1)
    new_dir = random.randint(0, 5)
    while new_dir == list_item[s][1]:
        new_dir = random.randint(0, 5)
    list_item[s] = (list_item[s][0], new_dir)


def crossover(list_item_a, list_item_b):  # 交叉配对（父亲，母亲）
    count = len(list_item_a)
    # 后代继承了母亲的装箱子顺序和父亲的装箱子姿势
    list_item_c = copy.deepcopy(list_item_a)
    c_pos = random.randint(1, count - 1)
    slice_a, slice_b = list_item_a[c_pos:], list_item_b[c_pos:]
    slice_a_id, slice_b_id = [i[0] for i in slice_a], [j[0] for j in slice_b]
    list_item_c[c_pos:] = list_item_b[c_pos:]
    for i in range(c_pos):
        c_id = list_item_c[i][0]
        if c_id in slice_b_id:
            while c_id in slice_b_id:
                c_id = slice_a_id[slice_b_id.index(c_id)]
            list_item_c[i] = slice_a[slice_a_id.index(c_id)]

    return list_item_c


def init_ethnic(list_item, ethnic_num):  # 初始化族群，个数为ethnic_num
    count = len(list_item)
    ethnic_list = []
    seq_id = list(range(count))
    for i in range(ethnic_num):
        random.shuffle(seq_id)
        seq_dir = [random.randint(0, 5) for j in range(count)]
        ethnic_list.append([(seq_id[j], seq_dir[j]) for j in range(count)])
    return ethnic_list


def ethnic_reproduction(list_item, box, ethic_num, p_cross, p_mut, max_iteration):

    # 初始化族群
    ethic_list = init_ethnic(list_item, ethic_num)
    space_ratio_list, info_list = [], []
    for i in range(ethic_num):
        space_ratio, info = pack_item_into_box(list_item, box, ethic_list[i])
        space_ratio_list.append(space_ratio)
        info_list.append(info)
    space_ratio_best = max(space_ratio_list)
    info_best = info_list[space_ratio_list.index(space_ratio_best)]
    # print((space_ratio_best, info))
    # print('\n')

    for i in tqdm(range(max_iteration)):
        for j in range(ethic_num):
            if random.random() <= p_cross:
                new_list_item = crossover(ethic_list[j], ethic_list[(j + 1) % ethic_num])
                if random.random() <= p_mut:
                    if random.random() > 0.5:
                        exchange_item(new_list_item)
                    else:
                        exchange_direction(new_list_item)
                ethic_list.append(new_list_item)
                space_ratio, info = pack_item_into_box(list_item, box, new_list_item)
                space_ratio_list.append(space_ratio)
                info_list.append(info)

        space_ratio_best_cur = max(space_ratio_list)
        if space_ratio_best_cur > space_ratio_best:
            space_ratio_best = space_ratio_best_cur
            info_best = list_item[space_ratio_list.index(space_ratio_best)]
        # print((space_ratio_best, info))

        select_id = []
        for j in range(ethic_num):
            select_one_round = np.random.choice(list(range(len(space_ratio_list))), 2, replace=False)
            if space_ratio_list[select_one_round[0]] >= space_ratio_list[select_one_round[1]]:
                select_id.append(select_one_round[0])
            else:
                select_id.append(select_one_round[1])
        space_ratio_list = [space_ratio_list[k] for k in select_id]
        info_list = [info_list[k] for k in select_id]
        ethic_list = [ethic_list[k] for k in select_id]

    return space_ratio_best, info_best
# def ethnic_reproduction(items, box, ethnic_num, p_cross, p_mut, max_iteration):  # p_mut: probability of mutation
#     item_num = len(items)
#     ethnic_list = init_ethnic(items, ethnic_num)
#     score_list, res_list = [], []
#     for i in range(ethnic_num):
#         # new_items = gen_new_items(items, ethnic_list[i])
#         # score, res = pack_item(new_items, x, y, z)
#         score, res = pack_item_into_box(items, box, ethnic_list[i])
#         score_list.append(score)
#         res_list.append(res)
#     score_best = max(score_list)
#     res_best = res_list[score_list.index(score_best)]
#
#     print((score_best, res_best))
#
#     for i in tqdm(range(max_iteration)):
#         for j in range(ethnic_num):
#             if random.random() <= p_cross:
#                 new_seq = crossover(ethnic_list[j], ethnic_list[(j + 1) % ethnic_num])
#                 if random.random() <= p_mut:
#                     if random.random() > 0.5:
#                         exchange_item(new_seq)
#                     else:
#                         exchange_item(new_seq)
#                 ethnic_list.append(new_seq)
#                 # new_items = gen_new_items(items, new_seq)
#                 # score, res = pack_item(new_items, x, y, z)
#                 score, res = pack_item_into_box(items, box, new_seq)
#                 score_list.append(score)
#                 res_list.append(res)
#
#         score_best_cur = max(score_list)
#         if score_best_cur > score_best:
#             score_best = score_best_cur
#             res_best = res_list[score_list.index(score_best)]
#         print((score_best, res_best))
#
#         select_id = []
#         for j in range(ethnic_num):
#             select_one_round = np.random.choice(list(range(len(score_list))), 2, replace=False)
#             if score_list[select_one_round[0]] >= score_list[select_one_round[1]]:
#                 select_id.append(select_one_round[0])
#             else:
#                 select_id.append(select_one_round[1])
#         score_list = [score_list[k] for k in select_id]
#         res_list = [res_list[k] for k in select_id]
#         ethnic_list = [ethnic_list[k] for k in select_id]
#
#         # print(ethnic_list)
#     return score_best, res_best

class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
    
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


if __name__ == '__main__':

    type = sys.getfilesystemencoding()
    sys.stdout=Logger("terminal_log.txt")

    box = {"dimensions": [587, 233, 220]}
    item_info = [
    #E1-1
    [
        {"id": "1", "size": [108, 76, 30], "count": 40},
        {"id": "2", "size": [110, 43, 25], "count": 33},
        {"id": "3", "size": [92, 81, 55], "count": 39},
    ],
    #E1-2
    [
        {"id": "1", "size": [91, 54, 45], "count": 32},
        {"id": "2", "size": [105, 77, 72], "count": 24},
        {"id": "3", "size": [79, 78, 48], "count": 30},
    ],
    #1-3
    [
        {"id": "1", "size": [91, 54, 45], "count": 32},
        {"id": "2", "size": [105, 77, 72], "count": 24},
        {"id": "3", "size": [79, 78, 48], "count": 30},
    ],
    #E1-4
    [
        {"id": "1", "size": [60, 40, 32], "count": 64},
        {"id": "2", "size": [98, 75, 55], "count": 40},
        {"id": "3", "size": [60, 59, 39], "count": 64},
    ],
    #E1-5
    [
        {"id": "1", "size": [78, 37, 27], "count": 63},
        {"id": "2", "size": [89, 70, 25], "count": 52},
        {"id": "3", "size": [90, 84, 41], "count": 55},
    ],
    #E2-1
    [
        {"id": "1", "size": [108, 76, 30], "count": 24},
        {"id": "2", "size": [110, 43, 25], "count": 7},
        {"id": "3", "size": [92, 81, 55], "count": 22},
        {"id": "4", "size": [81, 33, 28], "count": 13},
        {"id": "5", "size": [120, 99, 73], "count": 15},
    ],
    #E2-2
    [
        {"id": "1", "size": [49, 25, 21], "count": 22},
        {"id": "2", "size": [60, 51, 41], "count": 22},
        {"id": "3", "size": [103, 76, 64], "count": 28},
        {"id": "4", "size": [95, 70, 62], "count": 25},
        {"id": "5", "size": [111, 49, 26], "count": 17},
    ],
    #E2-3
    [
        {"id": "1", "size": [88, 54, 39], "count": 25},
        {"id": "2", "size": [94, 54, 36], "count": 27},
        {"id": "3", "size": [87, 77, 43], "count": 21},
        {"id": "4", "size": [100, 80, 72], "count": 20},
        {"id": "5", "size": [83, 40, 36], "count": 24},
    ],
    #E2-4
    [
        {"id": "1", "size": [90, 70, 63], "count": 16},
        {"id": "2", "size": [84, 78, 28], "count": 28},
        {"id": "3", "size": [94, 85, 39], "count": 20},
        {"id": "4", "size": [80, 76, 54], "count": 23},
        {"id": "5", "size": [69, 50, 45], "count": 31},
    ],
    #E2-5
    [
        {"id": "1", "size": [74, 63, 61], "count": 22},
        {"id": "2", "size": [71, 60, 25], "count": 12},
        {"id": "3", "size": [106, 80, 59], "count": 25},
        {"id": "4", "size": [109, 76, 42], "count": 24},
        {"id": "5", "size": [118, 56, 22], "count": 11},
    ],
    #E3-1
    [
        {"id": "1", "size": [108, 76, 30], "count": 24},
        {"id": "2", "size": [110, 43, 25], "count": 9},
        {"id": "3", "size": [92, 81, 55], "count": 8},
        {"id": "4", "size": [81, 33, 28], "count": 11},
        {"id": "5", "size": [120, 99, 73], "count": 11},
        {"id": "6", "size": [110, 70, 48], "count": 10},
        {"id": "7", "size": [98, 72, 46], "count": 12},
        {"id": "8", "size": [95, 66, 31], "count": 9},
    ],
    #E3-2
    [
        {"id": "1", "size": [97, 81, 27], "count": 10},
        {"id": "2", "size": [102, 78, 39], "count": 20},
        {"id": "3", "size": [113, 46, 36], "count": 18},
        {"id": "4", "size": [66, 50, 42], "count": 21},
        {"id": "5", "size": [101, 30, 26], "count": 16},
        {"id": "6", "size": [100, 56, 35], "count": 17},
        {"id": "7", "size": [91, 50, 40], "count": 22},
        {"id": "8", "size": [106, 61, 56], "count": 19},
    ],
    #E3-3
    [
        {"id": "1", "size": [88, 54, 39], "count": 16},
        {"id": "2", "size": [94, 54, 36], "count": 14},
        {"id": "3", "size": [87, 77, 43], "count": 20},
        {"id": "4", "size": [100, 80, 72], "count": 16},
        {"id": "5", "size": [83, 40, 36], "count": 6},
        {"id": "6", "size": [91, 54, 22], "count": 15},
        {"id": "7", "size": [109, 58, 54], "count": 17},
        {"id": "8", "size": [94, 55, 30], "count": 9},
    ],
    #E3-4
    [
        {"id": "1", "size": [49, 25, 21], "count": 16},
        {"id": "2", "size": [60, 51, 41], "count": 8},
        {"id": "3", "size": [103, 76, 64], "count": 16},
        {"id": "4", "size": [95, 70, 62], "count": 18},
        {"id": "5", "size": [111, 49, 26], "count": 18},
        {"id": "6", "size": [85, 84, 72], "count": 16},
        {"id": "7", "size": [48, 36, 31], "count": 17},
        {"id": "8", "size": [86, 76, 38], "count": 6},
    ],
    #E3-5
    [
        {"id": "1", "size": [113, 92, 33], "count": 23},
        {"id": "2", "size": [52, 37, 28], "count": 22},
        {"id": "3", "size": [57, 33, 29], "count": 26},
        {"id": "4", "size": [99, 37, 30], "count": 17},
        {"id": "5", "size": [92, 64, 33], "count": 23},
        {"id": "6", "size": [119, 59, 39], "count": 26},
        {"id": "7", "size": [54, 52, 49], "count": 18},
        {"id": "8", "size": [75, 45, 35], "count": 30},
    ],
    #E4-1
    [
        {"id": "1", "size": [49, 25, 21], "count": 13},
        {"id": "2", "size": [60, 51, 41], "count": 9},
        {"id": "3", "size": [103, 76, 64], "count": 11},
        {"id": "4", "size": [95, 70, 62], "count": 14},
        {"id": "5", "size": [111, 49, 26], "count": 13},
        {"id": "6", "size": [85, 84, 72], "count": 16},
        {"id": "7", "size": [48, 36, 31], "count": 12},
        {"id": "8", "size": [86, 76, 38], "count": 11},
        {"id": "9", "size": [71, 48, 47], "count": 16},
        {"id": "10", "size": [90, 43, 33], "count": 8},
    ],
    #E4-2
    [
        {"id": "1", "size": [97, 81, 27], "count": 8},
        {"id": "2", "size": [102, 78, 39], "count": 16},
        {"id": "3", "size": [113, 46, 36], "count": 12},
        {"id": "4", "size": [66, 50, 42], "count": 12},
        {"id": "5", "size": [101, 30, 26], "count": 18},
        {"id": "6", "size": [100, 56, 35], "count": 13},
        {"id": "7", "size": [91, 50, 40], "count": 14},
        {"id": "8", "size": [106, 61, 56], "count": 17},
        {"id": "9", "size": [103, 63, 58], "count": 12},
        {"id": "10", "size": [75, 57, 41], "count": 13},
    ],
    #E4-3
    [
        {"id": "1", "size": [86, 84, 45], "count": 18},
        {"id": "2", "size": [81, 45, 34], "count": 19},
        {"id": "3", "size": [70, 54, 37], "count": 13},
        {"id": "4", "size": [71, 61, 52], "count": 16},
        {"id": "5", "size": [78, 73, 40], "count": 10},
        {"id": "6", "size": [69, 63, 46], "count": 13},
        {"id": "7", "size": [72, 67, 56], "count": 10},
        {"id": "8", "size": [75, 75, 36], "count": 8},
        {"id": "9", "size": [94, 88, 50], "count": 12},
        {"id": "10", "size": [65, 51, 50], "count": 13},
    ],
    #E4-4
    [
        {"id": "1", "size": [113, 92, 33], "count": 15},
        {"id": "2", "size": [52, 37, 28], "count": 17},
        {"id": "3", "size": [57, 33, 29], "count": 17},
        {"id": "4", "size": [99, 37, 30], "count": 19},
        {"id": "5", "size": [92, 64, 33], "count": 13},
        {"id": "6", "size": [119, 59, 39], "count": 19},
        {"id": "7", "size": [54, 52, 49], "count": 13},
        {"id": "8", "size": [75, 45, 35], "count": 21},
        {"id": "9", "size": [79, 68, 44], "count": 13},
        {"id": "10", "size": [116, 49, 47], "count": 22},
    ],
    #E4-5
    [
        {"id": "1", "size": [118, 79, 51], "count": 16},
        {"id": "2", "size": [86, 32, 31], "count": 8},
        {"id": "3", "size": [64, 58, 52], "count": 14},
        {"id": "4", "size": [42, 42, 32], "count": 14},
        {"id": "5", "size": [64, 55, 43], "count": 16},
        {"id": "6", "size": [84, 70, 35], "count": 10},
        {"id": "7", "size": [76, 57, 36], "count": 14},
        {"id": "8", "size": [95, 60, 55], "count": 14},
        {"id": "9", "size": [80, 66, 52], "count": 14},
        {"id": "10", "size": [109, 73, 23], "count": 18},
    ],
    #E5-1
    [
        {"id": "1", "size": [98, 73, 44], "count": 6},
        {"id": "2", "size": [60, 60, 38], "count": 7},
        {"id": "3", "size": [105, 73, 60], "count": 10},
        {"id": "4", "size": [90, 77, 52], "count": 3},
        {"id": "5", "size": [66, 58, 24], "count": 5},
        {"id": "6", "size": [106, 76, 55], "count": 10},
        {"id": "7", "size": [55, 44, 36], "count": 12},
        {"id": "8", "size": [82, 58, 23], "count": 7},
        {"id": "9", "size": [74, 61, 58], "count": 6},
        {"id": "10", "size": [81, 39, 24], "count": 8},
        {"id": "11", "size": [71, 65, 39], "count": 11},
        {"id": "12", "size": [105, 97, 47], "count": 4},
        {"id": "13", "size": [114, 97, 69], "count": 5},
        {"id": "14", "size": [103, 78, 55], "count": 6},
        {"id": "15", "size": [93, 66, 55], "count": 6},
    ],
    #E5-2
    [
        {"id": "1", "size": [108, 76, 30], "count": 12},
        {"id": "2", "size": [110, 43, 25], "count": 12},
        {"id": "3", "size": [92, 81, 55], "count": 6},
        {"id": "4", "size": [81, 33, 28], "count": 9},
        {"id": "5", "size": [120, 99, 73], "count": 5},
        {"id": "6", "size": [111, 70, 48], "count": 12},
        {"id": "7", "size": [98, 72, 46], "count": 9},
        {"id": "8", "size": [95, 66, 31], "count": 10},
        {"id": "9", "size": [85, 84, 30], "count": 8},
        {"id": "10", "size": [71, 32, 25], "count": 3},
        {"id": "11", "size": [36, 34, 25], "count": 10},
        {"id": "12", "size": [97, 67, 62], "count": 7},
        {"id": "13", "size": [33, 25, 23], "count": 7},
        {"id": "14", "size": [95, 27, 26], "count": 10},
        {"id": "15", "size": [94, 81, 44], "count": 9},
    ],
    #E5-3
    [
        {"id": "1", "size": [49, 25, 21], "count": 13},
        {"id": "2", "size": [60, 51, 41], "count": 9},
        {"id": "3", "size": [103, 76, 64], "count": 8},
        {"id": "4", "size": [95, 70, 62], "count": 6},
        {"id": "5", "size": [111, 49, 26], "count": 10},
        {"id": "6", "size": [74, 42, 40], "count": 4},
        {"id": "7", "size": [85, 84, 72], "count": 10},
        {"id": "8", "size": [48, 36, 31], "count": 10},
        {"id": "9", "size": [86, 76, 38], "count": 12},
        {"id": "10", "size": [71, 48, 47], "count": 14},
        {"id": "11", "size": [90, 43, 33], "count": 9},
        {"id": "12", "size": [98, 52, 44], "count": 9},
        {"id": "13", "size": [73, 37, 23], "count": 10},
        {"id": "14", "size": [61, 48, 39], "count": 14},
        {"id": "15", "size": [75, 75, 63], "count": 11},
    ],
    #E5-4
    [
        {"id": "1", "size": [97, 81, 27], "count": 6},
        {"id": "2", "size": [102, 78, 39], "count": 6},
        {"id": "3", "size": [113, 46, 36], "count": 15},
        {"id": "4", "size": [66, 50, 42], "count": 8},
        {"id": "5", "size": [101, 30, 26], "count": 6},
        {"id": "6", "size": [100, 56, 35], "count": 7},
        {"id": "7", "size": [91, 50, 40], "count": 12},
        {"id": "8", "size": [106, 61, 56], "count": 10},
        {"id": "9", "size": [103, 63, 58], "count": 8},
        {"id": "10", "size": [75, 57, 41], "count": 11},
        {"id": "11", "size": [71, 68, 64], "count": 6},
        {"id": "12", "size": [85, 67, 39], "count": 14},
        {"id": "13", "size": [97, 63, 56], "count": 9},
        {"id": "14", "size": [61, 48, 30], "count": 11},
        {"id": "15", "size": [80, 54, 35], "count": 9},
    ],
    #E5-5
    [
        {"id": "1", "size": [113, 92, 33], "count": 8},
        {"id": "2", "size": [52, 37, 28], "count": 12},
        {"id": "3", "size": [57, 33, 29], "count": 5},
        {"id": "4", "size": [99, 37, 30], "count": 12},
        {"id": "5", "size": [92, 64, 33], "count": 9},
        {"id": "6", "size": [119, 59, 39], "count": 12},
        {"id": "7", "size": [54, 52, 49], "count": 8},
        {"id": "8", "size": [75, 45, 35], "count": 6},
        {"id": "9", "size": [79, 68, 44], "count": 12},
        {"id": "10", "size": [116, 49, 47], "count": 9},
        {"id": "11", "size": [83, 44, 23], "count": 11},
        {"id": "12", "size": [98, 96, 56], "count": 10},
        {"id": "13", "size": [78, 72, 57], "count": 8},
        {"id": "14", "size": [98, 88, 47], "count": 9},
        {"id": "15", "size": [41, 33, 31], "count": 13},
    ]
        # {"id": "1", "size": [113, 92, 33], "count": 8},
        # {"id": "2", "size": [52, 37, 28], "count": 12},
        # {"id": "3", "size": [57, 33, 29], "count": 5},
        # {"id": "4", "size": [99, 37, 30], "count": 12},
        # {"id": "5", "size": [92, 64, 33], "count": 9},
        # {"id": "6", "size": [54, 52, 49], "count": 8},
        # {"id": "7", "size": [75, 45, 35], "count": 6},
        # {"id": "8", "size": [79, 68, 44], "count": 12},
        # {"id": "9", "size": [116, 49, 47], "count": 9},
        # {"id": "10", "size": [83, 44, 23], "count": 11},
        # {"id": "11", "size": [98, 96, 56], "count": 10},
        # {"id": "12", "size": [78, 72, 57], "count": 8},
        # {"id": "13", "size": [98, 88, 47], "count": 9},
        # {"id": "14", "size": [119, 59, 39], "count": 12},
        # {"id": "15", "size": [41, 33, 31], "count": 13},

        # {"id": "1", "size": [108, 76, 30]},
        # {"id": "2", "size": [108, 76, 30]},
        # {"id": "3", "size": [108, 76, 30]},
        # {"id": "4", "size": [108, 76, 30]},
        # {"id": "5", "size": [108, 76, 30]},
        # {"id": "6", "size": [108, 76, 30]},
        # {"id": "7", "size": [108, 76, 30]},
        # {"id": "8", "size": [108, 76, 30]},
        # {"id": "9", "size": [108, 76, 30]},
        # {"id": "10", "size": [108, 76, 30]},
        # {"id": "11", "size": [108, 76, 30]},
        # {"id": "12", "size": [108, 76, 30]},
    ]

    lis_num = 2

    for k in range(lis_num):
        item_list = []
        for i in range(len(item_info[k])):
            for j in range(item_info[k][i]['count']):
                item_list.append(copy.deepcopy(item_info[k][i]))
        if k % 5 == 0:
            if k == 0:
                print("存在3种箱子的分配情况：")
            if k == 5:
                print("存在5种箱子的分配情况：")
            if k == 10:
                print("存在8种箱子的分配情况：")    
            if k == 15:
                print("存在10种箱子的分配情况：")
            if k == 20:
                print("存在15种箱子的分配情况：")
        #print("E"+(k/5+1)+"-"+(k%5+1)+":")
        print('E{0}-{1}：'.format(int(k/5+1), (k%5+1)))
        print(ethnic_reproduction(item_list, box, 20, 0.7, 0.05, 50))