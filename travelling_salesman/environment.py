import numpy as np
import random


class City:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def distance(self, city) -> float:
        return np.sqrt((self.x - city.x) ** 2 + (self.y - city.y) ** 2)

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"


class Fitness:
    def __init__(self, route) -> None:
        self.route = route
        self._distance = 0
        self._fitness = 0

    @property
    def distance(self) -> float:
        if self._distance == 0:
            path_distance = 0
            for i in range(len(self.route)):
                from_city = self.route[i]
                to_city = self.route[(i + 1) % len(self.route)]
                path_distance += from_city.distance(to_city)
            self._distance = path_distance
        return self._distance

    @property
    def fitness(self) -> float:
        if self._fitness == 0:
            self._fitness = 1 / float(self.distance)
        return self._fitness


def initialize_random_environment(num_cities=25, seed=None):
    city_list = []

    random.seed(seed)

    for _ in range(num_cities):
        city_list.append(City(x=random.randint(0, 200), y=random.randint(0, 200)))

    return city_list
