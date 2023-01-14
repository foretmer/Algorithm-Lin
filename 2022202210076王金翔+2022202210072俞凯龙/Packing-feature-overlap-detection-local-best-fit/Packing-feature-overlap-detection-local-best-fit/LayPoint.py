class LayPoint:
    def __init__(self, x=-1, y=-1, z=-1):
        self.x = x
        self.y = y
        self.z = z

    @property
    def is_valid(self) -> bool:
        return self.x >= 0 and self.y >= 0 and self.z >= 0

    @property
    def tuple(self) -> tuple:
        return self.x, self.y, self.z

    def __eq__(self, o: object) -> bool:
        if isinstance(o, LayPoint):
            return self.x == o.x and self.y == o.y and self.z == o.z

        return False
