
from math import sqrt

class Star:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def x(self):
        return self.x

    def y(self):
        return self.y

    def dist(self, other: Star):
        x_squared = (self.x - other.x) ^ 2
        y_squared = (self.y - other.y) ^ 2

        return sqrt(x_squared + y_squared)


def generate_stars(n: int):
    pass