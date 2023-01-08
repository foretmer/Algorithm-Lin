from typing import List, Tuple

import numpy as np
from tqdm import tqdm

ROTATIONS = np.array([
    [0, 1, 2],  # LWH
    [0, 2, 1],  # LHW
    [1, 0, 2],  # WLH
    [1, 2, 0],  # WHL
    [2, 0, 1],  # HLW
    [2, 1, 0],  # HWL
])


class Item:
    def __init__(self, name, l, w, h) -> None:
        self.name = name
        self.position = np.zeros(3, np.int32)
        self.rotation = 0
        self.lwh = np.array([l, w, h])

    @property
    def volume(self) -> int:
        return np.prod(self.lwh)

    @property
    def dimension(self) -> np.ndarray:
        return self.lwh[ROTATIONS[self.rotation]]

    def rect_intersect(self, other: "Item", a1, a2) -> bool:
        """判断是否在某个面相交

        Args:
            other: 另一个物体
            a1: 坐标轴 1
            a2: 坐标轴 2
        """

        p1 = self.position[[a1, a2]]
        p2 = other.position[[a1, a2]]
        d1 = self.dimension[[a1, a2]]
        d2 = other.dimension[[a1, a2]]

        c1 = p1 + d1 / 2
        c2 = p2 + d1 / 2

        distance = np.abs(c1 - c2)

        return np.all(distance < ((d1 + d2) / 2))

    def intersect(self, other: "Item") -> bool:
        return (
            self.rect_intersect(other, 0, 1) and
            self.rect_intersect(other, 1, 2) and
            self.rect_intersect(other, 2, 0)
        )

    def __str__(self) -> str:
        return (
            f"{{Name: {self.name}, " +
            f"Position: {self.position.tolist()}, " +
            f"Rotation: {ROTATIONS[self.rotation].tolist()}, " +
            f"LWH: {self.lwh.tolist()}}}"
        )


