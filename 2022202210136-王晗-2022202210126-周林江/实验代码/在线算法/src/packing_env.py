import copy
import warnings
from typing import List, Tuple, Union

import gym
import numpy as np
import plotly.graph_objects as go
from gym.spaces import Discrete, MultiDiscrete, MultiBinary
from gym.utils import seeding
from nptyping import NDArray

from src.packing_kernel import Box, Container
from src.utils import boxes_generator


class PackingEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(
            self,
            container_size: List[int],
            box_sizes: List[List[int]],
            num_visible_boxes: int = 1,
            render_mode: str = "human",
            options: dict = None,
    ) -> None:

        self.render_mode = render_mode
        self.container = Container(container_size)

        self.initial_boxes = [
            Box(box_size, position=[-1, -1, -1], id_=index)
            for index, box_size in enumerate(box_sizes)
        ]

        self.unpacked_hidden_boxes = self.initial_boxes.copy()

        self.unpacked_visible_boxes = []

        self.packed_boxes = []
        self.skipped_boxes = []

        self.num_visible_boxes = num_visible_boxes
        self.unpacked_visible_boxes = []
        self.state = {}
        self.done = False

        box_repr = np.zeros(shape=(num_visible_boxes, 3), dtype=np.int32)
        box_repr[:] = self.container.size + [1, 1, 1]

        height_map_repr = np.ones(
            shape=(container_size[0], container_size[1]), dtype=np.int32
        ) * (container_size[2] + 1)

        observation_dict = {
            "height_map": MultiDiscrete(height_map_repr),
            "visible_box_sizes": MultiDiscrete(box_repr),
            "action_mask": MultiBinary(
                container_size[0] * container_size[1] * num_visible_boxes
            ),
        }

        self.observation_space = gym.spaces.Dict(observation_dict)

        self.action_space = Discrete(
            container_size[0] * container_size[1] * num_visible_boxes
        )

    def seed(self, seed: int = 42):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def action_to_position(self, action: int) -> Tuple[int, NDArray]:

        box_index = action // (self.container.size[0] * self.container.size[1])
        res = action % (self.container.size[0] * self.container.size[1])

        position = np.array(
            [res // self.container.size[0], res % self.container.size[0]]
        )

        return box_index, position.astype(np.int32)

    def position_to_action(self, position, box_index=0):

        action = (
                box_index * self.container.size[0] * self.container.size[1]
                + position[0] * self.container.size[0]
                + position[1]
        )
        return action

    def reset(self, seed=None, options=None, return_info=False) -> dict[str, object]:

        if return_info:
            info = {}

        self.container.reset()

        self.unpacked_hidden_boxes = copy.deepcopy(self.initial_boxes)

        if self.num_visible_boxes > 1:
            self.unpacked_visible_boxes = self.unpacked_hidden_boxes[
                                          0: self.num_visible_boxes
                                          ]
            del self.unpacked_hidden_boxes[0: self.num_visible_boxes]
        else:
            self.unpacked_visible_boxes = [self.unpacked_hidden_boxes.pop(0)]

        self.packed_boxes = self.container.boxes

        visible_box_sizes = np.asarray(
            [box.size for box in self.unpacked_visible_boxes]
        )
        visible_box_sizes = np.reshape(
            visible_box_sizes, (self.num_visible_boxes, 3))

        hm = np.asarray(self.container.height_map, dtype=np.int32)
        action_mask = np.asarray(
            self.container.action_mask(box=self.unpacked_visible_boxes[0]),
            dtype=np.int8,
        )

        self.state = {
            "height_map": hm,
            "visible_box_sizes": visible_box_sizes,
            "action_mask": np.reshape(
                action_mask, (self.container.size[0] * self.container.size[1],)
            ),
        }
        self.done = False
        self.seed(seed)

        if return_info:
            return self.state, info
        else:
            return self.state

    def step(self, action: int) -> Tuple[NDArray, float, bool, dict]:

        box_index, position = self.action_to_position(action)

        if (
                self.container.check_valid_box_placement(
                    self.unpacked_visible_boxes[box_index], position, check_area=100
                )
                == 1
        ):

            if self.num_visible_boxes > 1:
                reward = self.unpacked_visible_boxes[box_index].size[0] * \
                         self.unpacked_visible_boxes[box_index].size[1] * \
                         self.unpacked_visible_boxes[box_index].size[2]
                self.container.place_box(
                    self.unpacked_visible_boxes.pop(box_index), position
                )
            else:
                reward = self.unpacked_visible_boxes[0].size[0] * \
                         self.unpacked_visible_boxes[0].size[1] * \
                         self.unpacked_visible_boxes[0].size[2]
                self.container.place_box(
                    self.unpacked_visible_boxes[0], position)
                self.unpacked_visible_boxes = []

            self.state["height_map"] = self.container.height_map

            self.packed_boxes = self.container.boxes



        else:
            self.skipped_boxes.append(
                self.unpacked_visible_boxes.pop(box_index))
            reward = 0

        if len(self.unpacked_hidden_boxes) > 0:
            self.unpacked_visible_boxes.append(
                self.unpacked_hidden_boxes.pop(0))

        if len(self.unpacked_visible_boxes) == 0:
            self.done = True
            terminated = self.done
            self.state["visible_box_sizes"] = []

        else:
            visible_box_sizes = np.asarray(
                [box.size for box in self.unpacked_visible_boxes]
            )
            visible_box_sizes = np.reshape(
                visible_box_sizes, (self.num_visible_boxes, 3)
            )

            self.state["visible_box_sizes"] = visible_box_sizes

            self.state["action_mask"] = np.reshape(
                self.container.action_mask(box=self.unpacked_visible_boxes[0]),
                (self.container.size[0] * self.container.size[1],),
            )

            terminated = False

        return self.state, reward, terminated, {}

    def render(self, mode="human") -> Union[go.Figure, NDArray]:

        if mode == "human":
            return self.container.plot()

        elif mode == "rgb_array":
            import io
            from PIL import Image

            fig_png = self.container.plot().to_image(format="png")
            buf = io.BytesIO(fig_png)
            img = Image.open(buf)
            return np.asarray(img, dtype=np.int8)

    def close(self) -> None:
        pass


if __name__ == "__main__":
    from src.utils import boxes_generator
    from gym import make
    from plotly_gif import GIF

    env = make(
        "PackingEnv-v0",
        container_size=[10, 10, 10],
        box_sizes=boxes_generator([10, 10, 10], 64, 42),
        num_visible_boxes=1,
    )
    obs = env.reset()

    gif = GIF(gif_name="random_rollout.gif", gif_path="../gifs")
    for step_num in range(80):
        fig = env.render()
        gif.create_image(fig)
        action_mask = obs["action_mask"]
        action = env.action_space.sample(mask=action_mask)
        obs, reward, done, info = env.step(action)
        if done:
            break

    gif.create_gif()
    gif.save_gif("random_rollout.gif")
