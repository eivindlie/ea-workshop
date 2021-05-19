import sys
from travelling_salesman.genetic_algorithm import main as tsp_ga
from travelling_salesman.hill_climbing import main as tsp_hc
from travelling_salesman.simulated_annealing import main as tsp_sa

from vehicle_routing.genetic_algorithm import main as vrp_ga
from vehicle_routing.map_elites import main as vrp_me

if __name__ == "__main__":
    if sys.argv[1] in ["tsp", "travelling_salesman"]:
        if len(sys.argv) > 2:
            if sys.argv[2] in ["hc", "hill_climbing"]:
                tsp_hc()
            elif sys.argv[2] in ["ga", "genetic_algorithm"]:
                tsp_ga()
            elif sys.argv[2] in ["sa", "simulated_annealing"]:
                tsp_sa()
        else:
            tsp_ga()
    elif sys.argv[1] in ["vrp", "vehicle_routing"]:
        if len(sys.argv) > 2:
            if sys.argv[2] in ["ga", "genetic_algorithm"]:
                vrp_ga()
            elif sys.argv[2] in ["me", "map-elites"]:
                vrp_me()
        else:
            vrp_ga()
