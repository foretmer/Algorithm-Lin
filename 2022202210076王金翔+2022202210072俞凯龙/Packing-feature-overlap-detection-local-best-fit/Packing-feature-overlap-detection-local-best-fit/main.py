# This is a sample Python script.

from Container import Container
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from box.BoxManager import BoxManager

total_boxes = []
# E1-5
manager = BoxManager(). \
    add_box_type(l=78, w=37, h=27, n=63). \
    add_box_type(l=89, w=70, h=25, n=52). \
    add_box_type(l=90, w=84, h=41, n=55)

# E2-3
# manager = BoxManager(). \
#     add_box_type(l=88, w=54, h=39, n=25). \
#     add_box_type(l=94, w=54, h=36, n=27). \
#     add_box_type(l=87, w=77, h=43, n=21). \
#     add_box_type(l=100, w=80, h=72, n=20). \
#     add_box_type(l=83, w=40, h=36, n=24)

# E4-3
# manager = BoxManager(). \
#     add_box_type(l=86, w=84, h=45, n=18). \
#     add_box_type(l=81, w=45, h=34, n=19). \
#     add_box_type(l=70, w=50, h=37, n=13). \
#     add_box_type(l=71, w=61, h=52, n=16). \
#     add_box_type(l=78, w=73, h=40, n=10). \
#     add_box_type(l=69, w=63, h=46, n=13). \
#     add_box_type(l=72, w=67, h=56, n=10). \
#     add_box_type(l=75, w=75, h=36, n=8). \
#     add_box_type(l=94, w=88, h=50, n=12). \
#     add_box_type(l=65, w=51, h=50, n=13)

container = Container(l=587, w=233, h=220)
while (not container.is_full) and (not manager.is_out_of_box):
    box = manager.get_box()
    if box is not None:
        point = container.add_box_if_available(box)
        # if not point.is_valid:
        #     manager.remove_box_type(box.type_id)
        #     if manager.is_repository_empty():
        #         container.is_full = True
        #         container.end()
    else:
        container.end()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
