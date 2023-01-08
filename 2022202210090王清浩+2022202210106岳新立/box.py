import numpy as np
from utils import point_in_polygen

class Stack(object):
    def __init__(self, centre, mass):
        self.centre = centre
        self.mass = mass

class Box(object):
    def __init__(self, x, y, z, lx, ly, lz, density, virtual=False):
        self.x = x
        self.y = y
        self.z = z
        self.lx = lx
        self.ly = ly
        self.lz = lz

        self.centre = np.array([self.lx + self.x / 2, self.ly + self.y / 2, self.lz + self.z / 2])
        self.vertex_low = np.array([self.lx, self.ly, self.lz])
        self.vertex_high = np.array([self.lx + self.x, self.ly + self.y, self.lz + self.z])
        self.mass = x * y * z * density
        if virtual: self.mass *= 1.0
        self.bottom_edges = []
        self.bottom_whole_contact_area = None

        self.up_edges = {}
        self.up_virtual_edges = {}

        self.thisStack = Stack(self.centre, self.mass)
        self.thisVirtualStack = Stack(self.centre, self.mass)
        self.involved = False


    def calculate_new_com(self, virtual=False):
        new_stack_centre = self.centre * self.mass
        new_stack_mass = self.mass

        for ue in self.up_edges.keys():
            if not ue.involved:
                new_stack_centre += self.up_edges[ue].centre * self.up_edges[ue].mass
                new_stack_mass += self.up_edges[ue].mass

        for ue in self.up_virtual_edges.keys():
            if ue.involved:
                new_stack_centre += self.up_virtual_edges[ue].centre * self.up_virtual_edges[ue].mass
                new_stack_mass += self.up_virtual_edges[ue].mass

        new_stack_centre /= new_stack_mass
        if virtual:
            self.thisVirtualStack.mass = new_stack_mass
            self.thisVirtualStack.centre = new_stack_centre
        else:
            self.thisStack.mass = new_stack_mass
            self.thisStack.centre = new_stack_centre

    def calculated_impact(self):
        if len(self.bottom_edges) == 0:
            return True
        elif not point_in_polygen(self.thisStack.centre[0:2],
                                  self.bottom_whole_contact_area):
            return False
        else:
            if len(self.bottom_edges) == 1:
                stack = self.thisStack
                self.bottom_edges[0].box.up_edges[self] = stack
                self.bottom_edges[0].box.calculate_new_com()
                if not self.bottom_edges[0].box.calculated_impact():
                    return False
            else:
                direct_edge = None
                for e in self.bottom_edges:
                    if self.thisStack.centre[0] > e.area[0] and self.thisStack.centre[0] < e.area[2] \
                            and self.thisStack.centre[1] > e.area[1] and self.thisStack.centre[1] < e.area[3]:
                        direct_edge = e
                        break

                if direct_edge is not None:
                    for edge in self.bottom_edges:
                        if edge == direct_edge:
                            edge.box.up_edges[self] = self.thisStack
                            edge.box.calculate_new_com()
                        else:
                            edge.box.up_edges[self] = Stack(self.thisStack.centre, 0)
                            edge.box.calculate_new_com()

                    for edge in self.bottom_edges:
                        if not edge.box.calculated_impact():
                            return False

                elif len(self.bottom_edges) == 2:
                    com2D = self.thisStack.centre[0:2]

                    tri_base_line = self.bottom_edges[0].centre2D - self.bottom_edges[1].centre2D
                    tri_base_len = np.linalg.norm(tri_base_line)
                    tri_base_line /= tri_base_len ** 2

                    ratio0 = abs(np.dot(com2D - self.bottom_edges[1].centre2D, tri_base_line))
                    ratio1 = abs(np.dot(com2D - self.bottom_edges[0].centre2D, tri_base_line))

                    com0 = np.array([*self.bottom_edges[0].centre2D, self.thisStack.centre[2]])
                    com1 = np.array([*self.bottom_edges[1].centre2D, self.thisStack.centre[2]])

                    stack0 = Stack(com0, self.thisStack.mass * ratio0)
                    stack1 = Stack(com1, self.thisStack.mass * ratio1)

                    self.bottom_edges[0].box.up_edges[self] = stack0
                    self.bottom_edges[0].box.calculate_new_com()

                    self.bottom_edges[1].box.up_edges[self] = stack1
                    self.bottom_edges[1].box.calculate_new_com()

                    if not self.bottom_edges[0].box.calculated_impact():
                        return False
                    if not self.bottom_edges[1].box.calculated_impact():
                        return False

                else:
                    com2D = self.thisStack.centre[0:2]
                    length = len(self.bottom_edges)
                    coefficient = np.zeros((int(length * (length - 1) / 2 + 1), length))
                    value = np.zeros((int(length * (length - 1) / 2 + 1), 1))
                    counter = 0
                    for i in range(length - 1):
                        for j in range(i + 1, length):
                            tri_base_line = self.bottom_edges[i].centre2D - self.bottom_edges[j].centre2D
                            molecular = np.dot(com2D - self.bottom_edges[i].centre2D, tri_base_line)
                            if molecular != 0:
                                ratioI2J = abs(np.dot(com2D - self.bottom_edges[j].centre2D, tri_base_line)) / molecular
                                coefficient[counter, i] = 1
                                coefficient[counter, j] = - ratioI2J
                            counter += 1

                    coefficient[-1, :] = 1
                    value[-1, 0] = 1
                    assgin_ratio = np.linalg.lstsq(coefficient, value, rcond=None)[0]

                    for i in range(length):
                        e = self.bottom_edges[i]
                        newAdded_mass = self.thisStack.mass * assgin_ratio[i][0]
                        newAdded_com = np.array([*e.centre2D, self.thisStack.centre[2]])
                        e.box.up_edges[self] = Stack(newAdded_com, newAdded_mass)
                        e.box.calculate_new_com()

                    for e in self.bottom_edges:
                        if not e.box.calculated_impact():
                            return False
            return True

    def calculated_impact_virtual(self, first=False):
        self.involved = True
        if len(self.bottom_edges) == 0:
            self.involved = False
            return True
        elif not point_in_polygen(self.thisVirtualStack.centre[0:2],
                                  self.bottom_whole_contact_area):
            self.involved = False
            return False
        else:
            if len(self.bottom_edges) == 1:
                stack = self.thisVirtualStack
                self.bottom_edges[0].box.up_virtual_edges[self] = stack
                self.bottom_edges[0].box.calculate_new_com(True)
                if not self.bottom_edges[0].box.calculated_impact_virtual():
                    self.involved = False
                    return False
            else:
                direct_edge = None
                for e in self.bottom_edges:
                    if self.thisVirtualStack.centre[0] > e.area[0] and self.thisVirtualStack.centre[0] < e.area[2] \
                            and self.thisVirtualStack.centre[1] > e.area[1] and self.thisVirtualStack.centre[1] < e.area[3]:
                        direct_edge = e
                        break

                if direct_edge is not None:
                    for edge in self.bottom_edges:
                        if edge == direct_edge:
                            edge.box.up_virtual_edges[self] = self.thisVirtualStack
                            edge.box.calculate_new_com(True)
                        else:
                            edge.box.up_virtual_edges[self] = Stack(self.centre, 0)
                            edge.box.calculate_new_com(True)

                    for edge in self.bottom_edges:
                        if not edge.box.calculated_impact_virtual():
                            self.involved = False
                            return False

                elif len(self.bottom_edges) == 2:
                    com2D = self.thisVirtualStack.centre[0:2]

                    tri_base_line = self.bottom_edges[0].centre2D - self.bottom_edges[1].centre2D
                    tri_base_len = np.linalg.norm(tri_base_line)
                    tri_base_line /= tri_base_len ** 2

                    ratio0 = abs(np.dot(com2D - self.bottom_edges[1].centre2D, tri_base_line))
                    ratio1 = abs(np.dot(com2D - self.bottom_edges[0].centre2D, tri_base_line))

                    com0 = np.array([*self.bottom_edges[0].centre2D, self.thisVirtualStack.centre[2]])
                    com1 = np.array([*self.bottom_edges[1].centre2D, self.thisVirtualStack.centre[2]])

                    stack0 = Stack(com0, self.thisVirtualStack.mass * ratio0)
                    stack1 = Stack(com1, self.thisVirtualStack.mass * ratio1)

                    self.bottom_edges[0].box.up_virtual_edges[self] = stack0
                    self.bottom_edges[0].box.calculate_new_com(True)
                    self.bottom_edges[1].box.up_virtual_edges[self] = stack1
                    self.bottom_edges[1].box.calculate_new_com(True)

                    if not self.bottom_edges[0].box.calculated_impact_virtual() \
                            or not self.bottom_edges[1].box.calculated_impact_virtual():
                        self.involved = False
                        return False

                else:
                    com2D = self.thisVirtualStack.centre[0:2]
                    length = len(self.bottom_edges)
                    coefficient = np.zeros((int(length * (length - 1) / 2 + 1), length))
                    value = np.zeros((int(length * (length - 1) / 2 + 1), 1))
                    counter = 0
                    for i in range(length - 1):
                        for j in range(i + 1, length):
                            tri_base_line = self.bottom_edges[i].centre2D - self.bottom_edges[j].centre2D
                            molecular = np.dot(com2D - self.bottom_edges[i].centre2D, tri_base_line)
                            if molecular != 0:
                                ratioI2J = abs(np.dot(com2D - self.bottom_edges[j].centre2D, tri_base_line)) / molecular
                                coefficient[counter, i] = 1
                                coefficient[counter, j] = -ratioI2J
                            counter += 1

                    coefficient[-1, :] = 1
                    value[-1, 0] = 1
                    x = np.linalg.lstsq(coefficient, value, rcond=None)
                    assgin_ratio = x[0]
                    for i in range(length):
                        e = self.bottom_edges[i]
                        newAdded_mass = self.thisVirtualStack.mass * assgin_ratio[i][0]
                        newAdded_com = np.array([*e.centre2D, self.thisVirtualStack.centre[2]])
                        e.box.up_virtual_edges[self] = Stack(newAdded_com, newAdded_mass)
                        e.box.calculate_new_com(True)

                    for e in self.bottom_edges:
                        if not e.box.calculated_impact_virtual():
                            self.involved = False
                            return False

            if first:
                for e in self.bottom_edges:
                    e.box.up_virtual_edges.pop(self)
            self.involved = False
            return True
