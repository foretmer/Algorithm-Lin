from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List, Tuple
import os

from Common import *
import utils.log_utils

LOGGER = utils.log_utils.SingleLogger().get_logger()

def make_data(position, size=(1,1,1)):
    X = [[[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 0]],
         [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],
         [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
         [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
         [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
         [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]]
    X = np.array(X).astype(float)
    for i in range(3):
        X[:,:,i] *= size[i]
    X += np.array(position)
    return X

def make_3D(positions, sizes=None, colors=None, **kwargs):
    if not isinstance(colors,(list,np.ndarray)): colors=["C0"]*len(positions)
    if not isinstance(sizes,(list,np.ndarray)): sizes=[(1,1,1)]*len(positions)
    faces = []
    for position,size,color in zip(positions,sizes,colors):
        faces.append(make_data(position, size=size))
    return Poly3DCollection(np.concatenate(faces),  
                            facecolors=np.repeat(colors,6), 
                            edgecolor="k",
                            **kwargs)
    

def draw(save_path:str,
         container_size:Tuple[int,int,int],
         positions:List[Tuple[int,int,int]], 
         sizes:List[Tuple[int,int,int]], 
         colors:List[str]=None):
    assert len(positions) == len(sizes) 
    if colors is not None:
        assert len(positions) == len(colors)
    else:
        colors = ["#FFFFFFAA"] * len(positions)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    plt.gca().set_box_aspect(container_size)
    # ax.set_aspect('equal')

    plot_data = make_3D(positions, sizes, colors)
    ax.add_collection3d(plot_data)    

    ax.set_xlim([0,container_size[0]])
    ax.set_ylim([0,container_size[1]])
    ax.set_zlim([0,container_size[2]])

    fig.savefig(save_path)
    LOGGER.info(f"File saved to {save_path}")

    plt.show()

def anime(save_path:str,
          container_size:Tuple[int,int,int],
          positions:List[Tuple[int,int,int]], 
          sizes:List[Tuple[int,int,int]], 
          colors:List[str]=None):
    assert len(positions) == len(sizes) 
    if colors is not None:
        assert len(positions) == len(colors)
    else:
        colors = ["#FFFFFFAA"] * len(positions)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    plt.gca().set_box_aspect(container_size)
    # ax.set_aspect('equal')

    def update(i):
        ax.clear()
        # ax.set_facecolor(plt.cm.Blues(.2)) # 设置背景颜色

        plot_data = make_3D(positions[:i+1], sizes[:i+1], colors[:i+1])
        ax.add_collection3d(plot_data)

        ax.set_xlim([0,container_size[0]])
        ax.set_ylim([0,container_size[1]])
        ax.set_zlim([0,container_size[2]])

        [spine.set_visible(False) for spine in ax.spines.values()] #移除图表轮廓
    

    anime = FuncAnimation(fig = fig,    
                          func = update,    
                          frames = len(positions),    
                          interval = 100)

    anime.save(save_path)
    LOGGER.info(f"File saved to {save_path}")

    plt.show()