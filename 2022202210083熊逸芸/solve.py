import random
import datetime
import numpy as np
import copy
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#设置图表刻度等格式
from matplotlib.ticker import MultipleLocator


def box(ax, x, y, z, dx, dy, dz, color='red'):
    '''
    make_pic的内置函数
    用来在图像里面不断添加立方体
    '''
    xx = [x, x, x + dx, x + dx, x]
    yy = [y, y + dy, y + dy, y, y]
    kwargs = {'alpha': 1, 'color': color}
    ax.plot3D(xx, yy, [z] * 5, **kwargs)  # 下底
    ax.plot3D(xx, yy, [z + dz] * 5, **kwargs)  # 上底
    ax.plot3D([x, x], [y, y], [z, z + dz], **kwargs)
    ax.plot3D([x, x], [y + dy, y + dy], [z, z + dz], **kwargs)
    ax.plot3D([x + dx, x + dx], [y + dy, y + dy], [z, z + dz], **kwargs)
    ax.plot3D([x + dx, x + dx], [y, y], [z, z + dz], **kwargs)
    return ax


def make_pic(Items):
    '''
    显示图形的函数：Items = [[num[0],num[1],num[2],num[3],num[4],num[5],num[6]],]
    Items是N个列表的列表，里面的每个列表数据[放置点O三维坐标，长宽高，颜色]
    '''
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.xaxis.set_major_locator(MultipleLocator(50))
    ax.yaxis.set_major_locator(MultipleLocator(50))
    ax.zaxis.set_major_locator(MultipleLocator(50))
    for num in Items:
        box(ax, num[0], num[1], num[2], num[3], num[4], num[5], num[6])
    plt.title('Cube')
    plt.show()


def make(O, C, color):
    '''
    根据图显需要的数据，把尺寸数据生成绘图数据
    '''
    data = [O[0], O[1], O[2], C[0], C[1], C[2], color]
    return data


def show_solve(warehouse_size, solve):
    '''
    解可视化
    '''
    show_cube = [make((0, 0, 0), warehouse_size, 'red')]  # 车厢数据
    for good in solve['put']:
        show_cube.append(make(good['loc'], good['size'], 'blue'))
    make_pic(show_cube)


def convert_goods():
    '''
    根据输入数据生成箱子
    '''
    x = input()
    kinds = x.split(", ")
    goods = []
    count = 0
    for kind in kinds:
        nums = kind[1:-1].split(" ")
        size = [int(nums[0]), int(nums[1]), int(nums[2])]
        num = int(nums[3])
        for i in range(num):
            goods.append({"id": count, "size": size})
            count += 1
    return goods


def judge_warehouse(select_point, j_good, warehouse):
    """
    判断新放入的箱子位置是否合法
    是否超出车厢边界
    """
    if select_point[0] + j_good['size'][0] <= warehouse['size'][0] and \
            select_point[1] + j_good['size'][1] <= warehouse['size'][1] and \
            select_point[2] + j_good['size'][2] <= warehouse['size'][2]:
        return True
    return False


def judge_other_goods(space, select_point, j_good):
    """
    判断新放入的箱子位置是否合法
    是否与其他箱子重合
    """
    x, y, z = select_point[0], select_point[1], select_point[2]
    d, w, h = j_good['size'][0], j_good['size'][1], j_good['size'][2]
    if space[x, y, z] | space[x + d - 1, y, z] | space[x, y + w - 1, z] | space[x, y, z + h - 1] | \
            space[x + d - 1, y + w - 1, z] | space[x + d - 1, y, z + h - 1] | space[x, y + w - 1, z + h - 1] | \
            space[x + d - 1, y + w - 1, z + h - 1]:
        return False
    return True



def put_box(space, select_point, j_good):
    '''
    将箱子放置在select_point
    箱子相应位置令为1表示不能再放置
    '''
    x, y, z = select_point[0], select_point[1], select_point[2]
    d, w, h = j_good['size'][0], j_good['size'][1], j_good['size'][2]
    space[x:x + d, y:y + w, z:z + h] = 1
    return space


def put_goods(a_popu, warehouse):
    """
    在warehouse中按照a_popu的顺序和方式放置
    返回空间利用率和放置结果
    """
    warehouse_d, warehouse_w, warehouse_h = warehouse['size']

    # 以1为单位分割车厢空间，0为未放置，1为已放置
    space = np.zeros((warehouse_d, warehouse_w, warehouse_h), dtype=np.int)  
    put_point = [[0, 0, 0]]  # 可选放置点
    solve = {'size': warehouse['size'], 'put': []}  # 最后装入物品的集合

    for i in range(len(a_popu)):
        # 排序放置点
        put_point.sort(key=lambda x: (x[2], x[1], x[0]))
        g = a_popu[i]
        g_d, g_w, g_h = g['size']
        # 跳过大于车厢的箱子
        if g_d > warehouse_d or g_w > warehouse_w or g_h > warehouse_h:
            continue

        # 在车厢的每个放置点尝试放置箱子
        for index, point in enumerate(put_point):
            # 若在当前放置点放置箱子合法
            if judge_warehouse(point, g, warehouse) and judge_other_goods(space, point, g):
                # 放置箱子，更新空间
                space = put_box(space, point, g)
                # 更新解决方案，装入车厢
                input_g={'id':g['id'],'size':g['size'],'loc':point}
                solve['put'].append(input_g)

                # 删除当前放置点
                put_point.pop(index)

                # 添加新的放置点，即当前箱子相邻位置
                put_point.append([point[0] + g_d, point[1], point[2]])
                put_point.append([point[0], point[1] + g_w, point[2]])
                put_point.append([point[0], point[1], point[2] + g_h])
                break

    space_ratio = space.sum() / (warehouse_d * warehouse_w * warehouse_h)
    return space_ratio, solve


