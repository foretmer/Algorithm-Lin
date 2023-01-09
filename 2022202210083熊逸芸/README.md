# 装箱问题解决方案

## 算法设计思路
输入：格式为 (l1, w1, h1, n1), (l2, w2, h2, n2),...的字符串，如(108 76 30 40), (110 43 25 33), (92 81 55 39)

输出：空间利用率，最优装箱策略(装入车厢的箱子位置、大小、id)，最优装箱策略3D展示

装箱问题采用遗传算法解决。考虑了六种放置方式，分别为长方体的三类面朝下摆放及旋转90度。设置遗传迭代最长时间为2s，超出则跳出迭代打印最优结果。

初始化：种群染色体为箱子的摆放方式和顺序。放置方式为从原点开始，在不超出车厢和不与其他箱子重合的前提下，与已放置箱子相邻摆放，旨在流出最大连续剩余空间摆放其余箱子。

交叉：父染色体1的装箱子顺序和父染色体2的装箱摆放方式得到子染色体。

变异：以一定概率随机交换两个箱子装箱顺序，或随机变换某个箱子的放置方式。

选择：淘汰空间利用率小的个体。

## 关键代码分析
介绍遗传算法解决装箱问题的遗传算法部分，分为种群初始化、交叉、变异和选择四部分。

遗传算法部分首先定义算法超参数，然后调用genetic\_algorithm()函数利用遗传算法解决装箱问题，最后打印最优装箱策略的结果。超参数包含截止时间、种群规模、交叉次数和变异次数。其中截止时间deadline在遗传迭代中使用，如果当前时间大于截至时间，停止迭代。

    deadline = datetime.datetime.now() + datetime.timedelta(seconds=2)  # 截止时间
    population_size = 60  # 种群规模
    exchange_n = 15  # 交叉次数
    mutation_n = 5  # 变异次数


遗传算法封装在genetic\_algorithm()函数中，包含初始箱子列表、种群规模、交叉次数、变异次数、截止时间和车厢信息六个参数。

    min_remains, best_solve = genetic_algorithm(goods, population_size, exchange_n, mutation_n, deadline, warehouse)


### 种群初始化
genetic\_algorithm()函数首先进行种群的初始化得到种群population。调用init\_population()函数进行初始箱子信息的交叉和变异，然后调用put\_goods()函数放置随机后的箱子。
    
    def genetic_algorithm(goods, population_size, exchange_n, mutation_n, deadline, warehouse):
	    population = init_population(goods, population_size)
	    values = []
	    solves = []
	    for i in range(len(population)):
	        value, solve = put_goods(population[i], warehouse)
	        values.append(value)
	        solves.append(solve)


init\_population()函数初始化种群，个数为population\_size。通过以50%的概率随机交换两个箱子放置顺序，50%的概率随机交换某个箱子的放置方式，对初始箱子信息进行随机操作得到初始化的种群。值得注意的是，需要用copy.deepcopy()进行复制防止每个种群信息的地址相同。

    def init_population(goods, population_size):
	    population = []
	    for i in range(population_size):
	        for j in range(100):
	            if random.random() > 0.5:
	                goods = exchange_good(goods)
	            else: 
	                goods = exchange_direction(goods)
	        population.append(copy.deepcopy(goods))
	    return population

init\_population()中随机交换某个箱子的放置方式通过exchange\_good()实现。算法采用了六种放置方式，分别为长方体的三类面朝下摆放及旋转90度。
    
    def exchange_good(goods):  # 随机交换两个箱子顺序
	    if len(goods) != 1:
	        s1, s2 = random.randint(0, len(goods) - 1), random.randint(0, len(goods) - 1)
	        while s1 == s2:
	            s2 = random.randint(0, len(goods) - 1)
	        goods[s1], goods[s2], = goods[s2], goods[s1]
	    return goods


put\_goods函数实现按照初始化种群后的箱子顺序和放置方式信息在车厢内放置箱子，将返回空间利用率和放置结果。put\_good函数首先调用split\_space()将车厢划分为小空间，然后初始化放置点为原点。
    
    def put_goods(a_popu, warehouse):
	    warehouse_d, warehouse_w, warehouse_h = warehouse['size']
	    space = split_space(warehouse_d, warehouse_w, warehouse_h)
	    put_point = [[0, 0, 0]]
	    solve = {'size': warehouse['size'], 'put': []}


