import operator
from operator import *




class Point(object):
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

        self.capable = 0

    @property
    def show(self):
        return [self.x, self.y, self.z]

def point_equal(point1:Point, point2:Point):
    if point1.x == point2.x and point1.y == point2.y and point1.z == point2.z:
        return True
    else:
        return False

class CargoType(object):
    def __init__(self, length: int, width: int, height: int, number:int, style:int) -> None:
        self._shape = [length, width, height]
        self._number = number
        self._style = style
        self._pose = -1
        # self.pose = 0

    @property
    def pose(self):
        return self._pose

    @pose.setter
    def pose(self, new_pose: int):
        edges = sorted(self._shape)
        # max side down
        if new_pose == 0:
            self._shape = [edges[2], edges[1], edges[0]]
        if new_pose == 1:
            self._shape = [edges[1], edges[2], edges[0]]

        # mid side down
        if new_pose == 2:
            self._shape = [edges[2], edges[0], edges[1]]
        if new_pose == 3:
            self._shape = [edges[0], edges[2], edges[1]]

        # small side down
        if new_pose == 4:
            self._shape = [edges[1], edges[0], edges[2]]
        if new_pose == 5:
            self._shape = [edges[0], edges[1], edges[2]]
        self._pose = new_pose

    @property
    def shape(self):
        return self._shape

    @property
    def volume(self) -> int:
        vol = self._shape[0] * self._shape[1] * self._shape[2]
        return vol

    @property
    def length(self) -> int:
        return self._shape[0]

    @property
    def width(self) -> int:
        return self._shape[1]

    @property
    def height(self) -> int:
        return self._shape[2]

    @property
    def number(self) -> int:
        return self._number

    @number.setter
    def number(self, n):
        self._number += n

class CargoPos(object):
    def __init__(self, cargo:CargoType, pos:Point) -> None:
        self.cargo = cargo
        self.pos = pos


class Cargo(object):
    def __init__(self) -> None:
        self.cargos = []
        self._len = 0

    @property
    def len(self):
        return self._len

    @len.setter
    def len(self, n):
        self._len += n

    # sorted by volume
    def extend(self, cargo):
        self.cargos.append(cargo)
        sortKey = operator.attrgetter('volume')
        self.cargos.sort(key=sortKey)
        self.len = 1

