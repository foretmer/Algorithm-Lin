import numpy as np
import argparse
from bin3D import Packing
import time

def BPH(env, times = 2000):
    done = False
    episode_utilization = []
    episode_length = []
    env.reset()
    item_idx = 0
    for counter in range(times):
        while True:
            if done:
                result = env.space.get_ratio()
                l = len(env.space.boxes)
                episode_utilization.append(result), episode_length.append(l)
                env.reset()
                done = False
                break

            EMS = env.space.EMS
            EMS = sorted(EMS, key=lambda ems: (ems[2], ems[1], ems[0]), reverse=False)

            bestAction = None
            next_box = env.next_box
            next_den = env.next_den
            stop = False


            for ems in EMS:
                if np.sum(np.abs(ems)) == 0:
                    continue
                for rot in range(env.orientation):
                    if rot == 0:
                        x, y, z = next_box
                    elif rot == 1:
                        y, x, z = next_box
                    elif rot == 2:
                        z, x, y = next_box
                    elif rot == 3:
                        z, y, x = next_box
                    elif rot == 4:
                        x, z, y = next_box
                    elif rot == 5:
                        y, z, x = next_box

                    feasible, height = env.space.drop_box_virtual([x, y, z], (ems[0], ems[1]), False, next_den, env.setting, returnH = True)
                    if feasible:
                        env.next_box = [x, y, z]
                        bestAction = [0, ems[0], ems[1], height]
                        stop = True
                        break
                if stop: break

            if bestAction is not None:
                item_idx += 1
                # f = open('result_BPH.txt', 'a', encoding='utf-8')
                # print('箱子{}: {}'.format(item_idx, tuple(bestAction[1:4])), file=f)
                # f.close()
                print('箱子{}: {}'.format(item_idx, tuple(bestAction[1:4])))
                _, _, done, _ = env.step(bestAction[0:3])
            else:
                done = True

    return np.mean(episode_utilization), int(np.mean(episode_length))

def DBL(env, times = 2000):
    def eval_ems(ems):
        s = 0
        valid = []
        for bs in env.item_set:
            bx, by, bz = bs
            if ems[3] - ems[0] >= bx and ems[4] - ems[1] >= by and ems[5] - ems[2] >= bz:
                valid.append(1)
        s += (ems[3] - ems[0]) * (ems[4] - ems[1]) * (ems[5] - ems[2])
        s += len(valid)
        if len(valid) == len(env.item_set):
            s += 10
        return s

    done = False
    episode_utilization = []
    episode_length = []
    env.reset()
    item_idx = 0
    for counter in range(times):
        while True:

            if done:
                result = env.space.get_ratio()
                l = len(env.space.boxes)
                episode_utilization.append(result), episode_length.append(l)
                env.reset()
                done = False
                break
            

            bestScore = -1e10
            EMS = env.space.EMS

            bestAction = None
            next_box = env.next_box
            next_den = env.next_den

            for ems in EMS:
                for rot in range(env.orientation):
                    if rot == 0:
                        x, y, z = next_box
                    elif rot == 1:
                        y, x, z = next_box
                    elif rot == 2:
                        z, x, y = next_box
                    elif rot == 3:
                        z, y, x = next_box
                    elif rot == 4:
                        x, z, y = next_box
                    elif rot == 5:
                        y, z, x = next_box

                    if ems[3] - ems[0] >= x and ems[4] - ems[1] >= y and ems[5] - ems[2] >= z:
                        lx, ly = ems[0], ems[1]
                        feasible, height = env.space.drop_box_virtual([x, y, z], (lx, ly), False,
                                                                          next_den, env.setting, returnH=True)
                        if feasible:
                            score = eval_ems(ems)
                            if score > bestScore:
                                bestScore = score
                                env.next_box = [x, y, z]
                                bestAction = [0, lx, ly, height]


            if bestAction is not None:
                item_idx += 1
                # f = open('result_DBL.txt', 'a', encoding='utf-8')
                # print('箱子{}: {}'.format(item_idx, tuple(bestAction[1:4])), file=f)
                # f.close()
                print('箱子{}: {}'.format(item_idx, tuple(bestAction[1:4])))
                _, _, done, _ = env.step(bestAction[0:3])
            else:
                done = True

    return  np.mean(episode_utilization), int(np.mean(episode_length))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Heuristic baseline arguments')
    parser.add_argument('--method', type=str, default='BPH', help='Options: BPH DBL')
    args = parser.parse_args()

    container_size = [587,233,220]
    data = open('3DLoad-test-dataSet.txt', encoding='utf-8')
    item_size_sets = []
    for line in data.readlines():
        if 'B' in line and 'l1' not in line:
            items = []
            temp1 = line.split('(')
            for i in range(1, len(temp1)):
                temp2 = temp1[i].split(')')[0].split(' ')
                num = int(temp2[-1])
                for j in range(num):
                    items.append((int(temp2[0]), int(temp2[1]), int(temp2[2])))
            item_size_sets.append(items)
    utilization_list = []
    length_list = []
    run_time_list = []
    if args.method == 'BPH':
        filename = 'result_BPH.txt'
    elif args.method == 'DBL':
        filename = 'result_DBL.txt'
    for i in range(len(item_size_sets)):
        # f = open(filename, 'a', encoding='utf-8')
        # print('序列{:d}'.format(i + 1), file=f)
        # f.close()
        print('序列{:d}'.format(i + 1))
        start_time = time.time()
        item_size_set = item_size_sets[i]
        PackingEnv = Packing

        env = PackingEnv(setting = 2,
                            container_size = container_size,
                            item_set = item_size_set,
                            internal_node_holder = 200,
                            leaf_node_holder = 1000)

        if args.method == 'BPH':
            utilization, length = BPH(env, 1)
        elif args.method == 'DBL':
            utilization, length = DBL(env, 1)
        end_time = time.time()
        run_time = end_time - start_time
        # f = open(filename, 'a', encoding='utf-8')
        # print('摆放箱子个数: {}'.format(length), file=f)
        # print('空间利用率: {:.2f}%'.format(utilization * 100.), file=f)
        # print('平均装箱时间: {:.4f}秒'.format(run_time / length), file=f)
        # f.close()
        print('摆放箱子个数: {}'.format(length))
        print('空间利用率: {:.2f}%'.format(utilization * 100.))
        print('平均装箱时间: {:.4f}秒'.format(run_time / length))
        length_list.append(length)
        utilization_list.append(utilization)
        run_time_list.append(run_time / length)
    for i in range(len(utilization_list)):
        print('序列{}: {:.2f}%'.format(i + 1, utilization_list[i] * 100.))
        # print('序列{}: {}\t{:.2f}%\t{:.4f}'.format(i + 1, length_list[i], utilization_list[i] * 100., run_time_list[i]))
    # print('平均摆放箱子个数: {}'.format(sum(length_list) / len(length_list)))
    print('平均空间利用率: {:.2f}%'.format(100. * sum(utilization_list) / len(utilization_list)))
    # print('平均装箱时间: {:.4f}秒'.format(sum(run_time_list) / len(run_time_list)))
