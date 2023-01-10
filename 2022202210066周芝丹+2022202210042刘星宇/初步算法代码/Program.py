from _container import *
import drawer
from _cargo import *
from __init__ import *
import time


if __name__ == "__main__":
    '''cargos = [Cargo(108,76,30) for _ in range(2)] #246240
    #cargos.extend([Cargo(110,43,25) for _ in range(25)]) #118250
    cargos.extend([Cargo(92,81,55) for _ in range(2)]) #409860
    cargos.extend([Cargo(210,120,100) for _ in range(1)])#'''

    '''cargos = [Cargo(108,76,30) for _ in range(40)] #246240
    cargos.extend([Cargo(110,43,25) for _ in range(33)]) #118250
    cargos.extend([Cargo(92,81,55) for _ in range(39)]) #409860'''
    '''cargos = [Cargo(91,54,45) for _ in range(32)] 
    cargos.extend([Cargo(105,77,72) for _ in range(24)]) 
    cargos.extend([Cargo(79,78,48) for _ in range(30)])# '''
    cargos = [Cargo(78,37,27) for _ in range(63)] 
    cargos.extend([Cargo(89,70,25) for _ in range(52)]) 
    cargos.extend([Cargo(90,84,41) for _ in range(55)])# '''


    '''cargos = [Cargo(49,25,21) for _ in range(22)] 
    cargos.extend([Cargo(60,51,41) for _ in range(22)]) 
    cargos.extend([Cargo(103,76,64) for _ in range(28)]) 
    cargos.extend([Cargo(95,70,62) for _ in range(25)]) 
    cargos.extend([Cargo(111,49,26) for _ in range(17)])#'''
    '''cargos = [Cargo(88,54,39) for _ in range(25)] 
    cargos.extend([Cargo(94,54,36) for _ in range(27)]) 
    cargos.extend([Cargo(87,77,43) for _ in range(21)]) 
    cargos.extend([Cargo(100,80,72) for _ in range(20)]) 
    cargos.extend([Cargo(83,40,36) for _ in range(24)])#'''
    '''cargos = [Cargo(90,70,63) for _ in range(16)] 
    cargos.extend([Cargo(84,78,28) for _ in range(28)]) 
    cargos.extend([Cargo(94,85,39) for _ in range(20)]) 
    cargos.extend([Cargo(80,76,54) for _ in range(23)]) 
    cargos.extend([Cargo(69,50,45) for _ in range(31)])#'''
    '''cargos = [Cargo(74,63,61) for _ in range(22)] 
    cargos.extend([Cargo(71,60,25) for _ in range(12)]) 
    cargos.extend([Cargo(106,80,59) for _ in range(25)]) 
    cargos.extend([Cargo(109,76,42) for _ in range(24)]) 
    cargos.extend([Cargo(118,56,22) for _ in range(11)])#'''


    '''cargos = [Cargo(98,73,44) for _ in range(6)] 
    cargos.extend([Cargo(60,60,38) for _ in range(7)]) 
    cargos.extend([Cargo(105,73,60) for _ in range(10)]) 
    cargos.extend([Cargo(90,77,52) for _ in range(3)]) 
    cargos.extend([Cargo(66,48,24) for _ in range(5)])
    cargos.extend([Cargo(106,76,55) for _ in range(10)]) 
    cargos.extend([Cargo(55,44,36) for _ in range(12)]) 
    cargos.extend([Cargo(82,58,23) for _ in range(7)]) 
    cargos.extend([Cargo(74,61,58) for _ in range(6)])
    cargos.extend([Cargo(81,39,24) for _ in range(8)]) 
    cargos.extend([Cargo(71,65,39) for _ in range(11)]) 
    cargos.extend([Cargo(105,97,47) for _ in range(4)]) 
    cargos.extend([Cargo(114,97,69) for _ in range(5)])
    cargos.extend([Cargo(103,78,55) for _ in range(6)]) 
    cargos.extend([Cargo(93,66,55) for _ in range(6)])#'''

    start = time.time()
    case = Container(587,233,220)
    print(
        encase_cargos_into_container(cargos,case,VolumeGreedyStrategy)
    )
    end = time.time()
    print("消耗时间为：", end - start)
    case.save_encasement_as_file()
    drawer.draw_reslut(case)

    