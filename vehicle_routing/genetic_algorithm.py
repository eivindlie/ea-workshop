from typing import List
import random
from .environment import Environment, City, plot_solution


def create_random_solution(environment: Environment) -> List[int]:
    solution = [i for i in range(len(environment.cities))] + \
               [-i for i in range(1, environment.num_vehicles)]
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


def main():
    environment = Environment(num_cities=25, num_vehicles=5, seed=None)
    solution = decode_solution(create_random_solution(environment), environment)
    plot_solution(solution, environment)




if __name__ == "__main__":
    main()
