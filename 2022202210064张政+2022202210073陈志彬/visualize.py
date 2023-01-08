import numpy as np
import matplotlib.pyplot as plt
import os


pallete = ['darkgreen', 'tomato', 'yellow', 'darkblue', 'darkviolet', 'indianred', 'yellowgreen', 'mediumblue', 'cyan',
           'black', 'indigo', 'pink', 'lime', 'sienna', 'plum', 'deepskyblue', 'forestgreen', 'fuchsia', 'brown',
           'turquoise', 'aliceblue', 'blueviolet', 'rosybrown', 'powderblue', 'lightblue', 'skyblue', 'lightskyblue',
           'steelblue', 'dodgerblue', 'lightslategray', 'lightslategrey', 'slategray',
           'slategrey', 'lightsteelblue', 'cornflowerblue', 'royalblue', 'ghostwhite', 'lavender',
           'midnightblue', 'navy', 'darkblue', 'blue', 'slateblue', 'darkslateblue',
           'mediumslateblue', 'mediumpurple', 'rebeccapurple', 'darkorchid',
           'darkviolet', 'mediumorchid', 'lightsalmon', 'lightseagreen', 'lavenderblush', 'aquamarine', 'palegreen',
           'yellow', 'firebrick', 'maroon', 'darkred', 'red', 'salmon',
           'darksalmon', 'coral', 'orangered',
           'lightcoral', 'chocolate', 'saddlebrown', 'sandybrown', 'olive', 'olivedrab', 'darkolivegreen',
           'greenyellow', 'chartreuse', 'lawngreen', 'darkseagreen', 'lightgreen', 'limegreen',
           'green', 'seagreen', 'mediumseagreen', 'springgreen', 'mediumspringgreen', 'mediumaquamarine',
           'mediumturquoise', 'lightcyan', 'paleturquoise', 'darkslategray',
           'darkslategrey', 'teal', 'darkcyan', 'aqua', 'cyan', 'darkturquoise', 'cadetblue', 'thistle',
           'violet', 'purple', 'darkmagenta', 'magenta', 'orchid', 'mediumvioletred', 'deeppink', 'hotpink',
           'palevioletred', 'crimson', 'lightpink', 'darkgreen', 'tomato', 'yellow', 'darkblue', 'darkviolet',
           'indianred', 'yellowgreen', 'mediumblue', 'cyan',
           'black', 'indigo', 'pink', 'lime', 'sienna', 'plum', 'deepskyblue', 'forestgreen', 'fuchsia', 'brown',
           'turquoise', 'aliceblue', 'blueviolet', 'rosybrown', 'powderblue', 'lightblue', 'skyblue', 'lightskyblue',
           'steelblue', 'dodgerblue', 'lightslategray', 'lightslategrey', 'slategray', 'slategrey', 'lightsteelblue',
           'cornflowerblue', 'royalblue', 'ghostwhite', 'lavender', 'midnightblue', 'navy', 'darkblue', 'blue',
           'slateblue', 'darkslateblue', 'mediumslateblue', 'mediumpurple', 'rebeccapurple', 'darkorchid',
           'darkviolet', 'mediumorchid']


def cuboid_data(o, size=(1, 1, 1)):
    l, w, h = size
    x = [[o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]],
         [o[0], o[0] + l, o[0] + l, o[0], o[0]]]
    y = [[o[1], o[1], o[1] + w, o[1] + w, o[1]],
         [o[1], o[1], o[1] + w, o[1] + w, o[1]],
         [o[1], o[1], o[1], o[1], o[1]],
         [o[1] + w, o[1] + w, o[1] + w, o[1] + w, o[1] + w]]
    z = [[o[2], o[2], o[2], o[2], o[2]],
         [o[2] + h, o[2] + h, o[2] + h, o[2] + h, o[2] + h],
         [o[2], o[2], o[2] + h, o[2] + h, o[2]],
         [o[2], o[2], o[2] + h, o[2] + h, o[2]]]
    return np.array(x), np.array(y), np.array(z)


def plotcuboid(pos=(0, 0, 0), size=(1, 1, 1), ax=None, **kwargs):
    if ax is not None:
        X, Y, Z = cuboid_data(pos, size)
        plt.gca().set_box_aspect((3, 1, 1))
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=1, **kwargs)  # 画图


def draw(pieces, ft, p_ind, new_dir_path, color_index=[]):
    positions = []
    sizes = []
    colors = []
    sorted_size = []
    for each in pieces:
        positions.append(each[0:3])
        sizes.append(each[3:])
        sorted_size.append(set(each[3:]))
    if len(color_index) == 0:
        colors = pallete[:len(positions)]
        color_index = [sorted_size, colors]
    else:
        dim = color_index[0]
        clr = color_index[1]
        for each in sorted_size:
            index = dim.index(each)
            colors.append(clr[index])
    # 画图
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    for p, s, c in zip(positions, sizes, colors):
        plotcuboid(pos=p, size=s, ax=ax, color=c)
    plt.title("第{}个实例下的最大填充率：{}%".format(p_ind + 1, ft))
    plt.savefig(os.path.join(new_dir_path, 'so_{}.jpg'.format(p_ind + 1)), dpi=400)
    # plt.show()
    # plt.pause(0)
