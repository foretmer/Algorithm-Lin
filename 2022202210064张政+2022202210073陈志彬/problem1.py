import random
from copy import deepcopy
from operator import itemgetter
import matplotlib.pyplot as plt
import visualize as vis
import time
import os
plt.rcParams['font.sans-serif']=['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False  # 用来正常显示负号


# 读取数据
def load_data():
    problem_list = {}
    with open('data.txt', encoding='utf-8', mode='r') as f:
        index = 0
        while True:
            line = f.readline()
            if not line:
                break
            if len(line) == 2 or len(line) == 3:
                for i in range(5):
                    sub_problem_list = {}
                    truck = f.readline()
                    truck = truck.strip("\n|(|) |'C'").split(' ')
                    truck = list(int(i) for i in truck)
                    box_list = []
                    boxes = f.readline()
                    boxes = boxes.strip("\n|'B'").split(',')
                    for _ in boxes:
                        box = _.strip("[ |( |) |] | [| ]| (| )").split(' ')
                        box = list(int(i) for i in box)
                        box_list.append(box)
                    sub_problem_list['truck dimension'] = truck
                    sub_problem_list['boxes'] = box_list
                    problem_list[str(index * 5 + i)] = sub_problem_list
                index = index + 1
    return problem_list


def init_pop(box_params, count, rotation):
    population = {}
    for i in range(4):  # 分别以长，宽，高，容积为维度，升序和降序，两种摆放方式，24
        # 从大到小排
        sorted_box = dict(sorted(box_params.items(), key=lambda x: x[1][i], reverse=True))
        population[i * 6] = {"order": list(sorted_box.keys()), "rotate": [random.randint(0, rotation - 1) for r in range(len(box_params))]}
        population[i * 6 + 1] = {"order": list(sorted_box.keys()), "rotate": [0 for r in range(len(box_params))]}  # 摆放方式全0
        population[i * 6 + 2] = {"order": list(sorted_box.keys()), "rotate": [1 for r in range(len(box_params))]}  # 摆放方式全1
        # 从小到大排
        sorted_box = dict(sorted(box_params.items(), key=lambda x: x[1][i]))
        population[i * 6 + 3] = {"order": list(sorted_box.keys()), "rotate": [random.randint(0, rotation - 1) for r in range(len(box_params))]}
        population[i * 6 + 4] = {"order": list(sorted_box.keys()), "rotate": [0 for r in range(len(box_params))]}  # 摆放方式全0
        population[i * 6 + 5] = {"order": list(sorted_box.keys()), "rotate": [1 for r in range(len(box_params))]}  # 摆放方式全1

    keys = list(box_params.keys())
    for i in range(24, count):  # 其余的个体是以随机顺序产生的。
        random.shuffle(keys)
        population[i] = {"order": deepcopy(keys), "rotate": [random.randint(0, rotation - 1) for r in range(len(box_params))]}
    return population


def evaluate(population, truck_dimension, boxes):
    container_vol = truck_dimension[0] * truck_dimension[1] * truck_dimension[2]  # 集装箱容量
    ft = {}
    for key, individual in population.items():
        remain_space = [[0, 0, 0] + truck_dimension]  # 初始剩余空间
        occupied_vol = 0
        number_boxes = 0
        result = []
        # 盒子放入编号和旋转角度,剩余空间排序最左（L）最下(H)，然后是(w)
        for box_number, r in zip(individual['order'], individual['rotate']):
            # 对剩余空间排序
            remain_space = sorted(remain_space, key=itemgetter(3))
            remain_space = sorted(remain_space, key=itemgetter(5))
            remain_space = sorted(remain_space, key=itemgetter(4))
            flag = 0
            for pos in remain_space:
                current = deepcopy(pos)
                space_vol = pos[3] * pos[4] * pos[5]  # 剩余空间体积
                box_vol = boxes[box_number][3]
                # 所给数据箱子的三个尺寸都是按照降序排列，最大面朝下
                if r == 0:
                    l, w, h = boxes[box_number][0:3]
                elif r == 1:
                    w, l, h = boxes[box_number][0:3]  # 基础部分的r为1或0
                elif r == 2:
                    l, h, w = boxes[box_number][0:3]
                elif r == 3:
                    h, l, w = boxes[box_number][0:3]
                elif r == 4:
                    h, w, l = boxes[box_number][0:3]
                else:
                    w, h, l = boxes[box_number][0:3]
                if space_vol >= box_vol and pos[3] >= l and pos[4] >= w and pos[5] >= h:  # 选中空间是否满足箱子
                    result.append(pos[0:3] + [l, w, h])  # 解的表示
                    occupied_vol += box_vol
                    number_boxes += 1
                    # 切分剩余空间，分成三个剩余的子空间，纵向分割
                    top_space = [pos[0], pos[1], pos[2] + h, l, w, pos[5] - h]
                    beside_space = [pos[0], pos[1] + w, pos[2], l, pos[4] - w, pos[5]]
                    front_space = [pos[0] + l, pos[1], pos[2], pos[3] - l, pos[4], pos[5]]
                    # 更新剩余空间
                    remain_space.remove(current)
                    remain_space.append(top_space)
                    remain_space.append(beside_space)
                    remain_space.append(front_space)
                    flag = 1
                    break
            if flag == 0:
                result.append(pos[0:3] + [0, 0, 0])  # 表示没找到解
        fitness = [round((occupied_vol / container_vol * 100), 4), number_boxes]
        ft[key] = fitness
        population[key]['fitness'] = deepcopy(fitness)
        population[key]['result'] = result
    return population, ft


# 交叉
def crossover(population, pc):
    # 选择父母
    parents = {}
    num = int(pc * len(population))
    individuals = list(population.values())
    for each in range(num):
        pool = random.sample(individuals, 2)  # 从样本中抽取两个，父母使用最优的那个，用锦标赛选取
        if pool[0]["fitness"][0] > pool[1]["fitness"][0]:
            parents[each] = pool[0]
            individuals.remove(pool[0])
        else:
            parents[each] = pool[1]
            individuals.remove(pool[1])
    # 交叉操作
    children = {}
    keys = list(parents.keys())
    random.shuffle(keys)  # 打乱
    for x in range(0, len(parents), 2):
        p_k1 = random.choice(keys)  # 找出两个父母
        p_o1 = deepcopy(parents[p_k1]['order'])
        p_r1 = deepcopy(parents[p_k1]['rotate'])
        keys.remove(p_k1)
        p_k2 = random.choice(keys)
        p_o2 = deepcopy(parents[p_k2]['order'])
        p_r2 = deepcopy(parents[p_k2]['rotate'])
        keys.remove(p_k2)
        # 找交叉的位置
        i = random.randint(1, int(len(p_o1) / 2) + 1)
        j = random.randint(i + 1, int(len(p_o1) - 1))
        # 生成子序列
        c_o1 = [-1] * len(p_o1)
        c_o2 = [-1] * len(p_o2)
        c_r1 = [-1] * len(p_r1)
        c_r2 = [-1] * len(p_r2)
        # 染色体是序列，所以直接交叉的话会存在重复
        c_o1[i:j + 1] = p_o1[i:j + 1]
        c_o2[i:j + 1] = p_o2[i:j + 1]
        c_r1[i:j + 1] = p_r1[i:j + 1]
        c_r2[i:j + 1] = p_r2[i:j + 1]
        # 交叉完后，遍历序列（两个子个体，每个个体有两个染色体，分别遍历），对没有的序列号进行添加
        pos = (j + 1) % len(p_o2)
        for k in range(len(p_o2)):
            if p_o2[k] not in c_o1 and c_o1[pos] == -1:  # 原序列该位置的序列号不在交叉后的序列，且该位置没有进行交叉
                c_o1[pos] = p_o2[k]
                pos = (pos + 1) % len(p_o2)
        pos = (j + 1) % len(p_o2)
        for k in range(len(p_o1)):
            if p_o1[k] not in c_o2 and c_o2[pos] == -1:
                c_o2[pos] = p_o1[k]
                pos = (pos + 1) % len(p_o1)
        pos = (j + 1) % len(p_o2)
        for k in range(len(p_r2)):
            if c_r1[pos] == -1:
                c_r1[pos] = p_r2[k]
                pos = (pos + 1) % len(p_r2)
        pos = (j + 1) % len(p_o2)
        for k in range(len(p_r1)):
            if c_r2[pos] == -1:
                c_r2[pos] = p_r1[k]
                pos = (pos + 1) % len(p_r1)
        children[x] = {'order': deepcopy(c_o1), 'rotate': deepcopy(c_r1)}
        children[x + 1] = {'order': deepcopy(c_o2), 'rotate': deepcopy(c_r2)}
    return children  # 产生的后代


# 变异
def mutate(children, pm1, pm2, rotation):
    for child in children.values():
        order = child['order']
        rotate = child['rotate']
        if random.uniform(0, 1) <= pm1:  # 概率判断是否变异，序列的变异
            i = random.randint(1, int(len(order) / 2) + 1)  # 产生位置
            j = random.randint(i + 1, int(len(order) - 1))
            order[i:j + 1] = order[j:i - 1:-1]  # 序列变异，翻转
            rotate[i:j + 1] = rotate[j:i - 1:-1]  # 对应的面变异，翻转
        # 摆放方式的变异
        for i in range(len(rotate)):
            if random.uniform(0, 1) <= pm2:
                rotate[i] = random.randint(0, rotation)
    return children


# 选择
def select(population, children, truck, boxes, count):
    survivors = {}
    children, fitness = evaluate(children, truck, boxes)  # 评估子代的适应值
    pool = list(population.values()) + list(children.values())  # 从父代和子代中进行选择
    # 根据适应值排序，选出新一代种群
    ft = [pool[i]["fitness"][0] for i in range(len(pool))]
    ind = sorted(range(len(ft)), key=lambda k: ft[k], reverse=True)
    avg_ft = 0
    for i in range(count):
        survivors[i] = pool[ind[i]]
        avg_ft += ft[ind[i]]
    avg_ft = round(avg_ft / count, 4)  # 计算平均适应值
    best_solution = pool[ind[0]]  # 找出种群中的最优解
    return survivors, avg_ft, best_solution


def plot_stats(avg_fts, max_fts, p_ind, new_dir_path):
    fig = plt.figure()
    x1 = range(len(avg_fts))
    plt.plot(x1, avg_fts, max_fts)
    plt.xlabel('迭代次数')
    plt.ylabel('适应值/填充率')
    plt.xticks(ticks=[t for t in x1 if t % 40 == 0])
    plt.title("第{}个实例的适应值/填充率变化情况".format(p_ind+1))
    plt.grid()
    plt.legend(['平均适应值/填充率曲线', '最大适应值/填充率曲线'])
    plt.savefig(os.path.join(new_dir_path, 'ft_{}.jpg'.format(p_ind + 1)), dpi=400)


# 遗传算法
ITERATIONS = 1  # 实验次数
INDIVIDUALS = 36  # 种群个体数量
GENERATIONS = 2  # 一次实验要迭代几次
PC = 0.8  # 交叉
PM1 = 0.2  # 变异，序列
PM2 = 0.02  # 变异，面
ROTATIONS = 2  # 2种摆放方式

problem_list = load_data()
problem_indices = list(problem_list.keys())
loca = time.strftime("%Y-%m-%d-%H-%M-%S")
new_dir_path = r'./results/p1_' + loca  # 保存结果路径
if not os.path.exists(new_dir_path):
    os.mkdir(new_dir_path)
for p_ind in problem_indices:  # 对每个实例
    print("----------第{}个实例----------".format(int(p_ind)+1))
    # 数据预处理
    truck_dimension = problem_list[p_ind]['truck dimension']  # 车厢尺寸
    boxes = problem_list[p_ind]['boxes']  # 箱子尺寸
    box_candit = []
    for candit in boxes:
        vol = candit[0] * candit[1] * candit[2]
        for i in range(candit[3]):  # 数量
            box_candit.append([candit[0], candit[1], candit[2], vol])  # 长、宽、高、体积
    boxes = box_candit
    box_params = {}
    # 从n中随机抽取m个
    # m = len(boxes)
    # random.seed(0)
    # candi_boxes = random.sample(boxes, m)
    # for index in range(len(candi_boxes)):
    #     box_params[index] = candi_boxes[index]
    for index in range(len(boxes)):
        box_params[index] = boxes[index]
    print("实例的箱子数量：{}".format(len(boxes)))

    # 存储每一次迭代的平均值
    for i in range(ITERATIONS):  # 要重复进行几次实验
        # 生成初始种群
        population = init_pop(box_params, INDIVIDUALS, ROTATIONS)
        avg_fts = []
        max_fts = []
        max_boxes = []
        best_solution = []
        time_start = time.time()
        for j in range(GENERATIONS):  # 每次实验迭代几次
            population, fitness = evaluate(population, truck_dimension, box_params)  # 计算适应值
            children = crossover(deepcopy(population), PC)  # 交叉
            children = mutate(children, PM1, PM2, ROTATIONS)  # 变异
            population, gen_ft, best_solution = select(population, children, truck_dimension, box_params, INDIVIDUALS)  # 选择新的下一代
            avg_fts.append(gen_ft)
            max_fts.append(best_solution["fitness"][0])
            max_boxes.append(best_solution["fitness"][1])
            # if j > 100 and len(set(deepcopy(gen_fts[-30:]))) > 1:  # 停止迭代的阈值
            #     break
        time_end = time.time()
        print("填充率：{} | 装箱数：{} | 时间：{}".format(max_fts[-1], max_boxes[-1], round(time_end - time_start, 4)))
        print("平均适应值：{}".format(avg_fts))
        print("最大适应值：{}".format(max_fts))
        print("最大箱子数：{}".format(max_boxes))
        # print("运行时间：{}".format(round(time_end - time_start, 4)))
        plot_stats(avg_fts, max_fts, int(p_ind), new_dir_path)  # 适应值图
        vis.draw(best_solution["result"], best_solution["fitness"][0], int(p_ind), new_dir_path)  # 放置结果可视化
    # if int(p_ind)==5:
    #     plt.show()
    #     break

plt.show()
