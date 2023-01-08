from Packing3D import *
from Packing3D import show
import time
import os


if __name__ == "__main__":      
    paths = 'data/E1-3.txt'  #数据所在的位置
    filename = os.path.basename(paths)  # 从文件路径中读取最后一个文件夹的名字
    filename = os.path.splitext(filename)[0] #去掉文件名后缀
    f = open(paths)  #打开文件
    lines = f.readline() #读取文件第一行数据
    lines = lines.replace(','," ")
    lines = lines.split()
    int_list = [int(x) for x in lines]

    case = Box(int_list[0],int_list[1],int_list[2])  #设置箱子的属性

    cargos= [Cargo(0,0,0) for _ in range(0)]
    while True:
        lines = f.readline()
        if(lines):
            lines = lines.replace(','," ")
            lines = lines.split()
            lines.pop(0)
            lines = [int(x) for x in lines]
            cargos.extend([Cargo(lines[0],lines[1],lines[2]) for _ in range(lines[3])])
        else:
            break
    f.close()

    start = time.time()
    print('空间利用率：',encase_cargos_into_container(cargos,case,VolumeGreedyStrategy))
    end = time.time()
    case.save_encasement_as_file(filename)
    print("所用时间：{}".format(end-start))

    show.draw_reslut(case)
    