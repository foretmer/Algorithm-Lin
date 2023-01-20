class BoxType:
    def __init__(self, type_id, l, w, h, n):
        self.type_id = type_id
        self.l = l
        self.w = w
        self.h = h
        self.n = n

    def get_box_if_available(self):
        if self.n > 0:
            self.n -= 1
            return True

        return False