def exchange_good(goods):
    '''
    随机交换两个箱子顺序
    '''
    if len(goods) != 1:
        s1, s2 = random.randint(0, len(goods) - 1), random.randint(0, len(goods) - 1)
        while s1 == s2:
            s2 = random.randint(0, len(goods) - 1)
        goods[s1], goods[s2], = goods[s2], goods[s1]
    return goods


def exchange_direction(goods):
    '''
    随机交换某个箱子的摆放状态
    '''
    s = random.randint(0, len(goods) - 1)
    g = goods[s]
    s1, s2 = random.randint(0, len(g['size']) - 1), random.randint(0, len(g['size']) - 1)
    while s1 == s2:
        s2 = random.randint(0, len(g['size']) - 1)
    g['size'][s1], g['size'][s2], = g['size'][s2], g['size'][s1]
    goods[s] = g
    return goods


def crossover(p1, p2):
    """
    交叉
    后代=P2装箱子顺序+P1装箱摆放方式
    """
    p3 = copy.deepcopy(p2)
    for i in range(len(p1)):
        max1 = p1[i]['size'].index(max(p1[i]['size']))
        p3[i]['size'][max1] = max(p2[i]['size'])

        min1 = p1[i]['size'].index(min(p1[i]['size']))
        p3[i]['size'][min1] = min(p2[i]['size'])

        max2 = p2[i]['size'].index(max(p2[i]['size']))
        min2 = p2[i]['size'].index(min(p2[i]['size']))
        index1 = list({0, 1, 2} - {max1, min1})[0]
        index2 = list({0, 1, 2} - {max2, min2})[0]
        p3[i]['size'][index1] = p2[i]['size'][index2]
    return p3


def integral(list_x):
    list_integral = []
    x_sum = 0
    for x in list_x:
        x_sum += x
        list_integral.append(x_sum)
    return list_integral


def my_random(list_integral):
    p = random.uniform(0, max(list_integral))
    for i in range(len(list_integral)):
        if p < list_integral[i]:
            break
    return i


def init_population(goods, population_size):
    '''
    初始化族群
    个数为population_size
    '''
    population = []
    for i in range(population_size):
        for j in range(100):
            if random.random() > 0.5:  # 随机交换两个箱子放置顺序
                goods = exchange_good(goods)
            else:  # 随机交换某个箱子的放置方式
                goods = exchange_direction(goods)
        population.append(copy.deepcopy(goods))
    return population


def genetic_algorithm(goods, population_size, exchange_n, mutation_n, deadline, warehouse):
    """
    遗传算法
    """
    # 初始化种群
    population = init_population(goods, population_size)
    values = []
    solves = []
    for i in range(len(population)):
        value, solve = put_goods(population[i], warehouse)
        values.append(value)
        solves.append(solve)

    # 记录最好解决方案
    min_value = max(values)  # 最好空间利用率
    index = values.index(min_value)
    best_solve = solves[index]  # 最好防止方式
    list_integral = integral(values)

    # 开始遗传
    # 若车厢装满，或所有箱子放置完毕，或当前时间大于ddl，停止迭代
    while len(goods) - len(best_solve['put']) > 0 and min_value != 1.0 and datetime.datetime.now() < deadline:
        # 交叉
        for i in range(exchange_n):
            s1, s2 = my_random(list_integral), my_random(list_integral)
            while s1 == s2:
                s2 = my_random(list_integral)
            solve_new = crossover(population[s1], population[s2])
            population.append(solve_new)
            value, solve = put_goods(solve_new, warehouse)
            values.append(value)
            solves.append(solve)

        # 变异
        for i in range(len(population)):
            for j in range(mutation_n):
                if random.random() > 0.5:  # 随机交换两个箱子顺序
                    population[i] = exchange_good(population[i])
                else:  # 随机变换某个箱子的放置方式
                    population[i] = exchange_direction(population[i])
            value, solve = put_goods(population[i], warehouse)
            values[i] = value
            solves[i] = solve

        # 自然选择，控制种群规模不变
        for i in range(exchange_n):
            index = values.index(min(values))
            del values[index]
            del solves[index]
            del population[index]

        # 记录最好解决方案
        min_value = max(values)  # 最好空间利用率
        index_best = values.index(min_value)
        best_solve = solves[index_best]  # 最好防止方式
        list_integral = integral(values)

    return min_value, best_solve


def main():
    # 车厢和货物
    goods = convert_goods()
    warehouse_size = [587, 233, 220]
    warehouse = {'size': warehouse_size, 'goods': []}

    # 超参数，通过调节超参数优化结果
    deadline = datetime.datetime.now() + datetime.timedelta(seconds=2) # 遗传ddl    
    population_size = 60  # 种群规模
    exchange_n = 15  # 交叉次数
    mutation_n = 5  # 变异次数

    # 遗传算法
    min_remains, best_solve = genetic_algorithm(goods, population_size, exchange_n, mutation_n, deadline, warehouse)

    # 最优装箱策略信息
    goods_no = []
    goods_ok = []
    for g in goods:
        for b in best_solve['put']:
            goods_ok.append(b['id'])  # 已装箱子id
        if g['id'] not in goods_ok:  # 未装箱子
            goods_no.append(g)

    print('空间利用率', min_remains)
    print('最好的装箱策略', best_solve)

    # 最优装箱策略可视化
    show_solve(warehouse['size'], best_solve)


if __name__ == "__main__":
    main()
