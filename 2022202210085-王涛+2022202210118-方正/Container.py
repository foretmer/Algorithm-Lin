from Common import *
import utils

from typing import Any, List, Tuple
from Bin import Bin
import numpy as np

class Container:
    def __init__(self, ml:float, mw:float, mh:float, precision:int=PRECISION):
        self.ml = ml
        self.mw = mw
        self.mh = mh
        self.precision = precision
        self.space = self.construct_space()
        self.envelope_space = self.construct_space()
        self.simple_space = self.construct_simple_space()
        self.candidate_points = []
        self.search_history = []

    @property
    def max_length(self):
        return utils.math_utils.to_precision(self.ml, self.precision)

    @property
    def max_width(self):
        return utils.math_utils.to_precision(self.mw, self.precision)

    @property
    def max_height(self):
        return utils.math_utils.to_precision(self.mh, self.precision)

    @property
    def size_list(self):
        return [self.max_length, self.max_width, self.max_height]

    @property
    def volumn(self):
        return self.max_length * self.max_width * self.max_height
    
    def __str__(self):
        format_ctrl = "({{0:.{0}f}},{{1:.{0}f}},{{2:.{0}f}})".format(self.precision)
        return format_ctrl.format(self.ml, self.mw, self.mh)

    def __repr__(self):
        format_ctrl = "[{{0:.{0}f}}({{3:d}}),{{1:.{0}f}}({{4:d}}),{{2:.{0}f}}({{5:d}})]".format(self.precision)
        return format_ctrl.format(self.ml, self.mw, self.mh,
                                  self.max_length, self.max_width, self.max_height)

    def construct_space(self) -> np.ndarray:
        return np.zeros((self.max_length, self.max_width, self.max_height), dtype=np.int32)

    def construct_simple_space(self) -> np.ndarray:
        return np.zeros((self.max_length, self.max_width), dtype=np.int32)

    @property
    def full_simple_space(self) -> np.ndarray:
        space = np.zeros((self.max_length, self.max_width, self.max_height), dtype=np.int32)
        for axis0 in range(self.simple_space.shape[0]):
            for axis1 in range(self.simple_space.shape[1]):
                space[axis0, axis1, :self.simple_space[axis0, axis1]] = 1
        return space
        
    @property
    def space_utilization(self) -> np.float32:
        return np.sum(self.space)/np.sum(np.ones_like(self.space))

    def str_2D_matrix(self, matrix:Any, compact:bool=False):
        map_str = str(matrix).replace("],","],\n").replace("'","").replace(",","").replace("1","█")
        if compact:
            map_str = map_str.replace(" ","").replace("[[","[").replace("]]","]")
        return map_str

    # h     h     w    
    # ↑     ↑     ↑    
    # |-→ w |-→ l |-→ l
    #   l     w     h
    def print_2D_slice(self, asix: Axis, slice_idx:int, compact:bool=False):
        if asix == Axis.LENGTH:
            matrix = np.transpose(self.space[slice_idx,:,:])
        elif asix == Axis.WIDTH:
            matrix = np.transpose(self.space[:,slice_idx,:])
        elif asix == Axis.HEIGHT:
            matrix = np.transpose(self.space[:,:,slice_idx])
        matrix = matrix[::-1,:]
        matrix = matrix.tolist()
        matrix_str = self.str_2D_matrix(matrix,compact)
        print(matrix_str)
    
    def point_within(self, position:Tuple[int,int,int]):
        length_within = \
        (0 <= position[0] and position[0] < self.space.shape[0]) 
        width_within = \
        (0 <= position[1] and position[1] < self.space.shape[1])
        height_within = \
        (0 <= position[2] and position[2] < self.space.shape[2])
        return length_within, width_within, height_within

    def within(self, new_bin:Bin, position:Tuple[int,int,int]) -> Tuple[bool, bool, bool]:
        length_within = \
        (0 <= position[0] and position[0] < self.space.shape[0]) and \
        (1 <= position[0] + new_bin.length and position[0] + new_bin.length <= self.space.shape[0])
        width_within = \
        (0 <= position[1] and position[1] < self.space.shape[1]) and \
        (1 <= position[1] + new_bin.width and position[1] + new_bin.width <= self.space.shape[1])
        height_within = \
        (0 <= position[2] and position[2] < self.space.shape[2]) and \
        (1 <= position[2] + new_bin.height and position[2] + new_bin.height <= self.space.shape[2])
        return length_within, width_within, height_within

    def stable(self, new_bin:Bin, position:Tuple[int,int,int], strict_level:int=3):
        lower_level = position[2] - 1
        if lower_level == -1:
            return True
        else:
            lower_level_slice = self.space[:,:,lower_level]
            bin_slice = lower_level_slice[position[0]:position[0]+new_bin.length,position[1]:position[1]+new_bin.width]
            # if np.sum(bin_slice)/np.sum(np.ones_like(bin_slice)) >= 1/2:
            #     return False
            if strict_level == 3:
                if bin_slice[0,0] == 1 and bin_slice[0,-1] == 1 and bin_slice[-1,0] == 1 and bin_slice[-1,-1] == 1:
                    return True
            elif strict_level == 2:
                if np.sum(bin_slice) > 0:
                    return True 
            elif strict_level == 1:
                if np.sum(lower_level_slice) > 0:
                    return True
            elif strict_level == 0:
                return True
        return False  

    def volumn_check(self, new_bin:Bin):
        remain_space = self.volumn - np.sum(self.space)
        if remain_space < new_bin.volume:
            return False
        else:
            return True
               
    def put(self, new_bin:Bin, position:Tuple[int,int,int], strict_level:int=3, just_try:bool=False) -> bool:
        within = self.within(new_bin, position)
        if not all(within):
            return (*within, True, True)
        if not self.stable(new_bin, position, strict_level):
            return (True, True, True, False, True)
        if np.sum(self.space[position[0]:position[0]+new_bin.length,
                             position[1]:position[1]+new_bin.width,
                             position[2]:position[2]+new_bin.height])  == 0:
            if not just_try:
                self.space[position[0]:position[0]+new_bin.length,
                           position[1]:position[1]+new_bin.width,
                           position[2]:position[2]+new_bin.height] = 1
                self.simple_space[position[0]:position[0]+new_bin.length,
                                   position[1]:position[1]+new_bin.width] = position[2]+new_bin.height
                self.envelope_space[:position[0]+new_bin.length,
                                   :position[1]+new_bin.width,
                                   :position[2]+new_bin.height] = 1
            return (True, True, True, True, True)            
        else:
            return (True, True, True, True, False)

    def find_envelope_in_slice(self,asix: Axis, slice_idx:int):
        if asix == Axis.LENGTH:
            matrix = self.envelope_space[slice_idx,:,:]
        elif asix == Axis.WIDTH:
            matrix = self.envelope_space[:,slice_idx,:]
        elif asix == Axis.HEIGHT:
            matrix = self.envelope_space[:,:,slice_idx]
        envelopes = []
        for x in range(len(matrix)):
            zero_idx = np.where(matrix[x]==0)[0]
            if len(zero_idx) == 0:
                return envelopes
            first_0 = np.min(zero_idx)
            if envelopes == []:
                envelopes.append((x, first_0))
            if first_0 == envelopes[-1][1]:
                continue
            else:
                envelopes.append((x, first_0))
        if asix == Axis.LENGTH:
            envelopes = [(slice_idx, envelope[0], envelope[1]) for envelope in envelopes]
        elif asix == Axis.WIDTH:
            envelopes = [(envelope[0], slice_idx, envelope[1]) for envelope in envelopes]
        elif asix == Axis.HEIGHT:
            envelopes = [(envelope[0], envelope[1], slice_idx) for envelope in envelopes]
        copy_envelopes = [envelope for envelope in envelopes]
        for envelope in copy_envelopes:
            near = 0
            if envelope[0] == 0 or self.envelope_space[envelope[0]-1,envelope[1],envelope[2]] == 1:
                near += 1
            if envelope[1] == 0 or self.envelope_space[envelope[0],envelope[1]-1,envelope[2]] == 1:
                near += 1  
            if envelope[2] == 0 or self.envelope_space[envelope[0],envelope[1],envelope[2]-1] == 1:
                near += 1  
            if near != 3:
                envelopes.remove(envelope)
        return envelopes          

    # TODO 这些点全部添加的效果并不好，考虑通过参数添加部分点
    def add_candidates(self, bin_place:Tuple[int,int,int], new_bin:Bin):
        length_slice = bin_place[0] + new_bin.length
        width_slice = bin_place[1] + new_bin.width
        height_slice = bin_place[2] + new_bin.height
        if length_slice < self.max_length:
            self.candidate_points.extend(self.find_envelope_in_slice(Axis.LENGTH, length_slice))
        if width_slice < self.max_width:
            self.candidate_points.extend(self.find_envelope_in_slice(Axis.WIDTH, width_slice))
        if height_slice < self.max_height:
            self.candidate_points.extend(self.find_envelope_in_slice(Axis.HEIGHT, height_slice))
        raw_surrounding_points = [(bin_place[0] + new_bin.length, bin_place[1], bin_place[2]),
                              (bin_place[0], bin_place[1] + new_bin.width, bin_place[2]),
                              (bin_place[0], bin_place[1], bin_place[2] + new_bin.height),
                              (bin_place[0] + new_bin.length, bin_place[1] + new_bin.width, bin_place[2]),
                              (bin_place[0] + new_bin.length, bin_place[1], bin_place[2] + new_bin.height),
                              (bin_place[0], bin_place[1] + new_bin.width, bin_place[2] + new_bin.height),
                              (bin_place[0] + new_bin.length, bin_place[1] + new_bin.width, bin_place[2] + new_bin.height)]
        surrounding_points = []
        for surrounding_point in raw_surrounding_points:
            if all(self.point_within(surrounding_point)):
                surrounding_points.append(surrounding_point)
        self.candidate_points.extend(surrounding_points)
        
        self.clear_occupied_candidates()
        self.clear_duplicate_candidates()
        self.candidates_sort()

    def clear_occupied_candidates(self):
        clear_idx = []
        for idx, candidate in enumerate(self.candidate_points):
            if self.envelope_space[candidate[0],candidate[1],candidate[2]] == 1:
                clear_idx.append(idx)
        idx_offset = 0
        for idx in clear_idx:
            self.candidate_points.pop(idx - idx_offset)
            idx_offset += 1              

    def clear_duplicate_candidates(self):
        candidates = []
        for idx, candidate in enumerate(self.candidate_points):
            already_in = False
            for in_candidate in candidates:
                if candidate[0] == in_candidate[0] and \
                   candidate[1] == in_candidate[1] and \
                   candidate[2] == in_candidate[2]:
                       already_in = True
                       break
            if not already_in:
                candidates.append(candidate)
        self.candidate_points = candidates

    # TODO 候选点的排列方法有问题，比当初分三个列表差，考虑通过参数选择排列方式
    def candidates_sort(self):
        point_scores = []
        for candidate in self.candidate_points:
            point_score = -(candidate[0] / self.max_length + candidate[1] / self.max_width + candidate[2] / self.max_height)
            point_scores.append(point_score)
        candidates = zip(self.candidate_points, point_scores)
        candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
        self.candidate_points = [candidate[0] for candidate in candidates]
    
    def update_history(self, 
                       new_bin:Bin, 
                       result:Tuple[int,int,int],
                       ori_method:SearchMethod,
                       real_method:SearchMethod):
        self.search_history.append((new_bin.size_list, result, ori_method, real_method))

    def search(self, 
               new_bin:Bin, 
               axises_rotate:Tuple[Axis, Axis, Axis], 
               method:SearchMethod, 
               strict_level:int=3, 
               **config):
        copy_bin = new_bin.copy()
        logger.info(f"Putting bin: {new_bin}, using {method}.")
        # 搜索历史检测，若上一个被放入的箱子没有找到，那同类型的也找不到
        last_end = (0, 0, 0)
        last_brute_end = (0, 0, 0)
        if self.search_history != [] and new_bin.size_list == self.search_history[-1][0]:
            if self.search_history[-1][1] == None:
                bin_location = None
                self.update_history(copy_bin, bin_location, method, SearchMethod.NONE)
                return bin_location
            else:
                if self.search_history[-1][2] == SearchMethod.BRUTE:
                    last_brute_end = self.search_history[-1][1]
                elif self.search_history[-1][2] == SearchMethod.GREEDY and self.search_history[-1][3] == SearchMethod.GREEDY:
                    last_end = self.search_history[-1][1]
                else:
                    if self.search_history[-1][3] == SearchMethod.BRUTE:
                        last_brute_end = self.search_history[-1][1]
        # 容量检测，如果容量过小，就肯定放不下
        if not self.volumn_check(new_bin):
            bin_location = None
            self.update_history(copy_bin, bin_location, method, SearchMethod.NONE)
            return bin_location
        
        new_bin.axis_sort(axises_rotate)
        # 选择搜索方法
        if method == SearchMethod.BRUTE:
            if not config["axises"]:
                config["axises"] = utils.axis_utils.full_axis_type()[0]
            bin_location, real_method = self.brute_search(space = self.space, 
                                                          new_bin = new_bin, 
                                                          axises = config["axises"], 
                                                          start_point = last_brute_end, 
                                                          strict_level = strict_level)          
        elif method == SearchMethod.CANDIDATE_POINTS:
            if not config["try_rotate"]:
                config["try_rotate"] = True
            bin_location, real_method = self.candidates_search(new_bin = new_bin, 
                                                               try_rotate = config["try_rotate"], 
                                                               strict_level = strict_level,
                                                               brute_start_point=last_brute_end)
        elif method == SearchMethod.SUB_SPACE:
            raise NotImplementedError("Serch method not implemented!")
        elif method == SearchMethod.GREEDY:
            if not config["axises"]:
                config["axises"] = utils.axis_utils.full_axis_type()[0][:2]
            bin_location, real_method = self.greedy_search(new_bin = new_bin,
                                                           axises = config["axises"],
                                                           start_point=last_end[:2],
                                                           strict_level = strict_level,
                                                           brute_start_point=last_brute_end)
            
        self.update_history(copy_bin, bin_location, method, real_method)
        return bin_location
  
    def brute_search(self, 
                     space:np.ndarray,
                     new_bin:Bin, 
                     axises:Tuple[Axis, Axis, Axis]=(Axis.LENGTH, Axis.WIDTH, Axis.HEIGHT), 
                     start_point:Tuple[int,int,int]=(0,0,0), 
                     strict_level:int=3) -> Tuple[Tuple[int,int,int], SearchMethod]:
        
        if not utils.axis_utils.valid_axis(axises):
            raise ValueError("Axises are not valid!")
        search_axis = utils.axis_utils.lwh_to_axis(self.size_list, axises)
        axis_start_point = utils.axis_utils.lwh_to_axis(start_point, axises)
        axis_space = np.transpose(space, (utils.axis_utils.lwh_to_axis_map(axises)))
        bin_axis = utils.axis_utils.lwh_to_axis(new_bin.size_list, axises)
        
        skip_axis = [False, False, False]
        for axis_0 in range(0, search_axis[0] - bin_axis[0] + 1):
            if axis_0 < axis_start_point[0]:
                continue
            if np.any(search_axis[1]*search_axis[2] - np.sum(axis_space[axis_0 : axis_0+bin_axis[0]], axis=(1,2)) < bin_axis[1] * bin_axis[2]):
                continue
            for axis_1 in range(0, search_axis[1] - bin_axis[1] + 1):
                if axis_0 == axis_start_point[0] and axis_1 < axis_start_point[1]:
                    continue
                if np.any(search_axis[2] - np.sum(axis_space[axis_0, axis_1 : axis_1+bin_axis[1]], axis=1) < bin_axis[2]):
                    continue
                for axis_2 in range(0, search_axis[2] - bin_axis[2] + 1):
                    if axis_0 == axis_start_point[0] and axis_1 == axis_start_point[1] and axis_2 < axis_start_point[2]:
                        continue
                    if axis_space[axis_0, axis_1, axis_2] == 1:
                        continue
                    axis_index_list = [axis_0, axis_1, axis_2]
                    idx_length, idx_width, idx_height = utils.axis_utils.axis_to_lwh(axis_index_list, axises)
                    results = self.put(new_bin, (idx_length, idx_width, idx_height), strict_level)
                    neg_result = [not result for result in results]
                    skip_axis = utils.axis_utils.lwh_to_axis(neg_result[:3], axises)
                    if any(skip_axis[:3]):
                        break
                    elif any(neg_result):
                        continue
                    else:
                        return (idx_length, idx_width, idx_height), SearchMethod.BRUTE
                if any(skip_axis[:2]):
                    break 
            if any(skip_axis[:1]):
                break
        return None, SearchMethod.BRUTE

    def candidates_search(self, 
                          new_bin:Bin,  
                          try_rotate:bool=True, 
                          strict_level:int=3,
                          brute_start_point:Tuple[int,int,int]=(0,0,0)) -> Tuple[Tuple[int,int,int], SearchMethod]:
        real_method = SearchMethod.CANDIDATE_POINTS
        if self.candidate_points == []:
            bin_location, real_method = self.brute_search(space = self.space, 
                                                          new_bin = new_bin, 
                                                          start_point = brute_start_point,
                                                          strict_level = strict_level)
        else:
            suit_one = False
            for idx_point, candidate_point in enumerate(self.candidate_points):
                suit = False
                if try_rotate:
                    for idx_axis, axis_type in enumerate(utils.axis_utils.full_axis_type()):
                        copy_bin = new_bin.copy()
                        copy_bin.axis_transform(axis_type)
                        results = self.put(copy_bin, candidate_point, strict_level)
                        if all(results):
                            if idx_axis != 0:
                                logger.info(f"Rotate bin to {axis_type}")
                            new_bin = copy_bin
                            bin_location = candidate_point
                            suit = True
                            break
                else:
                    results = self.put(new_bin, candidate_point, strict_level)
                    if all(results):
                        bin_location = candidate_point
                        suit = True
                if suit:
                    suit_one = True
                    break
            if not suit_one:
                bin_location, real_method = self.brute_search(space = self.space, 
                                                              new_bin = new_bin, 
                                                              start_point = brute_start_point,
                                                              strict_level = strict_level)
        if bin_location != None:
            self.add_candidates(bin_location, new_bin)
        return bin_location, real_method

    def sub_space_find(self, 
                       new_bin:Bin,  
                       strict_level:int=3,
                       brute_start_point:Tuple[int,int,int]=(0,0,0)) -> Tuple[Tuple[int,int,int], SearchMethod]:
        pass

    def greedy_search(self, 
                      new_bin:Bin,   
                      axises:Tuple[Axis, Axis]=(Axis.LENGTH, Axis.WIDTH),
                      start_point:Tuple[int,int,int]=(0,0),
                      strict_level:int=3,
                      brute_start_point:Tuple[int,int,int]=(0,0,0)) -> Tuple[Tuple[int,int,int], SearchMethod]: 
        assert len(axises) == 2
        search_axis = utils.axis_utils.lwh_to_axis(self.size_list[:2], axises)
        axis_start_point = utils.axis_utils.lwh_to_axis(start_point, axises)
        axis_space = np.transpose(self.simple_space, (utils.axis_utils.lwh_to_axis_map(axises)))
        bin_axis = utils.axis_utils.lwh_to_axis(new_bin.size_list[:2], axises)
        
        for axis_0 in range(0, search_axis[0] - bin_axis[0] + 1):
            if axis_0 < axis_start_point[0]:
                continue
            if np.any(search_axis[1] - np.sum(axis_space[axis_0 : axis_0 + bin_axis[0]], axis=1) < bin_axis[1]):
                continue
            for axis_1 in range(0, search_axis[1] - bin_axis[1] + 1):
                if axis_0 == axis_start_point[0] and axis_1 < axis_start_point[1]:
                    continue
                if axis_space[axis_0, axis_1] == 1:
                    continue
                bin_projection = axis_space[axis_0 : axis_0 + bin_axis[0], 
                                            axis_1 : axis_1 + bin_axis[1]]
                current_height = np.max(bin_projection)
                if (self.max_height - current_height >= new_bin.height):
                    axis_index_list = [axis_0, axis_1]
                    idx_length, idx_width, _ = utils.axis_utils.axis_to_lwh(axis_index_list, axises)
                    result = self.put(new_bin, (idx_length, idx_width, current_height), strict_level)
                    if all(result):
                        return (idx_length, idx_width, current_height), SearchMethod.GREEDY
        bin_location, real_method = self.brute_search(space = self.space, 
                                                      new_bin = new_bin, 
                                                      axises = [*axises, Axis.HEIGHT],
                                                      start_point = brute_start_point, 
                                                      strict_level = strict_level)
        return bin_location, real_method
                    