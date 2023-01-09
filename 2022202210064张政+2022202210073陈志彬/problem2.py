from copy import deepcopy
import matplotlib.pyplot as plt
import visualize as vis
import time
import os
plt.rcParams['font.sans-serif']=['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False  # 用来正常显示负号


# 读取数据
def load_data():
    problem_list = {}
    with open('data.txt', encoding='utf-8', mode='r') as f:
        index = 0
        while True:
            line = f.readline()
            if not line:
                break
            if len(line) == 2 or len(line) == 3:
                for i in range(5):
                    sub_problem_list = {}
                    truck = f.readline()
                    truck = truck.strip("\n|(|) |'C'").split(' ')
                    truck = list(int(i) for i in truck)
                    box_list = []
                    boxes = f.readline()
                    boxes = boxes.strip("\n|'B'").split(',')
                    for _ in boxes:
                        box = _.strip("[ |( |) |] | [| ]| (| )").split(' ')
                        box = list(int(i) for i in box)
                        box_list.append(box)
                    sub_problem_list['truck dimension'] = truck
                    sub_problem_list['boxes'] = box_list
                    problem_list[str(index * 5 + i)] = sub_problem_list
                index = index + 1
    return problem_list


a = 0.1
problem_list = load_data()
problem_indices = list(problem_list.keys())
loca = time.strftime("%Y-%m-%d-%H-%M-%S")
new_dir_path = r'./results/p2_' + loca
if not os.path.exists(new_dir_path):
    os.mkdir(new_dir_path)
for p_ind in problem_indices:  # 对每个实例
    print("----------第{}个实例----------".format(int(p_ind)+1))
    # 数据预处理
    truck_dimension = problem_list[p_ind]['truck dimension']  # 车厢尺寸
    boxes = problem_list[p_ind]['boxes']  # 箱子尺寸
    box_candit = []
    for candit in boxes:
        vol = candit[0] * candit[1] * candit[2]
        for i in range(candit[3]):  # 数量
            box_candit.append([candit[0], candit[1], candit[2], vol])  # 长、宽、高、体积
    boxes = box_candit
    box_params = {}
    for index in range(len(boxes)):
        box_params[index] = boxes[index]
    print("实例的箱子数量：{}".format(len(boxes)))

    container_vol = truck_dimension[0] * truck_dimension[1] * truck_dimension[2]  # 集装箱容量
    dblf = [[0, 0, 0] + truck_dimension]  # 初始剩余空间
    occupied_vol = 0
    number_boxes = 0
    result = []
    ft = {}
    unpack_boxes = []
    time_start = time.time()
    # 对于按顺序来的每个箱子
    for ind, box in enumerate(boxes):
        box_vol = box[3]
        result_tmp = []  # [剩余空间，lwh，值]
        # 对于每种摆放顺序
        for r in range(6):
            if r == 0:
                l, w, h = box[0:3]
            elif r == 1:
                w, l, h = box[0:3]
            elif r == 2:
                l, h, w = box[0:3]
            elif r == 3:
                h, l, w = box[0:3]
            elif r == 4:
                h, w, l = box[0:3]
            else:
                w, h, l = box[0:3]
            for pos in dblf:  # 对于每个剩余空间
                space_vol = pos[3] * pos[4] * pos[5]  # 剩余空间
                if space_vol >= box_vol and pos[3] >= l and pos[4] >= w and pos[5] >= h:  # 剩余空间是否能容纳箱子
                    ft_v = -(pos[3] - l + a) * (pos[4] - w + a)  # 计算一个评价函数值
                    result_tmp.append(pos + [l, w, h] + [ft_v])  # 保存临时结果
        # 更新
        if 0 == len(result_tmp):  # 如果该箱子不能放置则丢弃
            unpack_boxes.append(ind+1)
        else:  # 所有可能放置结果中找出最好的放置结果
            occupied_vol += box_vol
            number_boxes += 1

            ft_vs = [i[-1] for i in result_tmp]
            best_r = result_tmp[ft_vs.index(max(ft_vs))]  # pos[0-5],l,w,h,ft_v
            pos = best_r[0:6]
            l, w, h = best_r[6], best_r[7], best_r[8]
            result.append(pos[0:3] + [l, w, h])  # 解的表示
            # 更新剩余空间，横向和纵向两种划分方式
            top_space = [pos[0], pos[1], pos[2] + h, l, w, pos[5] - h]
            if (pos[3] - l)*pos[4] > (pos[4] - w)*pos[3]:  # 纵向
                beside_space = [pos[0], pos[1] + w, pos[2], l, pos[4] - w, pos[5]]
                front_space = [pos[0] + l, pos[1], pos[2], pos[3] - l, pos[4], pos[5]]
            else:  # 纵向
                beside_space = [pos[0], pos[1] + w, pos[2], pos[3], pos[4] - w, pos[5]]
                front_space = [pos[0] + l, pos[1], pos[2], pos[3] - l, w, pos[5]]
            dblf.remove(deepcopy(pos))
            dblf.append(top_space)
            dblf.append(beside_space)
            dblf.append(front_space)
    time_end = time.time()
    # 输出最终结果
    best_ft = round((occupied_vol / container_vol * 100), 4)
    print("填充率：{} | 装箱数：{} | 时间：{}".format(best_ft, number_boxes, round(time_end - time_start, 4)))
    print("未装入箱子的顺序：{}".format(unpack_boxes))
    vis.draw(result, best_ft, int(p_ind), new_dir_path)  # 放置结果可视化
plt.show()
