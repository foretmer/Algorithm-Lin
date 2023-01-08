import re


def max_area(cargo):
    maximum = 0
    set_way = 0
    if cargo[0] * cargo[1] > maximum:
        maximum = cargo[0] * cargo[1]
    if cargo[1] * cargo[2] > maximum:
        maximum = cargo[1] * cargo[2]
        set_way = 1
    if cargo[0] * cargo[2] > maximum:
        set_way = 2
    if set_way == 1:
        return [cargo[1], cargo[2], cargo[0], cargo[3]]
    elif set_way == 2:
        return [cargo[0], cargo[2], cargo[1], cargo[3]]
    else:
        return cargo


def calculate(cargoes):
    for i in range(len(cargoes)):
        cargoes[i] = max_area(cargoes[i])  # 找出货物三种旋转方式中底面积最大的放法
    # 进行每个货物的底面积的排序
    for i in range(len(cargoes)):
        for j in range(i + 1, len(cargoes)):
            if cargoes[i][0] * cargoes[i][1] < cargoes[j][0] * cargoes[j][1]:
                cargoes[i], cargoes[j] = cargoes[j], cargoes[i]
    return cargoes


def set_method(box, SR):
    result = []
    for i in range(len(SR)):
        space = SR[i]
        if box[0] <= space[3] and box[1] <= space[4] and box[2] <= space[5]:
            result.append([i, space[0], space[1], space[2], box[0], box[1], box[2]])
        if box[1] <= space[3] and box[0] <= space[4] and box[2] <= space[5]:
            result.append([i, space[0], space[1], space[2], box[0], box[1], box[2]])
        if len(result) > 0:
            return result
    return []


def combine(spaces):
    i = 0
    while i < len(spaces):
        three_dict = {}
        xi, yi, zi = spaces[i][0] + spaces[i][3], spaces[i][1], spaces[i][2]
        three_dict[(xi, yi, zi)] = [-1, spaces[i][4], spaces[i][5]]
        xi, yi, zi = spaces[i][0], spaces[i][1] + spaces[i][4], spaces[i][2]
        three_dict[(xi, yi, zi)] = [spaces[i][3], -1, spaces[i][5]]
        xi, yi, zi = spaces[i][0], spaces[i][1], spaces[i][2] + spaces[i][5]
        three_dict[(xi, yi, zi)] = [spaces[i][3], spaces[i][4], -1]
        for j in range(i+1, len(spaces)):
            flag = 0
            for item in three_dict:
                if spaces[j][0] == item[0] and spaces[j][1] == item[1] and spaces[j][2] == item[2]:
                    if three_dict[item][0] == -1:
                        if three_dict[item][1] == spaces[j][4] and three_dict[item][2] == spaces[j][5]:
                            spaces.append([spaces[i][0], spaces[i][1], spaces[i][2], spaces[i][3] + spaces[j][3], spaces[i][4], spaces[i][5]])
                            flag = 1
                            break
                    elif three_dict[item][1] == -1:
                        if three_dict[item][0] == spaces[j][3] and three_dict[item][2] == spaces[j][5]:
                            spaces.append([spaces[i][0], spaces[i][1], spaces[i][2], spaces[i][3], spaces[i][4] + spaces[j][4], spaces[i][5]])
                            flag = 1
                            break
                    elif three_dict[item][2] == -1:
                        if three_dict[item][0] == spaces[j][3] and three_dict[item][1] == spaces[j][4]:
                            spaces.append([spaces[i][0], spaces[i][1], spaces[i][2], spaces[i][3], spaces[i][4], spaces[i][5] + spaces[j][5]])
                            flag = 1
                            break
            if flag == 1:
                spaces.pop(i)
                i = i - 1
                spaces.pop(j)
                #length = length - 1
                break
        i = i + 1
    return spaces

