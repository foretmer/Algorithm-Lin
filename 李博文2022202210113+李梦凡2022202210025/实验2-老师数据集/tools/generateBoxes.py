import sys
sys.path.append("../tools/")
from box import Box
import random

# 三种箱子
E1_1 = [(108 ,76,30, 40), (110 ,43, 25, 33), (92, 81 ,55, 39)]
E1_2 = [(91 ,54 ,45 ,32), (105 ,77 ,72, 24), (79, 78 ,48 ,30)]
E1_3 = [(91 ,54 ,45 ,32), (105 ,77 ,72 ,24), (79 ,78 ,48, 30)]
E1_4 = [(60 ,40 ,32 ,64), (98, 75 ,55, 40), (60 ,59 ,39 ,64)]
E1_5 = [(78 ,37 ,27 ,63), (89 ,70 ,25 ,52), (90, 84 ,41 ,55)]

# 五种箱子
E2_1 = [(108 ,76 ,30 ,24), (110 ,43, 25 ,7), (92, 81, 55, 22), (81 ,33 ,28 ,13), (120, 99, 73 ,15)]
E2_2 = [(49 ,25 ,21 ,22), (60 ,51 ,41 ,22), (103, 76, 64, 28), (95, 70, 62, 25), (111, 49, 26 ,17)]
E2_3 = [(88 ,54 ,39 ,25), (94 ,54 ,36 ,27), (87, 77, 43, 21), (100, 80 ,72 ,20), (83 ,40, 36 ,24)]
E2_4 = [(90 ,70 ,63 ,16), (84 ,78 ,28 ,28), (94 ,85 ,39 ,20), (80 ,76 ,54 ,23), (69 ,50, 45, 31)]
E2_5 = [(74 ,63 ,61 ,22), (71 ,60 ,25 ,12), (106 ,80 ,59 ,25), (109 ,76 ,42, 24), (118 ,56 ,22 ,11)]

# 8种箱子
E3_1 = [(108,76,30,24), (110,43,25,9), (92,81,55,8), (81,33,28,11), (120,99,73,11),(111,70,48,10), (98,72,46,12), (95,66,31,9)]
E3_2 = [(97,81,27,10), (102,78,39,20), (113,46,36,18), (66,50,42,21), (101,30,26,16),(100,56,35,17), (91,50,40,22), (106,61,56,19)]
E3_3 = [(88,54,39,16), (94,54,36,14), (87,77,43,20), (100,80,72,16), (83,40,36,6),(91,54,22,15), (109,58,54,17), (94,55,30,9)]
E3_4 = [(49,25,21,16), (60,51,41,8), (103,76,64,16), (95,70,62,18), (111,49,26,18),(85,84,72,16), (48,36,31,17), (86,76,38,6)]
E3_5 = [(113,92,33,23), (52,37,28,22), (57,33,29,26), (99,37,30,17), (92,64,33,23),(119,59,39,26), (54,52,49,18), (75,45,35,30)]

# 10种箱子
E4_1 = [(49,25,21,13), (60,51,41,9), (103,76,64,11), (95,70,62,14), (111,49,26,13),(85,84,72,16), (48,36,31,12), (86,76,38,11), (71,48,47,16), (90,43,33,8)]
E4_2 = [(97,81,27,8), (102,78,39,16), (113,46,36,12), (66,50,42,12), (101,30,26,18),(100,56,35,13), (91,50,40,14), (106,61,56,17), (103,63,58,12), (75,57,41,13)]
E4_3 = [(86,84,45,18), (81,45,34,19), (70,54,37,13), (71,61,52,16), (78,73,40,10),(69,63,46,13), (72,67,56,10), (75,75,36,8), (94,88,50,12), (65,51,50,13)]
E4_4 = [(113,92,33,15), (52,37,28,17), (57,33,29,17), (99,37,30,19), (92,64,33,13),(119,59,39,19), (54,52,49,13), (75,45,35,21), (79,68,44,13), (116,49,47,22)]
E4_5 = [(118,79,51,16), (86,32,31,8), (64,58,52,14), (42,42,32,14), (64,55,43,16),(84,70,35,10), (76,57,36,14), (95,60,55,14), (80,66,52,14), (109,73,23,18)]

# 15种箱子
E5_1 = [(98,73,44,6), (60,60,38,7), (105,73,60,10), (90,77,52,3), (66,58,24,5), (106,76,55,10), (55,44,36,12), (82,58,23,7), (74,61,58,6), (81,39,24,8), (71,65,39,11), (105,97,47,4), (114,97,69,5), (103,78,55,6), (93,66,55,6)]
E5_2 = [(108,76,30,12), (110,43,25,12), (92,81,55,6), (81,33,28,9), (120,99,73,5), (111,70,48,12), (98,72,46,9), (95,66,31,10), (85,84,30,8), (71,32,25,3), (36,34,25,10), (97,67,62,7), (33,25,23,7), (95,27,26,10), (94,81,44,9)]
E5_3 = [(49,25,21,13), (60,51,41,9), (103,76,64,8), (95,70,62,6), (111,49,26,10), (74,42,40,4), (85,84,72,10), (48,36,31,10), (86,76,38,12), (71,48,47,14), (90,43,33,9), (98,52,44,9), (73,37,23,10), (61,48,39,14), (75,75,63,11)]
E5_4 = [(97,81,27,6), (102,78,39,6), (113,46,36,15), (66,50,42,8), (101,30,26,6), (100,56,35,7), (91,50,40,12), (106,61,56,10), (103,63,58,8), (75,57,41,11), (71,68,64,6), (85,67,39,14), (97,63,56,9), (61,48,30,11), (80,54,35,9)]
E5_5 = [(113,92,33,8), (52,37,28,12), (57,33,29,5), (99,37,30,12), (92,64,33,9), (119,59,39,12), (54,52,49,8), (75,45,35,6), (79,68,44,12), (116,49,47,9), (83,44,23,11), (98,96,56,10), (78,72,57,8), (98,88,47,9), (41,33,31,13)]

def generateBoxes(box_type):
    if (box_type == 1):
            box_shapes = random.choice([E1_1, E1_2, E1_3, E1_4, E1_5])
    elif box_type == 2:
            box_shapes = random.choice([E2_1, E2_2, E2_3, E2_4, E2_5])
    elif box_type == 3:
            box_shapes = random.choice([E3_1, E3_2, E3_3, E3_4, E3_5])
    elif box_type == 4:
            box_shapes = random.choice([E4_1, E4_2, E4_3, E4_4, E4_5])
    elif box_type == 5:
            box_shapes = random.choice([E5_1, E5_2, E5_3, E5_4, E5_5])
    else:
            print("unknown box_type")

    print('choose box shapes: {}'.format(box_shapes))
    boxes = []
    for box_shape in box_shapes:
        (l, w, h, n) = box_shape
        for i in range(n):
            boxes.append(Box(l, w, h))

    return boxes


if __name__ =='__main__':
    boxes = generateBoxes(1)
    for box in boxes:
        print(box)