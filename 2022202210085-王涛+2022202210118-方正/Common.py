import os
import random
from enum import Enum

random.seed(1)

class Axis(Enum):
    LENGTH = 0
    WIDTH = 1
    HEIGHT = 2

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    class UnknownAxis(Exception):
        def __init__(self):
            super().__init__()

    class InvalidAxis(Exception):
        def __init__(self):
            super().__init__()

class Method(Enum):
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

class OfflineSearchMethod(Method):
    NONE = 0
    CANDIDATE_POINTS = 1

    class UnknownSearchMethod(Exception):
        ...
    
class OnlineSearchMethod(Method):
    NONE = 0
    BRUTE = 1
    GREEDY = 2
    CANDIDATE_POINTS = 3
    SUB_SPACE = 4

    class UnknownSearchMethod(Exception):
        ...

class PointAddMethod(Method):
    NONE = 0
    AXIS = 1
    SURROUND = 2
    ENVELOPE = 3
    ALL = 4

    class UnknownAddMethod(Exception):
        ...

class PointSortMethod(Method):
    NONE = 0
    AXIS = 1
    SUM_MIN = 2
    PORTION_MIN = 3

    class UnknownSortMethod(Exception):
        ...

class BinSortMethod(Method):
    NONE = 0
    VOLUMN_MIN = 1
    VOLUMN_MAX = 2
    PORTION_SIMILAR = 3
    APPROXIMATE_MAX = 4

    class UnknownSortMethod(Exception):
        ...

PRECISION = 0 # =10^x

PROJECT_ROOT = os.path.split(os.path.realpath(__file__))[0]

LOG_DIR = os.path.abspath(os.path.join(PROJECT_ROOT,"Logs"))