由于放置点列表会进行更新，所以为保证约定的放置顺序，对放置点进行排序，并排除因为箱子大小超过车厢大小而无法放置的箱子。

    for i in range(len(a_popu)):
	    put_point.sort(key=lambda x: (x[2], x[1], x[0]))
	    g = a_popu[i]
	    g_d, g_w, g_h = g['size']
	    if g_d > warehouse_d or g_w > warehouse_w or g_h > warehouse_h:
	        continue


然后put\_goods函数依次实验在每个放置点放置包裹，如果箱子在这个位置能放成功，装入车厢。调用judge\_warehouse()函数和judge\_other\_goods()函数判断箱子在当前选定位置能否放进当前车厢，若能放进车厢则put\_box更新空间，并把箱子信息及放置位置加入当前解决方案。

    for index, point in enumerate(put_point):
	    if judge_warehouse(point, g, warehouse) and judge_other_goods(space, point, g):
	        space = put_box(space, point, g)
	        input_g={'id':g['id'],'size':g['size'],'loc':point}
	        solve['put'].append(input_g)


judge\_warehouse()函数通过判断箱子放置是否超出车厢边界，判断新放入的箱子放置是否合法。

    def judge_warehouse(select_point, j_good, warehouse):
	    if select_point[0] + j_good['size'][0] <= warehouse['size'][0] and \
	    select_point[1] + j_good['size'][1] <= warehouse['size'][1] and \
	    select_point[2] + j_good['size'][2] <= warehouse['size'][2]:
	    return True
	    else:
	    return False


judge\_other\_goods()函数通过判断新放置箱子是否与其他箱子放置空间重合，判断新放入的箱子放置是否合法，若新放置箱子八个顶点所在位置未填充则可以放入。

    def judge_other_goods(space, select_point, j_good):
	    x, y, z = select_point[0], select_point[1], select_point[2]
	    d, w, h = j_good['size'][0], j_good['size'][1], j_good['size'][2]
	    if space[x, y, z] | \
	            space[x + d - 1, y, z] | space[x, y + w - 1, z] | space[x, y, z + h - 1] | \
	            space[x + d - 1, y + w - 1, z] | space[x + d - 1, y, z + h - 1] | space[x, y + w - 1, z + h - 1] | \
	            space[x + d - 1, y + w - 1, z + h - 1]:
	        return False
	    else:
	        return True


回到put\_goods函数，如果箱子在选定位置能放置成功，还需要更新放置点，删除当前箱子放置点并添加与当前箱子相邻放置点。最后返回空间利用率和放置结果。

    put_point.pop(index)
    put_point.append([point[0] + g_d, point[1], point[2]])
    put_point.append([point[0], point[1] + g_w, point[2]])
    put_point.append([point[0], point[1], point[2] + g_h])


### 交叉
开始遗传操作。迭代进行交叉、变异和选择，知道所有箱子放置完毕或者时间大于截至时间，则停止迭代，输出最优结果。交叉操作随机选取两个不同的染色体s1和s2，然后利用crossover()函数实现交叉得到新染色体加入种群，并调用put\_goods()放置新箱子顺序即新染色体。

    while len(goods) - len(best_solve['put']) > 0 and min_value != 1.0 and datetime.datetime.now() < deadline:
	    for i in range(exchange_n):
	        s1, s2 = my_random(list_integral), my_random(list_integral)
	        while s1 == s2:
	            s2 = my_random(list_integral)
	        solve_new = crossover(population[s1], population[s2])
	        population.append(solve_new)
	        value, solve = put_goods(solve_new, warehouse)


crossover()函数实现父染色体p1和p2交叉得到新染色体p3。p3由P2装箱子顺序和P1装箱摆放方式得到。

    def crossover(p1, p2):
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


### 变异
交叉后进行变异操作。变异的策略为变异mutation\_n次，每次有50%的概率调用exchange\_good()随机交换两个箱子装箱顺序，另50%概率随机交换某个箱子的装柜姿势，然后根据新的箱子信息进行put\_goods()装箱，策略和种群初始化时相同。
    
    for i in range(len(population)):
	    for j in range(mutation_n):
	        if random.random() > 0.5:
	            population[i] = exchange_good(population[i])
	        else:
	            population[i] = exchange_direction(population[i])
	    value, solve = put_goods(population[i], warehouse)


### 选择
交叉变异后进行自然选择。由于交叉时两个父染色体会产生一个新的子染色体，为了控制种群规模不变，淘汰exchange\_n个染色体。淘汰策略为选择箱子占据空间小的染色体进行淘汰。
    
    for i in range(exchange_n):
	    index = values.index(min(values))
	    del values[index]
	    del solves[index]
	    del population[index]
