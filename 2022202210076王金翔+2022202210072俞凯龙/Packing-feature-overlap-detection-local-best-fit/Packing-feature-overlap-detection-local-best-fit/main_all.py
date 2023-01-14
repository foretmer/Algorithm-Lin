# This is a sample Python script.

import time

from Container import Container
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from box.BoxManager import BoxManager

Box_Type_entered = int(input("Please enter Box Type(3,5,8,10,15):"))


def Init3(l1, w1, h1, n1, l2, w2, h2, n2, l3, w3, h3, n3, lc=587, wc=233, hc=220):
    manager = BoxManager(). \
        add_box_type(l1, w1, h1, n1). \
        add_box_type(l2, w2, h2, n2). \
        add_box_type(l3, w3, h3, n3)
    container = Container(lc, wc, hc)

    return manager, container


def Init5(l1, w1, h1, n1, l2, w2, h2, n2, l3, w3, h3, n3,
          l4, w4, h4, n4, l5, w5, h5, n5, lc=587, wc=233, hc=220):
    manager = BoxManager(). \
        add_box_type(l1, w1, h1, n1). \
        add_box_type(l2, w2, h2, n2). \
        add_box_type(l3, w3, h3, n3). \
        add_box_type(l4, w4, h4, n4). \
        add_box_type(l5, w5, h5, n5)
    container = Container(lc, wc, hc)

    return manager, container


def Init8(l1, w1, h1, n1, l2, w2, h2, n2, l3, w3, h3, n3,
          l4, w4, h4, n4, l5, w5, h5, n5, l6, w6, h6, n6,
          l7, w7, h7, n7, l8, w8, h8, n8, lc=587, wc=233, hc=220):
    manager = BoxManager(). \
        add_box_type(l1, w1, h1, n1). \
        add_box_type(l2, w2, h2, n2). \
        add_box_type(l3, w3, h3, n3). \
        add_box_type(l4, w4, h4, n4). \
        add_box_type(l5, w5, h5, n5). \
        add_box_type(l6, w6, h6, n6). \
        add_box_type(l7, w7, h7, n7). \
        add_box_type(l8, w8, h8, n8)
    container = Container(lc, wc, hc)

    return manager, container


def Init10(l1, w1, h1, n1, l2, w2, h2, n2, l3, w3, h3, n3,
           l4, w4, h4, n4, l5, w5, h5, n5, l6, w6, h6, n6,
           l7, w7, h7, n7, l8, w8, h8, n8, l9, w9, h9, n9,
           l10, w10, h10, n10, lc=587, wc=233, hc=220):
    manager = BoxManager(). \
        add_box_type(l1, w1, h1, n1). \
        add_box_type(l2, w2, h2, n2). \
        add_box_type(l3, w3, h3, n3). \
        add_box_type(l4, w4, h4, n4). \
        add_box_type(l5, w5, h5, n5). \
        add_box_type(l6, w6, h6, n6). \
        add_box_type(l7, w7, h7, n7). \
        add_box_type(l8, w8, h8, n8). \
        add_box_type(l9, w9, h9, n9). \
        add_box_type(l10, w10, h10, n10)
    container = Container(lc, wc, hc)

    return manager, container


def Init15(l1, w1, h1, n1, l2, w2, h2, n2, l3, w3, h3, n3,
           l4, w4, h4, n4, l5, w5, h5, n5, l6, w6, h6, n6,
           l7, w7, h7, n7, l8, w8, h8, n8, l9, w9, h9, n9,
           l10, w10, h10, n10, l11, w11, h11, n11, l12, w12, h12, n12,
           l13, w13, h13, n13, l14, w14, h14, n14, l15, w15, h15, n15, lc=587, wc=233, hc=220):
    manager = BoxManager(). \
        add_box_type(l1, w1, h1, n1). \
        add_box_type(l2, w2, h2, n2). \
        add_box_type(l3, w3, h3, n3). \
        add_box_type(l4, w4, h4, n4). \
        add_box_type(l5, w5, h5, n5). \
        add_box_type(l6, w6, h6, n6). \
        add_box_type(l7, w7, h7, n7). \
        add_box_type(l8, w8, h8, n8). \
        add_box_type(l9, w9, h9, n9). \
        add_box_type(l10, w10, h10, n10). \
        add_box_type(l11, w11, h11, n11). \
        add_box_type(l12, w12, h12, n12). \
        add_box_type(l13, w13, h13, n13). \
        add_box_type(l14, w14, h14, n14). \
        add_box_type(l15, w15, h15, n15)
    container = Container(lc, wc, hc)

    return manager, container


def run(manager, container, group, index):
    while (not container.is_full) and (not manager.is_out_of_box):
        box = manager.get_box()
        if box is not None:
            if not container.add_box_if_available(box):
                manager.remove_box_type(box.type_id)
                if manager.is_repository_empty():
                    container.is_full = True
                    endtime = container.end(group, index)
        else:
            endtime = container.end(group, index)
    return endtime


