import drawer
from drawer import *
from structure import *
from Solver import Solver
import time

if __name__ == "__main__":
    # c1 = CargoType(49, 25, 21, 13, 0)
    # c2 = CargoType(60, 51, 41, 9, 1)
    # c3 = CargoType(103, 76, 64, 8, 2)
    # c4 = CargoType(95, 70, 62, 6, 3)
    # c5 = CargoType(111, 49, 26, 10, 4)
    # c6 = CargoType(74, 42, 40, 4, 5)
    # c7 = CargoType(85, 84, 72, 10, 6)
    # c8 = CargoType(48, 36, 31, 10, 7)
    # c9 = CargoType(86, 76, 38, 12, 8)
    # c10 = CargoType(71, 48, 47, 14, 9)
    # c11 = CargoType(90, 43, 33, 9, 10)
    # c12 = CargoType(98, 52, 44, 9, 11)
    # c13 = CargoType(73, 37, 23, 10, 12)
    # c14 = CargoType(61, 48, 39, 14, 13)
    # c15 = CargoType(75, 75, 63, 11, 14)
    #
    #
    # cargo = Cargo()
    # cargo.extend(c1)
    # cargo.extend(c2)
    # cargo.extend(c3)
    # cargo.extend(c4)
    # cargo.extend(c5)
    # cargo.extend(c6)
    # cargo.extend(c7)
    # cargo.extend(c8)
    # cargo.extend(c9)
    # cargo.extend(c10)
    # cargo.extend(c11)
    # cargo.extend(c12)
    # cargo.extend(c13)
    # cargo.extend(c14)
    # cargo.extend(c15)
    cargo = Cargo()
    for i in range(24):
        c = CargoType(108, 76, 30, 1, 1)
        cargo.extend(c)
    for i in range(7):
        c = CargoType(110,43, 25, 1, 1)
        cargo.extend(c)
    for i in range(22):
        c = CargoType(92, 81, 55, 1, 1)
        cargo.extend(c)
    for i in range(13):
        c = CargoType(81, 33, 28, 1, 1)
        cargo.extend(c)
    for i in range(15):
        c = CargoType(120, 99, 73, 1, 1)
        cargo.extend(c)
    container = Container(587, 233, 220)
    case = Solver(cargo, container, 0)
    # case = Solver(cargo, container, 0)
    # case = Solver(cargo, container, 1)
    time_start = time.time()
    case.solve()
    time_end = time.time()
    # print(container.volume)
    print(container.useage())
    time_c = time_end - time_start  # 运行所花时间
    print('time cost', time_c, 's')
    container.status_save()
    drawer.draw_reslut(container)