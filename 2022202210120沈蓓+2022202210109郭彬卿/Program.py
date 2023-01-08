from Encase3D import *
from Encase3D import drawer
import time


if __name__ == "__main__":      
    paths = 'data/8_4.txt'
    f = open(paths)
    lines = f.readline()
    lines = lines.replace(','," ")
    lines = lines.split()
    int_list = [int(x) for x in lines]
    case = Container(int_list[0],int_list[1],int_list[2])
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
    print('利用率：',encase_cargos_into_container(cargos,case,VolumeGreedyStrategy))
    end = time.time()
    case.save_encasement_as_file()
    print("运行时间：{}".format(end-start))
    drawer.draw_reslut(case)
    