# 3 box types
Box_3 = [[108, 76, 30, 40, 110, 43, 25, 33, 92, 81, 55, 39],
         [91, 54, 45, 32, 105, 77, 72, 24, 79, 78, 48, 30],
         [91, 54, 45, 32, 105, 77, 72, 24, 79, 78, 48, 31],
         [60, 40, 32, 64, 98, 75, 55, 40, 60, 59, 39, 64],
         [78, 37, 27, 63, 89, 70, 25, 52, 90, 84, 41, 55]]

Box_5 = [[108, 76, 30, 24, 110, 43, 25, 7, 92, 81, 55, 22, 81, 33, 28, 13, 120, 99, 73, 15],
         [49, 25, 21, 22, 60, 51, 41, 22, 103, 76, 64, 28, 95, 70, 62, 25, 111, 49, 26, 17],
         [88, 54, 39, 25, 94, 54, 36, 27, 87, 77, 43, 21, 100, 80, 72, 20, 83, 40, 36, 24],
         [90, 70, 63, 16, 84, 78, 28, 28, 94, 85, 39, 20, 80, 76, 54, 23, 69, 50, 45, 31],
         [108, 76, 30, 24, 110, 43, 25, 7, 92, 81, 55, 22, 81, 33, 28, 13, 120, 99, 73, 16]]

Box_8 = [
    [108, 76, 30, 24, 110, 43, 25, 7, 92, 81, 55, 22, 81, 33, 28, 13, 120, 99, 73, 15, 111, 70, 48, 10, 98, 72, 46, 12,
     95, 66, 31, 9],
    [97, 81, 27, 10, 102, 78, 39, 20, 113, 46, 36, 18, 66, 50, 42, 21, 101, 30, 26, 16, 100, 56, 35, 17, 91, 50, 40, 22,
     106, 61, 56, 19],
    [88, 54, 39, 16, 94, 54, 36, 14, 87, 77, 43, 20, 100, 80, 72, 16, 83, 40, 36, 6, 91, 54, 22, 15, 109, 58, 54, 17,
     94, 55, 30, 9],
    [49, 25, 21, 16, 60, 51, 41, 8, 103, 76, 64, 16, 95, 70, 62, 18, 111, 49, 26, 18, 85, 84, 72, 16, 48, 36, 31, 17,
     86, 76, 38, 6],
    [113, 92, 33, 23, 52, 37, 28, 22, 57, 33, 29, 26, 99, 37, 30, 17, 92, 64, 33, 23, 119, 59, 39, 26, 54, 52, 49, 18,
     75, 45, 35, 30]]

Box_10 = [
    [49, 25, 21, 13, 60, 51, 41, 9, 103, 76, 64, 11, 95, 70, 62, 14, 111, 49, 26, 13, 85, 84, 72, 16, 48, 36, 31, 12,
     86, 76, 38, 11, 71, 48, 47, 16, 90, 43, 33, 8],
    [97, 81, 27, 8, 102, 78, 39, 16, 113, 46, 36, 12, 66, 50, 42, 12, 101, 30, 26, 18, 100, 56, 35, 13, 91, 50, 40, 14,
     106, 61, 56, 17, 103, 63, 58, 12, 75, 57, 41, 13],
    [86, 84, 45, 18, 81, 45, 34, 19, 70, 54, 37, 13, 71, 61, 52, 16, 78, 73, 40, 10, 69, 63, 46, 13, 72, 67, 56, 10, 75,
     75, 36, 8, 94, 88, 50, 12, 65, 51, 50, 13],
    [113, 92, 33, 15, 52, 37, 28, 17, 57, 33, 29, 17, 99, 37, 30, 19, 92, 64, 33, 13, 119, 59, 39, 19, 54, 52, 49, 13,
     75, 45, 35, 21, 79, 68, 44, 13, 116, 49, 47, 22],
    [118, 79, 51, 16, 86, 32, 31, 8, 64, 58, 52, 14, 42, 42, 32, 14, 64, 55, 43, 16, 84, 70, 35, 10, 76, 57, 36, 14, 95,
     60, 55, 14, 80, 66, 52, 14, 109, 73, 23, 18]]

