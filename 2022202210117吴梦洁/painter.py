from matplotlib.patches import Rectangle,Circle
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
import numpy as np

class Painter:
    def __init__(self, trucks):
        ''' '''
        self.boxes = trucks.boxes
        self.width = trucks.length
        self.height = trucks.height
        self.length = trucks.width

    def _plotCube(self, ax, x, y, z, dx, dy, dz, color='red', mode=2):
        """ Auxiliary function to plot a cube. code taken somewhere from the web.  """
        xx = [x, x, x + dx, x + dx, x]
        yy = [y, y + dy, y + dy, y, y]

        kwargs = {'alpha': 1, 'color': color, 'linewidth': 1}
        if mode == 1:
            ax.plot3D(xx, yy, [z] * 5, **kwargs)
            ax.plot3D(xx, yy, [z + dz] * 5, **kwargs)
            ax.plot3D([x, x], [y, y], [z, z + dz], **kwargs)
            ax.plot3D([x, x], [y + dy, y + dy], [z, z + dz], **kwargs)
            ax.plot3D([x + dx, x + dx], [y + dy, y + dy], [z, z + dz], **kwargs)
            ax.plot3D([x + dx, x + dx], [y, y], [z, z + dz], **kwargs)
        else:
            p = Rectangle((x, y), dx, dy, fc=color, ec='black')
            p2 = Rectangle((x, y), dx, dy, fc=color, ec='black')
            p3 = Rectangle((y, z), dy, dz, fc=color, ec='black')
            p4 = Rectangle((y, z), dy, dz, fc=color, ec='black')
            p5 = Rectangle((x, z), dx, dz, fc=color, ec='black')
            p6 = Rectangle((x, z), dx, dz, fc=color, ec='black')
            ax.add_patch(p)
            ax.add_patch(p2)
            ax.add_patch(p3)
            ax.add_patch(p4)
            ax.add_patch(p5)
            ax.add_patch(p6)
            art3d.pathpatch_2d_to_3d(p, z=z, zdir="z")
            art3d.pathpatch_2d_to_3d(p2, z=z + dz, zdir="z")
            art3d.pathpatch_2d_to_3d(p3, z=x, zdir="x")
            art3d.pathpatch_2d_to_3d(p4, z=x + dx, zdir="x")
            art3d.pathpatch_2d_to_3d(p5, z=y, zdir="y")
            art3d.pathpatch_2d_to_3d(p6, z=y + dy, zdir="y")

    def _plotCylinder(self, ax, x, y, z, dx, dy, dz, color='red', mode=2):
        """ Auxiliary function to plot a Cylinder  """
        # plot the two circles above and below the cylinder
        p = Circle((x + dx / 2, y + dy / 2), radius=dx / 2, color=color, ec='black')
        p2 = Circle((x + dx / 2, y + dy / 2), radius=dx / 2, color=color, ec='black')
        ax.add_patch(p)
        ax.add_patch(p2)
        art3d.pathpatch_2d_to_3d(p, z=z, zdir="z")
        art3d.pathpatch_2d_to_3d(p2, z=z + dz, zdir="z")
        # plot a circle in the middle of the cylinder
        center_z = np.linspace(0, dz, 15)
        theta = np.linspace(0, 2 * np.pi, 15)
        theta_grid, z_grid = np.meshgrid(theta, center_z)
        x_grid = dx / 2 * np.cos(theta_grid) + x + dx / 2
        y_grid = dy / 2 * np.sin(theta_grid) + y + dy / 2
        z_grid = z_grid + z
        ax.plot_surface(x_grid, y_grid, z_grid, shade=False, fc=color, ec='black', alpha=1, color=color)

    def plotBoxAndItems(self, title=""):
        """ side effective. Plot the Bin and the items it contains. """
        fig = plt.figure()
        axGlob = plt.axes(projection='3d')

        counter = 0
        # fit rotation type
        for item in self.boxes:
            rt = item.rotation_type
            x, y, z = item.position
            [w, h, d] = item.get_dimension()
            color = '#FFFF37'

            self._plotCube(axGlob, float(x), float(y), float(z), float(w), float(h), float(d), color=color, mode=2)

            counter = counter + 1
            # plot bin
        self._plotCube(axGlob, 0, 0, 0, float(self.width), float(self.height), float(self.length), color='black', mode=1)

        plt.title('result')
        self.setAxesEqual(axGlob)
        plt.show()

    def setAxesEqual(self, ax):
        '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
        cubes as cubes, etc..  This is one possible solution to Matplotlib's
        ax.set_aspect('equal') and ax.axis('equal') not working for 3D.
        Input
        ax: a matplotlib axis, e.g., as output from plt.gca().'''
        x_limits = ax.get_xlim3d()
        y_limits = ax.get_ylim3d()
        z_limits = ax.get_zlim3d()

        x_range = abs(x_limits[1] - x_limits[0])
        x_middle = np.mean(x_limits)
        y_range = abs(y_limits[1] - y_limits[0])
        y_middle = np.mean(y_limits)
        z_range = abs(z_limits[1] - z_limits[0])
        z_middle = np.mean(z_limits)

        # The plot bounding box is a sphere in the sense of the infinity
        # norm, hence I call half the max range the plot radius.
        plot_radius = 0.5 * max([x_range, y_range, z_range])

        ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
        ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
        ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])