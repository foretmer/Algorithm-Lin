import pandas as pd
import random
import json
import time



#将测试数据集转化为json文件
def jsonfile_generation(excel_path,out_path):
    json_list = []
    data = pd.read_excel(excel_path, sheet_name=0)
    nrows = data.shape[0]
    cases = []
    for i in range(nrows):
        if pd.isna(data.iloc[i,0]):
            json_list.append(cases)
            cases = []
            continue
        box = {}
        box['boxName'] = data.iloc[i,0]
        box['length'] = data.iloc[i, 1]
        box['width'] = data.iloc[i, 2]
        box['height'] = data.iloc[i, 3]
        box['box_num'] = data.iloc[i, 4]
        cases.append(box)
    json_list.append(cases)
    with open(out_path,'w') as f:
        json.dump(json_list,f)

#将json文件中的每一个测试用例转化为所需要的box形式
def boxes_generation(case):
    boxes = []
    for item in case:
        box = {}
        box['boxName'] = item['boxName']
        box['length'] = item["length"]
        box['width'] = item['width']
        box['height'] = item['height']
        for _ in range(int(item['box_num'])):
            boxes.append(box)
    return boxes

#将箱子按照底面积大小堆成一堆
def Stacks_generation(boxes,carriageHeight):
    random.shuffle(boxes)
    stack = []
    stacks = []
    boxes_temp = boxes[:]
    for k1 in range(len(boxes)):
        i = 0
        j = 0
        l = len(boxes)
        if l == 0:
            break
        else:
            stack = [boxes[i]]
            stackh1 = 0
            stackh = boxes[i]['height']
            if l > 1:
                for k2 in range(1, len(boxes)):
                    l = len(boxes)
                    j = j + i + 1
                    if l > 1:
                        if boxes[i]['length'] == boxes[j]['length'] and boxes[i]['width'] == boxes[j]['width']:
                            stackh = stackh + boxes[j]['height']
                            if stackh <= carriageHeight:
                                stack.append(boxes[j])
                                stackh1 = boxes[j]['height']
                                del boxes[j]
                                j = j - 1
                            else:
                                stackh -= boxes[j]['height']
        del boxes[i]
        stacks.append(stack)
    return stacks

    # boxes = boxes_temp