Box_15 = [
    [98, 73, 44, 6, 60, 60, 38, 7, 105, 73, 60, 10, 90, 77, 52, 3, 66, 58, 24, 5, 106, 76, 55, 10, 55, 44, 36, 12, 82,
     58, 23, 7, 74, 61, 58, 6, 81, 39, 24, 8, 71, 65, 39, 11, 105, 97, 47, 4, 114, 97, 69, 5, 103, 78, 55, 6, 93, 66,
     55, 6],
    [108, 76, 30, 12, 110, 43, 25, 12, 92, 81, 55, 6, 81, 33, 28, 9, 120, 99, 73, 5, 111, 70, 48, 12, 98, 72, 46, 9, 95,
     66, 31, 10, 85, 84, 30, 8, 71, 32, 25, 3, 36, 34, 25, 10, 97, 67, 62, 7, 33, 25, 23, 7, 95, 27, 26, 10, 94, 81, 44,
     9],
    [49, 25, 21, 13, 60, 51, 41, 9, 103, 76, 64, 8, 95, 70, 62, 6, 111, 49, 26, 10, 74, 42, 40, 4, 85, 84, 72, 10, 48,
     36, 31, 10, 86, 76, 38, 12, 71, 48, 47, 14, 90, 43, 33, 9, 98, 52, 44, 9, 73, 37, 23, 10, 61, 48, 39, 14, 75, 75,
     63, 11],
    [97, 81, 27, 6, 102, 78, 39, 6, 113, 46, 36, 15, 66, 50, 42, 8, 101, 30, 26, 6, 100, 56, 35, 7, 91, 50, 40, 12, 106,
     61, 56, 10, 103, 63, 58, 8, 75, 57, 41, 11, 71, 68, 64, 6, 85, 67, 39, 14, 97, 63, 56, 9, 61, 48, 30, 11, 80, 54,
     35, 9],
    [113, 92, 33, 8, 52, 37, 28, 12, 57, 33, 29, 5, 99, 37, 30, 12, 92, 64, 33, 9, 119, 59, 39, 12, 54, 52, 49, 8, 75,
     45, 35, 6, 79, 68, 44, 12, 116, 49, 47, 9, 83, 44, 23, 11, 98, 96, 56, 10, 78, 72, 57, 8, 98, 88, 47, 9, 41, 33,
     31, 13]]

if Box_Type_entered == 3:
    for i in Box_3:
        manager, container = Init3(i[0], i[1], i[2], i[3],
                                   i[4], i[5], i[6], i[7],
                                   i[8], i[9], i[10], i[11])
        starttime = time.time()
        endtime = run(manager, container, 3, Box_3.index(i) + 1)
        print("Time cost:" + str(endtime - starttime) + "s\n\n")

elif Box_Type_entered == 5:
    for i in Box_5:
        manager, container = Init5(i[0], i[1], i[2], i[3],
                                   i[4], i[5], i[6], i[7],
                                   i[8], i[9], i[10], i[11],
                                   i[12], i[13], i[14], i[15],
                                   i[16], i[17], i[18], i[19])
        starttime = time.time()
        endtime = run(manager, container, 5, Box_5.index(i) + 1)
        print("Time cost:" + str(endtime - starttime) + "s\n\n")
elif Box_Type_entered == 8:
    for i in Box_8:
        manager, container = Init8(i[0], i[1], i[2], i[3],
                                   i[4], i[5], i[6], i[7],
                                   i[8], i[9], i[10], i[11],
                                   i[12], i[13], i[14], i[15],
                                   i[16], i[17], i[18], i[19],
                                   i[20], i[21], i[22], i[23],
                                   i[24], i[25], i[26], i[27],
                                   i[28], i[29], i[30], i[31])
        starttime = time.time()
        endtime = run(manager, container, 8, Box_8.index(i) + 1)
        print("Time cost:" + str(endtime - starttime) + "s\n\n")
elif Box_Type_entered == 10:
    for i in Box_10:
        manager, container = Init10(i[0], i[1], i[2], i[3],
                                    i[4], i[5], i[6], i[7],
                                    i[8], i[9], i[10], i[11],
                                    i[12], i[13], i[14], i[15],
                                    i[16], i[17], i[18], i[19],
                                    i[20], i[21], i[22], i[23],
                                    i[24], i[25], i[26], i[27],
                                    i[28], i[29], i[30], i[31],
                                    i[32], i[33], i[34], i[35],
                                    i[36], i[37], i[38], i[39])
        starttime = time.time()
        endtime = run(manager, container, 10, Box_10.index(i) + 1)
        print("Time cost:" + str(endtime - starttime) + "s\n\n")
elif Box_Type_entered == 15:
    for i in Box_15:
        manager, container = Init15(i[0], i[1], i[2], i[3],
                                    i[4], i[5], i[6], i[7],
                                    i[8], i[9], i[10], i[11],
                                    i[12], i[13], i[14], i[15],
                                    i[16], i[17], i[18], i[19],
                                    i[20], i[21], i[22], i[23],
                                    i[24], i[25], i[26], i[27],
                                    i[28], i[29], i[30], i[31],
                                    i[32], i[33], i[34], i[35],
                                    i[36], i[37], i[38], i[39],
                                    i[40], i[41], i[42], i[43],
                                    i[44], i[45], i[46], i[47],
                                    i[48], i[49], i[50], i[51],
                                    i[52], i[53], i[54], i[55],
                                    i[56], i[57], i[58], i[59])
        starttime = time.time()
        endtime = run(manager, container, 15, Box_15.index(i) + 1)
        print("Time cost:" + str(endtime - starttime) + "s\n\n")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
