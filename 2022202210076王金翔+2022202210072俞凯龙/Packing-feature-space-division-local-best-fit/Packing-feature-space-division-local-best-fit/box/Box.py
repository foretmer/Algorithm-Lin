from Coordinate import Coordinate


class Box:
    def __init__(self, ID, type_id=-1, l=0, w=0, h=0):
        self.ID = ID
        self.type_id = type_id

        self.l = l
        self.w = w
        self.h = h
        self.volume = l * w * h

        self.position = None
        self.is_packed = False

        self.lay_l = -1
        self.lay_w = -1
        self.lay_h = -1

    def pack(self, x, y, z, lay_l, lay_w, lay_h):
        self.position = Coordinate(x, y, z)
        self.is_packed = True
        self.lay_l = lay_l
        self.lay_w = lay_w
        self.lay_h = lay_h

    def str(self):
        return str(self.ID) + "[" + str(self.type_id) + "]: " + "(" + str(self.l) + ',' + str(self.w) + ',' + str(
            self.h) + ')'
