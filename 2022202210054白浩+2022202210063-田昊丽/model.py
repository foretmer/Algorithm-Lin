import math
import copy
import random
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

INFEASIBLE = 100000

"""
包装序列始终可以映射到可行的包装方案中，因此不用担心坐标重复，即在遗传算法中不用担心染色体重复
"""
def generateInstances(N=20, m=10, V=(100, 100, 100)):
    def ur(lb, ub):
        value = random.uniform(lb, ub)
        # return int(value) if value >= 1 else 1
        return value

    L, W, H = V
    p = []
    q = []
    r = []
    for i in range(N):
        p.append(round(ur(1 / 6 * L, 1 / 4 * L), 2))
        q.append(round(ur(1 / 6 * W, 1 / 4 * W), 2))
        r.append(round(ur(1 / 6 * H, 1 / 4 * H), 2))

    L = [L] * m
    W = [W] * m
    H = [H] * m
    return range(N), range(m), p, q, r, L, W, H


def generateInputs(N, m, V):
    N, M, p, q, r, L, W, H = generateInstances(N, m, V)
    inputs = {'v': list(zip(p, q, r)), 'V': list(zip(L, W, H))}
    return inputs


"""
放置货物，实时表示货物的尺寸以及集装箱（货车）的尺寸
"""


class Bin():
    def __init__(self, V, verbose=False):
        self.dimensions = V
        self.EMSs = [[np.array((0, 0, 0)), np.array(V)]]
        self.load_items = []

        if verbose:
            print('初始化 EMSs:', self.EMSs)

    def __getitem__(self, index):
        return self.EMSs[index]

    def __len__(self):
        return len(self.EMSs)

    """
    通过记录集装箱（货车）剩余的可用空间，来跟踪记录盒子的位置
    1、从现有的剩余可用空间集合中选择一个剩余可用空间
    2、盒子与现有的剩余可用空间相交产生新的剩余可用空间，并且删除所相交的剩余可用空间
    3、移除无法放置现有货物的剩余可用空间，和完全被其他剩余可用空间包容的剩余可用空间
    """

    def update(self, box, selected_EMS, min_vol=1, min_dim=1, verbose=False):

        # 1、在一个剩余可用空间中放置一个货物
        boxToPlace = np.array(box)
        # 在剩余可用空间中选择一个剩余可用空间
        selected_min = np.array(selected_EMS[0])
        # 计算货物在所选择的剩余可用空间中留下的最大空间
        ems = [selected_min, selected_min + boxToPlace]
        self.load_items.append(ems)

        if verbose:
            print('\n放置货物:\n剩余可用空间:', list(map(tuple, ems)))

        # 2、生成新的剩余可用空间，此由货物之间的交叉点产生
        for EMS in self.EMSs.copy():
            # 判断是否剩余可用空间之间有重叠覆盖
            if self.overlapped(ems, EMS):
                # 消除重叠覆盖的剩余可用空间
                self.eliminate(EMS)
                if verbose:
                    print('\n消除:\n去除的重叠剩余可用空间:', list(map(tuple, EMS)), '\nEMSs 剩余:',
                          list(map(lambda x: list(map(tuple, x)), self.EMSs)))

                # 相交的剩余可用空间最小和最大坐标
                x1, y1, z1 = EMS[0]
                x2, y2, z2 = EMS[1]
                # 货物的最小和最大坐标
                # x3, y3, z3 = ems[0]
                x4, y4, z4 = ems[1]
                # 三维空间下产生新的剩余可用空间
                # new_EMSs = [
                #     [(x1, y1, z1), (x3, y2, z2)],
                #     [(x4, y1, z1), (x2, y2, z2)],
                #     [(x1, y1, z1), (x2, y3, z2)],
                #     [(x1, y4, z1), (x2, y2, z2)],
                #     [(x1, y1, z1), (x2, y2, z3)],
                #     [(x1, y1, z4), (x2, y2, z2)]
                # ]
                # 在实际中，把盒子的最小坐标与剩余可用空间相等，因为通常情况下两个货物之间留下的空隙难以放下新的货物
                new_EMSs = [
                    [np.array((x4, y1, z1)), np.array((x2, y2, z2))],
                    [np.array((x1, y4, z1)), np.array((x2, y2, z2))],
                    [np.array((x1, y1, z4)), np.array((x2, y2, z2))]
                ]
                # 遍历新产生的剩余可用空间
                for new_EMS in new_EMSs:
                    new_box = new_EMS[1] - new_EMS[0]
                    isValid = True

                    if verbose:
                        print('\n新产生\n剩余可用空间:', list(map(tuple, new_EMS)))

                    # 3、消除掉完全被其他剩余可用空间包含的新产生的剩余可用空间
                    for other_EMS in self.EMSs:
                        if self.inscribed(new_EMS, other_EMS):
                            isValid = False
                            if verbose:
                                print('---> 完全被包含:', list(map(tuple, other_EMS)))

                    # 4、新产生的剩余可用空间不能小于剩余货物的体积
                    if np.min(new_box) < min_dim:
                        isValid = False
                        if verbose:
                            print('---> 新的剩余可用空间太小.')

                    # 5、新产生的剩余可用空间尺寸不能小于剩余货物中最小的尺寸
                    if np.product(new_box) < min_vol:
                        isValid = False
                        if verbose:
                            print('---> 新的剩余空间体积太小.')
                    # 6、如果有效，则添加新的剩余可用空间
                    if isValid:
                        self.EMSs.append(new_EMS)
                        if verbose:
                            print('---> 添加成功\n新产生的剩余可用空间:', list(map(tuple, new_EMS)))

        if verbose:
            print('\n结束:')
            print('剩余可用空间集合:', list(map(lambda x: list(map(tuple, x)), self.EMSs)))

    # 检查一个剩余可用空间是否与另一个剩余可用空间重叠
    def overlapped(self, ems, EMS):
        if np.all(ems[1] > EMS[0]) and np.all(ems[0] < EMS[1]):
            return True
        return False

    # 检查一个剩余可用空间是否包含于另一个剩余可用空间之中
    def inscribed(self, ems, EMS):
        if np.all(EMS[0] <= ems[0]) and np.all(ems[1] <= EMS[1]):
            return True
        return False

    def eliminate(self, ems):
        # numpy数组不能直接进行比较，需要进行转成list
        ems = list(map(tuple, ems))
        for index, EMS in enumerate(self.EMSs):
            if ems == list(map(tuple, EMS)):
                self.EMSs.pop(index)
                return

    # 获取剩余可用空间集合
    def get_EMSs(self):
        return list(map(lambda x: list(map(tuple, x)), self.EMSs))

    def load(self):
        return np.sum([np.product(item[1] - item[0]) for item in self.load_items]) / np.product(self.dimensions)


