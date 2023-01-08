# length in x-axis; width in y-axis; height in z-axis
class RotationType:
    RT_LWH = 0
    RT_HLW = 1
    RT_HWL = 2
    RT_WHL = 3
    RT_WLH = 4
    RT_LHW = 5

    ALL = [RT_LWH, RT_HLW, RT_HWL, RT_WHL, RT_WLH, RT_LHW]

# (x, y, z) --> (length, width, height)
class Axis:
    LENGTH = 0
    WIDTH = 1
    HEIGHT = 2

    ALL = [LENGTH, WIDTH, HEIGHT]