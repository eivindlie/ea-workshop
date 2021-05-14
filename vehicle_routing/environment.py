import random
from typing import List

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()


class City:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def distance(self, city) -> float:
        return np.sqrt((self.x - city.x) ** 2 + (self.y - city.y) ** 2)

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"


class Environment:
    def __init__(
        self, num_cities=25, num_vehicles=5, vehicle_capacity=10, seed=None
    ) -> None:
        random.seed(seed)

        self.cities = [
            City(x=random.randint(0, 200), y=random.randint(0, 200))
            for _ in range(num_cities)
        ]

        self.depot = City(x=random.randint(0, 200), y=random.randint(0, 200))

        self.num_vehicles = num_vehicles
        self.vehicle_capacity = vehicle_capacity


def evaluate(solution: List[List[City]], environment: Environment) -> float:
    distance = 0

    for vehicle_cities in solution:
        route = [environment.depot] + vehicle_cities + [environment.depot]

        for i in range(len(route) - 1):
            from_city = route[i]
            to_city = route[i + 1]
            distance += from_city.distance(to_city)

        if len(vehicle_cities) > environment.vehicle_capacity:
            distance += 500 * (len(vehicle_cities) - environment.vehicle_capacity)

    return 1 / distance


def plot_solution(
    solution: List[List[City]], environment: Environment, title: str = None
) -> None:
    colors = ["blue", "red", "yellow", "orange"]
    for r, vehicle_cities in enumerate(solution):
        color = colors[r % len(colors)]

        route = [environment.depot] + vehicle_cities + [environment.depot]

        for i in range(len(route) - 1):
            plt.plot(
                (route[i].x, route[i + 1].x), (route[i].y, route[i + 1].y), color=color
            )

    plt.scatter(
        [c.x for c in environment.cities],
        [c.y for c in environment.cities],
        color="black",
        s=10,
    )
    plt.scatter((environment.depot.x,), (environment.depot.y,), color="green", s=50)

    if title:
        plt.title(title)

    plt.show()
