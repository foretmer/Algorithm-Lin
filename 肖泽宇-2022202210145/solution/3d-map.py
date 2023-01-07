"""
3D-map法，将问题空间描述为2+1数组，形如：
{
    3,4,5,6,
    7,8,8,9,
    1,2,3,4
}
第i,j位置的值表示剩余的available的高度。
对新的obj，最佳利用是保证其长与宽所在的方块的高度都相等。这样就不会出现空间空悬。
"""
import time
import json
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--length",type=int,default=1220, required=False)
parser.add_argument("--width", type=int, default=244, required=False)
parser.add_argument("--height", type=int, default=290, required=False)
parser.add_argument("--input_path", type=str, default="../resources/input.json", required=False)
args=parser.parse_args()

LENGTH = args.length
WIDTH = args.width
HEIGHT = args.height
SPACE_V = LENGTH*WIDTH*HEIGHT

INPUT_JSON = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), args.input_path
)


def print_warning(msg):
    print(f"\033[33m{msg}\033[0m")


def timer(func):
    def timed_func(*args):
        start = time.time()
        rst = func(*args)
        end = time.time()
        print(f"{func.__name__} cost {(end-start)*1e3} ms", end="")
        return rst

    return timed_func


class Cube:
    def __init__(self, l, w, h) -> None:
        self._l = l
        self._w = w
        self._h = h
        self._v = l*w*h
        self.position = None

    def __iter__(self):
        yield from [self._l, self._w, self._h]

    def __repr__(self) -> str:
        if self.position is None:
            return f"{type(self).__name__}:{tuple(item*0.01 for item in tuple(self))}"
        else:
            return f"{type(self).__name__}:{tuple(round(item*0.01, 2) for item in tuple(self))} pos:{tuple(round(item*0.01, 2) for item in self.position)}"

    @property
    def length(self):
        return self._l

    @property
    def width(self):
        return self._w

    @property
    def height(self):
        return self._h

    @property
    def v(self):
        return self._v


class Space:
    def __init__(self) -> None:
        self.space = np.ones((LENGTH, WIDTH), dtype=np.int32) * HEIGHT

    @property
    def available(self):
        return np.sum(self.space)

    @property
    def usage_v(self):
        return SPACE_V - self.available

    @timer
    def put_in(self, cube: Cube):
        base_line = max(0, self.usage_v/SPACE_V-0.05)
        begin = int(base_line*LENGTH)
        for l_index in range(begin, LENGTH-cube.length+1):
            for w_index in range(0, WIDTH-cube.width+1):
                space_kernel = self.space[
                l_index : l_index + cube.length, w_index : w_index + cube.width
                ]
                if np.all(space_kernel>=cube.height):
                    space_kernel -= cube.height
                    min_height = np.min(space_kernel)
                    space_kernel = min_height
                    # 标记cube位置
                    cube.position = (l_index, w_index, HEIGHT-(min_height+cube.height))
                    return True
        print_warning(f"obj {cube} can't put in.")
        return False


@timer
def get_objs_from_json(json_path):
    with open(json_path, "r") as file:
        content = json.load(file)
    return np.array(content["input"])


@timer
def main():
    space = Space()
    # objs = np.random.randint(1,200,(5,3))
    objs = get_objs_from_json(INPUT_JSON)
    put_in_cubes = []
    try:
        for index, obj in enumerate(objs):
            cube = Cube(*obj)
            # 当放入时，增加利用了的体积.
            if space.put_in(cube):
                put_in_cubes.append(cube)
            print(f"->{index} in {len(objs)} {index/len(objs)}% space usage: {space.usage_v/SPACE_V}%")
    except KeyboardInterrupt:
        pass
    print(
        f"space usage:{space.usage_v} in {SPACE_V}  {space.usage_v/SPACE_V}%"
    )
    with open(f"{os.path.basename(args.input_path)}_result_pos.txt", "w") as file:
        content = "\n".join([str(cube) for cube in put_in_cubes])
        file.write(content)
    print_warning(f"{args.input_path} handle done.")



if __name__ == "__main__":
    # for _ in range(10):
    main()
