
class Coordinate:
    def __init__(self,x: int=None, y: int=None, z: int=None):
        self.x = x
        self.y = y
        self.z = z

    def getCoordinateTuple(self):
        return (self.x, self.y, self.z)
        
    def getCoordinate(self):
        return self
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z
    
    @staticmethod
    def cmp_coordinate(a, b):
        '''
        if b < a:
            return -1
        if a < b:
            return 1
        return 0
        '''
        if b.y < a.y:
            return -1
        if b.y > a.y:
            return 1
        if b.x < a.x:
            return -1
        if b.x > a.x:
            return 1
        if b.z < a.z:
            return -1
        if b.z >a.z:
            return 1
        return 0