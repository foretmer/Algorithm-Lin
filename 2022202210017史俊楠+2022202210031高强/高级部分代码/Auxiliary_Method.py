from decimal import Decimal
from constant import Axis
from item import Item

DEFAULT_NUMBER_OF_DECIMALS = 2
START_POSITION = [0, 0, 0]

# get the number of decimal places
def get_limit_number_of_decimals(number_of_decimals):
    return Decimal('1.{}'.format('0' * number_of_decimals))

# set the number to special decimal places
def set_to_decimal(value, number_of_decimals):
    number_of_decimals = get_limit_number_of_decimals(number_of_decimals)
    return Decimal(value).quantize(number_of_decimals)


def rect_intersect(item1, item2, x, y):
    """Estimate whether two items get intersection in one dimension.
    Args:
        item1, item2: any two items in item list.
        x,y: Axis.LENGTH/ Axis.Height/ Axis.WIDTH.
    Returns:
        Boolean variable: False when two items get intersection in one dimension; True when two items do not intersect in one dimension.
    """

    d1 = item1.get_dimension()
    d2 = item2.get_dimension()

    cx1 = item1.position[x] + d1[x] / 2
    cy1 = item1.position[y] + d1[y] / 2
    cx2 = item2.position[x] + d2[x] / 2
    cy2 = item2.position[y] + d2[y] / 2

    ix = max(cx1, cx2) - min(cx1, cx2)  # ix: |cx1-cx2|
    iy = max(cy1, cy2) - min(cy1, cy2)  # iy: |cy1-cy2|

    return ix < (d1[x] + d2[x]) / 2 and iy < (d1[y] + d2[y]) / 2


def intersect(item1, item2):
    """Estimate whether two items get intersection in 3D dimension.
    Args:
        item1, item2: any two items in item list.
    Returns:
        Boolean variable: False when two items get intersection; True when two items do not intersect.
    """

    return (
            rect_intersect(item1, item2, Axis.LENGTH, Axis.HEIGHT) and  # xz dimension
            rect_intersect(item1, item2, Axis.HEIGHT, Axis.WIDTH) and  # yz dimension
            rect_intersect(item1, item2, Axis.LENGTH, Axis.WIDTH))  # xy dimension


def stack(item1, item2):
    """Stack two items with same length, width, height or any two of three sides are same.
    Args:
        item1, item2: any two items in item list.
    Return:
        item1/ stacked_item_list/ stacked_item.
    """

    if (
            item1.length == item2.length and
            item1.width == item2.width and
            item1.height == item2.height
    ):
        stacked_item_1 = Item(item1.name + item2.name, item1.length + item2.length,
                              item1.width, item1.height, item1.weight + item2.weight)  # (2l, w, h)
        stacked_item_2 = Item(item1.name + item2.name, item1.length, item1.width + item2.width,
                              item1.height, item1.weight + item2.weight)  # (l, 2w, h)
        stacked_item_3 = Item(item1.name + item2.name, item1.length, item1.width,
                              item1.height + item2.height, item1.weight + item2.weight)  # (l, w, 2h)

        stacked_item_list = [stacked_item_1, stacked_item_2, stacked_item_3]

        return stacked_item_list

    elif (
            item1.length == item2.length and
            item1.width == item2.width and
            item1.height != item2.height
    ):
        stacked_item = Item(item1.name + item2.name, item1.length, item1.width,
                            item1.height + item2.height, item1.weight + item2.weight)  # (l, w, 2h)

        return stacked_item

    elif (
            item1.length == item2.length and
            item1.height == item2.height and
            item1.width != item2.width
    ):
        stacked_item = Item(item1.name + item2.name, item1.length, item1.width + item2.width,
                            item1.height, item1.weight + item2.weight)  # (l, 2w, h)

        return stacked_item

    elif (
            item1.width == item2.width and
            item1.height == item2.height and
            item1.length != item2.length
    ):
        stacked_item = Item(item1.name + item2.name, item1.length + item2.length,
                            item1.width, item1.height, item1.weight + item2.weight)

        return stacked_item  # (2l, w, h)

    else:
        return item1