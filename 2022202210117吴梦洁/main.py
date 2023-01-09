import argparse
from packer import *
from painter import *

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='static', help='static or online')
    parser.add_argument('--visualize', default=False, action='store_true',  help='visualize or not')
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    opt = parse_args()

    # Create the new packer
    packer = Packer()

    # Add the bins
    packer.add_truck(Truck("Truck", 587, 233, 220))

    # Add the items
    packer.add_box("Box 1", 108, 76, 30, 40) # E1-1
    packer.add_box("Box 2", 110, 43, 25, 33)
    packer.add_box("Box 3", 92, 81, 55, 39)

    # packer.add_box("Box 1", 108, 76, 30, 24) # E2-1
    # packer.add_box("Box 2", 110, 43, 25, 7)
    # packer.add_box("Box 3", 92, 81, 55, 22)
    # packer.add_box("Box 4", 81, 33, 28, 13)
    # packer.add_box("Box 5", 120, 99, 73, 15)

    # packer.add_box("Box 1", 108, 76, 30, 24) # E3-1
    # packer.add_box("Box 2", 110, 43, 25, 9)
    # packer.add_box("Box 3", 92, 81, 55, 8)
    # packer.add_box("Box 4", 81, 33, 28, 11)
    # packer.add_box("Box 5", 120, 99, 73, 11)
    # packer.add_box("Box 6", 111, 70, 48, 10)
    # packer.add_box("Box 7", 98, 72, 46, 12)
    # packer.add_box("Box 8", 95, 66, 31, 9)

    # packer.add_box("Box 1", 49, 25, 21, 13) # E4-1
    # packer.add_box("Box 2", 60, 51, 41, 9)
    # packer.add_box("Box 3", 103, 76, 64, 11)
    # packer.add_box("Box 4", 95, 70, 62, 14)
    # packer.add_box("Box 5", 111, 49, 26, 13)
    # packer.add_box("Box 6", 85, 84, 72, 16)
    # packer.add_box("Box 7", 48, 36, 31, 12)
    # packer.add_box("Box 8", 86, 76, 38, 11)
    # packer.add_box("Box 9", 71, 48, 47, 16)
    # packer.add_box("Box 10", 90, 43, 33, 8)

    # packer.add_box("Box 1", 98, 73, 44, 6) # E5-1
    # packer.add_box("Box 2", 60, 60, 38, 7)
    # packer.add_box("Box 3", 105, 73, 60, 10)
    # packer.add_box("Box 4", 90, 77, 52, 3)
    # packer.add_box("Box 5", 66, 58, 24, 5)
    # packer.add_box("Box 6", 106, 76, 55, 10)
    # packer.add_box("Box 7", 55, 44, 36, 12)
    # packer.add_box("Box 8", 82, 58, 23, 7)
    # packer.add_box("Box 9", 74, 61, 58, 6)
    # packer.add_box("Box 10", 81, 39, 24, 8)
    # packer.add_box("Box 11", 71, 65, 39, 11)
    # packer.add_box("Box 12", 105, 97, 47, 4)
    # packer.add_box("Box 13", 114, 97, 69, 5)
    # packer.add_box("Box 14", 103, 78, 55, 6)
    # packer.add_box("Box 15", 93, 66, 55, 6)

    # Pack the items into de bins
    packer.pack(mode=opt.mode) # mode: static or online

    # visualization
    if opt.visualize:
        truck = packer.trucks[0]
        painter = Painter(truck)
        painter.plotBoxAndItems()
