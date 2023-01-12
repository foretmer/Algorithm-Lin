from typing import List
from copy import deepcopy
from data import *

def _is_rectangles_overlap(rec1:tuple, rec2:tuple) -> bool:
    return not (
        rec1[0] >= rec2[2] or rec1[1] >= rec2[3] or
        rec2[0] >= rec1[2] or rec2[1] >= rec1[3]
    )

def _is_cargos_collide(cargo0: Cargo, cargo1: Cargo) -> bool:
    return (
        _is_rectangles_overlap(cargo0.get_shadow_of("xy"), cargo1.get_shadow_of("xy")) and
        _is_rectangles_overlap(cargo0.get_shadow_of("yz"), cargo1.get_shadow_of("yz")) and
        _is_rectangles_overlap(cargo0.get_shadow_of(
            "xz"), cargo1.get_shadow_of("xz"))
    )


class Container(object):
    def __init__(self, length: int, width: int, height: int) -> None:
        self._length = length
        self._width = width
        self._height = height
        self._refresh()

    def __repr__(self) -> str:
        return f"{self._length}, {self._width}, {self._height}"

    def _refresh(self):
        # self._horizontal_planar = 0  # 水平放置参考面
        # self._vertical_planar = 0  # 垂直放置参考面
        self._available_points = [Point(0, 0, 0)]  # 可放置点有序列表
        self._setted_cargos: List[Cargo] = []
        self._H_matrix = torch.zeros(L, W)

    def is_encasable(self, site: Point, cargo: Cargo) -> bool:
        encasable = True
        temp = deepcopy(cargo)
        temp.point = site
        if (
            temp.x + temp.length > self._length or
            temp.y + temp.width > self._width or
            temp.z + temp.height > self._height
        ):
            encasable = False
        for setted_cargo in self._setted_cargos:
            if _is_cargos_collide(temp, setted_cargo):
                encasable = False
        return encasable


    # 所有可放置的点及生成的转换
    def encase(self, cargo: Cargo):
        temp = cargo
        input = torch.zeros(1, 2, L, W)
        points = []
        poses = []
        is_encase = False
        for point in self._available_points:
            for tmp_pose in CargoPose:
                temp.pose = tmp_pose
                # 可以放置
                if self.is_encasable(point, temp):
                    # self._setted_cargos.append(cargo)
                    # cargo.point(point)
                    is_encase = True
                    cargo_matrix = torch.zeros(L, W)
                    # cargo_matrix[point.x: point.x+cargo.length][point.y, point.y+cargo.width] += cargo.height
                    for x in range(point.x, point.x+cargo.length):
                        for y in range(point.y, point.y+cargo.width):
                            cargo_matrix[x][y] += cargo.height

                    new_input = torch.stack((self._H_matrix, cargo_matrix), dim=0)
                    new_input = new_input.unsqueeze(0)
                    input = torch.cat((input, new_input), dim=0)
                    points.append(point)
                    poses.append(tmp_pose)

        if is_encase:
            return is_encase, input[1:], points, poses
        else:
            return is_encase, input, points, poses


    # 放置新的箱子
    def update_state(self, cargo:Cargo):
        # update settled cargos
        self._setted_cargos.append(cargo)

        # update available points
        origin_point = cargo.point
        self._available_points.remove(origin_point)
        new_point = Point(origin_point.x+cargo.length, origin_point.y, origin_point.z)
        # if not (new_point.z > 0 and self._H_matrix[new_point.x][new_point.y] == 0):
        self._available_points.append(new_point)

        new_point = Point(origin_point.x, origin_point.y+cargo.width, origin_point.z)
        # if not (new_point.z > 0 and self._H_matrix[new_point.x][new_point.y] == 0):
        self._available_points.append(new_point)

        new_point = Point(origin_point.x, origin_point.y, origin_point.z+cargo.height)
        #if not (new_point.z > 0 and self._H_matrix[new_point.x][new_point.y] == 0):
        self._available_points.append(new_point)

        # update H_matrix
        for x in range(origin_point.x, origin_point.x + cargo.length):
            for y in range(origin_point.y, origin_point.y + cargo.width):
                self._H_matrix[x][y] += cargo.height


    def maximalSquare(self) -> int:
        matrix = self._H_matrix
        #长度为0，直接返回0
        if len(matrix) == 0 or len(matrix[0]) == 0:
            return 0

        maxSide0 = 0
        rows, columns = len(matrix), len(matrix[0])

        #新增二个全为0的数组
        dp0 = [[0] * columns for _ in range(rows)]

        for i in range(rows):
            for j in range(columns):

                # 取0中的最大正方形
                if matrix[i][j] == 0:
                    # 第一行和第一列为0时，新数组值为1
                    if i == 0 or j == 0:
                        dp0[i][j] = 1
                    # 取改值左边、上边、左上中的最小值+1
                    else:
                        dp0[i][j] = min(dp0[i - 1][j], dp0[i][j - 1], dp0[i - 1][j - 1]) + 1
                    maxSide0 = max(maxSide0, dp0[i][j])

        maxSide = maxSide0
        maxSquare = maxSide * maxSide
        return maxSquare

    # obtain the reward R=D+w(V1+V2)
    def reward(self):
        # lines = self._H_matrix.norm(0, dim=0)
        # none_zeros = sum(lines)
        # zeros = self._H_matrix.size(0) * self._H_matrix.size(1) - none_zeros
        # maxSquare = self.maximalSquare()
        # V1_2 = zeros.item() + maxSquare

        length = self._length
        width = self._width
        for l in range(self._length - 1, -1, -1):
            if not (torch.equal(self._H_matrix[l], torch.zeros(self._H_matrix[l].shape))):
                length = l
                break

        for w in range(self._width - 1, -1, -1):
            if not (torch.equal(self._H_matrix[:, w], torch.zeros(self._H_matrix[:, w].shape))):
                width = w
                break

        length = self._length - (length + 1)
        width = self._width - (width + 1)
        V1_2 = length * width + self._width * length + self._length * width

        maxHeight = self._H_matrix.max()
        D = self._height - maxHeight.item()
        w = 256
        reward = D / H + w * V1_2 / (2 * L * W)
        return reward

    @property
    def volume(self) -> int:
        return self._height * self._length * self._width

    def occupy_volume(self):
        v_sum = 0
        for cargo in self._setted_cargos:
            v_sum += cargo.volume
        return v_sum
