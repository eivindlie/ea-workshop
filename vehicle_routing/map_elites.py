import random
from typing import List

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from .genetic_algorithm import (
    crossover,
    mutate,
    decode_solution,
    create_random_solution,
)
from .environment import (
    calculate_route_lengths,
    Environment,
    plot_solution,
)

class Archive:
    def __init__(
        self,
        environment,
        num_cars_dimension_size,
        average_route_length_dimension_size,
        max_average_route_length=2000,
    ):
        self.num_cars_dimension_size = num_cars_dimension_size
        self.average_route_length_dimension_size = average_route_length_dimension_size
        self.max_average_route_length = max_average_route_length
        self.archive = [
            [(-1, None) for _ in range(num_cars_dimension_size)]
            for _ in range(average_route_length_dimension_size)
        ]
        self.environment = environment

    def _get_num_cars(self, solution):
        max_num = sum(1 if x < 0 else 0 for x in solution)
        num = max_num - sum(
            1
            if i == 0
            and solution[i] < 0
            or i < len(solution) - 1
            and solution[i] < 0
            and solution[i + 1] < 0
            or solution[i] < 0
            and i == len(solution) - 1
            else 0
            for i in range(len(solution))
        )

        return int(((num - 1) / max_num) * self.num_cars_dimension_size)

    def _get_average_route_length(self, route_lengths):
        non_zero_lengths = [x for x in route_lengths if x > 0]
        avg = sum(non_zero_lengths) / len(non_zero_lengths)

        return int(
            min(0.99999, (avg / float(self.max_average_route_length)))
            * self.average_route_length_dimension_size
        )

    def evaluate_and_replace_solution(self, new_solution):
        route_lengths = calculate_route_lengths(
            decode_solution(new_solution, self.environment), self.environment
        )
        average_route_length = self._get_average_route_length(route_lengths)
        num_cars = self._get_num_cars(new_solution)

        score = 1 / sum(route_lengths)

        # TODO Finn ut om vi har funnet en bedre løsning, og erstatt i så fall den gamle løsningen i arkivet
        # Tips: Løsningen vi har funnet skal inn i self.archive[average_route_length][num_cars].
        # Løsninger lagres i arkivet som en tuppel (score, solution).

        old_score = self.archive[average_route_length][num_cars][0]
        if score > old_score:
            self.archive[average_route_length][num_cars] = (score, new_solution)

    def _get_flattened_archive(self):
        return [x for y in self.archive for x in y if x[0] != -1]

    def draw_random_solutions(self, n=1):
        pool = self._get_flattened_archive()

        return [x[1] for x in random.sample(pool, n)]

    def get_scores_as_array(self):
        scores = np.array(
            [
                [self.archive[x][y][0] for y in range(self.num_cars_dimension_size)]
                for x in range(self.average_route_length_dimension_size)
            ]
        )

        return scores

    def get_best_score(self):
        return max(self._get_flattened_archive(), key=lambda x: x[0])[0]

    def get_best_solution(self):
        return max(self._get_flattened_archive(), key=lambda x: x[0])[1]

    def plot_score_history(self, scores: List[np.ndarray], eval_frequency: int, show_plot: bool = True):
        best_score = max(x.max() for x in scores)
        ticks = list((i + 1) * (self.max_average_route_length // self.average_route_length_dimension_size) for i in range(self.average_route_length_dimension_size))

        fig = plt.figure(figsize=(15, 10))
        fig.suptitle("History of archive scores (animated)")

        cbar = True
        def plot(data: np.ndarray):
            nonlocal cbar
            data = data.T
            plt.cla()
            sns.heatmap(data, vmin=0, vmax=best_score, mask=(scores == -1), annot=True, xticklabels=ticks, cbar=cbar)
            cbar = False
        
        def init():
            plot(scores[0])
            plt.xlabel("Gjennomsnittlig rutelengde")
            plt.ylabel("Antall biler")

        def update(i: int):
            plot(scores[i])
            plt.title(f"Step {(i + 1) * eval_frequency:06}")
        
        anim = FuncAnimation(fig, update, np.arange(1, len(scores)), init_func=init)
        if show_plot:
            plt.show()
        return anim
    
    def plot_archive_solutions(self, show_plot: bool = True):
        fig, axes = plt.subplots(self.num_cars_dimension_size, self.average_route_length_dimension_size, figsize=(15, 10))
        fig.suptitle("All solutions from archive")
        best_solution = self.get_best_solution()

        for y in range(self.average_route_length_dimension_size):
            for x in range(self.num_cars_dimension_size):
                solution = self.archive[y][x][1]
                background_color = "xkcd:mint green" if solution == best_solution else None

                if solution is None:
                    continue
                plot_solution(
                    decode_solution(solution, self.environment),
                    self.environment,
                    ax=axes[x][y],
                    background_color=background_color
                )
        
        if show_plot:
            plt.show()
        return fig
        
def initialize(archive: Archive, environment: Environment, n_solutions: int = 10):
    for _ in range(n_solutions):
        solution = create_random_solution(environment)
        archive.evaluate_and_replace_solution(solution)


def advance_single_step(archive: Archive, mutation_rate: float):
    parents = archive.draw_random_solutions(2)
    child = crossover(parents[0], parents[1])
    mutated_child = mutate(child, mutation_rate)

    archive.evaluate_and_replace_solution(mutated_child)


def solve(
    environment: Environment,
    steps: int,
    mutation_rate: float,
    eval_frequency: int = 50,
    num_cars_dimension_size: int = 5,
    average_route_length_dimension_size: int = 10,
    max_average_route_length:int = 1000
):
    archive = Archive(
        environment,
        num_cars_dimension_size=num_cars_dimension_size,
        average_route_length_dimension_size=average_route_length_dimension_size,
        max_average_route_length=max_average_route_length
    )

    initialize(archive, environment, n_solutions=10)
    score_history = []

    try:        
        for g in range(steps):
            advance_single_step(archive, mutation_rate)

            if (g + 1) % eval_frequency == 0:
                best_current_score = archive.get_best_score()
                print(f"[{g + 1}/{steps}] Best distance: {1 / best_current_score}")
                score_history.append(archive.get_scores_as_array())
    except KeyboardInterrupt:
        pass

    archive_fig = archive.plot_archive_solutions(show_plot=False)
    anim = archive.plot_score_history(score_history, eval_frequency, show_plot=False)
    plt.show()


def main():
    environment = Environment(
        num_cities=25, num_vehicles=5, vehicle_capacity=6, seed=None
    )

    solve(
        environment,
        steps=150000,
        eval_frequency=500,
        mutation_rate=0.05,
        num_cars_dimension_size=environment.num_vehicles,
        average_route_length_dimension_size=10,
        max_average_route_length=3000
    )
