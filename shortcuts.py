from typing import List, Union

from geneticPacker import GeneticPacker
from box import Box, BoxList
from container import Container

from matplotlib import pyplot as plt
from drawCube import *

def pack_products_into_restrictions(products: List[Union[tuple, dict]],
                                    restrictions: tuple, population_size, probability, turns  ) -> Union[tuple, None]:
    

    container_width, container_depth, container_height = restrictions['width'], restrictions['depth'],restrictions['height']
    container = Container(container_width, container_depth, container_height,0,0,0)
    packager = GeneticPacker(container,population_size, probability, turns)

    box_list = []
    for product in products:
        box_list.extend(BoxList(product).box_items)

    fitness, unused_space, scheme = packager.pack(box_list)

    if not scheme:
        return None
    
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = ['SimHei']
    fig= plt.figure()
    ax = Axes3D(fig)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    print(fitness, scheme)

    # draw placed box
    for holder in scheme:
        plot_linear_cube(
            holder.x, holder.y, holder.z,
            holder.get_width(), holder.get_depth(), holder.get_height(),
            ax
        )
    # draw the dray cargo container
    plot_linear_cube(
            container.x, container.y, container.z,
            container.get_width(), container.get_depth(), container.get_height(),
            ax,'black'
        )
    # draw refenrence box
    plot_linear_cube(
            container.x, container.y, container.z,
            container.get_depth(), container.get_depth(), container.get_depth(),
            ax,'white'
        )
    '''
    # unused space
    for container in unused_space:
        plot_linear_cube(
            container.x, container.y, container.z,
            container.width, container.depth, container.height,
            ax,'blue'
        )
    print(unused_space)
    '''
    plt.show()
    return fitness, scheme
