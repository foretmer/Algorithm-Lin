import matplotlib.pyplot as plt


class VisualHelper:
    def __init__(self, boxes):
        self.boxes = boxes

    def display(self, group, index):
        fig = plt.figure()
        plt.title("BoxType:" + str(group) + " Index:" + str(index), fontsize=15)
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        for box in self.boxes:
            dx = box.lay_l
            dy = box.lay_w
            dz = box.lay_h

            ax.bar3d(box.lay_point.x, box.lay_point.y, box.lay_point.z, dx, dy, dz, shade=True)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()
