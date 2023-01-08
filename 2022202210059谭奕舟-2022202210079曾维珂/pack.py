from typing import Union
from coordinate import Coordinate
from dimension import Dimension
from space_holder import Holder
from box import Box
from container import Container

from matplotlib import pyplot as plt
from drawCube import *

# the Packer is the base class of packer algorithm to be inherited
class Packer:
    def __init__(self, container: Container):
        self.container = container
        self.scheme = None
    # param: boxLists --the boxes to be packed in
    # return a scheme
    def pack(self, boxLists):
        self.scheme = self.get_scheme(boxLists)
        return self.scheme
    
    def get_scheme(self, boxes):
        raise NotImplementedError