"""
放置货物策略类，利用启发式规则，在货物摆放的顺序中决定每一个货物需要摆放在哪一个剩余可用空间中
启发式规则：与集装箱（货车）的前顶角距离，货物每次都放在剩余可用空间中，同时保持距离最大化
"""
class PlacementProcedure():
    def __init__(self, inputs, solution, verbose=False):
        self.Bins = [Bin(V) for V in inputs['V']]
        self.boxes = inputs['v']
        self.BPS = np.argsort(solution[:len(self.boxes)])
        self.VBO = solution[len(self.boxes):]
        self.num_opend_bins = 1
        self.bin_used_volume = [0] * 2

        self.verbose = verbose
        if self.verbose:
            print('------------------------------------------------------------------')
            print('|--- 放置货物信息结果 ---')
            print('|---> 所有货物信息:', self.boxes)
            print('|---> 货物放置顺序:', self.BPS)
            print('|---> 货物摆放方式:', self.VBO)
            print('-------------------------------------------------------------------')

        self.infisible = False
        self.placement()

    """
    利用启发式规则，从现有的剩余可用空间集合中选择一个剩余可用空间来放置货物。
    根据n个货物的放置顺序，这个启发式规则重复使用n次；
    如果货物不能继续放入剩余可用空间中，将考虑放在新的集装箱（货车）中，
    boxes为货物的集合，bins为集装箱（货车）的集合，num_opened_bins为使用的集装箱（货车）的数量
    """

    def placement(self):
        # 按照货物的摆放顺序装入集装箱
        items_sorted = [self.boxes[i] for i in self.BPS]

        # 货物的选择
        for i, box in enumerate(items_sorted):
            if self.verbose:
                print('选择的箱子:', box)
                box_volume = box[0] * box[1] * box[2]

            # 选择的集装箱（货车）和剩余可用空间
            selected_bin = None
            selected_EMS = None
            for k in range(self.num_opend_bins):
                # 利用启发式规则选择满足距离最大化的剩余可用空间
                EMS = self.DFTRC_2(box, k)

                # 成功选择集装箱（货车）和剩余可用空间
                if EMS != None:
                    selected_bin = k
                    selected_EMS = EMS
                    break

            # 将货物放在新的集装箱（货车）中
            if selected_bin == None:
                self.num_opend_bins += 1
                selected_bin = self.num_opend_bins - 1
                if self.num_opend_bins > len(self.Bins):
                    self.infisible = True

                    if self.verbose:
                        print('集装箱数量不够，无法装载所有货物. [无解]')
                    return
                # 从新的集装箱中选择第一个也是唯一的剩余可用口空间
                selected_EMS = self.Bins[selected_bin].EMSs[0]
                if self.verbose:
                    print('没有可用的集装箱...... 打开集装箱', selected_bin)

            if self.verbose:
                print('选择货物摆放位置:', list(map(tuple, selected_EMS)))

            # 货物摆放状态的选择
            BO = self.selecte_box_orientaion(self.VBO[i], box, selected_EMS)

            # 确定消除规则的最小维度和最小尺寸
            min_vol, min_dim = self.elimination_rule(items_sorted[i + 1:])

            # 将货物放在集装箱（货车）中，并且更新状态信息
            self.Bins[selected_bin].update(self.orient(box, BO), selected_EMS, min_vol, min_dim)

            if self.verbose:
                print('添加货物到集装箱',selected_bin)
                self.bin_used_volume[selected_bin] += box_volume
                print('---> 集装箱内部状态:',self.Bins[selected_bin].get_EMSs())
                print('----------------------------------------------------------')

    # 启发式规则：与集装箱（货车）的前顶角距离
    def DFTRC_2(self, box, k):
        maxDist = -1
        selectedEMS = None

        for EMS in self.Bins[k].EMSs:
            # D, W, H 是一个集装箱（货车）的深度、宽度、高度
            D, W, H = self.Bins[k].dimensions
            # 遍历货物的摆放状态
            for direction in [1, 2, 3, 4, 5, 6]:
                d, w, h = self.orient(box, direction)
                # 如果货物满足当前的剩余可用空间
                if self.fitin((d, w, h), EMS):
                    # 剩余可用空间的最小坐标
                    x, y, z = EMS[0]
                    # 剩余可用空间与集装箱（货车）距离
                    distance = pow(D - x - d, 2) + pow(W - y - w, 2) + pow(H - z - h, 2)
                    # 找到最大距离的剩余可用空间
                    if distance > maxDist:
                        maxDist = distance
                        selectedEMS = EMS
        return selectedEMS

    # 确定货物的摆放状态
    def orient(self, box, BO=1):
        d, w, h = box
        # BO表示货物的摆放状态
        if BO == 1:
            return (d, w, h)
        elif BO == 2:
            return (d, h, w)
        elif BO == 3:
            return (w, d, h)
        elif BO == 4:
            return (w, h, d)
        elif BO == 5:
            return (h, d, w)
        elif BO == 6:
            return (h, w, d)

    def selecte_box_orientaion(self, VBO, box, EMS):
        # 在每一种编码解决方案中，前n个基因定义为货物的摆放顺序（BPS）
        # 随机密钥后n个基因编码表示为货物的摆放状态（6种之一）
        # BOs表示了货物所有可能的摆放状态，货物摆放状态向量
        BOs = []
        for direction in [1, 2, 3, 4, 5, 6]:
            if self.fitin(self.orient(box, direction), EMS):
                BOs.append(direction)

        # 依据货物摆放状态向量，选择货物的具体摆放状态
        selectedBO = BOs[math.ceil(VBO * len(BOs)) - 1]

        # if self.verbose:
        #     print('选择货物的摆放状态:', selectedBO,'  (所有可能的摆放状态',BOs, ', 货物的状态向量', VBO,')')
        return selectedBO

    def fitin(self, box, EMS):
        # 循环确保剩余可用空间完全可以包含货物
        for d in range(3):
            if box[d] > EMS[1][d] - EMS[0][d]:
                return False
        return True

    def elimination_rule(self, remaining_boxes):
        if len(remaining_boxes) == 0:
            return 0, 0

        min_vol = 999999999
        min_dim = 9999
        for box in remaining_boxes:
            # 最小化维度
            dim = np.min(box)
            if dim < min_dim:
                min_dim = dim

            # 最小化尺寸
            vol = np.product(box)
            if vol < min_vol:
                min_vol = vol
        return min_vol, min_dim

    """
    适应度函数：利用使用集装箱的数量进行计算
    原理：如果两个方案使用了相同的数量的集装箱，以及产生了相同的适应度函数的值，在没有装满的货物里面如果货物数量最少，在满的的集装箱里是摆放的更加紧凑
    """

    def evaluate(self):
        if self.infisible:
            return INFEASIBLE

        leastLoad = 1
        for k in range(self.num_opend_bins):
            load = self.Bins[k].load()
            if load < leastLoad:
                leastLoad = load
        return self.num_opend_bins + leastLoad % 1

