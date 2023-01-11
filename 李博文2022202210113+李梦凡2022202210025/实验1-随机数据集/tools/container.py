import numpy as np

class Container:
    def __init__(self, l=1500, w=250, h=250):
        self.l = l
        self.w = w
        self.h = h
        self.surface = np.ones((l, w))*h
        self.lastBoxI = 0
        self.lastBoxII = 0
        self.lastBoxJ = 0
        self.lastBoxJJ = 0

    # def caculateLoss(self, li, lii, wj, wjj, h)

    def getRemainingCapacity(self):
        return np.sum(self.surface)

    def updateSurface(self,li, lii, wj, wjj, curCapacity, boxH):
        self.surface[li:lii, wj:wjj] = curCapacity - boxH

    def getTotalCapacity(self):
        return self.l*self.w*self.h

    def putBox_Base(self, box):
        # [boxL, boxW] = box.getMaxSurface() # boxW是最长边
        # boxH = box.getMinH()
        [boxL, boxW] = box.getMinSurface()
        boxH = box.getMaxH()
        for j in range(0, self.w - boxW + 1):
            for i in range(0, self.l- boxL + 1):
                if np.all(self.surface[i: i+boxL, j: j+boxW]>=boxH):
                    curCapacity = np.min(self.surface[i: i+boxL, j: j+boxW])
                    self.updateSurface(i, boxL+i, j, j+boxW, curCapacity, boxH)
                    print('当前盒子放在', i, boxL+i, j, j+boxW)
                    return True


    def putBox_Advance(self, box):
        # 动态算法找最小面作为底面
        [boxL, boxW] = box.getMinSurface()
        boxH = box.getMaxH()
        # 用当前集装箱已用空间比值确定i的遍历起始点
        if box.getVolumn() < 200000:
            base_line = 0
            begin = int(base_line * self.l)
            for i in range(begin, self.l - boxL + 1, 1):
                for j in range(self.w - boxW + 1, -1, -1):
                    curCapacity = np.min(self.surface[i: i + boxL, j: j + boxW])
                    if i + boxL <= self.l and j + boxW <= self.w and curCapacity >= boxH:
                        self.updateSurface(i, boxL + i, j, j + boxW, curCapacity, boxH)
                        print('当前盒子放在', i, boxL + i, j, j + boxW)
                        return True
        else:
            base_line = max(0, (self.getTotalCapacity()-self.getRemainingCapacity())/self.getTotalCapacity()-0.05)
            begin = int(base_line * self.l)
            for i in range(begin, self.l - boxL + 1, 1):
                for j in range(0, self.w - boxW + 1, 1):
                    curCapacity = np.min(self.surface[i: i + boxL, j: j + boxW])
                    if i + boxL <= self.l and j + boxW <= self.w and curCapacity >= boxH:
                        self.updateSurface(i, boxL + i, j, j + boxW, curCapacity, boxH)
                        print('当前盒子放在', i, boxL + i, j, j + boxW)
                        return True