class Bin:
    """"""

    def __init__(self, l, w, h) -> None:
        self.lwh = np.array([l, w, h])
        self.items: List[Item] = []

    @property
    def volume(self) -> int:
        return np.prod(self.lwh)

    @property
    def filling_ratio(self):
        return sum(e.volume for e in self.items) / self.volume

    def can_hold_item_with_rotation(self, item: Item):
        """判断物体在某个位置是否能通过某些旋转放下

        Item.position 需要设置要放置的位置

        Returns:
            List[int]
        """
        if item in self.items:
            raise ValueError("Item put!")

        valid_rotation = []
        for r in range(len(ROTATIONS)):
            item.rotation = r
            dimension = item.dimension

            # 超出箱子边界
            if np.any(item.position + dimension > self.lwh):
                continue

            # 与现有物体相交
            if any(item.intersect(e) for e in self.items):
                continue

            valid_rotation.append(r)

        return valid_rotation

    def get_pivots_and_distances(self, item: Item) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """获得所有可用的临近的放置点和周围空闲距离"""
        pivots = []
        distances = []

        for ib in self.items:
            ib_dimension = ib.dimension

            # LENGTH
            pivot = ib.position + ib_dimension * np.array([1, 0, 0])
            item.position = pivot
            if self.can_hold_item_with_rotation(item):
                ib_neigh_x_axis = []
                ib_neigh_y_axis = []
                ib_neigh_z_axis = []

                # 添加箱子的间隔
                x_distance = self.lwh[0] - (ib.position[0] + ib_dimension[0])
                ib_neigh_x_axis.append(x_distance)

                y_distance = self.lwh[1] - ib.position[1]
                ib_neigh_y_axis.append(y_distance)

                z_distance = self.lwh[2] - ib.position[2]
                ib_neigh_z_axis.append(z_distance)

                # 添加所有邻居物体的间隔
                for ib_neighbor in self.items:
                    if ib_neighbor == ib:
                        continue

                    ib_n_dimension = ib_neighbor.dimension
                    if (
                            ib_neighbor.position[0] > ib.position[0] + ib_dimension[0] and
                            ib_neighbor.position[1] + ib_n_dimension[1] > ib.position[1] and
                            ib_neighbor.position[2] + ib_n_dimension[2] > ib.position[2]
                    ):
                        x_distance = ib_neighbor.position[0] - (ib.position[0] + ib_dimension[0])
                        ib_neigh_x_axis.append(x_distance)
                    elif (
                            ib_neighbor.position[1] >= ib.position[1] + ib_dimension[1] and
                            ib_neighbor.position[0] + ib_n_dimension[0] > ib.position[0] + ib_dimension[0] and
                            ib_neighbor.position[2] + ib_n_dimension[2] > ib.position[2]
                    ):
                        y_distance = ib_neighbor.position[1] - ib.position[1]
                        ib_neigh_y_axis.append(y_distance)
                    elif (
                            ib_neighbor.position[2] >= ib.position[2] + ib_dimension[2] and
                            ib_neighbor.position[0] + ib_n_dimension[0] > ib.position[0] + ib_dimension[0] and
                            ib_neighbor.position[1] + ib_n_dimension[1] > ib.position[1]
                    ):
                        z_distance = ib_neighbor.position[2] - ib.position[2]
                        ib_neigh_z_axis.append(z_distance)

                pivots.append(pivot)
                distances.append(np.array([min(ib_neigh_x_axis), min(ib_neigh_y_axis), min(ib_neigh_z_axis)]))

            # WIDTH
            pivot = ib.position + ib_dimension * np.array([0, 1, 0])
            item.position = pivot
            if self.can_hold_item_with_rotation(item):
                ib_neigh_x_axis = []
                ib_neigh_y_axis = []
                ib_neigh_z_axis = []

                x_distance = self.lwh[0] - ib.position[0]
                ib_neigh_x_axis.append(x_distance)

                y_distance = self.lwh[1] - (ib.position[1] + ib_dimension[1])
                ib_neigh_y_axis.append(y_distance)

                z_distance = self.lwh[2] - ib.position[2]
                ib_neigh_z_axis.append(z_distance)

                for ib_neighbor in self.items:
                    if ib_neighbor == ib:
                        continue

                    ib_n_dimension = ib_neighbor.dimension
                    if (
                            ib_neighbor.position[0] >= ib.position[0] + ib_dimension[0] and
                            ib_neighbor.position[1] + ib_n_dimension[1] > ib.position[1] + ib_dimension[1] and
                            ib_neighbor.position[2] + ib_n_dimension[2] > ib.position[2]
                    ):
                        x_distance = ib_neighbor.position[0] - ib.position[0]
                        ib_neigh_x_axis.append(x_distance)

                    elif (
                            ib_neighbor.position[1] > ib.position[1] + ib_dimension[1] and
                            ib_neighbor.position[0] + ib_n_dimension[0] > ib.position[0] and
                            ib_neighbor.position[2] + ib_n_dimension[2] > ib.position[2]
                    ):
                        y_distance = ib_neighbor.position[1] - (ib.position[1] + ib_dimension[1])
                        ib_neigh_y_axis.append(y_distance)

                    elif (
                            ib_neighbor.position[2] >= ib.position[2] + ib_dimension[2] and
                            ib_neighbor.position[0] + ib_n_dimension[0] > ib.position[0] and
                            ib_neighbor.position[1] + ib_n_dimension[1] > ib.position[1] + ib_dimension[1]
                    ):
                        z_distance = ib_neighbor.position[2] - ib.position[2]
                        ib_neigh_z_axis.append(z_distance)

                pivots.append(pivot)
                distances.append(np.array([min(ib_neigh_x_axis), min(ib_neigh_y_axis), min(ib_neigh_z_axis)]))

            # HEIGHT
            pivot = ib.position + ib_dimension * np.array([0, 0, 1])
            item.position = pivot
            if self.can_hold_item_with_rotation(item):
                ib_neigh_x_axis = []
                ib_neigh_y_axis = []
                ib_neigh_z_axis = []

                x_distance = self.lwh[0] - ib.position[0]
                ib_neigh_x_axis.append(x_distance)

                y_distance = self.lwh[1] - ib.position[1]
                ib_neigh_y_axis.append(y_distance)

                z_distance = self.lwh[2] - (ib.position[2] + ib_dimension[2])
                ib_neigh_z_axis.append(z_distance)

                for ib_neighbor in self.items:
                    if ib_neighbor == ib:
                        continue

                    ib_n_dimension = ib_neighbor.dimension
                    if (
                            ib_neighbor.position[0] >= ib.position[0] + ib_dimension[0] and
                            ib_neighbor.position[1] + ib_n_dimension[1] > ib.position[1] and
                            ib_neighbor.position[2] + ib_n_dimension[2] > ib.position[2] + ib_dimension[2]
                    ):
                        x_distance = ib_neighbor.position[0] - ib.position[0]
                        ib_neigh_x_axis.append(x_distance)

                    elif (
                            ib_neighbor.position[1] > ib.position[1] + ib_dimension[1] and
                            ib_neighbor.position[0] + ib_n_dimension[0] > ib.position[0] and
                            ib_neighbor.position[2] + ib_n_dimension[2] > ib.position[2] + ib_dimension[2]
                    ):
                        y_distance = ib_neighbor.position[1] - (ib.position[1] + ib_dimension[1])
                        ib_neigh_y_axis.append(y_distance)

                    elif (
                            ib_neighbor.position[2] >= ib.position[2] + ib_dimension[2] and
                            ib_neighbor.position[1] + ib_n_dimension[1] > ib.position[1] and
                            ib_neighbor.position[0] + ib_n_dimension[0] > ib.position[0]
                    ):
                        z_distance = ib_neighbor.position[2] - ib.position[2]
                        ib_neigh_z_axis.append(z_distance)

                pivots.append(pivot)
                distances.append(np.array([min(ib_neigh_x_axis), min(ib_neigh_y_axis), min(ib_neigh_z_axis)]))

        return (pivots, distances)

    def choose_best_pivot_and_distance(self, item: Item) -> Tuple[np.ndarray, np.ndarray]:
        """选出最好的放置点和边距"""

        if not self.items:
            return (np.array([0, 0, 0]), self.lwh)

        pivots, distances = self.get_pivots_and_distances(item)

        if not pivots:
            return (None, None)

        available_pivots = np.array(pivots)
        available_pivots_tmp = np.sort(available_pivots, axis=1)
        distances = np.array(distances)

        vertex_3d = np.min(available_pivots_tmp[:, 0])
        mask = (available_pivots_tmp[:, 0] == vertex_3d)
        available_pivots_tmp = available_pivots_tmp[mask]
        available_pivots = available_pivots[mask]
        distances = distances[mask]

        vertex_2d = np.min(available_pivots_tmp[:, 1])
        mask = (available_pivots_tmp[:, 1] == vertex_2d)
        available_pivots_tmp = available_pivots_tmp[mask]
        available_pivots = available_pivots[mask]
        distances = distances[mask]

        vertex_1d = np.min(available_pivots_tmp[:, 2])
        mask = (available_pivots_tmp[:, 2] == vertex_1d)
        available_pivots_tmp = available_pivots_tmp[mask]
        available_pivots = available_pivots[mask]
        distances = distances[mask]

        return (available_pivots[0], distances[0])

    def choose_best_rotation(self, item: Item, pivot: np.ndarray, distance: np.ndarray) -> int:
        """"""
        item.position = pivot
        rotation_type_list = self.can_hold_item_with_rotation(item)

        margins = []
        for r in rotation_type_list:
            item.rotation = r
            margins.append(distance - item.dimension)

        margins = np.array(margins)
        margins_tmp = np.sort(margins, axis=1)
        rotations = np.array(rotation_type_list)

        margin_3d = np.min(margins_tmp[:, 0])
        mask = (margins_tmp[:, 0] == margin_3d)
        margins_tmp = margins_tmp[mask]
        margins = margins[mask]
        rotations = rotations[mask]

        margin_2d = np.min(margins_tmp[:, 1])
        mask = (margins_tmp[:, 1] == margin_2d)
        margins_tmp = margins_tmp[mask]
        margins = margins[mask]
        rotations = rotations[mask]

        margin_1d = np.min(margins_tmp[:, 2])
        mask = (margins_tmp[:, 2] == margin_1d)
        margins_tmp = margins_tmp[mask]
        margins = margins[mask]
        rotations = rotations[mask]

        return rotations[0]

    def put_item(self, item: Item):
        """"""
        pivot, distance = self.choose_best_pivot_and_distance(item)
        if pivot is None:
            item.position = np.array([-1, -1, -1])
            return False

        rotation = self.choose_best_rotation(item, pivot, distance)
        item.position = np.copy(pivot)
        item.rotation = rotation

        self.items.append(item)
        return True


