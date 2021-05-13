import sys
from travelling_salesman.genetic_algorithm import main as tsp_ga

if __name__ == "__main__":
    if sys.argv[1] in ["tsp", "travelling_salesman"]:
        tsp_ga()