#箱子开始装箱
def Box_loader(carriage_Size, boxes):

    carriageLength = carriage_Size[0]
    carriageWidth = carriage_Size[1]
    carriageHeight = carriage_Size[2]
    loadratio_max = 0
    trucks_max = []
    loadratioVect = []
    loadratioVectTmp = []
    for s in range(1, 1000):
        boxes_temp = boxes[:]
        stacks = Stacks_generation(boxes,carriageHeight)
        boxes = boxes_temp
        # trucksize = [carriageLength, carriageWidth, carriageHeight]
        num_in = []  # 放进卡车的堆垛序号
        put_in_stacks = []  # 已经放进卡车的堆垛stack
        trucks_num = 0  # 卡车数量
        trucks = []
        trucksize_r1 = carriage_Size[0]
        trucksize_r2 = carriage_Size[0]
        trucksize_r3 = carriage_Size[0]
        to_put_in_stacks = stacks  # 将放进的堆垛
        k = -1

        for i in range(len(to_put_in_stacks)):
            if len(to_put_in_stacks) == 0:
                break
            else:
                for j in range(len(to_put_in_stacks)):
                    l = len(to_put_in_stacks)
                    k = k + 1
                    if k < l:
                        if list(to_put_in_stacks[k][0].values())[2] >= carriageWidth *2/ 3:
                            if trucksize_r1 > list(to_put_in_stacks[k][0].values())[1]:
                                trucksize_r1 = trucksize_r1 - list(to_put_in_stacks[k][0].values())[1]
                                trucksize_r2 = trucksize_r2 - list(to_put_in_stacks[k][0].values())[1]
                                trucksize_r3 = trucksize_r3 - list(to_put_in_stacks[k][0].values())[1]
                                num_in.append(k)
                                put_in_stacks.append(to_put_in_stacks[k])
                                del to_put_in_stacks[k]
                                k = k - 1
                            else:
                                continue
                        elif list(to_put_in_stacks[k][0].values())[2] < carriageWidth *2/ 3 and list(to_put_in_stacks[k][0].values())[2] >= carriageWidth / 3:
                            if trucksize_r1 >= list(to_put_in_stacks[k][0].values())[1]:
                                trucksize_r1 = trucksize_r1 - list(stacks[k][0].values())[1]
                                num_in.append(k)
                                put_in_stacks.append(to_put_in_stacks[k])
                                del to_put_in_stacks[k]
                                k = k - 1
                            elif trucksize_r2 >= list(to_put_in_stacks[k][0].values())[1]:
                                trucksize_r2 = trucksize_r2 - list(to_put_in_stacks[k][0].values())[1]
                                trucksize_r3 = trucksize_r3 - list(stacks[k][0].values())[1]
                                num_in.append(k)
                                put_in_stacks.append(to_put_in_stacks[k])
                                del to_put_in_stacks[k]
                                k = k - 1
                            else:
                                continue
                        else:
                            if trucksize_r1 >= list(to_put_in_stacks[k][0].values())[1]:
                                trucksize_r1 = trucksize_r1 - list(stacks[k][0].values())[1]
                                num_in.append(k)
                                put_in_stacks.append(to_put_in_stacks[k])
                                del to_put_in_stacks[k]
                                k = k - 1
                            elif trucksize_r2 >= list(to_put_in_stacks[k][0].values())[1]:
                                trucksize_r2 = trucksize_r2 - list(to_put_in_stacks[k][0].values())[1]
                                num_in.append(k)
                                put_in_stacks.append(to_put_in_stacks[k])
                                del to_put_in_stacks[k]
                                k = k - 1
                            elif trucksize_r3 >= list(to_put_in_stacks[k][0].values())[1]:
                                trucksize_r3 = trucksize_r3 - list(to_put_in_stacks[k][0].values())[1]
                                num_in.append(k)
                                put_in_stacks.append(to_put_in_stacks[k])
                                del to_put_in_stacks[k]
                                k = k - 1
                            else:
                                continue

                trucks.append(put_in_stacks)
                put_in_stacks = []
                trucksize_r1 = carriage_Size[0]
                trucksize_r2 = carriage_Size[0]
                trucksize_r3 = carriage_Size[0]
                k = -1
        trucks_num = len(trucks)
        # 计算满载率
        loadratio = 0
        boxes_volumn = 0
        trucks_volumn = 0
        tmp = 0
        if trucks_num == 1:
            trucks_volumn = carriage_Size[0] * carriage_Size[1] * carriage_Size[2]
            for j in range(len(trucks[0])):
                for k in range(len(trucks[0][j])):
                    boxes_volumn = boxes_volumn + list(trucks[0][j][k].values())[1] * list(trucks[0][j][k].values())[
                        2] * list(trucks[0][j][k].values())[3]
            loadratioVectTmp.append(boxes_volumn / (carriage_Size[0] * carriage_Size[1] * carriage_Size[2]))
            # print(1, '车的满载率：', boxes_volumn / (trucksize[0] * trucksize[1] * trucksize[2]))
            loadratio = boxes_volumn / trucks_volumn
            loadratio_max = loadratio
            trucks_max = trucks[:]
        else:
            for i in range(0, len(trucks) - 1):
                for j in range(len(trucks[i])):
                    for k in range(len(trucks[i][j])):
                        boxes_volumn = boxes_volumn + list(trucks[i][j][k].values())[1] * list(trucks[i][j][k].values())[
                            2] * list(trucks[i][j][k].values())[3]
                loadratioVectTmp.append(boxes_volumn / (carriage_Size[0] * carriage_Size[1] * carriage_Size[2]) - tmp)
                # print(i + 1, '车的满载率：', boxes_volumn / (trucksize[0] * trucksize[1] * trucksize[2]) - tmp)
                tmp = boxes_volumn / (carriage_Size[0] * carriage_Size[1] * carriage_Size[2])
                trucks_volumn = trucks_volumn + carriage_Size[0] * carriage_Size[1] * carriage_Size[2]
            loadratio = boxes_volumn / trucks_volumn
            if loadratio > loadratio_max:
                loadratioVect.clear()
                for tmpNum in range(len(loadratioVectTmp)):
                    loadratioVect.append(loadratioVectTmp[tmpNum])
                i = len(trucks) - 1
                for j in range(len(trucks[i])):
                    for k in range(len(trucks[i][j])):
                        boxes_volumn = boxes_volumn + list(trucks[i][j][k].values())[1] * list(trucks[i][j][k].values())[
                            2] * list(trucks[i][j][k].values())[3]
                loadratioVect.append(boxes_volumn / (carriage_Size[0] * carriage_Size[1] * carriage_Size[2]) - tmp)
                # print('第', i + 1, '车的满载率：', boxes_volumn / (trucksize[0] * trucksize[1] * trucksize[2]) - tmp)
                loadratio_max = loadratio
                trucks_max = trucks[:]
            loadratioVectTmp.clear()
    loadratio = loadratio_max
    print('一共需要车：', len(loadratioVect), '辆')
    for i in range(len(loadratioVect)):
        print('第', i + 1, '辆车的满裁率：', loadratioVect[i])

    sum = 0
    for i in range(len(loadratioVect)):
        sum += loadratioVect[i]
    allLoadratio = sum / len(loadratioVect)
    print('所有车的平均满载率：', allLoadratio)
    print('最终满载率为：', loadratio)





if __name__ == "__main__":
    # jsonfile_generation("./datalab/3_box.xlsx","./datalab/3_box.json")

    carriage_Size = [587,233,220]
    json_list = []
    with open("./15_box.json",'r') as f:
        json_list = json.load(f)
    for case in json_list:
        start = time.time()
        boxes = boxes_generation(case)
        Box_loader(carriage_Size,boxes)
        end = time.time()
        #print("运行时间:%.4f秒" % (end - start))
        start = end
        print('\n')
        print('-----------------')

