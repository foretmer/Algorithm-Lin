from Box import Box
from Space import Space
from VisualHelper import VisualHelper
import time

class Container:
    def __init__(self, l, w, h):
        self.l = l
        self.w = w
        self.h = h
        self.volume = l * w * h
        self.used_volume = 0

        self.boxes = []
        self.spaces = []
        self.spaces.append(Space(x=0, y=0, z=0, l=l, w=w, h=h))

        self.is_full = False

    def add_box(self, box: Box):
        space, lay_l, lay_h, lay_w = self._get_best_fit_space(box)

        if space is None:
            print('type ' + str(box.type_id) + ' fit failed!')
            return False

        box.pack(x=space.position.x, y=space.position.y, z=space.position.z, lay_l=lay_l, lay_w=lay_w, lay_h=lay_h)
        self.boxes.append(box)
        self.used_volume += box.volume
        self._log(box)
        self._divide_space(space, lay_l, lay_w, lay_h)
        return True

    def _get_best_fit_space(self, box: Box):
        for space in self.spaces:
            # 记录箱子放置的姿势
            lay_l, lay_w, lay_h = space.fit(box)
            if lay_l == -1:
                continue

            else:
                return space, lay_l, lay_h, lay_w

        return None, -1, -1, -1

    def _divide_space(self, space, box_l, box_w, box_h):
        # 空间的原点
        space_x = space.position.x
        space_y = space.position.y
        space_z = space.position.z
        # 一个空间装入一个箱子后划分为三个子空间
        space1 = Space(x=space_x, y=space_y, z=space_z + box_h, l=box_l, w=box_w, h=space.h - box_h)
        space2 = Space(x=space_x, y=space_y + box_w, z=space_z, l=box_l, w=space.w - box_w, h=space.h)
        space3 = Space(x=space_x + box_l, y=space_y, z=space_z, l=space.l - box_l, w=space.w, h=space.h)
        self.spaces.remove(space)
        self._add_space(space1)
        self._add_space(space2)
        self._add_space(space3)

    def _add_space(self, space):
        i = 0
        for temp in self.spaces:
            if space.volume < temp.volume:
                self.spaces.insert(i, space)
                return
            else:
                i += 1

        self.spaces.append(space)

    def end(self, group="unknown", index="unknown"):
        print('fit rate: ' + str(self.used_volume / self.volume))
        endtime = time.time()
        VisualHelper(self.boxes).display(group,index)
        return endtime

    def _log(self, box):
        v = 0
        for space in self.spaces:
            v += space.volume
        print(box.str() + " remain space: " + str(v))
