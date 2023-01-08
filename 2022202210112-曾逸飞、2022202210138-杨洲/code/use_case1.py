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
    if (i < 50):
        result = containerA.add_cargo_to_container(Cargo(108,76,30))
    elif (i >= 50 and i < 110):
        result = containerA.add_cargo_to_container(Cargo(110, 43, 25))
    else:
        result = containerA.add_cargo_to_container(Cargo(92, 81, 55))

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