class Container(object):
    def __init__(self, length: int, width: int, height: int) -> None:
        self.length = length
        self.width = width
        self.height = height
        self.available_points = [Point(0, 0, 0)]
        # expected CargoPos
        self.set_cargo = []
        self.used = []

    def place(self, cargo: CargoType, pos: Point):
        flag_float = True
        flag = True
        if cargo.number <= 0:
            flag = False
            return flag
        if cargo.length + pos.x > self.length:
            flag = False
            return flag
        if cargo.width + pos.y > self.width:
            flag = False
            return flag
        if cargo.height + pos.z > self.height:
            flag = False
            return flag

        # all vertex should not inside other cargo
        vertexs = []
        vertex1 = Point(pos.x + cargo.length, pos.y, pos.z)
        vertex2 = Point(pos.x, pos.y + cargo.width, pos.z)
        vertex3 = Point(pos.x + cargo.length, pos.y + cargo.width, pos.z)
        vertex4 = Point(pos.x, pos.y, pos.z + cargo.height)
        vertex5 = Point(pos.x + cargo.length, pos.y, pos.z + cargo.height)
        vertex6 = Point(pos.x, pos.y + cargo.width, pos.z + cargo.height)
        vertex7 = Point(pos.x + cargo.length, pos.y + cargo.width, pos.z + cargo.height)
        # set inside point to judge the situation that vertex lay on the edge
        far_average_x = pos.x + cargo.length / 2
        far_average_y = pos.y + cargo.width - 1
        far_average_z = pos.z + cargo.height / 2
        inside1 = Point(int(far_average_x), far_average_y, int(far_average_z))
        up_average_x = pos.x + cargo.length / 2
        up_average_y = pos.y + cargo.width / 2
        up_average_z = pos.z + cargo.height - 1
        inside2 = Point(int(up_average_x),  int(up_average_y), int(up_average_z))
        ri_average_x = pos.x + cargo.length - 1
        ri_average_y = pos.y + cargo.width / 2
        ri_average_z = pos.z + cargo.height / 2
        inside3 = Point(int(ri_average_x), int(ri_average_y), int(ri_average_z))
        do_average_x = pos.x + cargo.length / 2
        do_average_y = pos.y + cargo.width / 2
        do_average_z = pos.z + 1
        inside4 = Point(int(do_average_x), int(do_average_y), int(do_average_z))
        vertexs.append(vertex1)
        vertexs.append(vertex2)
        vertexs.append(vertex3)
        vertexs.append(vertex4)
        vertexs.append(vertex5)
        vertexs.append(vertex6)
        vertexs.append(vertex7)
        vertexs.append(inside1)
        vertexs.append(inside2)
        vertexs.append(inside3)
        vertexs.append(inside4)

        # prevent floating
        op = Point(pos.x, pos.y, pos.z - 1)
        x_p = Point(pos.x + cargo.length, pos.y, pos.z - 1)
        xf_p = Point(pos.x, pos.y + cargo.width, pos.z - 1)
        f_p = Point(pos.x + cargo.length, pos.y + cargo.width, pos.z - 1)
        floatp = [op, x_p, xf_p, f_p]
        for eachcargo in self.set_cargo:
            if not flag:
                return False
            x_min = eachcargo.pos.x
            x_max = eachcargo.pos.x + eachcargo.cargo.length
            y_min = eachcargo.pos.y
            y_max = eachcargo.pos.y + eachcargo.cargo.width
            z_min = eachcargo.pos.z
            z_max = eachcargo.pos.z + eachcargo.cargo.height
            for vertex in vertexs:
                if x_min < vertex.x < x_max and y_min < vertex.y < y_max and z_min < vertex.z < z_max:
                    flag = False

            for downp in floatp:
                if downp.z <= 0:
                    flag_float = False
                if x_min < downp.x < x_max and y_min < downp.y < y_max and z_min < downp.z < z_max:
                    flag_float = False
        if self.set_cargo != [] and flag_float:
            flag = False
        if flag:

            # Cargo
            newCargo = CargoPos(cargo, pos)
            self.set_cargo.append(newCargo)

            # Point
            self.used.append(pos)
            self.available_points.remove(pos)
            newPointX = Point(pos.x + cargo.length, pos.y, pos.z)
            newPointY = Point(pos.x, pos.y + cargo.width, pos.z)
            newPointZ = Point(pos.x, pos.y, pos.z + cargo.height)

            flagX = False
            flagY = False
            flagZ = False
            for point in self.used:
                if point_equal(newPointX, point):
                    flagX = True
                if point_equal(newPointY, point):
                    flagY = True
                if point_equal(newPointZ, point):
                    flagZ = True

            if not flagX:
                self.available_points.append(newPointX)
                self.used.append(newPointX)
            if not flagY:
                self.available_points.append(newPointY)
                self.used.append(newPointY)
            if not flagZ:
                self.available_points.append(newPointZ)
                self.used.append(newPointZ)

            # debug
            # print(newPointX.show)
            # print(newPointY.show)
            # print(newPointZ.show)
            # reduce Cargo
            cargo.number = -1
        return flag

    def place_test(self, cargo: CargoType, pos: Point):
        '''
        This function is used to say whether this point can be placed in this point
        :param cargo:
        :param pos:
        :return:
        '''
        flag_float = True
        flag = True
        if cargo.number <= 0:
            flag = False
            return flag, 0
        if cargo.length + pos.x > self.length:
            flag = False
            return flag, 0
        if cargo.width + pos.y > self.width:
            flag = False
            return flag, 0
        if cargo.height + pos.z > self.height:
            flag = False
            return flag, 0
        vertexs = []
        vertex1 = Point(pos.x + cargo.length, pos.y, pos.z)
        vertex2 = Point(pos.x, pos.y + cargo.width, pos.z)
        vertex3 = Point(pos.x + cargo.length, pos.y + cargo.width, pos.z)
        vertex4 = Point(pos.x, pos.y, pos.z + cargo.height)
        vertex5 = Point(pos.x + cargo.length, pos.y, pos.z + cargo.height)
        vertex6 = Point(pos.x, pos.y + cargo.width, pos.z + cargo.height)
        vertex7 = Point(pos.x + cargo.length, pos.y + cargo.width, pos.z + cargo.height)
        # set inside point to judge the situation that vertex lay on the edge
        far_average_x = pos.x + cargo.length / 2
        far_average_y = pos.y + cargo.width - 1
        far_average_z = pos.z + cargo.height / 2
        inside1 = Point(int(far_average_x), far_average_y, int(far_average_z))
        up_average_x = pos.x + cargo.length / 2
        up_average_y = pos.y + cargo.width / 2
        up_average_z = pos.z + cargo.height - 1
        inside2 = Point(int(up_average_x), int(up_average_y), int(up_average_z))
        ri_average_x = pos.x + cargo.length - 1
        ri_average_y = pos.y + cargo.width / 2
        ri_average_z = pos.z + cargo.height / 2
        inside3 = Point(int(ri_average_x), int(ri_average_y), int(ri_average_z))
        do_average_x = pos.x + cargo.length / 2
        do_average_y = pos.y + cargo.width / 2
        do_average_z = pos.z + 1
        inside4 = Point(int(do_average_x), int(do_average_y), int(do_average_z))
        vertexs.append(vertex1)
        vertexs.append(vertex2)
        vertexs.append(vertex3)
        vertexs.append(vertex4)
        vertexs.append(vertex5)
        vertexs.append(vertex6)
        vertexs.append(vertex7)
        vertexs.append(inside1)
        vertexs.append(inside2)
        vertexs.append(inside3)
        vertexs.append(inside4)

        # prevent floating
        op = Point(pos.x, pos.y, pos.z - 1)
        x_p = Point(pos.x + cargo.length, pos.y, pos.z - 1)
        xf_p = Point(pos.x, pos.y + cargo.width, pos.z - 1)
        f_p = Point(pos.x + cargo.length, pos.y + cargo.width, pos.z - 1)
        floatp = [op, x_p, xf_p, f_p]
        for eachcargo in self.set_cargo:
            if not flag:
                return False, 0
            x_min = eachcargo.pos.x
            x_max = eachcargo.pos.x + eachcargo.cargo.length
            y_min = eachcargo.pos.y
            y_max = eachcargo.pos.y + eachcargo.cargo.width
            z_min = eachcargo.pos.z
            z_max = eachcargo.pos.z + eachcargo.cargo.height
            for vertex in vertexs:
                if x_min < vertex.x < x_max and y_min < vertex.y < y_max and z_min < vertex.z < z_max:
                    flag = False

            for downp in floatp:
                if downp.z <= 0:
                    flag_float = False
                if x_min < downp.x < x_max and y_min < downp.y < y_max and z_min < downp.z < z_max:
                    flag_float = False
        if self.set_cargo != [] and flag_float:
            flag = False

        newPointX = Point(pos.x + cargo.length, pos.y, pos.z)
        newPointY = Point(pos.x, pos.y + cargo.width, pos.z)
        newPointZ = Point(pos.x, pos.y, pos.z + cargo.height)

        flagX = False
        flagY = False
        flagZ = False
        for point in self.used:
            if point_equal(newPointX, point):
                flagX = True
            if point_equal(newPointY, point):
                flagY = True
            if point_equal(newPointZ, point):
                flagZ = True
        newPointCount = 0
        pointlist = []
        if not flagX:
            pointlist.append(newPointX)
            newPointCount += 1
        if not flagY:
            pointlist.append(newPointY)
            newPointCount += 1
        if not flagZ:
            pointlist.append(newPointZ)
            newPointCount += 1

        return flag, newPointCount

    def place_test2(self, cargo: CargoType, pos: Point):
        '''
        This function is used to say whether this point can be placed in this point
        :param cargo:
        :param pos:
        :return:
        '''
        flag_float = True
        flag = True
        if cargo.number <= 0:
            flag = False
            return flag, 0
        if cargo.length + pos.x > self.length:
            flag = False
            return flag, 0
        if cargo.width + pos.y > self.width:
            flag = False
            return flag, 0
        if cargo.height + pos.z > self.height:
            flag = False
            return flag, 0
        vertexs = []
        vertex1 = Point(pos.x + cargo.length, pos.y, pos.z)
        vertex2 = Point(pos.x, pos.y + cargo.width, pos.z)
        vertex3 = Point(pos.x + cargo.length, pos.y + cargo.width, pos.z)
        vertex4 = Point(pos.x, pos.y, pos.z + cargo.height)
        vertex5 = Point(pos.x + cargo.length, pos.y, pos.z + cargo.height)
        vertex6 = Point(pos.x, pos.y + cargo.width, pos.z + cargo.height)
        vertex7 = Point(pos.x + cargo.length, pos.y + cargo.width, pos.z + cargo.height)
        # set inside point to judge the situation that vertex lay on the edge
        far_average_x = pos.x + cargo.length / 2
        far_average_y = pos.y + cargo.width - 1
        far_average_z = pos.z + cargo.height / 2
        inside1 = Point(int(far_average_x), far_average_y, int(far_average_z))
        up_average_x = pos.x + cargo.length / 2
        up_average_y = pos.y + cargo.width / 2
        up_average_z = pos.z + cargo.height - 1
        inside2 = Point(int(up_average_x), int(up_average_y), int(up_average_z))
        ri_average_x = pos.x + cargo.length - 1
        ri_average_y = pos.y + cargo.width / 2
        ri_average_z = pos.z + cargo.height / 2
        inside3 = Point(int(ri_average_x), int(ri_average_y), int(ri_average_z))
        do_average_x = pos.x + cargo.length / 2
        do_average_y = pos.y + cargo.width / 2
        do_average_z = pos.z + 1
        inside4 = Point(int(do_average_x), int(do_average_y), int(do_average_z))
        vertexs.append(vertex1)
        vertexs.append(vertex2)
        vertexs.append(vertex3)
        vertexs.append(vertex4)
        vertexs.append(vertex5)
        vertexs.append(vertex6)
        vertexs.append(vertex7)
        vertexs.append(inside1)
        vertexs.append(inside2)
        vertexs.append(inside3)
        vertexs.append(inside4)

        # prevent floating
        op = Point(pos.x, pos.y, pos.z - 1)
        x_p = Point(pos.x + cargo.length, pos.y, pos.z - 1)
        xf_p = Point(pos.x, pos.y + cargo.width, pos.z - 1)
        f_p = Point(pos.x + cargo.length, pos.y + cargo.width, pos.z - 1)
        floatp = [op, x_p, xf_p, f_p]
        for eachcargo in self.set_cargo:
            if not flag:
                return False, 0
            x_min = eachcargo.pos.x
            x_max = eachcargo.pos.x + eachcargo.cargo.length
            y_min = eachcargo.pos.y
            y_max = eachcargo.pos.y + eachcargo.cargo.width
            z_min = eachcargo.pos.z
            z_max = eachcargo.pos.z + eachcargo.cargo.height
            for vertex in vertexs:
                if x_min < vertex.x < x_max and y_min < vertex.y < y_max and z_min < vertex.z < z_max:
                    flag = False

            for downp in floatp:
                if downp.z <= 0:
                    flag_float = False
                if x_min < downp.x < x_max and y_min < downp.y < y_max and z_min < downp.z < z_max:
                    flag_float = False
        if self.set_cargo != [] and flag_float:
            flag = False

        newPointX = Point(pos.x + cargo.length, pos.y, pos.z)
        newPointY = Point(pos.x, pos.y + cargo.width, pos.z)
        newPointZ = Point(pos.x, pos.y, pos.z + cargo.height)

        flagX = False
        flagY = False
        flagZ = False
        for point in self.used:
            if point_equal(newPointX, point):
                flagX = True
            if point_equal(newPointY, point):
                flagY = True
            if point_equal(newPointZ, point):
                flagZ = True
        newPointCount = 0
        pointlist = []
        if not flagX:
            pointlist.append(newPointX)
        if not flagY:
            pointlist.append(newPointY)
        if not flagZ:
            pointlist.append(newPointZ)

        return flag, pointlist

    def status_save(self):
        file = open("test.csv", 'w', encoding='utf-8')
        file.write(f"index,x,y,z,length,width,height\n")
        i = 1
        for carogPos in self.set_cargo:
            file.write(f"{i},{carogPos.pos.x},{carogPos.pos.y},{carogPos.pos.z},")
            file.write(f"{carogPos.cargo.length},{carogPos.cargo.width},{carogPos.cargo.height}\n")
            i += 1
        file.write(f"container,,,,{self}\n")
        file.close()

    @property
    def volume(self) -> int:
        vol = self.length * self.width * self.height
        return vol



    def useage(self):
        sumV = 0
        for cargoSet in self.set_cargo:
            sumV += cargoSet.cargo.volume
        print(sumV)
        return sumV / self.volume

# def test():
#     c1 = CargoType(108, 76, 30, 24, 0)
#     c2 = CargoType(110, 43, 25, 7, 1)
#     c3 = CargoType(92, 81, 55, 22, 2)
#     c4 = CargoType(81, 33, 28, 13, 3)
#     c5 = CargoType(120, 99, 73, 15, 4)
#     cargo = Cargo()
#     cargo.extend(c1)
#     cargo.extend(c2)
#     cargo.extend(c3)
#     cargo.extend(c4)
#     cargo.extend(c5)
#     container = Container(587, 233, 220)
#     # print(c1.pose)
#     container.place(cargo.cargos[0], container.available_points[0])
#     container.status_save()
#     drawer.draw_reslut(container)
#
# if __name__ == "__main__":
#     test()