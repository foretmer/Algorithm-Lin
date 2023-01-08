from constants import *
from auxiliary_methods import *
from box import *
from truck import *
import time


class Packer:
    def __init__(self):
        self.trucks = []
        self.unplaced_boxes = []
        self.placed_boxes = []
        self.unfit_boxes = []
        self.total_boxes = 0
        self.total_used_trucks = 0  # not used yet
        self.used_trucks = []  # not used yet

    def add_truck(self, truck):
        return self.trucks.append(truck)

    # def add_box(self, box):
    #     """Add unplaced items into bin's unplaced_items list.
    #     Args:
    #         box: an unplaced item.
    #     Returns:
    #         The unplaced item is added into bin's unplaced_items list."""

    #     # self.total_boxes += 1
    #     # return self.unplaced_boxes.append(box)
    #     self.total_boxes += box.count
    #     for i in range(box.count):
    #         self.unplaced_boxes.append(box)
    def add_box(self, name, length, width, height, count):
        """Add unplaced items into bin's unplaced_items list.
        Args:
            box: an unplaced item.
        Returns:
            The unplaced item is added into bin's unplaced_items list."""

        self.total_boxes += count
        for i in range(count):
            self.unplaced_boxes.append(Box(name, length, width, height))

    def pivot_dict(self, truck, box):
        """For each item to be placed into a certain bin, obtain a corresponding comparison parameter of each optional pivot that the item can be placed.
        Args:
            truck: a bin in bin list that a certain item will be placed into.
            box: an unplaced item in item list.
        Returns:
            a pivot_dict contain all optional pivot point and their comparison parameter of the item.
            a empty dict may be returned if the item couldn't be placed into the bin.
        """

        pivot_dict = {}
        can_put = False

        for axis in range(0, 3):
            boxes_in_truck = truck.boxes
            boxes_in_truck_temp = boxes_in_truck[:]

            n = 0
            while n < len(boxes_in_truck):
                pivot = [0, 0, 0]

                if axis == Axis.LENGTH:  # axis = 0/ x-axis
                    ib = boxes_in_truck[n]
                    pivot = [ib.position[0] + ib.get_dimension()[0],
                             ib.position[1],
                             ib.position[2]]
                    try_put_box = truck.can_hold_box_with_rotation(box, pivot, self.rl)

                    if try_put_box:
                        can_put = True
                        # q = 0
                        q = 0
                        ib_neigh_x_axis = []
                        ib_neigh_y_axis = []
                        ib_neigh_z_axis = []
                        right_neighbor = False
                        front_neighbor = False
                        above_neighbor = False

                        while q < len(boxes_in_truck_temp):
                            if boxes_in_truck_temp[q] == boxes_in_truck[n]:
                                q += 1

                            else:
                                ib_neighbor = boxes_in_truck_temp[q]

                                if (
                                        ib_neighbor.position[0] > ib.position[0] + ib.get_dimension()[0] and
                                        ib_neighbor.position[1] + ib_neighbor.get_dimension()[1] > ib.position[1] and
                                        ib_neighbor.position[2] + ib_neighbor.get_dimension()[2] > ib.position[2]
                                ):
                                    right_neighbor = True
                                    x_distance = ib_neighbor.position[0] - (ib.position[0] + ib.get_dimension()[0])
                                    ib_neigh_x_axis.append(x_distance)

                                elif (
                                        ib_neighbor.position[1] >= ib.position[1] + ib.get_dimension()[1] and
                                        ib_neighbor.position[0] + ib_neighbor.get_dimension()[0] > ib.position[0] +
                                        ib.get_dimension()[0] and
                                        ib_neighbor.position[2] + ib_neighbor.get_dimension()[2] > ib.position[2]
                                ):
                                    front_neighbor = True
                                    y_distance = ib_neighbor.position[1] - ib.position[1]
                                    ib_neigh_y_axis.append(y_distance)

                                elif (
                                        ib_neighbor.position[2] >= ib.position[2] + ib.get_dimension()[2] and
                                        ib_neighbor.position[0] + ib_neighbor.get_dimension()[0] > ib.position[0] +
                                        ib.get_dimension()[0] and
                                        ib_neighbor.position[1] + ib_neighbor.get_dimension()[1] > ib.position[1]
                                ):
                                    above_neighbor = True
                                    z_distance = ib_neighbor.position[2] - ib.position[2]
                                    ib_neigh_z_axis.append(z_distance)

                                q += 1

                        if not right_neighbor:
                            x_distance = truck.length - (ib.position[0] + ib.get_dimension()[0])
                            ib_neigh_x_axis.append(x_distance)

                        if not front_neighbor:
                            y_distance = truck.width - ib.position[1]
                            ib_neigh_y_axis.append(y_distance)

                        if not above_neighbor:
                            z_distance = truck.height - ib.position[2]
                            ib_neigh_z_axis.append(z_distance)

                        distance_3D = [min(ib_neigh_x_axis), min(ib_neigh_y_axis), min(ib_neigh_z_axis)]
                        pivot_dict[tuple(pivot)] = distance_3D

                elif axis == Axis.WIDTH:  # axis = 1/ y-axis
                    ib = boxes_in_truck[n]
                    pivot = [ib.position[0],
                             ib.position[1] + ib.get_dimension()[1],
                             ib.position[2]]
                    try_put_box = truck.can_hold_box_with_rotation(box, pivot, self.rl)

                    if try_put_box:
                        can_put = True
                        q = 0
                        ib_neigh_x_axis = []
                        ib_neigh_y_axis = []
                        ib_neigh_z_axis = []
                        right_neighbor = False
                        front_neighbor = False
                        above_neighbor = False

                        while q < len(boxes_in_truck_temp):
                            if boxes_in_truck_temp[q] == boxes_in_truck[n]:
                                q += 1

                            else:
                                ib_neighbor = boxes_in_truck_temp[q]

                                if (
                                        ib_neighbor.position[0] >= ib.position[0] + ib.get_dimension()[0] and
                                        ib_neighbor.position[1] + ib_neighbor.get_dimension()[1] > ib.position[1] +
                                        ib.get_dimension()[1] and
                                        ib_neighbor.position[2] + ib_neighbor.get_dimension()[2] > ib.position[2]
                                ):
                                    right_neighbor = True
                                    x_distance = ib_neighbor.position[0] - ib.position[0]
                                    ib_neigh_x_axis.append(x_distance)

                                elif (
                                        ib_neighbor.position[1] > ib.position[1] + ib.get_dimension()[1] and
                                        ib_neighbor.position[0] + ib_neighbor.get_dimension()[0] > ib.position[0] and
                                        ib_neighbor.position[2] + ib_neighbor.get_dimension()[2] > ib.position[2]
                                ):
                                    front_neighbor = True
                                    y_distance = ib_neighbor.position[1] - (ib.position[1] + ib.get_dimension()[1])
                                    ib_neigh_y_axis.append(y_distance)

                                elif (
                                        ib_neighbor.position[2] >= ib.position[2] + ib.get_dimension()[2] and
                                        ib_neighbor.position[0] + ib_neighbor.get_dimension()[0] > ib.position[0] and
                                        ib_neighbor.position[1] + ib_neighbor.get_dimension()[1] > ib.position[1] +
                                        ib.get_dimension()[1]
                                ):
                                    above_neighbor = True
                                    z_distance = ib_neighbor.position[2] - ib.position[2]
                                    ib_neigh_z_axis.append(z_distance)

                                q += 1

                        if not right_neighbor:
                            x_distance = truck.length - ib.position[0]
                            ib_neigh_x_axis.append(x_distance)

                        if not front_neighbor:
                            y_distance = truck.width - (ib.position[1] + ib.get_dimension()[1])
                            ib_neigh_y_axis.append(y_distance)

                        if not above_neighbor:
                            z_distance = truck.height - ib.position[2]
                            ib_neigh_z_axis.append(z_distance)

                        distance_3D = [min(ib_neigh_x_axis), min(ib_neigh_y_axis), min(ib_neigh_z_axis)]
                        pivot_dict[tuple(pivot)] = distance_3D

                elif axis == Axis.HEIGHT:  # axis = 2/ z-axis
                    ib = boxes_in_truck[n]
                    pivot = [ib.position[0],
                             ib.position[1],
                             ib.position[2] + ib.get_dimension()[2]]
                    try_put_box = truck.can_hold_box_with_rotation(box, pivot, self.rl)

                    if try_put_box:
                        can_put = True
                        q = 0
                        ib_neigh_x_axis = []
                        ib_neigh_y_axis = []
                        ib_neigh_z_axis = []
                        right_neighbor = False
                        front_neighbor = False
                        above_neighbor = False

                        while q < len(boxes_in_truck_temp):
                            if boxes_in_truck_temp[q] == boxes_in_truck[n]:
                                q += 1

                            else:
                                ib_neighbor = boxes_in_truck_temp[q]

                                if (
                                        ib_neighbor.position[0] >= ib.position[0] + ib.get_dimension()[0] and
                                        ib_neighbor.position[1] + ib_neighbor.get_dimension()[1] > ib.position[1] and
                                        ib_neighbor.position[2] + ib_neighbor.get_dimension()[2] > ib.position[2] +
                                        ib.get_dimension()[2]
                                ):
                                    right_neighbor = True
                                    x_distance = ib_neighbor.position[0] - ib.position[0]
                                    ib_neigh_x_axis.append(x_distance)

                                elif (
                                        ib_neighbor.position[1] > ib.position[1] + ib.get_dimension()[1] and
                                        ib_neighbor.position[0] + ib_neighbor.get_dimension()[0] > ib.position[0] and
                                        ib_neighbor.position[2] + ib_neighbor.get_dimension()[2] > ib.position[2] +
                                        ib.get_dimension()[2]
                                ):
                                    front_neighbor = True
                                    y_distance = ib_neighbor.position[1] - (ib.position[1] + ib.get_dimension()[1])
                                    ib_neigh_y_axis.append(y_distance)

                                elif (
                                        ib_neighbor.position[2] >= ib.position[2] + ib.get_dimension()[2] and
                                        ib_neighbor.position[1] + ib_neighbor.get_dimension()[1] > ib.position[1] and
                                        ib_neighbor.position[0] + ib_neighbor.get_dimension()[0] > ib.position[0]
                                ):
                                    above_neighbor = True
                                    z_distance = ib_neighbor.position[2] - ib.position[2]
                                    ib_neigh_z_axis.append(z_distance)

                                q += 1

                        if not right_neighbor:
                            x_distance = truck.length - ib.position[0]
                            ib_neigh_x_axis.append(x_distance)

                        if not front_neighbor:
                            y_distance = truck.width - ib.position[1]
                            ib_neigh_y_axis.append(y_distance)

                        if not above_neighbor:
                            z_distance = truck.height - (ib.position[2] + ib.get_dimension()[2])
                            ib_neigh_z_axis.append(z_distance)

                        distance_3D = [min(ib_neigh_x_axis), min(ib_neigh_y_axis), min(ib_neigh_z_axis)]
                        pivot_dict[tuple(pivot)] = distance_3D

                n += 1

        return pivot_dict

    def pivot_list(self, truck, box):
        """Obtain all optional pivot points that one item could be placed into a certain bin.
        Args:
            truck: a bin in bin list that a certain item will be placed into.
            box: an unplaced item in item list.
        Returns:
            a pivot_list containing all optional pivot points that the item could be placed into a certain bin.
        """

        pivot_list = []

        for axis in range(0, 3):
            boxes_in_truck = truck.boxes

            for ib in boxes_in_truck:
                pivot = [0, 0, 0]
                if axis == Axis.LENGTH:  # axis = 0/ x-axis
                    pivot = [ib.position[0] + ib.get_dimension()[0],
                             ib.position[1],
                             ib.position[2]]
                elif axis == Axis.WIDTH:  # axis = 1/ y-axis
                    pivot = [ib.position[0],
                             ib.position[1] + ib.get_dimension()[1],
                             ib.position[2]]
                elif axis == Axis.HEIGHT:  # axis = 2/ z-axis
                    pivot = [ib.position[0],
                             ib.position[1],
                             ib.position[2] + ib.get_dimension()[2]]

                pivot_list.append(pivot)

        return pivot_list

    def choose_pivot_point(self, truck, box):
        """Choose the optimal one from all optional pivot points of the item after comparison.
        Args:
            truck: a truck in truck list that a certain box will be placed into.
            box: an unplaced item in item list.
        Returns:
            the optimal pivot point that a box could be placed into a truck.
        """

        can_put = False
        pivot_available = []
        pivot_available_temp = []
        vertex_3d = []
        vertex_2d = []
        vertex_1d = []

        n = 0
        m = 0
        p = 0

        pivot_list = self.pivot_list(truck, box)

        for pivot in pivot_list:
            try_put_box = truck.can_hold_box_with_rotation(box, pivot, self.rl)

            if try_put_box:
                can_put = True
                pivot_available.append(pivot)
                pivot_temp = sorted(pivot)
                pivot_available_temp.append(pivot_temp)

        if pivot_available:
            while p < len(pivot_available_temp):
                vertex_3d.append(pivot_available_temp[p][0])
                p += 1

            p = 0
            while p < len(pivot_available_temp):
                if pivot_available_temp[p][0] == min(vertex_3d):
                    n += 1
                    vertex_2d.append(pivot_available_temp[p][1])

                p += 1

            if n == 1:
                p = 0
                while p < len(pivot_available_temp):
                    if pivot_available_temp[p][0] == min(pivot_available_temp[p]):
                        return pivot_available[p]

                    p += 1

            else:
                p = 0
                while p < len(pivot_available_temp):
                    if (
                            pivot_available_temp[p][0] == min(pivot_available_temp[p]) and
                            pivot_available_temp[p][1] == min(vertex_2d)
                    ):
                        m += 1
                        vertex_1d.append(pivot_available_temp[p][2])

                    p += 1

            if m == 1:
                p = 0
                while p < len(pivot_available_temp):
                    if (
                            pivot_available_temp[p][0] == min(pivot_available_temp[p]) and
                            pivot_available_temp[p][1] == min(vertex_2d)
                    ):
                        return pivot_available[p]

                    p += 1

            else:
                p = 0
                while p < len(pivot_available_temp):
                    if (
                            pivot_available_temp[p][0] == min(pivot_available_temp[p]) and
                            pivot_available_temp[p][1] == min(vertex_2d) and
                            pivot_available_temp[p][2] == min(vertex_1d)
                    ):
                        return pivot_available[p]

                    p += 1

        if not pivot_available:
            return can_put

    def pack_to_truck(self, truck, box):
        """For each item and each bin, perform whole pack process with optimal orientation and pivot point.
        Args:
            truck: a bin in bin list that a certain item will be placed into.
            box: an unplaced item in item list.
        Returns: return value is void.
        """

        if not truck.boxes:
            response = truck.put_box(box, START_POSITION, [truck.length, truck.width, truck.height], self.rl)

            if not response:
                truck.unfitted_boxes.append(box)

            return response, box

        else:
            pivot_point = self.choose_pivot_point(truck, box)
            pivot_dict = self.pivot_dict(truck, box)

            if not pivot_point:
                truck.unfitted_boxes.append(box)
                response = False
                return response, box

            distance_3D = pivot_dict[tuple(pivot_point)]
            response = truck.put_box(box, pivot_point, distance_3D, self.rl)
            return response, box

    def pack(
            self, bigger_first=True, number_of_decimals=DEFAULT_NUMBER_OF_DECIMALS,  mode='static'):
        """For a list of items and a list of bins, perform the whole pack process.
        Args:
            bin: a bin in bin list that a certain item will be placed into.
            item: an unplaced item in item list.
            rotation_list: rotation type list.
        Returns:
            For each bin, print detailed information about placed and unplaced items.
            Then, print the optimal bin with highest packing rate.
        """
        if mode == 'static':
            self.rl = [0, 4]
        else:
            self.rl = [0, 1, 2, 3, 4, 5]

        for truck in self.trucks:
            truck.format_numbers(number_of_decimals)

        for unplaced_box in self.unplaced_boxes:
            unplaced_box.format_numbers(number_of_decimals)

        if mode == 'static':
            self.trucks.sort(
                key=lambda truck: truck.get_volume())  # default order of trucks: from smallest to biggest
            self.unplaced_boxes.sort(
                key=lambda unplaced_box: unplaced_box.get_volume(),
                reverse=bigger_first)  # default order of items: from biggest to smallest

        filling_ratio_list = []

        for truck in self.trucks:
            for unplaced_box in self.unplaced_boxes:
                truck.unplaced_boxes.append(unplaced_box)

        for truck in self.trucks:
            for unplaced_box in self.unplaced_boxes:
                start = time.time()
                responce, box = self.pack_to_truck(truck, unplaced_box)
                end = time.time()
                if mode == 'online':
                    if responce:
                        print("\nFITTED ITEMS:", box.string(), str(end-start))
                    else:
                        print("\nUNFITTED ITEMS:", box.string())


            if mode == 'static':
                print("\n:::::::::::", truck.string())
                print("FITTED ITEMS:")
                for box in truck.boxes:
                    print("====> ", box.string())

                print("\nUNFITTED ITEMS:")
                for box in truck.unfitted_boxes:
                    print("====> ", box.string())

            filling_ratio_list.append(truck.get_filling_ratio())

        max_filling_ratio = max(filling_ratio_list)

        for truck in self.trucks:
            if truck.get_filling_ratio() == max_filling_ratio:
                for box in truck.boxes:
                    self.placed_boxes.append(box)
                print("\nSelected bin with highest filling ratio: ", truck.string())