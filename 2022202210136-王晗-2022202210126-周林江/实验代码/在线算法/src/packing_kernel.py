from copy import deepcopy
from typing import List, Type

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from nptyping import NDArray, Int, Shape

from src.utils import (
    generate_vertices,
    boxes_generator,
    cuboids_intersection,
    cuboid_fits,
)


class Box:

    def __init__(self, size: List[int], position: List[int], id_: int) -> None:

        assert len(size) == len(
            position
        ), "Lengths of box size and position do not match"
        assert len(size) == 3, "Box size must be a list of 3 integers"

        assert (
                size[0] > 0 and size[1] > 0 and size[2] > 0
        ), "Lengths of edges must be positive"
        assert (position[0] == -1 and position[1] == -1 and position[2] == -1) or (
                position[0] >= 0 and position[1] >= 0 and position[2] >= 0
        ), "Position is not valid"

        self.id_ = id_
        self.position = np.asarray(position)
        self.size = np.asarray(size)

    @property
    def area_bottom(self) -> int:

        return self.size[0] * self.size[1]

    @property
    def volume(self) -> int:

        return self.size[0] * self.size[1] * self.size[2]

    @property
    def vertices(self) -> NDArray:

        vert = generate_vertices(self.size, self.position)
        return np.asarray(vert, dtype=np.int32)

    def __repr__(self):
        return (
            f"Box id: {self.id_}, Size: {self.size[0]} x {self.size[1]} x {self.size[2]}, "
            f"Position: ({self.position[0]}, {self.position[1]}, {self.position[2]})"
        )

    def plot(self, color, figure: Type[go.Figure] = None) -> Type[go.Figure]:

        vertices = generate_vertices(self.size, self.position).T
        x, y, z = vertices[0, :], vertices[1, :], vertices[2, :]

        i = [1, 2, 5, 6, 1, 4, 3, 6, 1, 7, 0, 6]
        j = [0, 3, 4, 7, 0, 5, 2, 7, 3, 5, 2, 4]
        k = [2, 1, 6, 5, 4, 1, 6, 3, 7, 1, 6, 0]

        edge_pairs = [
            (0, 1),
            (0, 2),
            (0, 4),
            (1, 3),
            (1, 5),
            (2, 3),
            (2, 6),
            (3, 7),
            (4, 5),
            (4, 6),
            (5, 7),
            (6, 7),
        ]
        for (m, n) in edge_pairs:
            vert_x = np.array([x[m], x[n]])
            vert_y = np.array([y[m], y[n]])
            vert_z = np.array([z[m], z[n]])

        if figure is None:

            figure = go.Figure(
                data=[
                    go.Mesh3d(
                        x=x,
                        y=y,
                        z=z,
                        i=i,
                        j=j,
                        k=k,
                        opacity=1,
                        color=color,
                        flatshading=True,
                    )
                ]
            )

            figure.add_trace(
                go.Scatter3d(
                    x=vert_x,
                    y=vert_y,
                    z=vert_z,
                    mode="lines",
                    line=dict(color="black", width=0),
                )
            )

        else:

            figure.add_trace(
                go.Mesh3d(
                    x=x,
                    y=y,
                    z=z,
                    i=i,
                    j=j,
                    k=k,
                    opacity=1,
                    color=color,
                    flatshading=True,
                )
            )

            figure.add_trace(
                go.Scatter3d(
                    x=vert_x,
                    y=vert_y,
                    z=vert_z,
                    mode="lines",
                    line=dict(color="black", width=0),
                )
            )

        return figure


