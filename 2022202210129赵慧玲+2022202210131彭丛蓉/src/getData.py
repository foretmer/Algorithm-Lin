import pandas as pd
import pickle

goal = input("goal:")
path = "../data/"+goal+".pkl"
flag = True
fp=open("../data/data.txt","r",encoding='utf-8')
for line in fp.readlines():
    if line.replace('\n', '') != goal and flag:
        continue
    else:
        flag = False
    if line[0] == 'B':
        width = depth = height = weight = volume = []
        line = line.replace('\n', '')
        line = line.replace('B [(', '')
        line = line.replace('(', '')
        line = line.replace(')', '')
        line = line.replace(']', '')
        line = line.replace(', ', ',')
        # print(line)
        item = line.split(',')
        for i in range(len(item)):
            value = item[i].split(' ')
            # print(value)
            for j in range(int(value[3])):
                width.append(int(value[0]))
                depth.append(int(value[1]))
                height.append(int(value[2]))
                weight.append(1)
                volume.append(int(value[0]) * int(value[1]) * int(value[2]))
        print(str(width) + ", " + str(depth) + ", " + str(height) + ", " + str(weight) + ", " + str(volume))
        # 字典中的key值即为列名
        dataframe = pd.DataFrame({'width': width, 'depth': depth, 'height': height, 'weight': weight, 'volume': volume})
        print('\n')
        # 将DataFrame存储为pkl,index表示是否显示行名，default=True
        dataframe.to_pickle(path)
        f = open(path, 'rb')
        data = pickle.load(f)
        print(data)
        break;


