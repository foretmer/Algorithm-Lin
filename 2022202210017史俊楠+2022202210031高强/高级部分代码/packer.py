from constant import Axis
from Auxiliary_Method import DEFAULT_NUMBER_OF_DECIMALS, START_POSITION


class Packer:
    def __init__(self):
        self.bins = []
        self.unplaced_items = []
        self.placed_items = []
        self.unfit_items = []
        self.total_items = 0
        self.total_used_bins = 0  # not used yet
        self.used_bins = []  # not used yet

    def add_bin(self, bin):
        return self.bins.append(bin)

    def add_item(self, item):
        """Add unplaced items into bin's unplaced_items list.
        Args:
            item: an unplaced item.
        Returns:
            The unplaced item is added into bin's unplaced_items list."""

        self.total_items += 1
        return self.unplaced_items.append(item)

    def pivot_dict(self, bin, item):
        """For each item to be placed into a certain bin, obtain a corresponding comparison parameter of each optional pivot that the item can be placed.
        Args:
            bin: a bin in bin list that a certain item will be placed into.
            item: an unplaced item in item list.
        Returns:
            a pivot_dict contain all optional pivot point and their comparison parameter of the item.
            a empty dict may be returned if the item couldn't be placed into the bin.
        """

        pivot_dict = {}
        can_put = False

        for axis in range(0, 3):
            items_in_bin = bin.items
            items_in_bin_temp = items_in_bin[:]

            n = 0
            while n < len(items_in_bin):
                pivot = [0, 0, 0]

                if axis == Axis.LENGTH:  # axis = 0/ x-axis
                    ib = items_in_bin[n]
                    pivot = [ib.position[0] + ib.get_dimension()[0],
                             ib.position[1],
                             ib.position[2]]
                    try_put_item = bin.can_hold_item_with_rotation(item, pivot)

                    if try_put_item:
                        can_put = True
                        q = 0
                        q = 0
                        ib_neigh_x_axis = []
                        ib_neigh_y_axis = []
                        ib_neigh_z_axis = []
                        right_neighbor = False
                        front_neighbor = False
                        above_neighbor = False

                        while q < len(items_in_bin_temp):
                            if items_in_bin_temp[q] == items_in_bin[n]:
                                q += 1

                            else:
                                ib_neighbor = items_in_bin_temp[q]

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
                            x_distance = bin.length - (ib.position[0] + ib.get_dimension()[0])
                            ib_neigh_x_axis.append(x_distance)

                        if not front_neighbor:
                            y_distance = bin.width - ib.position[1]
                            ib_neigh_y_axis.append(y_distance)

                        if not above_neighbor:
                            z_distance = bin.height - ib.position[2]
                            ib_neigh_z_axis.append(z_distance)

                        distance_3D = [min(ib_neigh_x_axis), min(ib_neigh_y_axis), min(ib_neigh_z_axis)]
                        pivot_dict[tuple(pivot)] = distance_3D

                elif axis == Axis.WIDTH:  # axis = 1/ y-axis
                    ib = items_in_bin[n]
                    pivot = [ib.position[0],
                             ib.position[1] + ib.get_dimension()[1],
                             ib.position[2]]
                    try_put_item = bin.can_hold_item_with_rotation(item, pivot)

                    if try_put_item:
                        can_put = True
                        q = 0
                        ib_neigh_x_axis = []
                        ib_neigh_y_axis = []
                        ib_neigh_z_axis = []
                        right_neighbor = False
                        front_neighbor = False
                        above_neighbor = False

                        while q < len(items_in_bin_temp):
                            if items_in_bin_temp[q] == items_in_bin[n]:
                                q += 1

                            else:
                                ib_neighbor = items_in_bin_temp[q]

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
                            x_distance = bin.length - ib.position[0]
                            ib_neigh_x_axis.append(x_distance)

                        if not front_neighbor:
                            y_distance = bin.width - (ib.position[1] + ib.get_dimension()[1])
                            ib_neigh_y_axis.append(y_distance)

                        if not above_neighbor:
                            z_distance = bin.height - ib.position[2]
                            ib_neigh_z_axis.append(z_distance)

                        distance_3D = [min(ib_neigh_x_axis), min(ib_neigh_y_axis), min(ib_neigh_z_axis)]
                        pivot_dict[tuple(pivot)] = distance_3D

                elif axis == Axis.HEIGHT:  # axis = 2/ z-axis
                    ib = items_in_bin[n]
                    pivot = [ib.position[0],
                             ib.position[1],
                             ib.position[2] + ib.get_dimension()[2]]
                    try_put_item = bin.can_hold_item_with_rotation(item, pivot)

                    if try_put_item:
                        can_put = True
                        q = 0
                        ib_neigh_x_axis = []
                        ib_neigh_y_axis = []
                        ib_neigh_z_axis = []
                        right_neighbor = False
                        front_neighbor = False
                        above_neighbor = False

                        while q < len(items_in_bin_temp):
                            if items_in_bin_temp[q] == items_in_bin[n]:
                                q += 1

                            else:
                                ib_neighbor = items_in_bin_temp[q]

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
                            x_distance = bin.length - ib.position[0]
                            ib_neigh_x_axis.append(x_distance)

                        if not front_neighbor:
                            y_distance = bin.width - ib.position[1]
                            ib_neigh_y_axis.append(y_distance)

                        if not above_neighbor:
                            z_distance = bin.height - (ib.position[2] + ib.get_dimension()[2])
                            ib_neigh_z_axis.append(z_distance)

                        distance_3D = [min(ib_neigh_x_axis), min(ib_neigh_y_axis), min(ib_neigh_z_axis)]
                        pivot_dict[tuple(pivot)] = distance_3D

                n += 1

        return pivot_dict

    def pivot_list(self, bin, item):
        """Obtain all optional pivot points that one item could be placed into a certain bin.
        Args:
            bin: a bin in bin list that a certain item will be placed into.
            item: an unplaced item in item list.
        Returns:
            a pivot_list containing all optional pivot points that the item could be placed into a certain bin.
        """

        pivot_list = []

        for axis in range(0, 3):
            items_in_bin = bin.items

            for ib in items_in_bin:
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

    def choose_pivot_point(self, bin, item):
        """Choose the optimal one from all optional pivot points of the item after comparison.
        Args:
            bin: a bin in bin list that a certain item will be placed into.
            item: an unplaced item in item list.
        Returns:
            the optimal pivot point that a item could be placed into a bin.
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

        pivot_list = self.pivot_list(bin, item)

        for pivot in pivot_list:
            try_put_item = bin.can_hold_item_with_rotation(item, pivot)

            if try_put_item:
                can_put = True
                pivot_available.append(pivot)
                # print("kkk",pivot)
                pivot_temp = sorted(pivot)
                # print("hhh",pivot_temp)
                pivot_available_temp.append(pivot_temp)

        if pivot_available:
            while p < len(pivot_available_temp):
                vertex_3d.append(pivot_available_temp[p][0])
                p += 1
            # print("jkdjcbjvbjv",vertex_3d)
            p = 0
            while p < len(pivot_available_temp):
                if pivot_available_temp[p][0] == min(vertex_3d):
                    # print("iii",min(vertex_3d))
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

    def pack_to_bin(self, bin, item):
        """For each item and each bin, perform whole pack process with optimal orientation and pivot point.
        Args:
            bin: a bin in bin list that a certain item will be placed into.
            item: an unplaced item in item list.
        Returns: return value is void.
        """

        if not bin.items:
            response = bin.put_item(item, START_POSITION, [bin.length, bin.width, bin.height])
            #print("JJJjjjdcdc")
            if not response:
                bin.unfitted_items.append(item)
            else:
                 self.placed_items.append(item)
            return

        else:
            pivot_point = self.choose_pivot_point(bin, item)
            pivot_dict = self.pivot_dict(bin, item)

            if not pivot_point:
                bin.unfitted_items.append(item)
                return

            distance_3D = pivot_dict[tuple(pivot_point)]
            response = bin.put_item(item, pivot_point, distance_3D)
            if response:
                self.placed_items.append(item)
            return

    def pack(
            self, bigger_first=True, number_of_decimals=DEFAULT_NUMBER_OF_DECIMALS):
        """For a list of items and a list of bins, perform the whole pack process.
        Args:
            bin: a bin in bin list that a certain item will be placed into.
            item: an unplaced item in item list.
        Returns:
            For each bin, print detailed information about placed and unplaced items.
            Then, print the optimal bin with highest packing rate.
        """

        for bin in self.bins:
            bin.format_numbers(number_of_decimals)

        for unplaced_item in self.unplaced_items:
            unplaced_item.format_numbers(number_of_decimals)

        self.bins.sort(
            key=lambda bin: bin.get_volume())  # default order of bins: from smallest to biggest
        # self.unplaced_items.sort(
        #     key=lambda unplaced_item: unplaced_item.get_volume(),
        #     reverse=bigger_first)  # default order of items: from biggest to smallest

        filling_ratio_list = []

        for bin in self.bins:
            for unplaced_item in self.unplaced_items:
                bin.unplaced_items.append(unplaced_item)

        for bin in self.bins:
            for unplaced_item in self.unplaced_items:
                self.pack_to_bin(bin, unplaced_item)

            print("\n:::::::::::", bin.string())
            print("FITTED ITEMS:")
            for item in bin.items:
                print("====> ", item.string())

            print("\nUNFITTED ITEMS:")
            for item in bin.unfitted_items:
                print("====> ", item.string())

            filling_ratio_list.append(bin.get_filling_ratio())

        max_filling_ratio = max(filling_ratio_list)

        for bin in self.bins:
            if bin.get_filling_ratio() == max_filling_ratio:
                for item in bin.items:
                    self.placed_items.append(item)
                print("\nSelected bin with highest filling ratio: ", bin.string())
