import numpy as np
import random
import copy
from tqdm import tqdm


def init_bins(x, y, z):
    return np.zeros((x, y, z), dtype=np.int)


def pack_item_one(bins, pos, l, w, h):
    x, y, z = pos[0], pos[1], pos[2]
    bins[x:x + l, y:y + w, z:z + h] = 1
    # return bins


# consider gravity (return down_distance)
def is_valid_pack(bins, pos, l, w, h):
    max_x, max_y, max_z = bins.shape
    x, y, z = pos[0], pos[1], pos[2]

    if x + l > max_x or y + w > max_y or z + 1 > max_z:
        return False, 0
    for i in range(x, x + l):
        for j in range(y, y + w):
            if bins[i, j, z]:
                return False, 0

    lower_z = z
    for k in range(z - 1, -1, -1):
        down = True
        for i in range(x, x + l):
            for j in range(y, y + w):
                if bins[i, j, k]:
                    down = False
                    break
            if not down:
                break
        if not down:
            break
        lower_z -= 1

    if lower_z + h > max_z:
        return False, z - lower_z

    for k in range(1, h - z + lower_z):
        for i in range(x, x + l):
            for j in range(y, y + w):
                if bins[i, j, z + k]:
                    return False, z - lower_z

    return True, z - lower_z


def pack_item(items, x, y, z, seq):
    bins = init_bins(x, y, z)  # bin_space_init
    pos_list = [[0, 0, 0]]
    res = []

    dir_trans = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]

    used_bins, total_bins = 0, x * y * z
    for i in range(len(items)):
        pos_list.sort(key=lambda p: (p[2], p[1], p[0]))
        item = items[seq[i][0]]
        seq_dir = seq[i][1]
        l, w, h = item['size'][dir_trans[seq_dir][0]], item['size'][dir_trans[seq_dir][1]], item['size'][
            dir_trans[seq_dir][2]]
        if l > x or w > y or h > z or (used_bins + l * w * h) > total_bins:
            continue
        for index, pos in enumerate(pos_list):
            isValid, down_dis = is_valid_pack(bins, pos, l, w, h)
            if isValid:
                new_pos = [pos[0], pos[1], pos[2] - down_dis]
                pack_item_one(bins, new_pos, l, w, h)
                res.append("{}-({},{},{})-{}".format(item['id'], l, w, h, new_pos))
                pos_list.pop(index)

                pos_list.append([new_pos[0] + l, new_pos[1], new_pos[2]])
                pos_list.append([new_pos[0], new_pos[1] + w, new_pos[2]])
                pos_list.append([new_pos[0], new_pos[1], new_pos[2] + h])

                used_bins += l * w * h
                break

    # score = bins.sum() / (x * y * z)
    score = used_bins / total_bins
    return score, res


def mutation_seq(seq):  # mutation of packing sequence
    item_num = len(seq)
    if item_num > 1:
        s1, s2 = random.randint(0, item_num - 1), random.randint(0, item_num - 1)
        while s1 == s2:
            s2 = random.randint(0, item_num - 1)
        seq[s1], seq[s2] = seq[s2], seq[s1]
    # return seq


def mutation_dir(seq):  # mutation of one item's direction
    item_num = len(seq)
    s = item_num + random.randint(0, item_num - 1)
    new_dir = random.randint(0, 5)
    while new_dir == seq[s][1]:
        new_dir = random.randint(0, 5)
    seq[s] = (seq[s][0], new_dir)
    # return seq


def crossover(seq1, seq2):
    item_num = len(seq1)
    seq3 = copy.deepcopy(seq1)
    c_pos = random.randint(1, item_num - 1)

    frag1, frag2 = seq1[c_pos:], seq2[c_pos:]
    frag1_id, frag2_id = [i[0] for i in frag1], [j[0] for j in frag2]

    seq3[c_pos:] = seq2[c_pos:]
    for i in range(c_pos):
        seq3_item_id = seq3[i][0]
        if seq3_item_id in frag2_id:
            while seq3_item_id in frag2_id:
                seq3_item_id = frag1_id[frag2_id.index(seq3_item_id)]
            seq3[i] = frag1[frag1_id.index(seq3_item_id)]
    return seq3


def init_ethnic(items, ethnic_num):
    item_num = len(items)
    ethnic_list = []
    seq_id = list(range(item_num))
    for i in range(ethnic_num):
        random.shuffle(seq_id)
        seq_dir = [random.randint(0, 5) for j in range(item_num)]
        ethnic_list.append([(seq_id[j], seq_dir[j]) for j in range(item_num)])
    return ethnic_list


