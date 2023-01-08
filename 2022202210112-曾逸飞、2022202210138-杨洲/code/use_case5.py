from add_box import *
from time import process_time

process_time()
containerA = Container(587, 233, 220)
collect = []
import random

test_num = [i for i in range(160)]
random.shuffle(test_num)  # 随机打乱顺序
for t in range(160):
    i = test_num[t]
    if (i < 10):
        result = containerA.add_cargo_to_container(Cargo(108, 76, 30))
    elif (i >= 10 and i < 20):
        result = containerA.add_cargo_to_container(Cargo(110, 43, 25))
    elif (i >= 20 and i < 30):
        result = containerA.add_cargo_to_container(Cargo(92, 81, 55))
    elif (i >= 30 and i < 40):
        result = containerA.add_cargo_to_container(Cargo(110, 43, 25))
    elif (i >= 40 and i < 50):
        result = containerA.add_cargo_to_container(Cargo(81, 33, 28))
    elif (i >= 50 and i < 60):
        result = containerA.add_cargo_to_container(Cargo(120, 99, 73))
    elif (i >= 60 and i < 70):
        result = containerA.add_cargo_to_container(Cargo(98, 72, 46))
    elif (i >= 70 and i < 80):
        result = containerA.add_cargo_to_container(Cargo(95, 66, 31))
    elif (i >= 80 and i < 90):
        result = containerA.add_cargo_to_container(Cargo(85, 84, 30))
    elif (i >= 90 and i < 100):
        result = containerA.add_cargo_to_container(Cargo(71, 32, 25))
    elif (i >= 100 and i < 110):
        result = containerA.add_cargo_to_container(Cargo(36, 34, 25))
    elif (i >= 110 and i < 120):
        result = containerA.add_cargo_to_container(Cargo(97, 67, 62))
    elif (i >= 120 and i < 130):
        result = containerA.add_cargo_to_container(Cargo(33, 25, 23))
    elif (i >= 130 and i < 140):
        result = containerA.add_cargo_to_container(Cargo(95, 27, 26))
    else:
        result = containerA.add_cargo_to_container(Cargo(94, 81, 44))

    if (result == False):
        print('编号' + str(t) + "无法装入")
        collect.append(containerA.calculate_usage())
    else:
        collect.append(containerA.calculate_usage())
        # print(containerA.calculate_usage())
print("程序运行时间是: {:9.9}s".format(process_time()))
draw_reslut(containerA)
plt.figure()
plt.plot([i for i in range(160)],collect)
print('利用率', containerA.calculate_usage())
plt.xlabel("箱子编号")
plt.ylabel("累计利用率")
plt.show()

