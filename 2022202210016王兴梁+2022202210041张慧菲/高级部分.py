# 设车厢为长方形，其长宽高分别为L，W，H；共有n个箱子
# 箱子也为长方形，第i个箱子的长宽高为li，wi，hi（n个箱子的体积总和是要远远大于车厢的体积）
import random
import numpy as np
import pandas as pd
import datetime
import time
import datetime

def judge_empty(L, W, H, carriage, l0, w0, h0, l1, w1, h1):  # 判断位置（l0,w0,h0)是否空余（l1,w1,h1)
    # print('judge empty')
    for i in range(l0, l0 + l1):
        for j in range(w0, w0 + w1):
            for k in range(h0, h0 + h1):
                if (i > L - 1):
                    return False
                if (j > W - 1):
                    return False
                if (k > H - 1):
                    return False
                # print('i:',i,'  j:',j,'  k:',k)
                if (carriage[i][j][k] == 1):
                    return False
    return True


def addi(L, W, H, carriage, i, j, k, max):
    for m in range(i, max):
        if (carriage[m][j][k] == 0):
            return m - 1
    return L - 1


def addj(L, W, H, carriage, i, j, k, max):
    for m in range(j, max):
        if (carriage[i][m][k] == 0):
            return m - 1
    return W - 1


def addk(L, W, H, carriage, i, j, k, max):
    for m in range(k, max):
        if (carriage[i][j][m] == 0):
            return m - 1
    return H - 1


def find_position(L, W, H, carriage, l, w, h,l_last,w_last,h_last):
    # print('findpos')
    if (l > L):
        return [-1, -1, -1]
    if (w > W):
        return [-1, -1, -1]
    if (h > H):
        return [-1, -1, -1]
    back0=0
    if (l_last+l>L):
        back0=1
    if (w_last + w > W):
        back0 = 1
    if (h_last+h>H):
        back0=1
    if(back0==0):
        for i in range(l_last, L - l):
            for j in range(w_last, W - w):
                for k in range(h_last, H - h):
                    # 定位到了具体存放的点
                    if (judge_empty(L, W, H, carriage, i, j, k, l, w, h)):
                        # 这个位置可以放
                        return i, j, k
    else:
        for i in range(L - l):
            for j in range(W - w):
                for k in range(H - h):
                    # 定位到了具体存放的点
                    if (judge_empty(L, W, H, carriage, i, j, k, l, w, h)):
                        # 这个位置可以放
                        return i, j, k
    return -1, -1, -1

