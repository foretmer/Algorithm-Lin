import time

from Space import Space
from VisualHelper import VisualHelper
from box.Box import Box


class Container:
    def __init__(self, l, w, h):
        self.l = l
        self.w = w
        self.h = h
        self.volume = l * w * h

        self.used_l = 0
        self.used_w = 0
        self.used_h = 0
        self.used_volume = 0
        self.used_v = 0
        self.local_fit_rate = 0

        self.boxes = []
        self.spaces = []
        self.spaces.append(Space(x=0, y=0, z=0, l=l, w=w, h=h))

        self.is_full = False

    def add_box_if_available(self, box: Box):
        space, posture = self._get_best_fit_space(box)

        if space is None:
            print('type ' + str(box.type_id) + ' fit failed!')
            return False

        box.pack(x=space.position.x, y=space.position.y, z=space.position.z, lay_l=posture.lay_l, lay_w=posture.lay_w,
                 lay_h=posture.lay_h)
        self.boxes.append(box)
        self.used_v += box.volume
        self.used_l, self.used_w, self.used_h, self.used_volume, self.local_fit_rate = self._update_used_volume(space,
                                                                                                                posture)
        self._log(box)
        self._divide_space(space, posture)
        return True

    def _update_used_volume(self, space, posture):
        if space.position.x + posture.lay_l > self.used_l:
            used_l = space.position.x + posture.lay_l
        else:
            used_l = self.used_l

        if space.position.y + posture.lay_w > self.used_w:
            used_w = space.position.y + posture.lay_w
        else:
            used_w = self.used_w

        if space.position.z + posture.lay_h > self.used_h:
            used_h = space.position.z + posture.lay_h
        else:
            used_h = self.used_h

        used_volume = self.used_volume + posture.lay_l * posture.lay_w * posture.lay_h
        local_fit_rate = used_volume / (used_l * used_w * used_h)

        return used_l, used_w, used_h, used_volume, local_fit_rate

    def _get_best_fit_space(self, box: Box):
        best_local_fit_rate = 0
        best_space = None
        best_posture = None

        for space in self.spaces:
            # 找出所有塞的下姿势
            postures = space.find_available_postures(box)
            if len(postures) == 0:
                continue

            else:
                temp_best_local_fit_rate = 0
                temp_best_posture = None
                for posture in postures:
                    used_l, used_w, used_h, used_volume, local_fit_rate = self._update_used_volume(space, posture)
                    if local_fit_rate > temp_best_local_fit_rate:
                        temp_best_local_fit_rate = local_fit_rate
                        temp_best_posture = posture

                if temp_best_local_fit_rate > best_local_fit_rate:
                    best_space = space
                    best_local_fit_rate = temp_best_local_fit_rate
                    best_posture = temp_best_posture

        return best_space, best_posture

    def _divide_space(self, space, posture):
        # 空间的原点
        space_x = space.position.x
        space_y = space.position.y
        space_z = space.position.z
        lay_l = posture.lay_l
        lay_w = posture.lay_w
        lay_h = posture.lay_h
        # 一个空间装入一个箱子后划分为三个子空间
        space1 = Space(x=space_x, y=space_y, z=space_z + lay_h, l=lay_l, w=lay_w, h=space.h - lay_h)
        space2 = Space(x=space_x, y=space_y + lay_w, z=space_z, l=lay_l, w=space.w - lay_w, h=space.h)
        space3 = Space(x=space_x + lay_l, y=space_y, z=space_z, l=space.l - lay_l, w=space.w, h=space.h)
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
        used_v = 0
        for box in self.boxes:
            used_v += box.volume
        print('fit rate: ' + str(used_v / self.volume))

        end_time = time.time()
        VisualHelper(self.boxes).display(group, index)
        return end_time

    def _log(self, box):
        print(box.str())