def procedure(dic):
    # map记录货舱内的摆放情况，map中的元素为[xi, yi, zi, lx, ly, lz], （xi,yi,zi)表示货物的左下后角的点坐标，lx, ly, lz分别表示货物在各个坐标轴方向上占据的长度
    map = []
    # boxes存储货物，实现按照底面积大小降序排序
    SR = [[0, 0, 0]]
    a = 0.1  # 修正参数
    for item in dic:
        boxes = calculate(dic[item])
        V = item[0] * item[1] * item[2]
        SR[0].extend(
            item)  # 初始化剩余空间集合SR, SR中的元素为[xi, yi, zi, lx, ly, lz]，（xi,yi,zi)表示剩余空间的左下后角的点坐标，lx, ly,
        # lz分别表示剩余空间在各个坐标轴方向上占据的长度
    index = 0
    i = 0
    while len(boxes) > index:
        i = i + 1
        while boxes[index][3] == 0:
            index = index + 1
        if index < len(boxes):
            box = boxes[index]
        else:
            break
        # 两种放置方式， 两种切割方式 ——> 四种放置切割方式
        SF = set_method(box, SR)
        if len(SF) > 0:
            max = -(SR[SF[0][0]][3] - SF[0][4] + a) * (SR[SF[0][0]][4] - SF[0][5] + a)
            max_index = 0
            for i in range(1, len(SF)):
                evaluation = -(SR[SF[i][0]][3] - SF[i][4] + a) * (SR[SF[i][0]][4] - SF[i][5] + a)
                if evaluation > max:
                    max = evaluation
                    max_index = i
            map.append([SF[max_index][1], SF[max_index][2], SF[max_index][3], SF[max_index][4], SF[max_index][5],
                        SF[max_index][6]])
            # 空间分割————更新SR
            s2 = SF[max_index][4] * (SR[SF[max_index][0]][4] - SF[max_index][5])
            s3 = (SR[SF[max_index][0]][3] - SF[max_index][4]) * SF[max_index][5]
            l = SF[max_index][4]
            w = SF[max_index][5]
            h = SR[SF[max_index][0]][5] - SF[max_index][6]
            if l > 0 and w > 0 and h > 0:
                SR.append([SF[max_index][1], SF[max_index][2], SF[max_index][3] + SF[max_index][6], l, w, h])  # S1 box[xi], box[yi], box[zi] + lz, lx, ly, SR[SF[max_index][0]][5] - lz
            if s3 >= s2:  # 纵向切割
                l = SF[max_index][4]
                w = SR[SF[max_index][0]][4] - SF[max_index][5]
                h = SR[SF[max_index][0]][5]
                if l > 0 and w > 0 and h > 0:
                    SR.append([SF[max_index][1], SF[max_index][2] + SF[max_index][5], SF[max_index][3], l, w, h])  # S2 box[xi], box[yi] + ly , box[zi], SR[SF[max_index][0]][3] - SF[max_index][
                    # 4], SR[SF[max_index][0]][4] - SF[max_index][5], SR[SF[max_index][0]][5]
                l = SR[SF[max_index][0]][3] - SF[max_index][4]
                w = SR[SF[max_index][0]][4]
                h = SR[SF[max_index][0]][5]
                if l > 0 and w > 0 and h > 0:
                    SR.append([SF[max_index][1] + SF[max_index][4], SF[max_index][2], SF[max_index][3], l, w, h])  # S3 box[xi] + lx, box[yi], box[zi], SR[SF[max_index][0]][3] - SF[max_index][4],
                    # SR[SF[max_index][0]][4], SR[SF[max_index][0]][5]
            else:  # 横向切割
                l = SR[SF[max_index][0]][3] - SF[max_index][4]
                w = SF[max_index][5]
                h = SR[SF[max_index][0]][5]
                if l > 0 and w > 0 and h > 0:
                    SR.append([SF[max_index][1] + SF[max_index][4], SF[max_index][2], SF[max_index][3], l, w, h])  # S3
                l = SR[SF[max_index][0]][3]
                w = SR[SF[max_index][0]][4] - SF[max_index][5]
                h = SR[SF[max_index][0]][5]
                if l > 0 and w > 0 and h > 0:
                    SR.append(
                        [SF[max_index][1], SF[max_index][2] + SF[max_index][5], SF[max_index][3], l, w, h])  # S2
            SR.pop(SF[max_index][0])
            boxes[0][3] = boxes[0][3] - 1
            # 合并SR
            SR = combine(SR)
        else:
            index = index + 1
    V_boxes = 0
    for box in map:
        V_boxes += box[3] * box[4] * box[5]
        #print('(' + str(box[0]) + "," + str(box[1]) + "," + str(box[2]) + ")" + '->' + str(box[3]) + ' ' + str(box[4]) + ' ' + str(box[5]))
        with open('result.txt', 'a') as output_file:
            output_file.write('(' + str(box[0]) + "," + str(box[1]) + "," + str(box[2]) + ")" + '->' + str(box[3]) + ' ' + str(box[4]) + ' ' + str(box[5]) + '\n')
    print("车厢的填充率为" + str(V_boxes / V))
    with open('result.txt', 'a') as output_file:
        output_file.write(
            "车厢的填充率为" + str(V_boxes / V) + '\n\n')
    #print()
    #print()

if __name__ == '__main__':
    """
    （1）处理输入，输入形式如下：
    (587 233 220) # 第一行表示货车车厢的长l、宽w、高h
    [(108 76 30 40), (110 43 25 33), (92 81 55 39)] # 第二行为list，list中的每个元素表示每个货物的长、宽、高、和数量四个属性
    （2）对货物按照最大底面积（每种货物3种旋转放置方式）进行降序排序
    （3）实现评价度函数
    （4）实现剩余空间分割算法
    （5）实现主流程
    """
    with open("dataset.txt", 'r') as input_file:
        lines = input_file.readlines()
    dic = dict()
    for line in lines:
        if 'C' in line:
            list = re.findall('\((.*?)\)', line)
            num_list = list[0].split()
        if 'B' in line:
            list = re.findall('\((.*?)\)', line)
            C_list = []
            for num in num_list:
                C_list.append(int(num))
            B_list = []
            for item in list:
                num_list = item.split()
                new_num_list = []
                for num in num_list:
                    new_num_list.append(int(num))
                B_list.append(new_num_list)
            dic[tuple(C_list)] = B_list
            procedure(dic)
            dic.clear()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