#L=int(input('请输入车厢的长：'))
#W=int(input('请输入车厢的宽：'))
#H=int(input('请输入车厢的高：'))
L=587
W=233
H=220
# 标记箱子放入车厢里OR没放入车厢
mark = []
# 标记箱子放的位置
position = []
print(position)
# 用一个三维空间矩阵表示车厢使用情况
carriage = np.zeros((L, W, H))
# 车厢容量
carriage_capacity = L * H * W
# 车厢使用的容量
carriage_capacity_used = 0
# 车厢剩余容量
carriage_capacity_rest = L * H * W
# 对箱子容量进行排序
boxes_capacity = []
l_last, w_last, h_last=0,0,0
while(1):
    print()
    l = int(input('请输入箱子的长(-1退出)：'))
    if (l == -1):
        break
    h = int(input('请输入箱子的宽(-1退出)：'))
    if (h == -1):
        break
    w = int(input('请输入箱子的高(-1退出)：'))
    if (w == -1):
        break

    starttime=  time.time()
    capacity = l * w * h
    if (capacity > carriage_capacity_rest):  # 该箱子容量>车厢剩余容量
        print('箱子太大，无法放入车厢')
        continue
    # 按长，宽，高来放
    p, q, r = find_position(L, W, H, carriage, l, w, h, l_last, w_last, h_last)
    if(p>-1):
        for TEMPi in range(p, p + l):
            for TEMPj in range(q, q + w):
                for TEMPk in range(r, r + h):
                    carriage[TEMPi][TEMPj][TEMPk] = 1

        mark.append(1)  # 正常放
        position.append([p, q, r])
        l_last, w_last, h_last = p + l, q + w, r + h
        carriage_capacity_used = carriage_capacity_used + capacity
        carriage_capacity_rest = carriage_capacity_rest - capacity
        print('放入箱子')
        print('剩余容量：', carriage_capacity_rest)
        print('已使用容量:', carriage_capacity_used)
        position[-1].append(mark[-1])
        endtime=  time.time()
        print('执行时间：',int(round(endtime * 1000))-int(round(starttime * 1000)),'毫秒')  # 毫秒级时间戳
        continue
    #按长，高，宽来放
    p, q, r = find_position(L, W, H, carriage, l, h, w, l_last, w_last, h_last)
    if (p > -1):
        for TEMPi in range(p, p + l):
            for TEMPj in range(q, q + h):
                for TEMPk in range(r, r + w):
                    carriage[TEMPi][TEMPj][TEMPk] = 1

        mark.append(1)  # 正常放
        position.append([p, q, r])
        l_last, w_last, h_last = p + l, q + h, r + w
        carriage_capacity_used = carriage_capacity_used + capacity
        carriage_capacity_rest = carriage_capacity_rest - capacity
        print('放入箱子')
        print('剩余容量：', carriage_capacity_rest)
        print('已使用容量:', carriage_capacity_used)
        position[-1].append(mark[-1])
        print('hhhh:',(endtime-starttime).seconds)
        continue
    #按宽，长，高来放
    p, q, r = find_position(L, W, H, carriage, w, l, h, l_last, w_last, h_last)
    if (p > -1):
        for TEMPi in range(p, p + w):
            for TEMPj in range(q, q + l):
                for TEMPk in range(r, r + h):
                    carriage[TEMPi][TEMPj][TEMPk] = 1

        mark.append(1)  # 正常放
        position.append([p, q, r])
        l_last, w_last, h_last = p + w, q + l, r + h
        carriage_capacity_used = carriage_capacity_used + capacity
        carriage_capacity_rest = carriage_capacity_rest - capacity
        print('放入箱子')
        print('剩余容量：', carriage_capacity_rest)
        print('已使用容量:', carriage_capacity_used)
        position[-1].append(mark[-1])
        endtime = time.time()
        print('执行时间：', int(round(endtime * 1000)) - int(round(starttime * 1000)), '毫秒')  # 毫秒级时间戳
        print()
        continue
    #按宽，高，长来放
    p, q, r = find_position(L, W, H, carriage,  w, h,l, l_last, w_last, h_last)
    if (p > -1):
        for TEMPi in range(p, p + w):
            for TEMPj in range(q, q + h):
                for TEMPk in range(r, r + l):
                    carriage[TEMPi][TEMPj][TEMPk] = 1

        mark.append(1)  # 正常放
        position.append([p, q, r])
        l_last, w_last, h_last = p + w, q + h, r + l
        carriage_capacity_used = carriage_capacity_used + capacity
        carriage_capacity_rest = carriage_capacity_rest - capacity
        print('放入箱子')
        print('剩余容量：', carriage_capacity_rest)
        print('已使用容量:', carriage_capacity_used)
        position[-1].append(mark[-1])
        endtime = time.time()
        print('执行时间：', int(round(endtime * 1000)) - int(round(starttime * 1000)), '毫秒')  # 毫秒级时间戳
        print()
        continue
    #按高，长，宽来放
    p, q, r = find_position(L, W, H, carriage, h, l, w, l_last, w_last, h_last)
    if (p > -1):
        for TEMPi in range(p, p + h):
            for TEMPj in range(q, q + l):
                for TEMPk in range(r, r + w):
                    carriage[TEMPi][TEMPj][TEMPk] = 1

        mark.append(1)  # 正常放
        position.append([p, q, r])
        l_last, w_last, h_last = p + h, q + l, r + w
        carriage_capacity_used = carriage_capacity_used + capacity
        carriage_capacity_rest = carriage_capacity_rest - capacity
        print('放入箱子')
        print('剩余容量：', carriage_capacity_rest)
        print('已使用容量:', carriage_capacity_used)
        position[-1].append(mark[-1])
        endtime = time.time()
        print('执行时间：', int(round(endtime * 1000)) - int(round(starttime * 1000)), '毫秒')  # 毫秒级时间戳
        print()
        continue
    #按高，宽，长来放
    p, q, r = find_position(L, W, H, carriage, h, w, l, l_last, w_last, h_last)
    if (p > -1):
        for TEMPi in range(p, p + h):
            for TEMPj in range(q, q + w):
                for TEMPk in range(r, r + l):
                    carriage[TEMPi][TEMPj][TEMPk] = 1

        mark.append(1)  # 正常放
        position.append([p, q, r])
        l_last, w_last, h_last = p + h, q + w, r + l
        carriage_capacity_used = carriage_capacity_used + capacity
        carriage_capacity_rest = carriage_capacity_rest - capacity
        print('放入箱子')
        print('剩余容量：', carriage_capacity_rest)
        print('已使用容量:', carriage_capacity_used)
        position[-1].append(mark[-1])
        endtime = time.time()
        print('执行时间：', int(round(endtime * 1000)) - int(round(starttime * 1000)), '毫秒')  # 毫秒级时间戳
        print()
        continue
    print('无法放入箱子')
    print('剩余容量：', carriage_capacity_rest)
    print('已使用容量:', carriage_capacity_used)
    print('容量使用率：', carriage_capacity_used / carriage_capacity)
    endtime = time.time()
    print('执行时间：', int(round(endtime * 1000)) - int(round(starttime * 1000)), '毫秒')  # 毫秒级时间戳
    print()




