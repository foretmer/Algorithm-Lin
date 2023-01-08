from enum import Enum


class CargoPose(Enum):
    tall_wide = 0
    tall_thin = 1
    mid_wide = 2
    mid_thin = 3
    short_wide = 4
    short_thin = 5


class Point(object):
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"({self.x},{self.y},{self.z})"
    
    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y and self.z == __o.z

    @property
    def is_valid(self) -> bool:
        return self.x >= 0 and self.y >=0 and self.z>= 0
    
    @property
    def tuple(self) -> tuple:
        return (self.x, self.y, self.z)


class Cargo(object):
    def __init__(self, length: int, width: int, height: int) -> None:
        self._point = Point(-1, -1, -1)
        self._shape = {length, width, height}
        self._pose = CargoPose.tall_thin

    def __repr__(self) -> str:
        return f"{self._point} {self.shape}"

    @property
    def pose(self) -> CargoPose:
        return self._pose

    @pose.setter
    def pose(self, new_pose: CargoPose):
        self._pose = new_pose

    @property
    def _shape_swiche(self) -> dict:
        edges = sorted(self._shape)
        return {
            CargoPose.tall_thin: (edges[1], edges[0], edges[-1]),
            CargoPose.tall_wide: (edges[0], edges[1], edges[-1]),
            CargoPose.mid_thin: (edges[-1], edges[0], edges[1]),
            CargoPose.mid_wide: (edges[0], edges[-1], edges[-1]),
            CargoPose.short_thin: (edges[-1], edges[1], edges[0]),
            CargoPose.short_wide: (edges[1], edges[-1], edges[0])
        }

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, new_point:Point):
        self._point = new_point

    @property
    def x(self) -> int:
        return self._point.x

    @x.setter
    def x(self, new_x: int):
        self._point = Point(new_x, self.y, self.z)

    @property
    def y(self) -> int:
        return self._point.y

    @y.setter
    def y(self, new_y: int):
        self._point = Point(self.x, new_y, self.z)

    @property
    def z(self) -> int:
        return self._point.z

    @z.setter
    def z(self, new_z: int):
        self._point = Point(self.z, self.y, new_z)

    @property
    def length(self) -> int:
        return self.shape[0]

    @property
    def width(self) -> int:
        return self.shape[1]

    @property
    def height(self) -> int:
        return self.shape[-1]

    def get_shadow_of(self, planar: str) -> tuple:
        if planar in ("xy", "yx"):
            x0, y0 = self.x, self.y
            x1, y1 = self.x + self.length, self.y + self.width
        elif planar in ("xz", "zx"):
            x0, y0 = self.x, self.z
            x1, y1 = self.x + self.length, self.z + self.height
        elif planar in ("yz", "zy"):
            x0, y0 = self.y, self.z
            x1, y1 = self.y + self.width, self.z + self.height
        return (x0, y0, x1, y1)

    @property
    def shape(self) -> tuple:
        return self._shape_swiche[self._pose]

    @shape.setter
    def shape(self, length, width, height):
        self._shape = {length, width, height}

    @property
    def volume(self) -> int:
        reslut = 1
        for i in self._shape:
            reslut *= i
        return reslut
