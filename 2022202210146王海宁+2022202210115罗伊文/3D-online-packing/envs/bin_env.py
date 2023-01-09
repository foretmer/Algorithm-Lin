import numpy as np
import random
from envs.binCreator import RandomBoxCreator, LoadBoxCreator, BoxCreator
from envs.space import Space


class PackingDiscrete():
    def __init__(self,
                 container_size=(10, 10, 10),
                 item_set=None, data_name=None, load_test_data=False,
                 internal_node_holder=200, leaf_node_holder=1000, next_holder=1,
                 shuffle=False,
                 **kwags):

        self.internal_node_holder = internal_node_holder
        self.leaf_node_holder = leaf_node_holder
        self.next_holder = next_holder

        self.shuffle = shuffle
        self.bin_size = container_size
        self.size_minimum = np.min(np.array(item_set))
        self.item_set = item_set
        self.orientation = 6

        # The class that maintains the contents of the bin.
        # 包括当前item的信息，ems列表，装好的items的列表
        self.space = Space(*self.bin_size, self.size_minimum, self.internal_node_holder)

        # Generator for train/test data
        if not load_test_data:
            assert item_set is not None
            self.box_creator = RandomBoxCreator(item_set)
            assert isinstance(self.box_creator, BoxCreator)
        if load_test_data:
            self.box_creator = LoadBoxCreator(data_name)

        self.test = load_test_data
        # 下一个待装item的信息
        self.next_box_vec = np.zeros((self.next_holder, 9))


    def seed(self, seed=None):
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
            self.SEED = seed
        return [seed]

    # Calculate space utilization inside a bin.
    def get_box_ratio(self):
        coming_box = self.next_box
        return (coming_box[0] * coming_box[1] * coming_box[2]) / (
                    self.space.plain_size[0] * self.space.plain_size[1] * self.space.plain_size[2])

    def reset(self):
        self.box_creator.reset()
        self.packed = []
        self.space.reset()
        self.box_creator.generate_box_size()
        cur_observation = self.cur_observation()
        return cur_observation

    # Count and return all PCT nodes.
    def cur_observation(self):
        boxes = []
        leaf_nodes = []
        # 获取下一个item
        self.next_box = self.gen_next_box()

        if self.test:
            self.next_den = 1
            self.next_box = [int(self.next_box[0]), int(self.next_box[1]), int(self.next_box[2])]
        else:
            # item的密度
            self.next_den = 1

        boxes.append(self.space.box_vec)
        leaf_nodes.append(self.get_possible_position())

        next_box = sorted(list(self.next_box))
        self.next_box_vec[:, 3:6] = next_box
        self.next_box_vec[:, 0] = self.next_den
        self.next_box_vec[:, -1] = 1
        # ((80+1000+1)*9,)
        return np.reshape(np.concatenate((*boxes, *leaf_nodes, self.next_box_vec)), (-1))

    # Generate the next item to be placed.
    def gen_next_box(self):
        return self.box_creator.preview(1)[0]

    # Detect potential leaf nodes and check their feasibility.
    def get_possible_position(self):
        allPostion = self.space.EMSPoint(self.next_box)

        if self.shuffle:
            np.random.shuffle(allPostion)

        leaf_node_idx = 0
        leaf_node_vec = np.zeros((self.leaf_node_holder, 9))
        tmp_list = []

        for position in allPostion:
            # 放置位置的DBL和OUR点
            xs, ys, zs, xe, ye, ze = position
            # 该rot下item的x,y,z大小
            x = xe - xs
            y = ye - ys
            z = ze - zs

            # 对放置位置做边缘检测
            if self.space.drop_box_virtual([x, y, z], (xs, ys), False, self.next_den):
                # 满足边缘检测，就将放置位置的DBL点以及OUR点（z设为bin的高度）保存进tmp_list
                tmp_list.append([xs, ys, zs, xe, ye, self.bin_size[2], 0, 0, 1])
                leaf_node_idx += 1

            if leaf_node_idx >= self.leaf_node_holder: break

        if len(tmp_list) != 0:
            # 讲所有tmp_list的点保存为叶子节点，并返回
            leaf_node_vec[0:len(tmp_list)] = np.array(tmp_list)

        return leaf_node_vec

    # Convert the selected leaf node to the placement of the current item.
    def LeafNode2Action(self, leaf_node):
        if np.sum(leaf_node[0:6]) == 0: return (0, 0, 0), self.next_box
        x = int(leaf_node[3] - leaf_node[0])
        y = int(leaf_node[4] - leaf_node[1])
        z = list(self.next_box)
        z.remove(x)
        z.remove(y)
        z = z[0]
        action = (0, int(leaf_node[0]), int(leaf_node[1]))
        next_box = (x, y, int(z))
        return action, next_box

    def step(self, action):
        if len(action) != 3:
            action, next_box = self.LeafNode2Action(action)
        else:
            # rot
            next_box = self.next_box

        # pos的lx,ly
        idx = [action[1], action[2]]
        bin_index = 0
        rotation_flag = action[0]
        succeeded = self.space.drop_box(next_box, idx, rotation_flag, self.next_den)

        if not succeeded:
            reward = 0.0
            done = True
            info = {'counter': len(self.space.boxes), 'ratio': self.space.get_ratio(),
                    'reward': self.space.get_ratio() * 10}
            return self.cur_observation(), reward, done, info

        ################################################
        ############# cal leaf nodes here ##############
        ################################################
        packed_box = self.space.boxes[-1]

        self.space.GENEMS([packed_box.lx, packed_box.ly, packed_box.lz,
                            packed_box.lx + packed_box.x, packed_box.ly + packed_box.y,
                            packed_box.lz + packed_box.z])

        self.packed.append(
            [packed_box.x, packed_box.y, packed_box.z, packed_box.lx, packed_box.ly, packed_box.lz, bin_index])

        box_ratio = self.get_box_ratio()
        self.box_creator.drop_box()  # remove current box from the list
        self.box_creator.generate_box_size()  # add a new box to the list
        reward = box_ratio * 10

        done = False
        info = dict()
        info['counter'] = len(self.space.boxes)
        return self.cur_observation(), reward, done, info