# def gen_new_items(items, seq):
#     new_items = []
#     dir_trans = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]
#     for (seq_id, seq_dir) in seq:
#         new_items.append(copy.deepcopy(items[seq_id]))
#         new_items[-1]['size'] = [new_items[-1]['size'][dir_trans[seq_dir][i]] for i in range(3)]
#     return new_items

def ethnic_iteration(items, x, y, z, ethnic_num, p_cross, p_mut, max_iteration):  # p_mut: probability of mutation
    item_num = len(items)
    ethnic_list = init_ethnic(items, ethnic_num)
    score_list, res_list = [], []
    for i in range(ethnic_num):
        # new_items = gen_new_items(items, ethnic_list[i])
        # score, res = pack_item(new_items, x, y, z)
        score, res = pack_item(items, x, y, z, ethnic_list[i])
        score_list.append(score)
        res_list.append(res)
    score_best = max(score_list)
    res_best = res_list[score_list.index(score_best)]

    print((score_best, res_best))

    for i in tqdm(range(max_iteration)):
        for j in range(ethnic_num):
            if random.random() <= p_cross:
                new_seq = crossover(ethnic_list[j], ethnic_list[(j + 1) % ethnic_num])
                if random.random() <= p_mut:
                    if random.random() > 0.5:
                        mutation_seq(new_seq)
                    else:
                        mutation_seq(new_seq)
                ethnic_list.append(new_seq)
                # new_items = gen_new_items(items, new_seq)
                # score, res = pack_item(new_items, x, y, z)
                score, res = pack_item(items, x, y, z, new_seq)
                score_list.append(score)
                res_list.append(res)

        score_best_cur = max(score_list)
        if score_best_cur > score_best:
            score_best = score_best_cur
            res_best = res_list[score_list.index(score_best)]
        print((score_best, res_best))

        select_id = []
        for j in range(ethnic_num):
            select_one_round = np.random.choice(list(range(len(score_list))), 2, replace=False)
            if score_list[select_one_round[0]] >= score_list[select_one_round[1]]:
                select_id.append(select_one_round[0])
            else:
                select_id.append(select_one_round[1])
        score_list = [score_list[k] for k in select_id]
        res_list = [res_list[k] for k in select_id]
        ethnic_list = [ethnic_list[k] for k in select_id]

        # print(ethnic_list)
    return score_best, res_best


