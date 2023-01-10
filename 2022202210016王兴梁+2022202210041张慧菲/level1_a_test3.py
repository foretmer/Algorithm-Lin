# 设车厢为长方形，其长宽高分别为L，W，H；共有n个箱子
# 箱子也为长方形，第i个箱子的长宽高为li，wi，hi（n个箱子的体积总和是要远远大于车厢的体积）
import random
import numpy as np
import pandas as pd
from openpyxl import load_workbook


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


def find_position(L, W, H, carriage, l, w, h, l_last, w_last, h_last):
    # print('findpos')
    if (l > L):
        return [-1, -1, -1]
    if (w > W):
        return [-1, -1, -1]
    if (h > H):
        return [-1, -1, -1]
    for i in range(l_last, L - l):
        for j in range(w_last, W - w):
            for k in range(h_last, H - h):
                # 定位到了具体存放的点
                if (judge_empty(L, W, H, carriage, i, j, k, l, w, h)):
                    # 这个位置可以放
                    return i, j, k
                '''else:
                    i=addi(i,j,k,L-l)
                    j=addj(i,j,k,W-w)
                    k=addk(i,j,k,H-h)'''
    for i in range(L - l):
        for j in range(W - w):
            for k in range(H - h):
                # 定位到了具体存放的点
                if (judge_empty(L, W, H, carriage, i, j, k, l, w, h)):
                    # 这个位置可以放
                    return i, j, k
    return -1, -1, -1


sheet_name = ['Sheet1', 'Sheet2', 'Sheet3', 'Sheet4', 'Sheet5']
path2 = r'D:\python\高级算法\result.xlsx'

writer = pd.ExcelWriter(path2)
# writer = pd.ExcelWriter(path2,mode='a',if_sheet_exists='replace',engine='openpyxl')




def main(L, W, H, n, boxes, rows, count,name):
    # 标记箱子放入车厢里OR没放入车厢
    # 初始化为全0
    mark = [0] * n
    # 标记箱子放的位置
    position = [[-1, -1, -1]] * n
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
    for i in range(n):
        boxes_capacity.append(boxes[i][0] * boxes[i][1] * boxes[i][2])
    # 排序
    for i in range(n):
        for j in range(n - i - 1):
            if boxes_capacity[j] < boxes_capacity[j + 1]:
                boxes_capacity[j], boxes_capacity[j + 1] = boxes_capacity[j + 1], boxes_capacity[j]
                boxes[j], boxes[j + 1] = boxes[j + 1], boxes[j]
    l_last, w_last, h_last = 0, 0, 0
    df2 = pd.DataFrame(columns=['长', '宽', '高'], data=boxes)
    df2.to_excel(writer, index=True, header=True, startrow=3, startcol=6 * count, sheet_name=sheet_name[rows])
    writer.save()

