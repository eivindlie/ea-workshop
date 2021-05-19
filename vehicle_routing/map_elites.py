import random

from .genetic_algorithm import crossover, mutate, decode_solution, create_random_solution
from .environment import calculate_route_lengths, Environment, plot_solution


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
        avg = sum(route_lengths) / len(route_lengths)

        return int(
            min(0.99999, (avg / self.max_average_route_length))
            * self.num_cars_dimension_size
        )

    def evaluate_and_replace_solution(self, new_solution):
        route_lengths = calculate_route_lengths(decode_solution(new_solution, self.environment), self.environment)
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

    def get_best_score(self):
        flattened_archive = self._get_flattened_archive()
        return max(self._get_flattened_archive(), key=lambda x: x[0])[0]

    def get_best_solution(self):
        return max(self._get_flattened_archive(), key=lambda x: x[1])[1]


def initialize(archive: Archive, environment: Environment, n_solutions: int = 10):
    for i in range(n_solutions):
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
):
    archive = Archive(
        environment,
        num_cars_dimension_size=environment.num_vehicles,
        average_route_length_dimension_size=10,
    )

    initialize(archive, environment, n_solutions=10)

    for g in range(steps):
        advance_single_step(archive, mutation_rate)

        if (g + 1) % eval_frequency == 0:
            best_current_score = archive.get_best_score()
            print(f"[{g + 1}/{steps}] Best distance: {1 / best_current_score}")

    best_final_solution = archive.get_best_solution()
    plot_solution(decode_solution(best_final_solution, environment), environment, "Final best solution")


def main():
    environment = Environment(
        num_cities=25, num_vehicles=5, vehicle_capacity=8, seed=None
    )

    solve(
        environment,
        steps=100000,
        mutation_rate=0.05,
    )
