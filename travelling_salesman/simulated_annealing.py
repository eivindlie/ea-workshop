from typing import List
import random
from scipy.special import expit
from travelling_salesman.plotting import plot_history, plot_route
from .environment import City, Fitness, initialize_random_environment


def create_random_route(cities: List[City]) -> List[City]:
    route = random.sample(cities, len(cities))
    return route


def get_neighbours(solution: List[City]) -> List[List[City]]:
    neighbours = []

    for i in range(len(solution) - 1):
        neighbour = [x for x in solution]
        neighbour[i], neighbour[i + 1] = neighbour[i + 1], neighbour[i]
        neighbours.append(neighbour)

    return neighbours


def evaluate(solutions: List[List[City]]) -> List[Fitness]:
    return [Fitness(x) for x in solutions]


def select(current_solution: Fitness, solutions: List[Fitness], temp: float) -> Fitness:
    next_solution = random.sample(solutions, 1)[0]
    if next_solution.fitness > current_solution.fitness:
        return next_solution
    elif random.random() < expit(
        (next_solution.fitness - current_solution.fitness) / temp
    ):
        return next_solution
    return current_solution


def next_generation(cur_solution: List[City], temp: float) -> List[City]:
    neighbours = get_neighbours(cur_solution)
    fitness = evaluate(neighbours)
    next_gen = select(Fitness(cur_solution), fitness, temp)

    return next_gen.route


def exponential_multiplicative_decay(initial_value, decay):
    return lambda t: initial_value * decay ** t


def solve(
    cities: List[City],
    generations: int = 500,
    eval_frequency: int = 50,
    show_plots: bool = True,
    temperature_function=None,
) -> Fitness:
    if temperature_function == None:
        temperature_function = exponential_multiplicative_decay(40, 0.95)

    initial_solution = create_random_route(cities)
    best_initial_solution = evaluate([initial_solution])[0]
    print(f"Initial distance: {best_initial_solution.distance}")
    if show_plots:
        plot_route(best_initial_solution, "Initial")

    solution = initial_solution
    history = [(0, best_initial_solution)]

    for g in range(generations):
        temp = temperature_function(g)
        solution = next_generation(solution, temp)

        if (g + 1) % eval_frequency == 0:
            best_current_solution = evaluate([solution])[0]
            history.append((g, best_current_solution))
            print(f"[{g+1}/{generations}] Distance: {best_current_solution.distance}")

            if show_plots:
                plot_route(best_current_solution.route, f"Generation {g + 1}")

    best_final_solution = evaluate([solution])[0]
    print(f"Final distance: {best_final_solution.distance}")
    plot_history(history)
    plot_route(best_final_solution.route, "Final solution")

    return best_final_solution.route


def main():
    cities = initialize_random_environment()

    best_route = solve(
        cities,
        generations=2500,
        eval_frequency=200,
        show_plots=False,
        temperature_function=exponential_multiplicative_decay(100, 0.99),
    )


if __name__ == "__main__":
    main()
