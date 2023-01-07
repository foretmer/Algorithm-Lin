import random as rd
from typing import List

import numpy as np
from nptyping import NDArray, Int, Shape


def boxes_generator(
        bin_size: List[int], num_items: int = 64, seed: int = 42
) -> List[List[int]]:
    rd.seed(seed)
    np.random.seed(seed)
    dim = len(bin_size)
    item_sizes = []
    x, y, z = bin_size[0], bin_size[1], bin_size[2]
    items_x = np.random.randint(1, x, num_items)
    items_y = np.random.randint(1, y, num_items)
    items_z = np.random.randint(1, z, num_items)
    for i in range(0, num_items):
        item_sizes.append([items_x[i], items_y[i], items_x[i]])

    return item_sizes


def generate_vertices(
        cuboid_len_edges: NDArray, cuboid_position: NDArray
) -> NDArray[Shape["3, 8"], Int]:
    v0 = cuboid_position
    v0 = np.asarray(v0, dtype=np.int32)
    v1 = v0 + np.asarray([cuboid_len_edges[0], 0, 0], dtype=np.int32)
    v2 = v0 + np.asarray([0, cuboid_len_edges[1], 0], dtype=np.int32)
    v3 = v0 + np.asarray([cuboid_len_edges[0], cuboid_len_edges[1], 0], dtype=np.int32)
    v4 = v0 + np.asarray([0, 0, cuboid_len_edges[2]], dtype=np.int32)
    v5 = v1 + np.asarray([0, 0, cuboid_len_edges[2]], dtype=np.int32)
    v6 = v2 + np.asarray([0, 0, cuboid_len_edges[2]], dtype=np.int32)
    v7 = v3 + np.asarray([0, 0, cuboid_len_edges[2]], dtype=np.int32)
    vertices = np.vstack((v0, v1, v2, v3, v4, v5, v6, v7))
    return vertices


def interval_intersection(a: List[int], b: List[int]) -> bool:
    assert a[1] > a[0], "a[1] must be greater than a[0]"
    assert b[1] > b[0], "b[1] must be greater than b[0]"
    return min(a[1], b[1]) - max(a[0], b[0]) > 0


def cuboids_intersection(cuboid_a: List[int], cuboid_b: List[int]) -> bool:
    assert len(cuboid_a) == 6, "cuboid_a must be a list of length 6"
    assert len(cuboid_b) == 6, "cuboid_b must be a list of length 6"

    assert np.all(
        np.less_equal([0, 0, 0], cuboid_a[:3])
    ), "cuboid_a must have nonnegative coordinates"
    assert np.all(
        np.less_equal([0, 0, 0], cuboid_b[:3])
    ), "cuboid_b must have nonnegative coordinates"

    assert np.all(
        np.less(cuboid_a[:3], cuboid_a[3:])
    ), "cuboid_a must have nonzero volume"

    assert np.all(
        np.less(cuboid_b[:3], cuboid_b[3:])
    ), "cuboid_b must have nonzero volume"

    inter = [
        interval_intersection([cuboid_a[0], cuboid_a[3]], [cuboid_b[0], cuboid_b[3]]),
        interval_intersection([cuboid_a[1], cuboid_a[4]], [cuboid_b[1], cuboid_b[4]]),
        interval_intersection([cuboid_a[2], cuboid_a[5]], [cuboid_b[2], cuboid_b[5]]),
    ]

    return np.all(inter)


def cuboid_fits(cuboid_a: List[int], cuboid_b: List[int]) -> bool:
    assert len(cuboid_a) == 6, "cuboid_a must be a list of length 3"
    assert len(cuboid_b) == 6, "cuboid_b must be a list of length 3"

    assert len(cuboid_a) == 6, "cuboid_a must be a list of length 6"
    assert len(cuboid_b) == 6, "cuboid_b must be a list of length 6"

    assert np.all(
        np.less_equal([0, 0, 0], cuboid_a[:3])
    ), "cuboid_a must have nonnegative coordinates"
    assert np.all(
        np.less_equal([0, 0, 0], cuboid_b[:3])
    ), "cuboid_b must have nonnegative coordinates"

    assert np.all(
        np.less(cuboid_a[:3], cuboid_a[3:])
    ), "cuboid_a must have nonzero volume"

    assert np.all(
        np.less(cuboid_b[:3], cuboid_b[3:])
    ), "cuboid_b must have nonzero volume"

    return np.all(np.less_equal(cuboid_a[:3], cuboid_b[:3])) and np.all(
        np.less_equal(cuboid_b[3:], cuboid_a[3:])
    )
