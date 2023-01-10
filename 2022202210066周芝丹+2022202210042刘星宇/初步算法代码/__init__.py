from typing import Iterable, List
from _cargo import *
from _container import *
import random

class Strategy(object):
    # 继承此类 重写两个静态函数 实现自定义两个装载策略: 装箱顺序 和 货物.
    @staticmethod
    def encasement_sequence(cargos:Iterable) -> Iterable:
        return cargos

    @staticmethod
    def choose_cargo_poses(cargo:Cargo, container:Container) -> list:
        return list(CargoPose)

def encase_cargos_into_container(
    cargos:Iterable, 
    container:Container, 
    strategy:type
) -> float:
    sorted_cargos:List[Cargo] = strategy.encasement_sequence(cargos)
    i = 0 # 记录发当前货物
    print(sorted_cargos,'ffff')
    # 随意调换四个摆放顺序
    for k in range(4):
        p1 = random.randint(int(len(sorted_cargos)/2), int(len(sorted_cargos)*3/4)-1)
        p2 = random.randint(int(len(sorted_cargos)*3/4), len(sorted_cargos)-1)
        sorted_cargos[p1], sorted_cargos[p2] = sorted_cargos[p2], sorted_cargos[p1]

    print(sorted_cargos,'ssss')

    while i < len(sorted_cargos):
        j = 0 # 记录当前摆放方式
        cargo = sorted_cargos[i]
        poses = strategy.choose_cargo_poses(cargo, container)

        # 没加任何东西：
        temp_flag = []
        while j < len(poses):
            cargo.pose = poses[j]
            is_encased = container._encase(cargo)
            temp_flag.append(deepcopy(is_encased))
            if is_encased.is_valid:
                break # 可以装入 不在考虑后续摆放方式
            j += 1  # 不可装入 查看下一个摆放方式
        container._extend_points(cargo, temp_flag[-1])

        # 一直都用最小面
        '''area = [0 for _ in range(len(poses))]
        temp_flag = []
        while j < len(poses):
            cargo.pose = poses[j]
            is_encased = container._encase(cargo)
            temp_flag.append(deepcopy(is_encased))
            if is_encased.is_valid:
                print(area)
                area[j] = container.rectangles_overlap_area_sum(cargo) 
            j += 1
        b = area.index(max(area))
        cargo.pose = poses[b]
        container._extend_points(cargo, temp_flag[b])'''

        # 先随机放，再用最小面
        '''if i <= 0.3*len(sorted_cargos):
            temp_flag = []
            while j < len(poses):
                cargo.pose = poses[j]
                is_encased = container._encase(cargo)
                temp_flag.append(deepcopy(is_encased))
                if is_encased.is_valid:
                    break # 可以装入 不在考虑后续摆放方式
                j += 1  # 不可装入 查看下一个摆放方式
            container._extend_points(cargo, temp_flag[-1])

        elif i > 0.3*len(sorted_cargos):
            area = [0 for _ in range(len(poses))]
            temp_flag = []
            while j < len(poses):
                cargo.pose = poses[j]
                is_encased = container._encase(cargo)
                temp_flag.append(deepcopy(is_encased))
                if is_encased.is_valid:
                    print(area)
                    area[j] = container.rectangles_overlap_area_sum(cargo) 
                j += 1
            b = area.index(max(area))
            cargo.pose = poses[b]
            container._extend_points(cargo, temp_flag[b])#'''
        
        # 放底面最大面
        '''area = [99999999 for _ in range(len(poses))]
        temp_flag = []
        while j < len(poses):
            cargo.pose = poses[j]
            is_encased = container._encase(cargo)
            temp_flag.append(deepcopy(is_encased))
            if is_encased.is_valid:
                area[j] = container.rectangles_overlap_area_bottom(cargo) 
                #print(area,'~~')
                #print(cargo,'!!')
            j += 1
        b = area.index(min(area))
        cargo.pose = poses[b]
        print(cargo,'!!!')
        container._extend_points(cargo, temp_flag[b])'''

        #放底面最小面
        '''area = [0 for _ in range(len(poses))]
        temp_flag = []
        while j < len(poses):
            cargo.pose = poses[j]
            is_encased = container._encase(cargo)
            temp_flag.append(deepcopy(is_encased))
            if is_encased.is_valid:
                print(area)
                area[j] = container.rectangles_overlap_area_bottom(cargo) 
            j += 1
        b = area.index(max(area))
        cargo.pose = poses[b]
        container._extend_points(cargo, temp_flag[b])'''

        
        if is_encased.is_valid:
            container._setted_cargos.append(cargo)
            i += 1 # 成功放入 继续装箱
        elif is_encased == Point(-1,-1,0):
            continue # 没放进去但是修改了参考面位置 重装
        else :
            i += 1 # 纯纯没放进去 跳过看下一个箱子
    return sum(list(map(
            lambda cargo:cargo.volume,container._setted_cargos
        ))) / container.volume



class VolumeGreedyStrategy(Strategy):
    @staticmethod
    def encasement_sequence(cargos:Iterable) -> Iterable:
        return sorted(cargos, key= lambda cargo:cargo.volume,reverse=1)

    @staticmethod
    def choose_cargo_poses(cargo:Cargo, container:Container) -> list:
        return list(CargoPose)