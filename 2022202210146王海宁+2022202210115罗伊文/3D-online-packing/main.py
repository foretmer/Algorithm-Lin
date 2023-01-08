
import numpy as np
from envs import PackingDiscrete
from tools import get_args_heuristic
from draw_3d import show_3d
import time
'''
Randomly pick placements from full coordinates.
'''


def random(env, times=2000):
    done = False
    episode_utilization = []
    episode_length = []
    episode_packed_items = []
    env.reset()
    bin_size = env.bin_size

    for counter in range(times):
        packed_items = []
        while True:
            if done:
                # Reset the enviroment when the episode is done
                result = env.space.get_ratio()
                l = len(env.space.boxes)
                print('Result of episode {}, utilization: {}, length: {}'.format(counter, result, l))
                episode_utilization.append(result), episode_length.append(l)
                env.reset()
                done = False
                break

            next_box = env.next_box
            next_den = env.next_den

            # Check the feasibility of all placements.
            candidates = []
            candidates_packed = []
            for lx in range(bin_size[0] - next_box[0] + 1):
                for ly in range(bin_size[1] - next_box[1] + 1):
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

                        feasible, height = env.space.drop_box_virtual([x, y, z], (lx, ly), False,
                                                                         next_den, True, False)
                        if not feasible:
                            continue

                        candidates.append([[x, y, z], [0, lx, ly]])
                        candidates_packed.append([x,y,z,lx,ly,height])

            if len(candidates) != 0:
                # Pick one placement randomly from all possible placements
                idx = np.random.randint(0, len(candidates))
                env.next_box = candidates[idx][0]
                env.step(candidates[idx][1])
                packed_items.append(candidates_packed[idx])
                done = False
            else:
                # No feasible placement, this episode is done.
                episode_packed_items.append(packed_items)
                done = True

    return episode_utilization, episode_length, episode_packed_items


'''
An Online Packing Heuristic for the Three-Dimensional Container Loading
Problem in Dynamic Environments and the Physical Internet
https://doi.org/10.1007/978-3-319-55792-2\_10
'''


def OnlineBPH(env, times=2000):
    done = False
    episode_utilization = []
    episode_length = []
    episode_packed_items = []
    env.reset()

    for counter in range(times):
        packed_items = []
        while True:
            if done:
                # Reset the enviroment when the episode is done
                result = env.space.get_ratio()
                l = len(env.space.boxes)
                print('Result of episode {}, utilization: {}, length: {}'.format(counter, result, l))
                episode_utilization.append(result), episode_length.append(l)
                env.reset()
                done = False
                break

            # Sort the ems placement with deep-bottom-left order.
            EMS = env.space.EMS
            EMS = sorted(EMS, key=lambda ems: (ems[2], ems[1], ems[0]), reverse=False)

            bestAction = None
            next_box = env.next_box
            next_den = env.next_den
            stop = False

            for ems in EMS:
                # Find the first suitable placement within the allowed orientation.
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

                    # Check the feasibility of this placement
                    feasible, height = env.space.drop_box_virtual([x, y, z], (ems[0], ems[1]), False,
                                                                      next_den, True, False)
                    if feasible:
                        env.next_box = [x, y, z]
                        bestAction = [0, ems[0], ems[1]]
                        packed_item = [x, y, z, ems[0], ems[1], height]
                        stop = True
                        break
                if stop: break

            if bestAction is not None:
                # Place this item in the environment with the best action.
                _, _, done, _ = env.step(bestAction)
                packed_items.append(packed_item)
            else:
                # No feasible placement, this episode is done.
                episode_packed_items.append(packed_items)
                done = True

    return episode_utilization, episode_length, episode_packed_items


