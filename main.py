import vrplib

from algorithm.GreedySolver import GreedySolver

## For now let's use one example for testing
instance = vrplib.read_instance("./data/Li/Li_21.vrp")
solution = vrplib.read_solution("./data/Li/Li_21.sol")

greedy_solver = GreedySolver()
our_solution = greedy_solver.solve(instance)
print(our_solution.get_total_travel_distance())
print(our_solution.get_number_of_trucks())
print("best result " + str(solution['cost']))
print("best result " + str(len(solution['routes'])))
