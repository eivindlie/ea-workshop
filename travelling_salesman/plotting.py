from typing import List, Tuple
import math
import matplotlib.pyplot as plt
import seaborn as sns
from .environment import Fitness

sns.set()


def plot_route(route, title=None) -> None:
    for i in range(len(route)):
        city = route[i]
        next_city = route[(i + 1) % len(route)]
        plt.scatter(city.x, city.y, c="red")
        plt.plot((city.x, next_city.x), (city.y, next_city.y), c="black")

    if title:
        plt.title(title)

    plt.show()


def plot_history(history: Tuple[int, List[Fitness]]) -> None:
    # Plot score history
    fig, ax1 = plt.subplots(figsize=(8, 6))
    ax1.set_title("Score history")
    color = "tab:red"
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness", color=color)
    ax1.plot([x[1].fitness for x in history], label="Fitness", color=color)
    ax1.tick_params(axis="y", labelcolor=color)

    color = "tab:blue"
    ax2 = ax1.twinx()
    ax2.plot([x[1].distance for x in history], label="Distance", color=color)
    ax2.set_ylabel("Distance", color=color)
    ax2.tick_params(axis="y", labelcolor=color)

    # Plot routes
    cols = min(len(history), 5)
    rows = math.ceil(len(history) / 5)
    fix, axes = plt.subplots(rows, cols, figsize=(15, 10))
    axes = axes.flatten()

    for i, gen in enumerate(history):
        ax = axes[i]
        ax.set_title(f"Generation {gen[0] + 1}")
        route = gen[1].route

        for i in range(len(route)):
            city = route[i]
            next_city = route[(i + 1) % len(route)]
            ax.scatter(city.x, city.y, c="red")
            ax.plot((city.x, next_city.x), (city.y, next_city.y), c="black")

    plt.show()