def MyHeuristic(env, times=2000):
    done = False
    episode_utilization = []
    episode_length = []
    env.reset()

    for counter in range(times):
        while True:
            if done:
                # Reset the enviroment when the episode is done
                result = env.space.get_ratio()
                l = len(env.space.boxes)
                print('Result of episode {}, utilization: {}, length: {}'.format(counter, result, l))
                episode_utilization.append(result), episode_length.append(l)
                env.reset()
                done = False
                break

            next_box = env.next_box
            next_den = env.next_den

            bestAction = None

            EMS_utilization, EMS_posvec = env.space.EMSUtilization(next_box, next_den)

            candidate_ems = []
            candidate_pos = set()

            best_ems_utilization = max(EMS_utilization.values())
            # print(best_ems_utilization)
            for key in EMS_utilization.keys():
                if EMS_utilization[key] == best_ems_utilization:
                    candidate_ems.append(key)
                    poses = EMS_posvec[key]
                    for i in range(len(poses)):
                        candidate_pos.add(poses[i])

            if len(candidate_pos) == 0:
                done = True
                continue

            # 计算DBL最佳解集
            candidate_pos_DBL_score = dict()
            second_candidate_pos = set()
            for pos in candidate_pos:
                pos_list = list(pos)
                lx = pos_list[0]
                ly = pos_list[1]
                lz = pos_list[2]
                DBL_score = lx + ly + 100 * lz
                candidate_pos_DBL_score[pos] = DBL_score
            best_DBL_score = min(candidate_pos_DBL_score.values())
            for pos in candidate_pos_DBL_score.keys():
                if candidate_pos_DBL_score[pos] == best_DBL_score:
                    second_candidate_pos.add(pos)

            # 计算OUR最佳解集
            candidate_pos_OUR_score = dict()
            best_pos = None
            for pos in second_candidate_pos:
                pos_list = list(pos)
                rx = pos_list[3]
                ry = pos_list[4]
                rz = pos_list[5]
                OUR_score = rx + ry + 100 * rz
                candidate_pos_OUR_score[pos] = OUR_score
            best_OUR_score = min(candidate_pos_OUR_score.values())
            for pos in candidate_pos_OUR_score.keys():
                if candidate_pos_OUR_score[pos] == best_OUR_score:
                    best_pos = pos
                    break

            # 最佳动作
            if best_pos is not None:
                lx = best_pos[0]
                ly = best_pos[1]
                lz = best_pos[2]
                rx = best_pos[3]
                ry = best_pos[4]
                rz = best_pos[5]
                env.next_box = [rx - lx, ry - ly, rz - lz]
                bestAction = [0, lx, ly]

            if bestAction is not None:
                # Place this item in the environment with the best action.
                _, _, done, _ = env.step(bestAction)
            else:
                # No feasible placement, this episode is done.
                done = True

    return np.mean(episode_utilization), np.var(episode_utilization), np.mean(episode_length)


'''
A Hybrid Genetic Algorithm for Packing in 3D with Deepest Bottom Left with Fill Method
https://doi.org/10.1007/978-3-540-30198-1\_45
'''


def DBL(env, times=2000):
    done = False
    episode_utilization = []
    episode_length = []
    episode_packed_items = []
    env.reset()
    bin_size = env.bin_size

    for counter in range(times):
        packed_items = []
        while True:
            if done:
                # Reset the enviroment when the episode is done
                result = env.space.get_ratio()
                # pack的Item的个数
                l = len(env.space.boxes)
                print('Result of episode {}, utilization: {}, length: {}'.format(counter, result, l))
                episode_utilization.append(result), episode_length.append(l)
                env.reset()
                done = False
                break

            bestScore = 1e10
            bestAction = []
            packed_item = []

            # 当前的item
            next_box = env.next_box
            # item密度为1
            next_den = env.next_den

            for lx in range(bin_size[0] - next_box[0] + 1):
                for ly in range(bin_size[1] - next_box[1] + 1):
                    # Find the most suitable placement within the allowed orientation.
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

                        # Check the feasibility of this placement
                        feasible, height = env.space.drop_box_virtual([x, y, z], (lx, ly), False,
                                                                      next_den, True, False)
                        if not feasible:
                            continue

                        # Score the given placement.
                        score = lx + ly + 100 * height
                        if score < bestScore:
                            bestScore = score
                            env.next_box = [x, y, z]
                            bestAction = [0, lx, ly]
                            packed_item = [x, y, z, lx, ly, height]

            if len(bestAction) != 0:
                # Place this item in the environment with the best action.
                env.step(bestAction)
                packed_items.append(packed_item)
                done = False
            else:
                # No feasible placement, this episode is done.
                episode_packed_items.append(packed_items)
                done = True

    return episode_utilization, episode_length, episode_packed_items


if __name__ == '__main__':
    args = get_args_heuristic()

    env = PackingDiscrete(container_size=args.container_size,
                          item_set=args.item_size_set,
                          data_name=args.dataset_path,
                          load_test_data=args.load_dataset,
                          internal_node_holder=200,
                          leaf_node_holder=1000)

    if args.heuristic == 'RANDOM':
        episode_utilization, episode_length, episode_packed_items = random(env, args.evaluation_episodes)
    elif args.heuristic == 'OnlineBPH':
        episode_utilization, episode_length, episode_packed_items = OnlineBPH(env, args.evaluation_episodes)
    elif args.heuristic == 'DBL':
        episode_utilization, episode_length, episode_packed_items = DBL(env, args.evaluation_episodes)
        # mean, var, length = MyHeuristic(env, args.evaluation_episodes)
    start=time.time()
    print('The average space utilization:', np.mean(episode_utilization))
    print('The variance of space utilization:', np.var(episode_utilization))
    print('The average number of packed items:', np.mean(episode_length))
    for i in range(len(episode_packed_items)):
        print("--------第{}次装箱，坐标打印--------".format(i+1))
        # 每个元素是个长为6个列表，列表的前三个是物品的大小x,y,z，后三个是物品的左下角坐标x,y,z
        print(episode_packed_items[i])
    end=time.time()
    best_utilization = 0
    best_time = -1
    for i in range(len(episode_utilization)):
        if best_utilization < episode_utilization[i]:
            best_utilization = episode_utilization[i]
            best_time = i
    print(list(env.bin_size))
    show_3d(list(env.bin_size), episode_packed_items[best_time])
