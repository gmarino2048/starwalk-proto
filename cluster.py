
import math
import random
from copy import copy
from stargen import Star

class Cluster:

    def __init__(self, star: Star):
        self.stars = []

        self.centroid = (float(star.get_x()), float(star.get_y()))
        self.objects = 1

        self.stars.append(star)

    def x(self):
        return self.centroid[0]

    def y(self):
        return self.centroid[1]

    def absorb(self, cluster):
        self.centroid = self._weighted_centroid(cluster)
        self.objects = self.objects + cluster.objects
        self.stars.extend(cluster.stars)

    def _weighted_centroid(self, cluster):
        this_size, other_size = self.objects, cluster.objects
        sum_x = (self.x() * this_size) + (cluster.x() * other_size)
        sum_y = (self.y() * this_size) + (cluster.y() * other_size)

        return sum_x / (this_size + other_size), sum_y / (this_size + other_size)

    def dist(self, other):
        x_dist = abs(self.x() - other.x())
        y_dist = abs(self.y() - other.y())

        return x_dist + y_dist


def cluster (stars: [Star], size: int, inclusion: float) -> [Cluster]:
    clusters = []
    remaining_stars = copy(stars)

    # Randomly select stars to be the starting point for each major cluster
    for _ in range(size):
        starter = random.choice(remaining_stars)
        clusters.append(Cluster(starter))

        remaining_stars.remove(starter)

    # Assign stars to the closest cluster
    for star in remaining_stars:
        new_cluster = Cluster(star)
        closest = min(clusters, key = lambda clust: clust.dist(new_cluster))
        closest.absorb(new_cluster)

    return clusters