
from random import random
from math import sqrt, floor

class Star:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def dist(self, other):
        x_squared = (self.x - other.x) ^ 2
        y_squared = (self.y - other.y) ^ 2

        return sqrt(x_squared + y_squared)


def generate_stars(n: int, limits: (int, int), should_floor: bool = False) -> [Star]:
    star_list = []

    for _ in range(n):
        # TODO: Make the random function pseudorandom
        x = random() * limits[0]
        y = random() * limits[1]

        if should_floor:
            x = floor(x)
            y = floor(y)
        
        star = Star(x, y)
        star_list.append(star)

    return star_list

