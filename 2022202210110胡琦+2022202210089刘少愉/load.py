from typing import Iterable
from container import *
import time

class Strategy(object):
    # 继承此类 重写两个静态函数 实现自定义两个装载策略: 装箱顺序 和 货物.
    @staticmethod
    def encasement_sequence(cargos:Iterable) -> Iterable:
        return cargos

    @staticmethod
    def choose_cargo_poses(cargo:Cargo, container:Container) -> list:
        return list(CargoPose)

def encase_cargos_into_container_byone(
    cargos:Iterable,
    container:Container,
    strategy:type
) -> float:
    # sorted_cargos:List[Cargo] = strategy.encasement_sequence(cargos)
    # occupancy = 0
    start_time = time.time()
    i = 0 # 记录发当前货物
    while i < len(cargos):
        j = 0 # 记录当前摆放方式
        cargo = cargos[i]
        poses = strategy.choose_cargo_poses(cargo, container)
        while j < len(poses):
            cargo.pose = poses[j]
            is_encased = container._encase(cargo)
            if is_encased.is_valid:
                break # 可以装入 不在考虑后续摆放方式
            j += 1  # 不可装入 查看下一个摆放方式
        if is_encased.is_valid:
            i += 1 # 成功放入 继续装箱
            container._occupancy += cargo.volume / container.volume
            print('该箱子的放置位置为:',cargo._point,'摆放状态为:',cargo._pose,'箱子调整到摆放状态所对应的长宽高为:',cargo.length,cargo.width,cargo.height)
            print('目前容器的占用率为:',container._occupancy)
        elif is_encased == Point(-1,-1,0):
            continue # 没放进去但是修改了参考面位置 重装
        else :
            i += 1 # 纯纯没放进去 跳过看下一个箱子
            print('该箱子装不进容器！')
            print('目前容器的占用率为:', container._occupancy)
        end_time = time.time()
        print('花费时间%f秒' % (end_time - start_time))
    return cargo, container


class VolumeGreedyStrategy(Strategy):
    @staticmethod
    def encasement_sequence(cargos:Iterable) -> Iterable:
        return sorted(cargos, key= lambda cargo:cargo.volume,reverse=1)

    @staticmethod
    def choose_cargo_poses(cargo:Cargo, container:Container) -> list:
        return list(CargoPose)