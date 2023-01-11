from decimal import Decimal

class RotationType:
    LWH = 0
    WHL = 1
    WLH = 2
    HLW = 3
    HWL = 4
    LHW = 5

    ALL = [LWH, WHL, WLH, HLW, HWL, LHW]



class Axis:
    LENGTH = 0
    WIDTH = 1
    HEIGHT = 2

    ALL = [LENGTH, WIDTH, HEIGHT]



def rect_intersect(item1, item2, x, y):
    d1 = item1.get_size()
    d2 = item2.get_size()

    cx1 = item1.position[x] + d1[x]/2
    cy1 = item1.position[y] + d1[y]/2
    cx2 = item2.position[x] + d2[x]/2
    cy2 = item2.position[y] + d2[y]/2

    ix = max(cx1, cx2) - min(cx1, cx2)
    iy = max(cy1, cy2) - min(cy1, cy2)

    return ix < (d1[x]+d2[x])/2 and iy < (d1[y]+d2[y])/2


def intersect(item1, item2):
    return (
        rect_intersect(item1, item2, Axis.LENGTH, Axis.WIDTH)
        and rect_intersect(item1, item2, Axis.WIDTH, Axis.HEIGHT)
        and rect_intersect(item1, item2, Axis.LENGTH, Axis.HEIGHT)
    )


def get_limit_number_of_decimals(decimals):
    return Decimal('1.{}'.format('0' * decimals))


def set_to_decimal(value, number_of_decimals):
    number_of_decimals = get_limit_number_of_decimals(number_of_decimals)

    return Decimal(value).quantize(number_of_decimals)