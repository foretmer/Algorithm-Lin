import random
from container import *
from cargo import *
from load import *
from plot import *
import plot

if __name__ == "__main__":
    case = Container(587,233,220)
    i = 0
    cargos = []
    # while True:
    #     userinput = input("是否开始/继续放置箱子？y/n ")
    #     if userinput == "n":
    #         print("箱子放置结束！")
    #         break
    #     elif(userinput == "y"):
    #         l = input("请输入要放置的箱子长度(小数点后两位):")
    #         w = input("请输入要放置的箱子宽度(小数点后两位):")
    #         h = input("请输入要放置的箱子高度(小数点后两位):")
    #         cargos = [Cargo(float(l), float(w), float(h))]
    #         cargo, container = encase_cargos_into_container_byone(cargos, case, VolumeGreedyStrategy)
    while True:
        userinput = input("是否开始/继续放置箱子？y/n ")
        if userinput == "n":
            print("箱子数据读取结束！")
            break
        elif(userinput == "y"):
            l = input("请输入要放置的箱子长度(小数点后两位):")
            w = input("请输入要放置的箱子宽度(小数点后两位):")
            h = input("请输入要放置的箱子高度(小数点后两位):")
            n = input("请输入要放置的箱子数量(正整数):")
            cargos.extend([Cargo(float(l), float(w), float(h)) for _ in range(int(n))])

    print("---------开始放置箱子-----------")
    print(cargos)
    # 在线算法实现：随机打乱箱子顺序，箱子按打乱后的顺序在线到达
    random.shuffle(cargos)
    print(len(cargos))
    length = len(cargos)
    # cargos = [Cargo(float(l), float(w), float(h))]
    for i in range(length):
        print(i)
        print(cargos[i])
        cargo1 = [cargos[i]]
        cargo, container = encase_cargos_into_container_byone(cargo1, case, VolumeGreedyStrategy)
    print("---------箱子放置结束-----------")
    case.save_encasement_as_file()
    plot.draw_reslut(case)

    