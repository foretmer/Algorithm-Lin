from Common import *
import argparse

def to_axis(char):
    assert len(char) == 1, Axis.UnknownAxis
    if char == "l":
        return Axis.LENGTH
    elif char == "w":
        return Axis.WIDTH
    elif char == "h":
        return Axis.HEIGHT
    else:
        raise Axis.UnknownAxis

def to_online_method(method):
    if method == "brute":
        return OnlineSearchMethod.BRUTE
    elif method == "greedy":
        return OnlineSearchMethod.GREEDY
    elif method == "candidate_points":
        return OnlineSearchMethod.CANDIDATE_POINTS
    elif method == "sub_space":
        return OnlineSearchMethod.SUB_SPACE
    else:
        raise OnlineSearchMethod.UnknownSearchMethod

def to_offline_method(method):
    if method == "candidate_points":
        return OfflineSearchMethod.CANDIDATE_POINTS
    else:
        raise OfflineSearchMethod.UnknownSearchMethod

def to_bin_sort_method(method):
    if method == "volumn_min":
        return BinSortMethod.VOLUMN_MIN
    elif method == "volumn_max":
        return BinSortMethod.VOLUMN_MAX
    elif method == "portion_similar":
        return BinSortMethod.PORTION_SIMILAR
    elif method == "approximate_max":
        return BinSortMethod.APPROXIMATE_MAX
    else:
        raise BinSortMethod.UnknownSortMethod

def to_point_add_method(method):
    if method == "axis":
        return PointAddMethod.AXIS
    elif method == "surround":
        return PointAddMethod.SURROUND
    elif method == "envelope":
        return PointAddMethod.ENVELOPE
    elif method == "all":
        return PointAddMethod.ALL
    else:
        raise PointAddMethod.UnknownAddMethod

def to_point_sort_method(method):
    if method == "axis":
        return PointSortMethod.AXIS
    elif method == "sum_min":
        return PointSortMethod.SUM_MIN
    elif method == "portion_min":
        return PointSortMethod.PORTION_MIN
    else:
        raise PointSortMethod.UnknownSortMethod

def get_args():
    # parse_known_args()
    task_parser = argparse.ArgumentParser()
    task_parser.add_argument("--bin_types", type=int, required=True, choices=[3,5,8,10,15])
    task_parser.add_argument("--test_index", type=int, required=False, default=0, choices=[0,1,2,3,4,5])
    task_parser.add_argument("--strict_level", type=int, required=False ,default=2, choices=[0,1,2,3])  
    task_args, remain_args = task_parser.parse_known_args()

    type_parser = argparse.ArgumentParser()
    type_parser.add_argument("--type", required=True, choices=["online", "offline"])
    type_args, remain_args = type_parser.parse_known_args(remain_args)
    
    method_parser = argparse.ArgumentParser()

    if type_args.type == "online":
        method_parser.add_argument("--method", type=to_online_method, required=True, choices=[OnlineSearchMethod.BRUTE,OnlineSearchMethod.GREEDY,OnlineSearchMethod.CANDIDATE_POINTS,OnlineSearchMethod.SUB_SPACE])
        method_args, remain_args = method_parser.parse_known_args(remain_args)
        
        config_parser = argparse.ArgumentParser()
        config_parser.add_argument("--axises_rotate", nargs=3, type=to_axis, required=False, default=[Axis.LENGTH,Axis.WIDTH,Axis.HEIGHT])
        if method_args.method == OnlineSearchMethod.BRUTE:  # 暴力搜索 
            config_parser.add_argument("--axises", nargs=3, type=to_axis, required=False, default=[Axis.LENGTH,Axis.WIDTH,Axis.HEIGHT])
            config_args = config_parser.parse_args(remain_args)
        elif method_args.method == OnlineSearchMethod.GREEDY: # 贪心算法
            config_parser.add_argument("--axises", nargs=2, type=to_axis, required=False, default=[Axis.LENGTH,Axis.WIDTH])
            config_args = config_parser.parse_args(remain_args)
        elif method_args.method == OnlineSearchMethod.CANDIDATE_POINTS: # 候选点搜索
            config_parser.add_argument("--candidate_add_method", type=to_point_add_method, required=False, default=PointAddMethod.ALL)
            config_parser.add_argument("--candidate_sort_method", type=to_point_sort_method, required=False, default=PointSortMethod.SUM_MIN)
            config_parser.add_argument("--axises", nargs=3, type=to_axis, required=False, default=[Axis.LENGTH,Axis.WIDTH,Axis.HEIGHT])
            config_parser.add_argument("--try_rotate", action="store_true")
            config_args = config_parser.parse_args(remain_args) 
    elif type_args.type == "offline":
        method_parser.add_argument("--method", type=to_offline_method, required=True, choices=[OfflineSearchMethod.CANDIDATE_POINTS])
        method_args, remain_args = method_parser.parse_known_args(remain_args)
        config_parser = argparse.ArgumentParser()
        config_parser.add_argument("--axises_rotate", nargs=3, type=to_axis, required=False, default=[Axis.LENGTH,Axis.WIDTH,Axis.HEIGHT])
        if method_args.method == OfflineSearchMethod.CANDIDATE_POINTS:  
            config_parser.add_argument("--bin_sort_method", type=to_bin_sort_method, required=False, default=BinSortMethod.APPROXIMATE_MAX)
            config_parser.add_argument("--candidate_add_method", type=to_point_add_method, required=False, default=PointAddMethod.ALL)
            config_parser.add_argument("--candidate_sort_method", type=to_point_sort_method, required=False, default=PointSortMethod.SUM_MIN)
            config_parser.add_argument("--axises", nargs=3, type=to_axis, required=False, default=[Axis.LENGTH,Axis.WIDTH,Axis.HEIGHT])
            config_args = config_parser.parse_args(remain_args)

    return task_args, type_args, method_args, config_args




