class Box:
    def __init__(self, x, y, z):
        self.l = x
        self.w = y
        self.h = z
        self.sortList = sorted([self.l, self.w, self.h])

    def getVolumn(self):
        return self.l * self.w * self.h

    def getMaxSurface(self):
        return self.sortList[1:3]
    def getMinH(self):
        return self.sortList[0]

    def getMinSurface(self):
        return self.sortList[0:2]
    def getMaxH(self):
        return self.sortList[-1]



    def __str__(self):
        return 'l: ' + str(self.l) +' w: ' + str(self.w) + ' h: '+ str(self.h)