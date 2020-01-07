
import math
import random
from copy import copy
from stargen import Star

class Cluster:

    def __init__(self, star: Star):
        self.stars = []

        self.centroid = (float(star.get_x()), float(star.get_y()))
        self.objects = 1

        self.mapping = []

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

    def generate_map(self):
        connected = [[star, False] for star in self.stars]

        dist = lambda s1, s2: abs(s1.get_x() - s2.get_x()) + abs(s1.get_y() - s2.get_y())

        for tup in connected:
            distances = [(dist(tup[0], item[0]), item) for item in connected if item != tup]

            #Abort if there's fewer than one star in the list
            if len(distances) == 0:
                continue

            min_dist = min(distances, key=lambda item: item[0])

            if min_dist[1][1]:
                distances.remove(min_dist)

                #Abort if there was only one item in the list
                if len(distances) == 0:
                    continue

                min_dist = min(distances, key=lambda item: item[0])
            
            star = tup[0]
            other = min_dist[1][0]

            self.mapping.append((star, other))

            tup[1] = True
            min_dist[1][1] = True


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