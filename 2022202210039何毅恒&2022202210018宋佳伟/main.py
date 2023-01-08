import json
import random
from classes import *
import mplt


# 变成占比小数list
def list_occ(input_list: List[int]):
    list_sum = sum(input_list)
    for i, x in enumerate(input_list):
        input_list[i] = x / list_sum
    return input_list


def load_boxes(online_boxes_list: List[Box], container: Container):
    # 按输入顺序进行装配
    idx_box = 0
    # 根据当前container的形状设置初始权重
    pose_weight_occ = list_occ(list_occ([5, 4, 3, 1, 2, 0]))
    # print(pose_weight_occ)

    while idx_box < len(online_boxes_list):
        idx_pose = 0
        box = online_boxes_list[idx_box]
        # 依次遍历各个pose，找到能放下的pose
        pose_weight_occ = list_occ(pose_weight_occ)

        # 权重以一定概率进行变异(20%)
        # print("be pose_weight_occ=", pose_weight_occ)
        if random.choice([1, 0, 0, 0, 0]):
            # 随机从除第一大外的权重进行变异
            chose_idx = random.choice(list(range(1, 5)))
            pose_weight_occ[chose_idx] += 0.3
            pose_weight_occ = list_occ(pose_weight_occ)
            # print("pose_weight_occ=", pose_weight_occ)

        new_idx = [x[0] for x in sorted(enumerate(pose_weight_occ), key=lambda x:x[1])]
        poses = [list(BoxPose)[x] for x in new_idx]
        # print("pose_weight=", pose_weight_occ)
        while idx_pose < len(poses):
            box.pose = poses[idx_pose]
            box.current_pose_weight = pose_weight_occ
            is_loaded = container.load(box)
            # 该pose成功装入
            if is_loaded.is_valid:
                pose_weight_occ[idx_pose] += 0.01
                break
            # 继续遍历其它pose
            idx_pose += 1
        # 该pose成功装入
        if is_loaded.is_valid:
            pose_weight_occ[idx_pose] += 0.01
            idx_box += 1
            # 更新pose权重
        elif is_loaded == Point(-1, -1, 0):
            # 更新参考面位置
            continue
        else:
            # 装入失败
            idx_box += 1
    # 返回最终的货柜占用率
    return sum(list(map(lambda x: x.volume, container._loaded_boxes))) / container.volume


if __name__ == "__main__":
    with open("output.csv", 'a', encoding='utf-8') as csv_f:
        csv_f.write(f"list_name,index,x,y,z,length,width,height,pose")
        csv_f.write(f",short_narrow,short_wide,normal_narrow,tall_narrow,normal_wide,tall_wide\n")
    # 从json文件中加载数据集
    with open('./3DLoad-test-dataSet.json', 'r') as data_f:
        dataset = json.load(data_f)
        print(dataset)

        # 分别输入数据集中的各组数据进行测试
        for i_types in [1]:
            for i_E in [0]:
        # for i_types in range(len(dataset['dataset'])):
        #     for i_E in range(len(dataset['dataset'][i_types]['data'])):
                idx_boxes_types = i_types
                idx_E = i_E
                print("boxes-types:", dataset['dataset'][idx_boxes_types]['boxes-types'])
                print("name:", dataset['dataset'][idx_boxes_types]['data'][idx_E]['name'])
                # print("Container(L, W, H):", dataset['dataset'][idx_boxes_types]['data'][idx_E]['Container'])
                print("Boxes(L, W, H, N):", dataset['dataset'][idx_boxes_types]['data'][idx_E]['Boxes'])
                current_boxes_list = dataset['dataset'][idx_boxes_types]['data'][idx_E]['Boxes']
                boxes = []
                for i in range(len(current_boxes_list)):
                    if i == 1:
                        boxes = [Box(current_boxes_list[i][0], current_boxes_list[i][1], current_boxes_list[i][2]) for _ in
                                 range(current_boxes_list[i][3])]
                    else:
                        boxes.extend([Box(current_boxes_list[i][0], current_boxes_list[i][1], current_boxes_list[i][2]) for _ in
                                      range(current_boxes_list[i][3])])
                # 加载货柜大小
                container_size = dataset['dataset'][idx_boxes_types]['data'][idx_E]['Container']
                case = Container(container_size[0], container_size[1], container_size[2])

                # 模拟boxes随机到达
                random.seed(123456)
                online_boxes_list = list(boxes)
                random.shuffle(online_boxes_list)
                print("online_boxes_list=", online_boxes_list)
                # 调用执行装箱
                occ_rate = load_boxes(online_boxes_list, case)
                print(occ_rate)
                # 将输出的摆法存入csv文件
                case.save_csv(dataset['dataset'][idx_boxes_types]['data'][idx_E]['name'],
                              str(online_boxes_list).replace(", ", ""), str(occ_rate))
                # 画图
                mplt.draw(case)
                print()
