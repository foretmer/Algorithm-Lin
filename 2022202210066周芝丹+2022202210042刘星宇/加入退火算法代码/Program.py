from _container import *
import drawer
from _cargo import *
from __init__ import *
from random import *
import numpy as np


if __name__ == "__main__":
    #模拟退火参数设置
    St = 1
    L = 0
    Et = 0.4
    dL = 3
    dt = 0.9
    ###################

    # E1-1
    cargos = [Cargo(108, 76, 30 ) for _ in range(40)]
    cargos.extend([Cargo(110, 43, 25) for _ in range(33)])
    cargos.extend([Cargo(92, 81, 55) for _ in range(39)])

    case = Container(587,233,220)
    sorted_list = sorted(cargos, key=lambda cargo: cargo.volume, reverse=1)
    print(sorted_list)
    start_list = deepcopy(sorted_list)
    fstart = encase_cargos_into_container(cargos,case,sorted_cargos=sorted_list) #初始摆放时的空间利用率
    print(start_list,'1111')
    f = fstart
    fbest = fstart
    #print(f)
    Bbest = case._setted_cargos     #初识摆放时的放置顺序
    for i in [1,2]: # 进行两次退火
        print("第%d次退火" %i)
        t = St
        Lt = L
        while(t >= Et):
            for j in range(Lt):
                #E1-1
                cargos = [Cargo(108, 76, 30 ) for _ in range(40)]
                cargos.extend([Cargo(110, 43, 25) for _ in range(33)])
                cargos.extend([Cargo(92, 81, 55) for _ in range(39)])
                case = Container(587,233,220)              

                # 交换路径中的这2个节点的顺序
                s1, s2 = randint(0, int(len(sorted_list)/2) - 1), randint(int(len(sorted_list)/2), len(sorted_list) - 1)
                start_list[s1], start_list[s2], = start_list[s2], start_list[s1]
                
                print(start_list,'!!')
                print(len(start_list))
                temp_list = deepcopy(start_list)
                temp_list2 = deepcopy(start_list)
                f1 = encase_cargos_into_container(cargos, case, sorted_cargos = temp_list)
                print("第%d次的利用率 = " %j, f1)
                #drawer.draw_reslut(case,'')  # 画出最终装箱的效果图
                B1 = case._setted_cargos
                df = f1 - f
                if(df > 0):
                    f = f1
                    B = B1
                    if (f > fbest):
                        fbest = f
                        Bbest = B
                        start_list = temp_list2
                else:
                    x = random()
                    if(x < np.exp(10*df/t)):
                        f = f1
                        B = B1
                        start_list = temp_list2
            Lt += dL
            t *= dt
    
    print("初始装箱率=", fstart)
    print("最高的装箱率=", fbest)