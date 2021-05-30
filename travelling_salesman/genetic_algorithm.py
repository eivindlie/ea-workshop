import random
from typing import List

from .environment import Fitness, City, initialize_random_environment
from .plotting import plot_route, plot_history


def create_random_route(cities: List[City]) -> List[City]:
    route = random.sample(cities, len(cities))
    return route


def initialize_population(population_size: int, cities: List[City]) -> List[List[City]]:
    population = []

    # TODO Initialiser populasjonen med population_size løsninger

    return population


def evaluate(population) -> List[Fitness]:
    fitness_results = [Fitness(x) for x in population]
    return sorted(fitness_results, key=lambda x: x.fitness, reverse=True)


def selection(population_ranked: List[Fitness], elite_size: float):
    selection_results = []

    # Velger ut de beste løsningene basert på elite_size
    for i in range(elite_size):
        selection_results.append(population_ranked[i])

    # TODO Implementer selection-mekanisme som velger ut kandidater til crossover.
    # Pass på at størrelsen på populasjonen ikke endres!

    return [x.route for x in selection_results]


def crossover(parent1, parent2) -> List[City]:
    # TODO Implementer crossover

    child = parent1

    return child


def recombine(mating_pool: List[List[City]], elite_size: int) -> List[List[City]]:
    children = []
    length = len(mating_pool) - elite_size

    # Lar igjen de beste løsningene bli med direkte
    for i in range(elite_size):
        children.append(mating_pool[i])

    pool = random.sample(mating_pool, len(mating_pool))
    for i in range(length):
        child = crossover(pool[i], pool[-i - 1])
        children.append(child)

    return children


def mutate(individual: List[City], mutation_rate: float) -> List[City]:
    individual = [x for x in individual]

    # TODO Implementer mutation-mekanisme

    return individual


def mutate_population(
    population: List[List[City]], mutation_rate: float
) -> List[List[City]]:
    mutated_pop = [mutate(x, mutation_rate) for x in population]

    return mutated_pop


def next_generation(
    current_gen: List[List[City]], elite_size: int, mutation_rate: float
) -> List[List[City]]:
    pop_ranked = evaluate(current_gen)
    mating_pool = selection(pop_ranked, elite_size)
    children = recombine(mating_pool, elite_size)
    next_gen = mutate_population(children, mutation_rate)

    return next_gen


def solve(
    cities: List[City],
    population_size: int,
    elite_size: int,
    mutation_rate: float,
    generations: int,
    eval_frequency: int = 50,
    show_plots: bool = True,
) -> List[City]:
    initial_pop = initialize_population(population_size, cities)
    best_initial_solution = evaluate(initial_pop)[0]
    print(f"Initial distance: {best_initial_solution.distance}")
    if show_plots:
        plot_route(best_initial_solution.route, "Initial")

    pop = initial_pop

    history = [(0, best_initial_solution)]

    for g in range(generations):
        pop = next_generation(pop, elite_size, mutation_rate)

        if (g + 1) % eval_frequency == 0:
            best_current_solution = evaluate(pop)[0]
            history.append((g, best_current_solution))
            print(
                f"[{g+1}/{generations}] Best distance: {best_current_solution.distance}"
            )

            if show_plots:
                plot_route(best_current_solution.route, f"Generation {g + 1}")

    best_final_solution = evaluate(pop)[0]
    print(f"Final distance: {best_final_solution.distance}")
    plot_history(history)
    plot_route(best_final_solution.route, "Final solution")

    return best_final_solution.route


def main():
    city_list = initialize_random_environment()

    best_route = solve(
        cities=city_list,
        population_size=100,
        elite_size=5,
        mutation_rate=0.05,
        generations=150,
        eval_frequency=10,
        show_plots=False,
    )


if __name__ == "__main__":
    main()
