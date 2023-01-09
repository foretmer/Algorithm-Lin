from decimal import Decimal
from constants import Axis

DEFAULT_NUMBER_OF_DECIMALS = 2
START_POSITION = [0, 0, 0]

def get_limit_number_of_decimals(number_of_decimals):
    return Decimal('1.{}'.format('0' * number_of_decimals))

def set_to_decimal(value, number_of_decimals):
    number_of_decimals = get_limit_number_of_decimals(number_of_decimals)

    return Decimal(value).quantize(number_of_decimals)


def rect_intersect(box1, box2, x, y):
    """Estimate whether two boxs get intersection in one dimension.
    Args:
        box1, box2: any two boxs in item list.
        x,y: Axis.LENGTH/ Axis.Height/ Axis.WIDTH.
    Returns:
        Boolean variable: True when two boxs get intersection in one dimension; False when two boxs do not intersect in one dimension.
    """

    d1 = box1.get_dimension()
    d2 = box2.get_dimension()

    cx1 = box1.position[x] + d1[x] / 2
    cy1 = box1.position[y] + d1[y] / 2
    cx2 = box2.position[x] + d2[x] / 2
    cy2 = box2.position[y] + d2[y] / 2

    ix = max(cx1, cx2) - min(cx1, cx2)  # ix: |cx1-cx2|
    iy = max(cy1, cy2) - min(cy1, cy2)  # iy: |cy1-cy2|

    return ix < (d1[x] + d2[x]) / 2 and iy < (d1[y] + d2[y]) / 2


def intersect(box1, box2):
    """Estimate whether two items get intersection in 3D dimension.
    Args:
        item1, item2: any two items in item list.
    Returns:
        Boolean variable: True when two items get intersection; False when two items do not intersect.
    """

    return (
            rect_intersect(box1, box2, Axis.LENGTH, Axis.HEIGHT) and  # xz dimension
            rect_intersect(box1, box2, Axis.HEIGHT, Axis.WIDTH) and  # yz dimension
            rect_intersect(box1, box2, Axis.LENGTH, Axis.WIDTH))  # xy dimension


def support(box1, box2):
    """Estimate whether box1 supports box2.
        Args:
            box1, box2: any two boxes in box list.
        Returns:
            Boolean variable: False when box1 doesn't supports box2; True when box1 supports box2.
        """
    if box1.position[2] + box1.get_dimension()[2] == box2.position[2]:
        if rect_intersect(box1, box2, Axis.LENGTH, Axis.WIDTH):
            return True
    return False