"""
有偏随机密钥遗传算法类
"""
class BRKGA():
    def __init__(self, inputs, num_generations=100, num_individuals=60, num_elites=10, num_mutants=7, eliteCProb=0.7,
                 multiProcess=False):
        # 多线程处理设置
        self.multiProcess = multiProcess
        # 输入，货物的数量
        self.inputs = copy.deepcopy(inputs)
        self.N = len(inputs['v'])

        # 定义遗传算法中种群和个体的数量
        self.num_generations = num_generations
        self.num_individuals = int(num_individuals)
        # 货物的数量为self.N，随机密钥（基因染色体）的长度为2*self.N
        self.num_gene = 2 * self.N
        # 精英组的数量
        self.num_elites = int(num_elites)
        # 产生新的突变个体的数量
        self.num_mutants = int(num_mutants)
        # 选择父辈来自精英组的概率
        self.eliteCProb = eliteCProb

        # 解决方案信息
        self.used_bins = -1
        self.solution = None
        self.best_fitness = -1
        self.history = {
            'mean': [],
            'min': []
        }

    def decoder(self, solution):
        placement = PlacementProcedure(self.inputs, solution)
        return placement.evaluate()

    def cal_fitness(self, population):
        fitness_list = list()

        for solution in population:
            decoder = PlacementProcedure(self.inputs, solution)
            fitness_list.append(decoder.evaluate())
        return fitness_list

    # 每一代种群根据适应度函数值，分为精英种群和非精英种群
    def partition(self, population, fitness_list):
        # 前n个基因定义为货物的摆放顺序，利用 np.argsort函数进行升序排列，之后获取对应的索引
        sorted_indexs = np.argsort(fitness_list)
        return population[sorted_indexs[:self.num_elites]], population[sorted_indexs[self.num_elites:]], \
        np.array(fitness_list)[sorted_indexs[:self.num_elites]]

    def crossover(self, elite, non_elite):
        # 交叉操作，对于每一个基因都有一定的概率从精英组或者非精英组中进行选择
        return [elite[gene] if np.random.uniform(low=0.0, high=1.0) < self.eliteCProb else non_elite[gene] for gene in
                range(self.num_gene)]

    # 有偏的选择父辈其中包括一个来自精英组，另一个来自非精英组
    def mating(self, elites, non_elites):
        # 子代的数量取决于每个种群的个体的数量和突变体的数量
        num_offspring = self.num_individuals - self.num_elites - self.num_mutants
        return [self.crossover(random.choice(elites), random.choice(non_elites)) for i in range(num_offspring)]

    # 突变操作，没有在原本的基因的基础之上产生突变基因，而是产生新的个体插入到种群之中
    def mutants(self):
        return np.random.uniform(low=0.0, high=1.0, size=(self.num_mutants, self.num_gene))

    # 进化过程：所有的精英组的个体都被保留到下一代种群中，在交叉和突变中产生的新的个体也保留到下一代种群中，评估每一代的适应度函数，保留最优值
    def fit(self, patient=15, verbose=True):
        # 初始化种群信息，进行编码，种群信息表示为在[0,1]范围之内矢量
        population = np.random.uniform(low=0.0, high=1.0, size=(self.num_individuals, self.num_gene))
        # 初始化适应度函数值
        fitness_list = self.cal_fitness(population)

        if verbose:
            print('\n初始种群信息:')
            print('  ---> 种群形状:', population.shape)
            print('  ---> 适应度:', max(fitness_list))

        # 最好的适应度函数以及最好的解决方案（种群）
        best_fitness = np.min(fitness_list)
        best_solution = population[np.argmin(fitness_list)]
        self.history['min'].append(np.min(fitness_list))
        self.history['mean'].append(np.mean(fitness_list))

        # 重复进行遗传迭代
        best_iter = 0
        for g in range(self.num_generations):

            # 如果当前种群与最优种群满足一定条件，提前终止迭代，搜索结束
            if g - best_iter > patient:
                self.used_bins = math.floor(best_fitness)
                self.best_fitness = best_fitness
                self.solution = best_solution
                if verbose:
                    print('提前停止迭代', g, '(结束搜索)')
                return '有解'

            # 选择精英组，非精英组，以及适应度函数
            elites, non_elites, elite_fitness_list = self.partition(population, fitness_list)

            # 有偏的进行交叉，产生后代新的个体
            offsprings = self.mating(elites, non_elites)

            # 进行变异产生后代中新的个体
            mutants = self.mutants()

            # 产生所有新的后代以及对应后代的适应度函数值
            offspring = np.concatenate((mutants, offsprings), axis=0)

            offspring_fitness_list = self.cal_fitness(offspring)
            # 新的种群由所有的精英组和产生新的后代组成
            population = np.concatenate((elites, offspring), axis=0)
            fitness_list = list(elite_fitness_list) + list(offspring_fitness_list)

            # 更新最优的适应度函数值
            for fitness in fitness_list:
                if fitness < best_fitness:
                    best_iter = g
                    best_fitness = fitness
                    best_solution = population[np.argmin(fitness_list)]

            self.history['min'].append(np.min(fitness_list))
            self.history['mean'].append(np.mean(fitness_list))

            if verbose:
                print("迭代次数 :", g, ' \t(适应度:', best_fitness, ')', )

        self.used_bins = math.floor(best_fitness)
        self.best_fitness = best_fitness
        self.solution = best_solution
        return '有解'