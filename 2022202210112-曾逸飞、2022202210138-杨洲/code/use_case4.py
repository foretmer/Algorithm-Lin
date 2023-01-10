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
    if (i < 15):
        result = containerA.add_cargo_to_container(Cargo(97,81,27))
    elif (i >= 15 and i < 30):
        result = containerA.add_cargo_to_container(Cargo(113,46,36))
    elif (i >= 30 and i < 45):
        result = containerA.add_cargo_to_container(Cargo(66,50,42))
    elif (i >= 45 and i < 60):
        result = containerA.add_cargo_to_container(Cargo(110, 43, 25))
    elif (i >= 60 and i < 75):
        result = containerA.add_cargo_to_container(Cargo(100,56,35))
    elif (i >= 75 and i < 90):
        result = containerA.add_cargo_to_container(Cargo(91,50,40))
    elif (i >= 90 and i < 105):
        result = containerA.add_cargo_to_container(Cargo(106,61,56))
    elif (i >= 105 and i < 120):
        result = containerA.add_cargo_to_container(Cargo(103,63,58))
    elif (i >= 120 and i < 135):
        result = containerA.add_cargo_to_container(Cargo(103, 63, 58))
    else:
        result = containerA.add_cargo_to_container(Cargo(102,78,39))

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
