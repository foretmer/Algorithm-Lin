from typing import Union
from coordinate import Coordinate
from dimension import Dimension
from space_holder import Holder
from box import Box

class Container(Dimension,Coordinate):
    def __init__(self,w: int=None, d: int=None, h: int=None, x: int=None, y: int=None, z: int=None):
        Dimension.__init__(self, w, d, h)
        Coordinate.__init__(self, x, y, z)
    @staticmethod
    def merge(old_container, new_container):
        if old_container.x == new_container.x and  old_container.y == new_container.y and old_container.z != new_container.z:
            old_container.z = (old_container.z if (old_container.z<new_container.z) else new_container.z)
            old_container.depth = (old_container.depth if (old_container.depth<new_container.depth) else new_container.depth)
            old_container.width = (old_container.width if (old_container.width<new_container.width) else new_container.width)
            old_container.height = (old_container.height if (old_container.height<new_container.height) else new_container.height)
        
        elif (old_container.x == new_container.x and  old_container.z == new_container.z and old_container.width==new_container.width):
            old_container.y = (old_container.y if (old_container.y<new_container.y) else new_container.y)
            old_container.height = (old_container.height if (old_container.height<new_container.height) else new_container.height)
            old_container.depth = old_container.depth + new_container.depth
            old_container.width = new_container.width
        
        elif (old_container.z == new_container.z and  old_container.y == new_container.y and old_container.depth==new_container.depth):
            old_container.x = (old_container.x if (old_container.x<new_container.x) else new_container.x)
            old_container.height = (old_container.height if (old_container.height<new_container.height) else new_container.height)
            old_container.width = old_container.width+new_container.width
            old_container.depth = new_container.depth
        else:
            return False
        return True

    def fit(self, box: Box):
        holderList = []
        if self.height < box.height :
            return holderList
        if self.width >= box.width and self.depth >= box.depth :
            holderList.append(Holder(self, box, 0))
        if self.width >= box.depth and self.depth >= box.height :
            holderList.append(Holder(self, box, 1))
        return holderList
    def fit_orientation(self, box: Box, orientation: int):
        if self.height < box.height :
            return None
        if orientation == 0 and self.width >= box.width and self.depth >= box.depth :
            return Holder(self, box, 0)
        if orientation == 1 and self.width >= box.depth and self.depth >= box.width :
            return Holder(self, box, 1)
        return None
    def fit_holder(self, holder: Holder):
        free_space = []
        if self.height < holder.get_height() :
            return free_space
        if self.width >= holder.get_width() and self.depth >=holder.get_depth() :
            return free_space
        return self.get_free_space(holder)
    def get_free_space(self, holder: Holder):
        free_space = []
        topContainer = Container(holder.get_width(), holder.get_depth(), self.height - holder.get_height(), self.x, self.y, self.z+holder.get_height())
        leftContainer = Container(self.width - holder.get_width(), holder.get_depth(), self.height, self.x + holder.get_width(), self.y, self.z)
        frontContainer = Container(self.width, self.depth - holder.get_depth(), self.height, self.x, self.y + holder.get_depth(), self.z)
        if not topContainer.is_empty():
            free_space.append(topContainer)
        if not leftContainer.is_empty():
            free_space.append(leftContainer)
        if not frontContainer.is_empty():
            free_space.append(frontContainer)
        return  free_space

