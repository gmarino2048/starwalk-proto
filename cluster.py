
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



def cluster (stars: [Star], size: int, inclusion: float) -> [Cluster]:
    clusters = []
    new_clusters = []

    for star in stars:
        if random.random() < inclusion:
            clusters.append([Cluster(star), True])

    while len(clusters) > size:
        length = len(clusters)

        for tup in clusters:
            if not tup[1]:
                continue

            cluster = tup[0]
            tup[1] = False

            min_dist = math.inf
            closest = None

            for other_tup in clusters:
                if not other_tup[1]:
                    continue

                other = other_tup[0]
                dist = abs(cluster.x() - other.x()) + abs(cluster.y() - other.y())

                if dist < min_dist:
                    closest = other_tup

            if closest is None:
                new_clusters.append(cluster)
                break

            closest[1] = False
            cluster.absorb(closest[0])

            new_clusters.append(cluster)

            remaining = [item for item in clusters if item[1]]
            if len(remaining) + len(new_clusters) <= size:
                remaining_clusters = [item[0] for item in remaining]
                new_clusters.extend(remaining_clusters)
                return new_clusters

        if len(new_clusters) < size:
            break

        clusters = [[cluster, True] for cluster in new_clusters]
        new_clusters = []
        pass

    return new_clusters