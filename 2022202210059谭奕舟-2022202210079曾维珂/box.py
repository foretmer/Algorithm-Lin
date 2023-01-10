from typing import Union

from dimension import Dimension


class Box(Dimension):
    def __init__(self,w: int=None, d: int=None, h: int=None, typeName = None):
        Dimension.__init__(self, w, d, h)
        self.boxType = typeName
    def __str__(self):
        return f'Box [name={self.boxType}, width={self.width}, depth={self.depth}, ' \
               f'height={self.height}, volume={self.volume}]'
    
    def __repr__(self):
        return self.__str__()

class BoxList:
    count = 0
    def __init__(self, product, typeName = None):
        self.box_items=[]
        if isinstance(product, dict):
            num = product.get('quantity')
            if isinstance(num, int) and num >0 :
                for n in range(num):
                    self.box_items.append(
                        Box(product['width'], product['depth'], product['height'], BoxList.count)
                    )
        BoxList.count += 1

    '''



    def rotate_largest_footprint_3d(self, w_or_dimension: Union[Dimension, int],
                                    d: int=None, h: int=None):
        """Rotate box to largest footprint (downwards area) within a free space.

        :param w_or_dimension: space to fit within,
        :return if this object fits within the input dimensions."""

        if isinstance(w_or_dimension ,Dimension):
            dimension = w_or_dimension
            return self.rotate_largest_footprint_3d(
                dimension.get_width(), dimension.get_depth(), dimension.get_height()
            )
        else:
            w = w_or_dimension

            java_integer_min_value = -2147483648
            a = java_integer_min_value
            if self.height_up(w, d, h):
                a = self.width * self.depth

            b = java_integer_min_value
            if self.width_up(w, d, h):
                b = self.height * self.depth

            c = java_integer_min_value
            if self.depth_up(w, d, h):
                c = self.width * self.height

            if a == java_integer_min_value and b == java_integer_min_value \
                    and c == java_integer_min_value:
                return False

            if a > b and a > c:
                # no rotate
                pass
            elif b > c:
                self.rotate_3d()
            else:
                self.rotate_3d()
                self.rotate_3d()

            if h < self.height:
                raise ValueError(f'Expected height {self.height} to fit within height '
                                 f'constraint {h}')

            if self.width > w or self.depth > d:
                # use the other orientation
                self.rotate_2d()

            if self.width > w or self.depth > d:
                raise ValueError(f'Expected width {self.width} and depth {self.depth} '
                                 f'to fit within constraint width {w} and depth {d}')

            return True

    def height_up(self, w: int, d: int, h: int):

        if h < self.height:
            return False

        return (d >= self.width and w >= self.depth) or (w >= self.width and d >= self.depth)

    def width_up(self, w: int, d: int, h: int):

        if h < self.width:
            return False

        return (d >= self.height and w >= self.depth) or (w >= self.height and d >= self.depth)

    def depth_up(self, w: int, d: int, h: int):

        if h < self.depth:
            return False

        return (d >= self.height and w >= self.width) or (w >= self.height and d >= self.width)

    def fit_rotate_2d(self, w_or_dimension: Union[Dimension, int], d: int=None):
        """Rotate box within a free space in 2D

        :param w_or_dimension: space to fit within,
        :return if this object fits within the input dimension."""

        if isinstance(w_or_dimension, Dimension):
            dimension = w_or_dimension
            return self.fit_rotate_2d(dimension.get_width(), dimension.get_depth())
        else:
            w = w_or_dimension
            if w >= self.width and d >= self.depth:
                return True

            if d >= self.width and w >= self.depth:
                self.rotate_2d()
                return True
            print(w, d, self.width, self.height)
            return False

    def fit_rotate_3d_smallest_footprint(self, w_or_space: Union[Dimension, int],
                                         d: int=None, h: int=None):
        """Rotate box to smallest footprint (downwards area - width*depth) within a free space.

        :param w_or_space: free space
        :return False if box does not fit."""

        if isinstance(w_or_space, Dimension):
            space = w_or_space
            self.fit_rotate_3d_smallest_footprint(space.get_width(), space.get_depth(),
                                                  space.get_height())
        else:
            w = w_or_space

            java_integer_max_value = 2147483647
            a = java_integer_max_value
            if self.height_up(w, d, h):
                a = self.width * self.depth

            b = java_integer_max_value
            if self.width_up(w, d, h):
                b = self.height * self.depth

            c = java_integer_max_value
            if self.depth_up(w, d, h):
                c = self.width * self.height

            if a == java_integer_max_value and b == java_integer_max_value \
                    and c == java_integer_max_value:
                return False

            if a < b and a < c:
                # no rotate
                pass
            elif b < c:
                self.rotate_3d()
            else:
                self.rotate_3d()
                self.rotate_3d()

            if h < self.height:
                raise ValueError(f'Expected height {self.height} to fit height constraint {h}')

            if self.width > w or self.depth > d:
                self.rotate_2d()

            if self.width > w or self.depth > d:
                raise ValueError(f'Expected width {self.width} and depth {self.depth} '
                                 f'to fit constraint width {w} and depth {d}')

            return True

    def current_surface_area(self):
        return self.width * self.depth

    def clone(self):
        return Box(self.name, self.width, self.depth, self.height)

    def rotate_2d(self):
        """Rotate box, i.e. in 2 dimensions, keeping the height constant."""

        self.depth, self.width = self.width, self.depth

        return self

    def rotate_2d_3d(self):
        # rotate2D()
        # width -> depth
        # depth -> width
        #
        # rotate3D()
        # height = width
        # width = depth
        # depth = height
        #
        # so
        # height -> width -> depth
        # width -> depth -> width
        # depth -> height

        self.depth, self.height = self.height, self.depth

        return self
    def rotate_3d(self):
        """Rotate box, i.e. in 3D.

        :return self instance."""

        self.height, self.width, self.depth = self.width, self.depth, self.height
        return self
    '''