from constants import *
from auxiliary_methods import *

class Truck:
    def __init__(self, name, length, width, height):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        # self.capacity = capacity
        self.total_boxes = 0  # number of total items in one bin
        self.boxes = []  # item in one bin -- a blank list initially
        self.unplaced_boxes = []
        self.unfitted_boxes = []  # unfitted item in one bin -- a blank list initially
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS

    def format_numbers(self, number_of_decimals):
        self.length = set_to_decimal(self.length, number_of_decimals)
        self.height = set_to_decimal(self.height, number_of_decimals)
        self.width = set_to_decimal(self.width, number_of_decimals)
        # self.capacity = set_to_decimal(self.capacity, number_of_decimals)
        self.number_of_decimals = number_of_decimals

    def get_volume(self):
        return set_to_decimal(
            self.length * self.height * self.width, self.number_of_decimals)

    # def get_total_weight(self):
    #     total_weight = 0

    #     for box in self.boxes:
    #         total_weight += box.weight

    #     return set_to_decimal(total_weight, self.number_of_decimals)

    def get_filling_ratio(self):
        total_filling_volume = 0
        total_filling_ratio = 0

        for box in self.boxes:
            total_filling_volume += box.get_volume()

        total_filling_ratio = total_filling_volume / self.get_volume()
        return set_to_decimal(total_filling_ratio, self.number_of_decimals)

    def can_hold_box_with_rotation(self, box, pivot, rl):
        """Evaluate whether one item can be placed into bin with all optional orientations.
        Args:
            box: any item in item list.
            pivot: an (x, y, z) coordinate, the back-lower-left corner of the item will be placed at the pivot.
            rl: a limited rotation type list
        Returns:
            a list containing all optional orientations. If not, return an empty list.
        """

        fit = False
        valid_item_position = [0, 0, 0]
        box.position = pivot
        rotation_type_list = []

        if not rl:
            for i in range(0, len(RotationType.ALL)):
                box.rotation_type = i
                dimension = box.get_dimension()
                if (
                        pivot[0] + dimension[0] <= self.length and  # x-axis
                        pivot[1] + dimension[1] <= self.width and  # y-axis
                        pivot[2] + dimension[2] <= self.height  # z-axis
                ):

                    fit = True

                    for current_box_in_truck in self.boxes:
                        if support(current_box_in_truck, box):
                            fit = True
                            break
                        else:
                            fit = False

                    for current_box_in_truck in self.boxes:
                        if intersect(current_box_in_truck, box):
                            fit = False
                            # box.position = [0, 0, 0]
                            break

                    if fit:
                        rotation_type_list.append(box.rotation_type)
                        # if self.get_total_weight() + box.weight > self.capacity:  # estimate whether bin reaches its capacity
                        #     fit = False
                        #     box.position = [0, 0, 0]
                        #     continue

                        # else:
                            # rotation_type_list.append(box.rotation_type)

                else:
                    continue
        else:
            for i in rl:
                box.rotation_type = i
                dimension = box.get_dimension()
                if (
                        pivot[0] + dimension[0] <= self.length and  # x-axis
                        pivot[1] + dimension[1] <= self.width and  # y-axis
                        pivot[2] + dimension[2] <= self.height  # z-axis
                ):

                    fit = True

                    if box.position[2] > 0:
                        for current_box_in_truck in self.boxes:
                            if support(current_box_in_truck, box):
                                fit = True
                                break
                            else:
                                fit = False

                    for current_box_in_truck in self.boxes:
                        if intersect(current_box_in_truck, box):
                            fit = False
                            # box.position = [0, 0, 0]
                            break

                    if fit:
                        rotation_type_list.append(box.rotation_type)

                else:
                    continue
        if not rotation_type_list:
            box.position = [0, 0, 0]
        return rotation_type_list

    def put_box(self, box, pivot, distance_3d, rl):
        """Evaluate whether an item can be placed into a certain bin with which orientation. If yes, perform put action.
        Args:
            box: any item in item list.
            pivot: an (x, y, z) coordinate, the back-lower-left corner of the item will be placed at the pivot.
            distance_3d: a 3D parameter to determine which orientation should be chosen.
        Returns:
            Boolean variable: False when an item couldn't be placed into the bin; True when an item could be placed and perform put action.
        """

        fit = False
        rotation_type_list = self.can_hold_box_with_rotation(box, pivot, rl)
        margins_3d_list = []
        margins_3d_list_temp = []
        margin_3d = []
        margin_2d = []
        margin_1d = []

        n = 0
        m = 0
        p = 0

        if not rotation_type_list:
            return fit

        else:
            fit = True

            rotation_type_number = len(rotation_type_list)

            if rotation_type_number == 1:
                box.rotation_type = rotation_type_list[0]
                self.boxes.append(box)
                self.total_boxes += 1
                return fit

            else:
                for rotation in rotation_type_list:
                    box.rotation_type = rotation
                    dimension = box.get_dimension()
                    margins_3d = [distance_3d[0] - dimension[0],
                                  distance_3d[1] - dimension[1],
                                  distance_3d[2] - dimension[2]]
                    margins_3d_temp = sorted(margins_3d)
                    margins_3d_list.append(margins_3d)
                    margins_3d_list_temp.append(margins_3d_temp)

                while p < len(margins_3d_list_temp):
                    margin_3d.append(margins_3d_list_temp[p][0])
                    p += 1

                p = 0
                while p < len(margins_3d_list_temp):
                    if margins_3d_list_temp[p][0] == min(margin_3d):
                        n += 1
                        margin_2d.append(margins_3d_list_temp[p][1])

                    p += 1

                if n == 1:
                    p = 0
                    while p < len(margins_3d_list_temp):
                        if margins_3d_list_temp[p][0] == min(margin_3d):
                            box.rotation_type = rotation_type_list[p]
                            self.boxes.append(box)
                            self.total_boxes += 1
                            return fit

                        p += 1

                else:
                    p = 0
                    while p < len(margins_3d_list_temp):
                        if (
                                margins_3d_list_temp[p][0] == min(margin_3d) and
                                margins_3d_list_temp[p][1] == min(margin_2d)
                        ):
                            m += 1
                            margin_1d.append(margins_3d_list_temp[p][2])

                        p += 1

                if m == 1:
                    p = 0
                    while p < len(margins_3d_list_temp):
                        if (
                                margins_3d_list_temp[p][0] == min(margin_3d) and
                                margins_3d_list_temp[p][1] == min(margin_2d)
                        ):
                            box.rotation_type = rotation_type_list[p]
                            self.boxes.append(box)
                            self.total_boxes += 1
                            return fit

                        p += 1

                else:
                    p = 0
                    while p < len(margins_3d_list_temp):
                        if (
                                margins_3d_list_temp[p][0] == min(margin_3d) and
                                margins_3d_list_temp[p][1] == min(margin_2d) and
                                margins_3d_list_temp[p][2] == min(margin_1d)
                        ):
                            box.rotation_type = rotation_type_list[p]
                            self.boxes.append(box)
                            self.total_boxes += 1
                            return fit

                        p += 1

    def string(self):
        return "%s(%sx%sx%s) vol(%s) box_number(%s) filling_ratio(%s)" % (
            self.name, self.length, self.width, self.height, 
            self.get_volume(), self.total_boxes, self.get_filling_ratio())
