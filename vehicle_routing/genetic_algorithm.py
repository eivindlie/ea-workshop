from typing import List, Tuple
import random
from .environment import Environment, City, plot_solution, evaluate as evalute_solution


def create_random_solution(environment: Environment) -> List[int]:
    solution = [i for i in range(len(environment.cities))] + [
        -i for i in range(1, environment.num_vehicles)
    ]
    random.shuffle(solution)
    return solution


def decode_solution(solution: List[int], environment: Environment) -> List[List[City]]:
    decoded_solution = [[]]
    cur_vehicle = 0
    for gene in solution:
        if gene < 0:
            decoded_solution.append([])
            cur_vehicle += 1
        else:
            decoded_solution[cur_vehicle].append(environment.cities[gene])

    return decoded_solution


def initialize_population(
    population_size: int, environment: Environment
) -> List[List[int]]:
    population = []

    # TODO Initialiser populasjonen
    for _ in range(population_size):
        population.append(create_random_solution(environment))

    return population


def evaluate(
    population: List[List[int]], environment: Environment
) -> List[Tuple[float, List[int]]]:
    fitness_results = [
        (evalute_solution(decode_solution(ind, environment), environment), ind)
        for ind in population
    ]

    return sorted(fitness_results, key=lambda x: x[0], reverse=True)


def selection(
    population_ranked: List[Tuple[float, List[int]]], elite_size: float
) -> List[List[int]]:
    selection_results = []

    for i in range(elite_size):
        selection_results.append(population_ranked[i][1])

    # TODO Implementer selection-mekanisme
    while len(selection_results) < len(population_ranked):
        competitors = random.sample(population_ranked, 5)
        winner = max(competitors, key=lambda x: x[0])
        selection_results.append(winner[1])

    return selection_results


def crossover(parent1, parent2) -> List[int]:
    # TODO Implementer crossover

    crossover_point = random.randint(0, len(parent1) - 1)

    child_p1 = parent1[:crossover_point]
    child_p2 = [x for x in parent2 if x not in child_p1]

    child = child_p1 + child_p2

    return child


def recombine(mating_pool: List[List[int]], elite_size: int) -> List[List[int]]:
    children = mating_pool[:elite_size]
    length = len(mating_pool) - elite_size

    pool = random.sample(mating_pool, len(mating_pool))
    children = children + [crossover(pool[i], pool[-i - 1]) for i in range(length)]

    return children


def mutate(individual: List[int], mutation_rate: float) -> List[int]:
    individual = [x for x in individual]

    # TODO Implementer mutation-mekanisme
    for swapped in range(len(individual)):
        if random.random() < mutation_rate:
            swap_with = random.randint(0, len(individual) - 1)
            individual[swapped], individual[swap_with] = (
                individual[swap_with],
                individual[swapped],
            )

    return individual


def mutate_population(
    population: List[List[int]], mutation_rate: float
) -> List[List[int]]:
    mutated_pop = [mutate(x, mutation_rate) for x in population]

    return mutated_pop


def next_generation(
    current_gen: List[List[int]],
    environment: Environment,
    elite_size: int,
    mutation_rate: float,
) -> List[List[int]]:
    pop_ranked = evaluate(current_gen, environment)
    mating_pool = selection(pop_ranked, elite_size)
    children = recombine(mating_pool, elite_size)
    next_gen = mutate_population(children, mutation_rate)

    return next_gen


def solve(
    environment: Environment,
    population_size: int,
    elite_size: int,
    mutation_rate: float,
    generations: int,
    eval_frequency: int = 50,
    show_plots: bool = True,
) -> List[int]:
    initial_pop = initialize_population(population_size, environment)
    best_initial_solution = evaluate(initial_pop, environment)[0]
    print(f"Initial distance: {1 / best_initial_solution[0]}")
    if show_plots:
        plot_solution(
            decode_solution(best_initial_solution[1], environment),
            environment,
            "Initial",
        )

    pop = initial_pop
    history = [
        (
            0,
            best_initial_solution[0],
            decode_solution(best_initial_solution[1], environment),
        )
    ]

    for g in range(generations):
        pop = next_generation(pop, environment, elite_size, mutation_rate)

        if (g + 1) % eval_frequency == 0:
            best_current_solution = evaluate(pop, environment)[0]
            history.append(
                (
                    g,
                    best_current_solution[0],
                    decode_solution(best_current_solution[1], environment),
                )
            )
            print(
                f"[{g+1}/{generations}] Best distance: {1 / best_current_solution[0]}"
            )

            if show_plots:
                plot_solution(history[-1][2], environment, f"Generation {g + 1}")

    best_final_solution = evaluate(pop, environment)[0]
    print(f"Final distance: {1 / best_final_solution[0]}")
    print(f"Final chromosome: {best_final_solution[1]}")
    plot_solution(
        decode_solution(best_final_solution[1], environment),
        environment,
        "Final solution",
    )


def main():
    environment = Environment(
        num_cities=25,
        num_vehicles=5,
        vehicle_capacity=8,
        seed=None
    )
    
    solve(
        environment,
        population_size=50,
        elite_size=5,
        mutation_rate=0.05,
        generations=2000,
        eval_frequency=100,
        show_plots=False,
    )


if __name__ == "__main__":
    main()