if __name__ == '__main__':
    print('[*] Solver for 3D Bin Packing Problem')

    x, y, z = 587, 233, 220

    items_info = [
        # E1
        {"items_set": [
            {"id": "item-01", "size": [108, 76, 30]},
            {"id": "item-02", "size": [110, 43, 25]},
            {"id": "item-03", "size": [92, 81, 55]}
        ], "items_num": [40, 33, 39]},
        {"items_set": [
            {"id": "item-01", "size": [91, 54, 45]},
            {"id": "item-02", "size": [105, 77, 72]},
            {"id": "item-03", "size": [79, 78, 48]}
        ], "items_num": [32, 24, 30]},
        {"items_set": [
            {"id": "item-01", "size": [60, 40, 32]},
            {"id": "item-02", "size": [98, 75, 55]},
            {"id": "item-03", "size": [60, 59, 39]}
        ], "items_num": [64, 40, 64]},
        {"items_set": [
            {"id": "item-01", "size": [78, 37, 27]},
            {"id": "item-02", "size": [89, 70, 25]},
            {"id": "item-03", "size": [90, 84, 41]}
        ], "items_num": [63, 52, 55]},

        # E2
        {"items_set": [
            {"id": "item-01", "size": [108, 76, 30]},
            {"id": "item-02", "size": [110, 43, 25]},
            {"id": "item-03", "size": [92, 81, 55]},
            {"id": "item-04", "size": [81, 33, 28]},
            {"id": "item-05", "size": [120, 99, 73]}
        ], "items_num": [24, 7, 22, 13, 15]},
        {"items_set": [
            {"id": "item-01", "size": [49, 25, 21]},
            {"id": "item-02", "size": [60, 51, 41]},
            {"id": "item-03", "size": [103, 76, 64]},
            {"id": "item-04", "size": [95, 70, 62]},
            {"id": "item-05", "size": [111, 49, 26]}
        ], "items_num": [22, 22, 28, 25, 17]},
        {"items_set": [
            {"id": "item-01", "size": [88, 54, 39]},
            {"id": "item-02", "size": [94, 54, 36]},
            {"id": "item-03", "size": [87, 77, 43]},
            {"id": "item-04", "size": [100, 80, 72]},
            {"id": "item-05", "size": [83, 40, 36]}
        ], "items_num": [25, 27, 21, 20, 24]},
        {"items_set": [
            {"id": "item-01", "size": [90, 70, 63]},
            {"id": "item-02", "size": [84, 78, 28]},
            {"id": "item-03", "size": [94, 85, 39]},
            {"id": "item-04", "size": [80, 76, 54]},
            {"id": "item-05", "size": [69, 50, 45]}
        ], "items_num": [16, 28, 20, 23, 31]},
        {"items_set": [
            {"id": "item-01", "size": [74, 63, 61]},
            {"id": "item-02", "size": [71, 60, 25]},
            {"id": "item-03", "size": [106, 80, 59]},
            {"id": "item-04", "size": [109, 76, 42]},
            {"id": "item-05", "size": [118, 56, 22]}
        ], "items_num": [22, 12, 25, 24, 11]},

        # E3
        {"items_set": [
            {"id": "item-01", "size": [108, 76, 30]},
            {"id": "item-02", "size": [110, 43, 25]},
            {"id": "item-03", "size": [92, 81, 55]},
            {"id": "item-04", "size": [81, 33, 28]},
            {"id": "item-05", "size": [120, 99, 73]},
            {"id": "item-06", "size": [111, 70, 48]},
            {"id": "item-07", "size": [98, 72, 46]},
            {"id": "item-08", "size": [95, 66, 31]}
        ], "items_num": [24, 9, 8, 11, 11, 10, 12, 9]},
        {"items_set": [
            {"id": "item-01", "size": [97, 81, 27]},
            {"id": "item-02", "size": [102, 78, 39]},
            {"id": "item-03", "size": [113, 46, 36]},
            {"id": "item-04", "size": [66, 50, 42]},
            {"id": "item-05", "size": [101, 30, 26]},
            {"id": "item-06", "size": [100, 56, 35]},
            {"id": "item-07", "size": [91, 50, 40]},
            {"id": "item-08", "size": [106, 61, 56]}
        ], "items_num": [10, 20, 18, 21, 16, 17, 22, 19]},
        {"items_set": [
            {"id": "item-01", "size": [88, 54, 39]},
            {"id": "item-02", "size": [94, 54, 36]},
            {"id": "item-03", "size": [87, 77, 43]},
            {"id": "item-04", "size": [100, 80, 72]},
            {"id": "item-05", "size": [83, 40, 36]},
            {"id": "item-06", "size": [91, 54, 22]},
            {"id": "item-07", "size": [109, 58, 54]},
            {"id": "item-08", "size": [94, 55, 30]}
        ], "items_num": [16, 14, 20, 16, 6, 15, 17, 9]},
        {"items_set": [
            {"id": "item-01", "size": [49, 25, 21]},
            {"id": "item-02", "size": [60, 51, 41]},
            {"id": "item-03", "size": [103, 76, 64]},
            {"id": "item-04", "size": [95, 70, 62]},
            {"id": "item-05", "size": [111, 49, 26]},
            {"id": "item-06", "size": [85, 84, 72]},
            {"id": "item-07", "size": [48, 36, 31]},
            {"id": "item-08", "size": [86, 76, 38]}
        ], "items_num": [16, 8, 16, 18, 18, 16, 17, 6]},
        {"items_set": [
            {"id": "item-01", "size": [113, 92, 33]},
            {"id": "item-02", "size": [52, 37, 28]},
            {"id": "item-03", "size": [57, 33, 29]},
            {"id": "item-04", "size": [99, 37, 30]},
            {"id": "item-05", "size": [92, 64, 33]},
            {"id": "item-06", "size": [119, 59, 39]},
            {"id": "item-07", "size": [54, 52, 49]},
            {"id": "item-08", "size": [75, 45, 35]}

        ], "items_num": [23, 22, 26, 17, 23, 26, 18, 30]},

        # E4
        {"items_set": [
            {"id": "item-01", "size": [49, 25, 21]},
            {"id": "item-02", "size": [60, 51, 41]},
            {"id": "item-03", "size": [103, 76, 64]},
            {"id": "item-04", "size": [95, 70, 62]},
            {"id": "item-05", "size": [111, 49, 26]},
            {"id": "item-06", "size": [85, 84, 72]},
            {"id": "item-07", "size": [48, 36, 31]},
            {"id": "item-08", "size": [86, 76, 38]},
            {"id": "item-09", "size": [71, 48, 47]},
            {"id": "item-10", "size": [90, 43, 33]}
        ], "items_num": [13, 9, 11, 14, 13, 16, 12, 11, 16, 8]},
        {"items_set": [
            {"id": "item-01", "size": [97, 81, 27]},
            {"id": "item-02", "size": [102, 78, 39]},
            {"id": "item-03", "size": [113, 46, 36]},
            {"id": "item-04", "size": [66, 50, 42]},
            {"id": "item-05", "size": [101, 30, 26]},
            {"id": "item-06", "size": [100, 56, 35]},
            {"id": "item-07", "size": [91, 50, 40]},
            {"id": "item-08", "size": [106, 61, 56]},
            {"id": "item-09", "size": [103, 63, 58]},
            {"id": "item-10", "size": [75, 57, 41]}
        ], "items_num": [8, 16, 12, 12, 18, 13, 14, 17, 12, 13]},
        {"items_set": [
            {"id": "item-01", "size": [86, 84, 45]},
            {"id": "item-02", "size": [81, 45, 34]},
            {"id": "item-03", "size": [70, 54, 37]},
            {"id": "item-04", "size": [71, 61, 52]},
            {"id": "item-05", "size": [78, 73, 40]},
            {"id": "item-06", "size": [69, 63, 46]},
            {"id": "item-07", "size": [72, 67, 56]},
            {"id": "item-08", "size": [75, 75, 36]},
            {"id": "item-09", "size": [94, 88, 50]},
            {"id": "item-10", "size": [65, 51, 50]}
        ], "items_num": [18, 19, 13, 16, 10, 13, 10, 8, 12, 13]},
        {"items_set": [
            {"id": "item-01", "size": [113, 92, 33]},
            {"id": "item-02", "size": [52, 37, 28]},
            {"id": "item-03", "size": [57, 33, 29]},
            {"id": "item-04", "size": [99, 37, 30]},
            {"id": "item-05", "size": [92, 64, 33]},
            {"id": "item-06", "size": [119, 59, 39]},
            {"id": "item-07", "size": [54, 52, 49]},
            {"id": "item-08", "size": [75, 45, 35]},
            {"id": "item-09", "size": [79, 68, 44]},
            {"id": "item-10", "size": [116, 49, 47]}
        ], "items_num": [15, 17, 17, 19, 13, 19, 13, 21, 13, 22]},
        {"items_set": [
            {"id": "item-01", "size": [118, 79, 51]},
            {"id": "item-02", "size": [86, 32, 31]},
            {"id": "item-03", "size": [64, 58, 52]},
            {"id": "item-04", "size": [42, 42, 32]},
            {"id": "item-05", "size": [64, 55, 43]},
            {"id": "item-06", "size": [84, 70, 35]},
            {"id": "item-07", "size": [76, 57, 36]},
            {"id": "item-08", "size": [95, 60, 55]},
            {"id": "item-09", "size": [80, 66, 52]},
            {"id": "item-10", "size": [109, 73, 23]}
        ], "items_num": [16, 8, 14, 14, 16, 10, 14, 14, 14, 18]},

        # E5
        {"items_set": [
            {"id": "item-01", "size": [98, 73, 44]},
            {"id": "item-02", "size": [60, 60, 38]},
            {"id": "item-03", "size": [105, 73, 60]},
            {"id": "item-04", "size": [90, 77, 52]},
            {"id": "item-05", "size": [66, 58, 24]},
            {"id": "item-06", "size": [106, 76, 55]},
            {"id": "item-07", "size": [55, 44, 36]},
            {"id": "item-08", "size": [82, 58, 23]},
            {"id": "item-09", "size": [74, 61, 58]},
            {"id": "item-10", "size": [81, 39, 24]},
            {"id": "item-11", "size": [71, 65, 39]},
            {"id": "item-12", "size": [105, 97, 47]},
            {"id": "item-13", "size": [114, 97, 69]},
            {"id": "item-14", "size": [103, 78, 55]},
            {"id": "item-15", "size": [93, 66, 55]},
        ], "items_num": [6, 7, 10, 3, 5, 10, 12, 7, 6, 8, 11, 4, 5, 6, 6]},
        {"items_set": [
            {"id": "item-01", "size": [108, 76, 30]},
            {"id": "item-02", "size": [110, 43, 25]},
            {"id": "item-03", "size": [92, 81, 55]},
            {"id": "item-04", "size": [81, 33, 28]},
            {"id": "item-05", "size": [120, 99, 73]},
            {"id": "item-06", "size": [111, 70, 48]},
            {"id": "item-07", "size": [98, 72, 46]},
            {"id": "item-08", "size": [95, 66, 31]},
            {"id": "item-09", "size": [85, 84, 30]},
            {"id": "item-10", "size": [71, 32, 25]},
            {"id": "item-11", "size": [36, 34, 25]},
            {"id": "item-12", "size": [97, 67, 62]},
            {"id": "item-13", "size": [33, 25, 23]},
            {"id": "item-14", "size": [95, 27, 26]},
            {"id": "item-15", "size": [94, 81, 44]},
        ], "items_num": [12, 12, 6, 9, 5, 12, 9, 10, 8, 3, 10, 7, 7, 10, 9]},
        {"items_set": [
            {"id": "item-01", "size": [49, 25, 21]},
            {"id": "item-02", "size": [60, 51, 41]},
            {"id": "item-03", "size": [103, 76, 64]},
            {"id": "item-04", "size": [95, 70, 62]},
            {"id": "item-05", "size": [111, 49, 26]},
            {"id": "item-06", "size": [74, 42, 40]},
            {"id": "item-07", "size": [85, 84, 72]},
            {"id": "item-08", "size": [48, 36, 31]},
            {"id": "item-09", "size": [86, 76, 38]},
            {"id": "item-10", "size": [71, 48, 47]},
            {"id": "item-11", "size": [90, 43, 33]},
            {"id": "item-12", "size": [98, 52, 44]},
            {"id": "item-13", "size": [73, 37, 23]},
            {"id": "item-14", "size": [61, 48, 39]},
            {"id": "item-15", "size": [75, 75, 63]},
        ], "items_num": [13, 9, 8, 6, 10, 4, 10, 10, 12, 14, 9, 9, 10, 14, 11]},
        {"items_set": [
            {"id": "item-01", "size": [97, 81, 27]},
            {"id": "item-02", "size": [102, 78, 39]},
            {"id": "item-03", "size": [113, 46, 36]},
            {"id": "item-04", "size": [66, 50, 42]},
            {"id": "item-05", "size": [101, 30, 26]},
            {"id": "item-06", "size": [100, 56, 35]},
            {"id": "item-07", "size": [91, 50, 40]},
            {"id": "item-08", "size": [106, 61, 56]},
            {"id": "item-09", "size": [103, 63, 58]},
            {"id": "item-10", "size": [75, 57, 41]},
            {"id": "item-11", "size": [71, 68, 64]},
            {"id": "item-12", "size": [85, 67, 39]},
            {"id": "item-13", "size": [97, 63, 56]},
            {"id": "item-14", "size": [61, 48, 30]},
            {"id": "item-15", "size": [80, 54, 35]},
        ], "items_num": [6, 6, 15, 8, 6, 7, 12, 10, 8, 11, 6, 14, 9, 11, 9]},
        {"items_set": [
            {"id": "item-01", "size": [113, 92, 33]},
            {"id": "item-02", "size": [52, 37, 28]},
            {"id": "item-03", "size": [57, 33, 29]},
            {"id": "item-04", "size": [99, 37, 30]},
            {"id": "item-05", "size": [92, 64, 33]},
            {"id": "item-06", "size": [119, 59, 39]},
            {"id": "item-07", "size": [54, 52, 49]},
            {"id": "item-08", "size": [75, 45, 35]},
            {"id": "item-09", "size": [79, 68, 44]},
            {"id": "item-10", "size": [116, 49, 47]},
            {"id": "item-11", "size": [83, 44, 23]},
            {"id": "item-12", "size": [98, 96, 56]},
            {"id": "item-13", "size": [78, 72, 57]},
            {"id": "item-14", "size": [98, 88, 47]},
            {"id": "item-15", "size": [41, 33, 31]},
        ], "items_num": [8, 12, 5, 12, 9, 12, 8, 6, 12, 9, 11, 10, 8, 9, 13]},
    ]

    k = 23
    items = []
    for i in range(len(items_info[k]["items_set"])):
        for j in range(items_info[k]["items_num"][i]
                       ):
            items.append(copy.deepcopy(items_info[k]["items_set"][i]))

    print(ethnic_iteration(items, x, y, z, 20, 0.7, 0.05, 100))

