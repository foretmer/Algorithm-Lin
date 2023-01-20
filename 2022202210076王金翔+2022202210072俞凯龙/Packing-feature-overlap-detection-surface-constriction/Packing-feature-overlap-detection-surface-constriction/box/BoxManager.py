from collections import deque

import numpy as np

from box.Box import Box
from box.BoxType import BoxType


class BoxManager:
    def __init__(self):
        self.box_num = 0
        self.type_num = 0

        self.box_repository = []
        self.retry_boxes = deque()

        self.is_out_of_box = False

    def add_box_type(self, l, w, h, n):
        self.type_num += 1
        self.box_repository.append(BoxType(self.type_num, l, w, h, n))
        return self

    def add_retry_box(self, box: Box):
        if box is not None:
            self.retry_boxes.appendleft(box)

    def get_box(self):
        if len(self.retry_boxes) > 0:
            return self.retry_boxes.pop()

        while len(self.box_repository) != 0:
            box_type: BoxType = self.box_repository[np.random.randint(0, self.type_num)]
            if box_type.get_box_if_available():
                self.box_num += 1
                print("type[" + str(box_type.type_id) + "]" + " remain: " + str(
                    self.get_remain_box_num(box_type.type_id)))
                return Box(self.box_num, box_type.type_id, box_type.l, box_type.w, box_type.h)
            else:
                print("type_id " + str(box_type.type_id) + " is out of box!")
                self.box_repository.remove(box_type)
                self.type_num -= 1

        print('out of box!')
        self.is_out_of_box = True
        return None

    def get_remain_box_num(self, type_id):
        for box_type in self.box_repository:
            if box_type.type_id == type_id:
                return box_type.n

        return 0

    def remove_box_type(self, type_id):
        for box_type in self.box_repository:
            if box_type.type_id == type_id:
                self.box_repository.remove(box_type)
                self.type_num -= 1

    def is_repository_empty(self):
        return len(self.box_repository) == 0

    def _log(self, box, type_id):
        print(box.str() + ' type remain:' + str(self.get_remain_box_num(type_id)))
