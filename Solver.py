import random

from structure import *
import operator
import drawer
from drawer import *


class Solver(object):
    def __init__(self, cargo: Cargo, container: Container, strategy) -> None:
        self.cargos = cargo
        self.container = container
        self.strategy = strategy

    def solve(self):
        # strategy choose
        if self.strategy == 0:
            cargoIndex = -1
            count = 0
            while cargoIndex >= -self.cargos.len:
                # choose point
                self.container.available_points.sort(key=lambda x: x.x)
                self.container.available_points.sort(key=lambda x: x.y)
                self.container.available_points.sort(key=lambda x: x.z)

                # for point in self.container.available_points:
                #     print(point.show)
                # print('\n')
                # sortKey = operator.attrgetter('x')
                # self.container.available_points.sort(key=sortKey, reverse=True)
                m = len(self.container.available_points)
                for i in range(0, m):
                    flag = self.container.place(self.cargos.cargos[cargoIndex], self.container.available_points[i])
                    if flag:
                        # self.container.available_points.sort(key=lambda x: x.x)
                        # self.container.available_points.sort(key=lambda x: x.y)
                        # self.container.available_points.sort(key=lambda x: x.z)
                        # for p in  self.container.available_points:
                        #     print(p.show)
                        # print('/n')
                        cargoIndex += 1
                        break

                cargoIndex -= 1
            # cargoIndex = -1
            # count = 0
            # while cargoIndex >= -self.cargos.len:
            #     # choose point
            #     self.container.available_points.sort(key=lambda x: x.x)
            #     self.container.available_points.sort(key=lambda x: x.y)
            #     self.container.available_points.sort(key=lambda x: x.z)
            #
            #     # for point in self.container.available_points:
            #     #     print(point.show)
            #     # print('\n')
            #     # sortKey = operator.attrgetter('x')
            #     # self.container.available_points.sort(key=sortKey, reverse=True)
            #     m = len(self.container.available_points)
            #     for i in range(0, m):
            #         flag = self.container.place(self.cargos.cargos[cargoIndex], self.container.available_points[i])
            #         if flag:
            #             # self.container.available_points.sort(key=lambda x: x.x)
            #             # self.container.available_points.sort(key=lambda x: x.y)
            #             # self.container.available_points.sort(key=lambda x: x.z)
            #             # for p in  self.container.available_points:
            #             #     print(p.show)
            #             # print('/n')
            #             cargoIndex += 1
            #             break
            #
            #     cargoIndex -= 1

        if self.strategy == 1:
            cargoIndex = -1
            count = 0
            while cargoIndex >= -self.cargos.len:
                print(cargoIndex)
                # choose point
                self.container.available_points.sort(key=lambda x: x.x)
                self.container.available_points.sort(key=lambda x: x.y)
                self.container.available_points.sort(key=lambda x: x.z)

                # for point in self.container.available_points:
                #     print(point.show)
                # print('\n')
                # sortKey = operator.attrgetter('x')
                # self.container.available_points.sort(key=sortKey, reverse=True)
                m = len(self.container.available_points)
                morePointMax = 0
                indexSaver = -1
                pointindex = -1
                for i in range(0, m):
                    success, pointIncrease = self.container.place_test(self.cargos.cargos[cargoIndex],
                                                                                 self.container.available_points[i])
                    if success and pointIncrease > morePointMax:
                        morePointMax = pointIncrease
                        indexSaver = cargoIndex
                        pointindex = i
                if indexSaver != -1 and pointindex != -1:
                    flag = self.container.place(self.cargos.cargos[indexSaver],
                                                self.container.available_points[pointindex])
                    if flag:
                        self.container.available_points.sort(key=lambda x: x.x)
                        self.container.available_points.sort(key=lambda x: x.y)
                        self.container.available_points.sort(key=lambda x: x.z)
                        cargoIndex += 1

                cargoIndex -= 1

        if self.strategy == 2:
            cargoIndex = -1
            count = 0
            chance = True
            while cargoIndex >= -self.cargos.len:
                print(cargoIndex)
                # choose point
                self.container.available_points.sort(key=lambda x: x.x)
                self.container.available_points.sort(key=lambda x: x.y)
                self.container.available_points.sort(key=lambda x: x.z)

                # for point in self.container.available_points:
                #     print(point.show)
                # print('\n')
                # sortKey = operator.attrgetter('x')
                # self.container.available_points.sort(key=sortKey, reverse=True)
                m = len(self.container.available_points)
                maxsocre = 0
                carndex = 0
                posindex = -1
                allflag = True
                # 为每个点计算分数
                for i in range(0, m):
                    addPoint = []
                    socre = 0
                    success, addPoint = self.container.place_test2(self.cargos.cargos[cargoIndex],
                                                                   self.container.available_points[i])
                    if success:
                        allflag = False
                    if addPoint == 0:
                        continue
                    if success:
                        for j in range(len(addPoint)):
                            for k in range(self.cargos.len):
                                success2, morePoint = self.container.place_test(self.cargos.cargos[k],
                                                                               addPoint[j])
                                if success2:
                                    socre += 1
                    if maxsocre < socre:
                        maxsocre = socre
                        carndex = cargoIndex
                        posindex = i
                # print(str(carndex) + ' cargoindex')
                # print(str(posindex) + ' psoindex')

                if carndex != 0 and posindex != -1:
                    print('a')
                    flag = self.container.place(self.cargos.cargos[carndex],
                                                self.container.available_points[posindex])

                    if flag:
                        print('place')

                if allflag or maxsocre == 0:
                    cargoIndex -= 1


        if self.strategy == 3:
            # 在线
            loopflag = True
            chance = 3
            while loopflag:
                cargoIndex = random.randint(0, self.cargos.len - 1)
                while self.cargos.cargos[cargoIndex].number <= 0:
                    cargoIndex = random.randint(0, self.cargos.len - 1)

                # sort point
                self.container.available_points.sort(key=lambda x: x.x)
                self.container.available_points.sort(key=lambda x: x.y)
                self.container.available_points.sort(key=lambda x: x.z)


                m = len(self.container.available_points)
                maxsocre = 0
                carndex = 0
                posindex = -1
                poseindex = -1
                allflag = True
                # 为每个点计算分数
                for i in range(0, m):
                    for j in range(6):
                        self.cargos.cargos[cargoIndex].pose = j
                        success, addPoint = self.container.place_test2(self.cargos.cargos[cargoIndex],
                                                                       self.container.available_points[i])
                        socre = 0
                        if success:
                            allflag = False
                            for jj in range(len(addPoint)):
                                for kk in range(self.cargos.len):
                                    for kkk in range(6):

                                        or_pose = self.cargos.cargos[kk].pose
                                        if or_pose == -1:
                                            or_pose = 0

                                        self.cargos.cargos[kk].pose = kkk
                                        success2, morePoint = self.container.place_test(self.cargos.cargos[kk],
                                                                                        addPoint[jj])
                                        self.cargos.cargos[kk].pose = or_pose
                                        if success2:
                                            socre += 1
                                            # if j == 0 and socre != 0:
                                            #     socre += 20
                        self.cargos.cargos[cargoIndex].pose = j
                        if maxsocre < socre:
                            maxsocre = socre
                            carndex = cargoIndex
                            posindex = i
                            poseindex = j

                if maxsocre == 0:
                    self.cargos.cargos[carndex].pose = poseindex
                    flag = self.container.place(self.cargos.cargos[carndex],
                                                self.container.available_points[posindex])
                    break
                if allflag:
                    if chance >= 0:
                        chance -= 1

                    else:
                        loopflag = False

                else:
                    print(poseindex)
                    self.cargos.cargos[carndex].pose = poseindex
                    print(self.cargos.cargos[carndex].pose)
                    print(self.cargos.cargos[carndex].shape)
                    flag = self.container.place(self.cargos.cargos[carndex],
                                                self.container.available_points[posindex])


