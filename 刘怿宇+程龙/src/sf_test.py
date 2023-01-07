import numpy as np
import time
import random
from sf import *
from sf_auxiliary import C, Bs

def judge(C, B, random_order=False, random_float=False):
    packer = Packer()

    C = (C[1], C[2], C[0])
    B = [(i[1], i[2], i[0], i[3]) for i in B]

    items = []
    for tmp in B:
        for _ in range(tmp[3]):
            items.append((tmp[0], tmp[1], tmp[2]))
    items_count = len(items)
    items_volumes = 0
    if random_order:
        items_order = random.sample(range(0, items_count), items_count)   # 生成一个items_count长的随机序列
    else:
        items_order = list(range(0, items_count))

    stime = time.time()
    packer.add_bin(Bin('box', C[0], C[1], C[2], 0xff))
    for index in range(items_count):
        item = items[items_order[index]]  # 按照items_order的顺序选一个物品进行加入

        if random_float:
            tmp_item = Item('[item type]'.format(index), item[0] + round(random.uniform(-1, 1), 2), item[1] + round(random.uniform(-1, 1), 2), item[2] + round(random.uniform(-1, 1), 2), 1)
        else:
            tmp_item = Item('[item type]'.format(index), item[0], item[1], item[2], 1)
        packer.add_item(tmp_item)
        items_volumes += tmp_item.get_volume()

    packer.pack(bigger_first=True)
    etime = time.time()

    bin = packer.bins[0]
    total_vol = bin.get_volume()
    used_vol = 0
    for item in bin.items:
        used_vol += item.get_volume()
    
    used_percent = round(used_vol / total_vol, 2)
    max_used_percent = round(items_volumes / total_vol, 2)
    used_time = round(etime - stime, 2)
    return used_percent, max_used_percent, used_time

for category in Bs:
    B = Bs[category]
    print(category)

    # 用随机顺序来模拟随机到达
    random_order = True
    # 用随机的(-1, 1)之间的两位小数来模拟数据不为整数的情况
    random_float = True
    # 测试次数
    test_count = 10

    # 基础部分
    # random_order, random_float, test_count = False, False, 1

    useds = []
    maxs = []
    times = []
    for _ in range(test_count):
        used_percent, max_used_percent, used_time = judge(C, B, random_order, random_float)
        
        useds.append(used_percent)
        maxs.append(max_used_percent)
        times.append(used_time)

    average_used_percent = np.mean(useds)
    average_max_used_percent = np.mean(maxs)
    average_used_time = np.mean(times)
    print("{}".format(average_used_percent))
    print("{}s".format(round(average_used_time, 2)))
    print()
    
    # print(times)
    # exit()