class Packer:
    def __init__(self, name) -> None:
        self.name = name
        self.unplaced_items = []
        self.unfitted_items = []
        self.bin = Bin(0, 0, 0)

    def set_bin(self, l, w, h):
        self.bin = Bin(l, w, h)

    def add_item(self, item):
        self.unplaced_items.append(item)

    def pack(self):
        self.unplaced_items.sort(key=lambda x: x.volume, reverse=True)

        for item in tqdm(self.unplaced_items, self.name):
            if not self.bin.put_item(item):
                self.unfitted_items.append(item)

        print("================== Placed Items ==================")
        for item in self.bin.items:
            print(item)
        print(f"Count: {len(self.bin.items)}")

        print("================= Unfitted Items =================")
        for item in self.unfitted_items:
            print(item)
        print(f"Count: {len(self.unfitted_items)}")

        print("==================================================")
        print(f"Total filling ratio: {self.bin.filling_ratio:.4f}")


data1 = [
    [(108, 76, 30, 40), (110, 43, 25, 33), (92, 81, 55, 39)],
    [(91, 54, 45, 32), (105, 77, 72, 24), (79, 78, 48, 30)],
    [(91, 54, 45, 32), (105, 77, 72, 24), (79, 78, 48, 30)],
    [(60, 40, 32, 64), (98, 75, 55, 40), (60, 59, 39, 64)],
    [(78, 37, 27, 63), (89, 70, 25, 52), (90, 84, 41, 55)],
]
data2 = [
    [(108, 76, 30, 24), (110, 43, 25, 7), (92, 81, 55, 22), (81, 33, 28, 13), (120, 99, 73, 15)],
    [(49, 25, 21, 22), (60, 51, 41, 22), (103, 76, 64, 28), (95, 70, 62, 25), (111, 49, 26, 17)],
    [(88, 54, 39, 25), (94, 54, 36, 27), (87, 77, 43, 21), (100, 80, 72, 20), (83, 40, 36, 24)],
    [(90, 70, 63, 16), (84, 78, 28, 28), (94, 85, 39, 20), (80, 76, 54, 23), (69, 50, 45, 31)],
    [(74, 63, 61, 22), (71, 60, 25, 12), (106, 80, 59, 25), (109, 76, 42, 24), (118, 56, 22, 11)],
]
data3 = [
    [(108, 76, 30, 24), (110, 43, 25, 9), (92, 81, 55, 8), (81, 33, 28, 11),
     (120, 99, 73, 11), (111, 70, 48, 10), (98, 72, 46, 12), (95, 66, 31, 9)],
    [(97, 81, 27, 10), (102, 78, 39, 20), (113, 46, 36, 18), (66, 50, 42, 21),
     (101, 30, 26, 16), (100, 56, 35, 17), (91, 50, 40, 22), (106, 61, 56, 19)],
    [(88, 54, 39, 16), (94, 54, 36, 14), (87, 77, 43, 20), (100, 80, 72, 16),
     (83, 40, 36, 6), (91, 54, 22, 15), (109, 58, 54, 17), (94, 55, 30, 9)],
    [(49, 25, 21, 16), (60, 51, 41, 8), (103, 76, 64, 16), (95, 70, 62, 18),
     (111, 49, 26, 18), (85, 84, 72, 16), (48, 36, 31, 17), (86, 76, 38, 6)],
    [(113, 92, 33, 23), (52, 37, 28, 22), (57, 33, 29, 26), (99, 37, 30, 17),
     (92, 64, 33, 23), (119, 59, 39, 26), (54, 52, 49, 18), (75, 45, 35, 30)],
]
data4 = [
    [(49, 25, 21, 13), (60, 51, 41, 9), (103, 76, 64, 11), (95, 70, 62, 14), (111, 49, 26, 13),
     (85, 84, 72, 16), (48, 36, 31, 12), (86, 76, 38, 11), (71, 48, 47, 16), (90, 43, 33, 8)],
    [(97, 81, 27, 8), (102, 78, 39, 16), (113, 46, 36, 12), (66, 50, 42, 12), (101, 30, 26, 18),
     (100, 56, 35, 13), (91, 50, 40, 14), (106, 61, 56, 17), (103, 63, 58, 12), (75, 57, 41, 13)],
    [(86, 84, 45, 18), (81, 45, 34, 19), (70, 54, 37, 13), (71, 61, 52, 16), (78, 73, 40, 10),
     (69, 63, 46, 13), (72, 67, 56, 10), (75, 75, 36, 8), (94, 88, 50, 12), (65, 51, 50, 13)],
    [(113, 92, 33, 15), (52, 37, 28, 17), (57, 33, 29, 17), (99, 37, 30, 19), (92, 64, 33, 13),
     (119, 59, 39, 19), (54, 52, 49, 13), (75, 45, 35, 21), (79, 68, 44, 13), (116, 49, 47, 22)],
    [(118, 79, 51, 16), (86, 32, 31, 8), (64, 58, 52, 14), (42, 42, 32, 14), (64, 55, 43, 16),
     (84, 70, 35, 10), (76, 57, 36, 14), (95, 60, 55, 14), (80, 66, 52, 14), (109, 73, 23, 18)],
]
data5 = [
    [(98, 73, 44, 6), (60, 60, 38, 7), (105, 73, 60, 10), (90, 77, 52, 3), (66, 58, 24, 5),
     (106, 76, 55, 10), (55, 44, 36, 12), (82, 58, 23, 7), (74, 61, 58, 6), (81, 39, 24, 8),
     (71, 65, 39, 11), (105, 97, 47, 4), (114, 97, 69, 5), (103, 78, 55, 6), (93, 66, 55, 6)],
    [(108, 76, 30, 12), (110, 43, 25, 12), (92, 81, 55, 6), (81, 33, 28, 9), (120, 99, 73, 5),
     (111, 70, 48, 12), (98, 72, 46, 9), (95, 66, 31, 10), (85, 84, 30, 8), (71, 32, 25, 3),
     (36, 34, 25, 10), (97, 67, 62, 7), (33, 25, 23, 7), (95, 27, 26, 10), (94, 81, 44, 9)],
    [(49, 25, 21, 13), (60, 51, 41, 9), (103, 76, 64, 8), (95, 70, 62, 6), (111, 49, 26, 10),
     (74, 42, 40, 4), (85, 84, 72, 10), (48, 36, 31, 10), (86, 76, 38, 12), (71, 48, 47, 14),
     (90, 43, 33, 9), (98, 52, 44, 9), (73, 37, 23, 10), (61, 48, 39, 14), (75, 75, 63, 11)],
    [(97, 81, 27, 6), (102, 78, 39, 6), (113, 46, 36, 15), (66, 50, 42, 8), (101, 30, 26, 6),
     (100, 56, 35, 7), (91, 50, 40, 12), (106, 61, 56, 10), (103, 63, 58, 8), (75, 57, 41, 11),
     (71, 68, 64, 6), (85, 67, 39, 14), (97, 63, 56, 9), (61, 48, 30, 11), (80, 54, 35, 9)],
    [(113, 92, 33, 8), (52, 37, 28, 12), (57, 33, 29, 5), (99, 37, 30, 12), (92, 64, 33, 9),
     (119, 59, 39, 12), (54, 52, 49, 8), (75, 45, 35, 6), (79, 68, 44, 12), (116, 49, 47, 9),
     (83, 44, 23, 11), (98, 96, 56, 10), (78, 72, 57, 8), (98, 88, 47, 9), (41, 33, 31, 13)]
]

dataset = [data1, data2, data3, data4, data5]

if __name__ == "__main__":
    for i, data in enumerate(dataset):
        for j, items in enumerate(data):
            test_name = f"E{i+1}-{j+1}"

            packer = Packer(test_name)
            packer.set_bin(587, 233, 220)

            print("="*25 + " " + test_name + " " + "="*25)
            for l, w, h, c in items:
                for num in range(c):
                    packer.add_item(Item(f"{l}x{w}x{h}-{num}", l, w, h))

            packer.pack()
            print()
