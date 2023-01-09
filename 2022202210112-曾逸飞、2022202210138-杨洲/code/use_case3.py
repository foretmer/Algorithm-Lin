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
    if (i < 20):
        result = containerA.add_cargo_to_container(Cargo(97, 81, 27))
    elif (i >= 20 and i < 40):
        result = containerA.add_cargo_to_container(Cargo(102, 78, 39))
    elif (i >= 40 and i < 60):
        result = containerA.add_cargo_to_container(Cargo(113, 46, 36))
    elif (i >= 60 and i < 80):
        result = containerA.add_cargo_to_container(Cargo(101, 30, 26))
    elif (i >= 80 and i < 100):
        result = containerA.add_cargo_to_container(Cargo(66, 50, 42))
    elif (i >= 100 and i < 120):
        result = containerA.add_cargo_to_container(Cargo(100, 56, 35))
    elif (i >= 120 and i < 140):
        result = containerA.add_cargo_to_container(Cargo(91, 50, 40))
    else:
        result = containerA.add_cargo_to_container(Cargo(106, 61, 56))

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