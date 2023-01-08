import numpy as np
import json
import os

# 生成随机货物
NUMS = int(4000)
MIN_SIZE = 8
MAX_SIZE = 53


def random_input():
    objs = np.random.randint(MIN_SIZE, MAX_SIZE + 1, (NUMS, 3))
    data_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../resources/input.json"
    )
    with open(data_path, "w") as file:
        dic = {"input": objs.tolist()}
        json.dump(dic, file, indent=4)


if __name__ == "__main__":
    random_input()