class Container:

    def __init__(
            self,
            size: NDArray[Shape["1,3"], Int],
            position: NDArray[Shape["1,3"], Int] = None,
            id_: int = 0,
    ) -> None:

        if position is None:
            position = np.zeros(shape=3, dtype=np.int32)

        assert len(size) == len(
            position), "Sizes of size and position do not match"
        assert len(size) == 3, "Size of size is different from 3"
        position = np.asarray(position)
        np.testing.assert_equal(position[2], 0), "Position is not valid"

        self.id_ = id_
        self.position = np.asarray(position, dtype=np.int32)
        self.size = np.asarray(size, dtype=np.int32)
        self.boxes = []
        self.height_map = np.zeros(shape=(size[0], size[1]), dtype=np.int32)

    @property
    def vertices(self):

        return generate_vertices(self.size, self.position)

    def reset(self):

        self.boxes = []
        self.height_map = np.zeros(
            shape=[self.size[0], self.size[1]], dtype=np.int32)

    def _update_height_map(self, box):

        self.height_map[
        box.position[0]: box.position[0] + box.size[0],
        box.position[1]: box.position[1] + box.size[1],
        ] += box.size[2]

    def __repr__(self):
        return (
            f"Container id: {self.id_}, Size: {self.size[0]} x {self.size[1]} x {self.size[2]}, "
            f"Position: ({self.position[0]}, {self.position[1]}, {self.position[2]})"
        )

    def get_height_map(self):

        return deepcopy(self.height_map)

    def check_valid_box_placement(
            self, box: Box, new_pos: NDArray, check_area: int = 100
    ) -> int:

        assert len(new_pos) == 2

        v = generate_vertices(np.asarray(box.size), np.asarray([*new_pos, 1]))

        v0, v1, v2, v3 = v[0, :], v[1, :], v[2, :], v[3, :]

        w = generate_vertices(self.size, self.position)

        w0, w1, w2, w3 = w[0, :], w[1, :], w[2, :], w[3, :]

        cond_0 = np.all(np.logical_and(v0[0:2] >= w0[0:2], v0[0:2] <= w3[0:2]))
        cond_1 = np.all(np.logical_and(v1[0:2] >= w0[0:2], v1[0:2] <= w3[0:2]))
        cond_2 = np.all(np.logical_and(v2[0:2] >= w0[0:2], v2[0:2] <= w3[0:2]))
        cond_3 = np.all(np.logical_and(v3[0:2] >= w0[0:2], v3[0:2] <= w3[0:2]))

        if not np.all([cond_0, cond_1, cond_2, cond_3]):
            return 0

        corners_levels = [
            self.height_map[v0[0], v0[1]],
            self.height_map[v1[0] - 1, v1[1]],
            self.height_map[v2[0], v2[1] - 1],
            self.height_map[v3[0] - 1, v3[1] - 1],
        ]

        if corners_levels.count(corners_levels[0]) != len(corners_levels):
            return 0

        lev = corners_levels[0]

        bottom_face_lev = self.height_map[
                          v0[0]: v0[0] + box.size[0], v0[1]: v0[1] + box.size[1]
                          ]

        if not np.array_equal(lev, np.amax(bottom_face_lev)):
            return 0

        count_level = np.count_nonzero(bottom_face_lev == lev)

        support_perc = int((count_level / (box.size[0] * box.size[1])) * 100)
        if support_perc < check_area:
            return 0

        dummy_box = deepcopy(box)
        dummy_box.position = [*new_pos, lev]

        dummy_box_min_max = [
            dummy_box.position[0],
            dummy_box.position[1],
            dummy_box.position[2],
            dummy_box.position[0] + dummy_box.size[0],
            dummy_box.position[1] + dummy_box.size[1],
            dummy_box.position[2] + dummy_box.size[2],
        ]

        container_min_max = [
            self.position[0],
            self.position[1],
            self.position[2],
            self.position[0] + self.size[0],
            self.position[1] + self.size[1],
            self.position[2] + self.size[2],
        ]

        if not cuboid_fits(container_min_max, dummy_box_min_max):
            return 0

        for other_box in self.boxes:
            if other_box.id_ == dummy_box.id_:
                continue
            other_box_min_max = [
                other_box.position[0],
                other_box.position[1],
                other_box.position[2],
                other_box.position[0] + other_box.size[0],
                other_box.position[1] + other_box.size[1],
                other_box.position[2] + other_box.size[2],
            ]

            if cuboids_intersection(dummy_box_min_max, other_box_min_max):
                return 0

        return 1

    def action_mask(
            self, box: Box, check_area: int = 100
    ) -> NDArray[Shape["*, *"], Int]:

        action_mask = np.zeros(
            shape=[self.size[0], self.size[1]], dtype=np.int8)

        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                if (
                        self.check_valid_box_placement(
                            box, np.array([i, j], dtype=np.int32), check_area
                        )
                        == 1
                ):
                    action_mask[i, j] = 1
        return action_mask

    def place_box(self, box: Box, new_position: List[int], check_area=100) -> None:

        assert (
                self.check_valid_box_placement(box, new_position, check_area) == 1
        ), "Invalid position for box"

        height = self.height_map[new_position[0], new_position[1]]

        box.position = np.asarray([*new_position, height], dtype=np.int32)

        self.boxes.append(box)

        self._update_height_map(box)

    def plot(self, figure: Type[go.Figure] = None) -> Type[go.Figure]:

        if figure is None:
            figure = go.Figure()

        vertices = generate_vertices(self.size, self.position).T
        x, y, z = vertices[0, :], vertices[1, :], vertices[2, :]
        edge_pairs = [
            (0, 1),
            (0, 2),
            (0, 4),
            (1, 3),
            (1, 5),
            (2, 3),
            (2, 6),
            (3, 7),
            (4, 5),
            (4, 6),
            (5, 7),
            (6, 7),
        ]

        for (m, n) in edge_pairs:
            vert_x = np.array([x[m], x[n]])
            vert_y = np.array([y[m], y[n]])
            vert_z = np.array([z[m], z[n]])
            figure.add_trace(
                go.Scatter3d(
                    x=vert_x,
                    y=vert_y,
                    z=vert_z,
                    mode="lines",
                    line=dict(color="yellow", width=3),
                )
            )

        color_list = px.colors.qualitative.Dark24

        for item in self.boxes:
            item_color = color_list[(item.volume + item.id_) % len(color_list)]
            figure = item.plot(item_color, figure)

        camera = dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=1.25, y=1.25, z=1.25),
        )

        figure.update_layout(
            showlegend=False,
            scene_camera=camera,
            width=1200,
            height=1200,
            template="plotly_dark",
        )

        max_x = self.position[0] + self.size[0]
        max_y = self.position[1] + self.size[1]
        max_z = self.position[2] + self.size[2]
        figure.update_layout(
            scene=dict(
                xaxis=dict(nticks=int(max_x + 2), range=[0, max_x + 5]),
                yaxis=dict(nticks=int(max_y + 2), range=[0, max_y + 5]),
                zaxis=dict(nticks=int(max_z + 2), range=[0, max_z + 5]),
                aspectmode="cube",
            ),
            width=1200,
            margin=dict(r=20, l=10, b=10, t=10),
        )

        figure.update_scenes(
            xaxis_showgrid=False, yaxis_showgrid=False, zaxis_showgrid=False
        )
        figure.update_scenes(
            xaxis_showticklabels=False,
            yaxis_showticklabels=False,
            zaxis_showticklabels=False,
        )

        return figure

    def first_fit_decreasing(self, boxes: List[Box], check_area: int = 100) -> None:

        boxes.sort(key=lambda x: x.volume, reverse=True)

        for box in boxes:

            action_mask = self.action_mask(box, check_area)

            top_lev = self.size[2] - box.size[2]

            max_occupied = np.max(self.height_map)
            lev = min(top_lev, max_occupied)

            k = lev
            while k >= 0:
                locations = np.zeros(
                    shape=(self.size[0], self.size[1]), dtype=np.int32)
                kth_level = np.logical_and(
                    self.height_map == k, np.equal(action_mask, 1)
                )
                if kth_level.any():
                    locations[kth_level] = 1

                    position = [
                        np.nonzero(locations == 1)[0][0],
                        np.nonzero(locations == 1)[1][0],
                    ]

                    self.place_box(box, position, check_area)
                    break
                k -= 1


if __name__ == "__main__":
    len_bin_edges = [10, 10, 10]

    boxes_sizes = boxes_generator(len_bin_edges, num_items=64, seed=42)
    boxes = [
        Box(size, position=[-1, -1, -1], id_=i) for i, size in enumerate(boxes_sizes)
    ]

    container = Container(np.array([12, 12, 12], dtype=np.int32))

    container.first_fit_decreasing(boxes, check_area=100)

    fig = container.plot()
    fig.show()
