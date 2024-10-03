import numpy as np


class Grad:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, grad):
        x_distance = abs(self.x - grad.x)
        y_distance = abs(self.y - grad.y)
        return np.sqrt((x_distance ** 2) + (y_distance ** 2))

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
