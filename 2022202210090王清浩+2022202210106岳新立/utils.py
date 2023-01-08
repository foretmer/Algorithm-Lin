import numpy as np

def binary_search(the_array, item, start, end):
    if start == end:
        if the_array[start] > item:
            return start
        else:
            return start + 1
    if start > end:
        return start
    mid = round((start + end) / 2)
    if the_array[mid] < item:
        return binary_search(the_array, item, mid + 1, end)
    elif the_array[mid] > item:
        return binary_search(the_array, item, start, mid - 1)
    else:
        return mid

def maintainEvent(cbox, x_up, y_left, x_bottom, y_right):
    cx_min, cy_min, cx_max, cy_max = cbox

    if cx_min not in x_up:
        index = binary_search(x_up, cx_min, 0, len(x_up) - 1)
        x_up.insert(index, cx_min)

    if cx_max not in x_bottom:
        index = binary_search(x_bottom, cx_max, 0, len(x_bottom) - 1)
        x_bottom.insert(index, cx_max)

    if cy_min not in y_left:
        index = binary_search(y_left, cy_min, 0, len(y_left) - 1)
        y_left.insert(index, cy_min)

    if cy_max not in y_right:
        index = binary_search(y_right, cy_max, 0, len(y_right) - 1)
        y_right.insert(index, cy_max)

def maintainEventBottom(cbox, x_start, y_start, x_end, y_end, plain_size):
    cx_start, cy_start, cx_end, cy_end = cbox

    if cx_end not in x_start and cx_end < plain_size[0]:
        index = binary_search(x_start, cx_end, 0, len(x_start) - 1)
        x_start.insert(index, cx_end)

    if cx_start not in x_end:
        index = binary_search(x_end, cx_start, 0, len(x_end) - 1)
        x_end.insert(index, cx_start)

    if cy_end not in y_start and cy_end < plain_size[1]:
        index = binary_search(y_start, cy_end, 0, len(y_start) - 1)
        y_start.insert(index, cy_end)

    if cy_start not in y_end:
        index = binary_search(y_end, cy_start, 0, len(y_end) - 1)
        y_end.insert(index, cy_start)

def AddNewEMSZ(cbox3d, seleBin):
    cx_min, cy_min, cz_min, cx_max, cy_max, cz_max = cbox3d
    cbox2d = [cx_min, cy_min, cx_max, cy_max]
    if cz_max in seleBin.ZMAP.keys():
        r = seleBin.ZMAP[cz_max]
        maintainEvent(cbox2d, r['x_up'], r['y_left'], r['x_bottom'], r['y_right'])
    else:
        addflags = []
        delflags = []
        seleBin.ZMAP[cz_max] = dict()
        r = seleBin.ZMAP[cz_max]
        r['x_up'] = []
        r['y_left'] = []
        r['x_bottom'] = []
        r['y_right'] = []
        maintainEvent(cbox2d, r['x_up'], r['y_left'], r['x_bottom'], r['y_right'])
        seleBin.serial_number += 1

class Line2D(object):
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
        if self.p2[0] != self.p1[0]:
            self.slope = (self.p2[1] - self.p1[1]) \
                     / (self.p2[0] - self.p1[0])
        else:
            self.slope = (self.p2[1] - self.p1[1]) * np.inf

    def orientation(self,line2):
        slope1 = self.slope
        slope2 = line2.slope

        if abs(slope1) == np.inf and abs(slope2) == np.inf:
            return 0

        diff = slope2-slope1
        if diff > 0:
            return -1
        elif diff == 0:
            return 0
        else:
            return 1

def sortPoints(point_list):
    point_list = sorted(point_list,key = lambda x:x[0])
    return point_list

def ConvexHull(point_list):
    point_list = np.array(point_list).astype(np.float)
    point_list[:,0] += point_list[:,1] * 1e-6
    point_list = point_list.tolist()
    upperHull = []
    lowerHull = []
    sorted_list = sortPoints(point_list)

    for point in sorted_list:
        if len(lowerHull) >= 2:
            line1 = Line2D(lowerHull[len(lowerHull) - 2],
                           lowerHull[len(lowerHull) - 1])
            line2 = Line2D(lowerHull[len(lowerHull) - 1],
                           point)
        while len(lowerHull) >= 2 and line1.orientation(line2) != -1:
            removed = lowerHull.pop()
            if lowerHull[0] == lowerHull[len(lowerHull) - 1]:
                break
            line1 = Line2D(lowerHull[len(lowerHull) - 2],
                           lowerHull[len(lowerHull) - 1])
            line2 = Line2D(lowerHull[len(lowerHull) - 1],
                           point)
        lowerHull.append(point)
    reverse_list = sorted_list[::-1]
    for point in reverse_list:
        if len(upperHull) >= 2:
            line1 = Line2D(upperHull[len(upperHull) - 2],
                           upperHull[len(upperHull) - 1])
            line2 = Line2D(upperHull[len(upperHull) - 1],
                           point)
        while len(upperHull) >= 2 and \
                line1.orientation(line2) != -1:
            removed = upperHull.pop()
            if upperHull[0] == upperHull[len(upperHull) - 1]:
                break
            line1 = Line2D(upperHull[len(upperHull) - 2],
                           upperHull[len(upperHull) - 1])
            line2 = Line2D(upperHull[len(upperHull) - 1],
                           point)
        upperHull.append(point)

    removed = upperHull.pop()
    removed = lowerHull.pop()
    convexHullPoints = lowerHull + upperHull
    convexHullPoints = np.array(convexHullPoints)

    return convexHullPoints

def point_in_polygen(point, coords):
    lat, lon = point
    polysides = len(coords)
    j = polysides - 1
    oddnodes = False

    for i in range(polysides):
        if np.sum(np.cross(coords[i] - point, point - coords[j])) == 0:
            return False

        if (coords[i][1] < lon and coords[j][1] >= lon) or (coords[j][1] < lon and coords[i][1] >= lon):
            if (coords[i][0] + (lon - coords[i][1]) / (coords[j][1] - coords[i][1]) * (coords[j][0] - coords[i][0])) < lat:
                oddnodes = not oddnodes
        j = i

    return oddnodes
