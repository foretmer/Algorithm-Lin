import numpy as np
import copy

class BoxCreator(object):
    def __init__(self):
        self.box_list = []

    def reset(self):
        self.box_list.clear()

    def generate_box_size(self, **kwargs):
        pass

    def preview(self, length):
        while len(self.box_list) < length:
            self.generate_box_size()
        return copy.deepcopy(self.box_list[:length])

    def drop_box(self):
        assert len(self.box_list) >= 0
        self.box_list.pop(0)

class RandomBoxCreator(BoxCreator):
    default_box_set = []
    for i in range(5):
        for j in range(5):
            for k in range(5):
                default_box_set.append((2+i, 2+j, 2+k))

    def __init__(self, box_size_set=None):
        super().__init__()
        self.box_set = box_size_set
        if self.box_set is None:
            self.box_set = RandomBoxCreator.default_box_set

    def generate_box_size(self, **kwargs):
        idx = np.random.randint(0, len(self.box_set))
        self.box_list.append(self.box_set[idx])
