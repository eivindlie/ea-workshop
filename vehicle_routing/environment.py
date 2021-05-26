import random
from typing import List

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()


OVERFILLED_VEHICLE_PENALTY = 250

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

        self.depot = City(x=random.randint(70, 130), y=random.randint(70, 130))

        self.num_vehicles = num_vehicles
        self.vehicle_capacity = vehicle_capacity


def calculate_route_lengths(
    solution: List[List[City]], environment: Environment
) -> List[float]:
    all_distances = []

    for vehicle_cities in solution:
        distance = 0
        route = [environment.depot] + vehicle_cities + [environment.depot]

        for i in range(len(route) - 1):
            from_city = route[i]
            to_city = route[i + 1]
            distance += from_city.distance(to_city)

        if len(vehicle_cities) > environment.vehicle_capacity:
            distance += OVERFILLED_VEHICLE_PENALTY * (len(vehicle_cities) - environment.vehicle_capacity)

        all_distances.append(distance)

    return all_distances


def evaluate(solution: List[List[City]], environment: Environment) -> float:
    distance = sum(calculate_route_lengths(solution, environment))

    return 1 / distance


def plot_solution(
    solution: List[List[City]], environment: Environment, title: str = None, ax=None, background_color=None
) -> None:
    plotter = ax if ax is not None else plt
    colors = ["blue", "red", "yellow", "orange", "green", "cyan"]
    for r, vehicle_cities in enumerate(solution):
        color = colors[r % len(colors)]

        route = [environment.depot] + vehicle_cities + [environment.depot]

        for i in range(len(route) - 1):
            plotter.plot(
                (route[i].x, route[i + 1].x), (route[i].y, route[i + 1].y), color=color
            )

    plotter.scatter(
        [c.x for c in environment.cities],
        [c.y for c in environment.cities],
        color="black",
        s=10,
    )
    plotter.scatter((environment.depot.x,), (environment.depot.y,), color="green", s=50)

    if title:
        if ax is not None:
            ax.set_title(title)
        else:
            plt.title(title)
    
    if background_color is not None:
        if ax is not None:
            ax.set_facecolor(background_color)

    if ax is None:
        plt.show()
