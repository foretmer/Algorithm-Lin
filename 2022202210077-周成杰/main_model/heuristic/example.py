#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from packer import *
from constants import *
from methods import *
from item import *
from bin import *
from time import time
from random import shuffle

for run in range(10):
    packer = Packer()
    packer.add_bin(Bin("C", 587, 233, 220))
    item = []
    for i in range(22):
        item.append([49, 25, 21])
    for i in range(22):
        item.append([60, 51, 41])
    for i in range(28):
        item.append([103, 76, 64])
    for i in range(25):
        item.append([95, 70, 62])
    for i in range(17):
        item.append([111, 49, 26])
    s = [x for x in range(0, len(item))]
    shuffle(s)
    print(s)
    for i in s:
        packer.add_item(Item(i, item[i][0], item[i][1], item[i][2]))
    all_item = len(item)
    start_time = time()
    packer.pack()
    over_time = time()
    print('time: ',(over_time - start_time) / all_item)