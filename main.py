import vrplib

from algorithm.IteratedLocalSearch import IteratedLocalSearch
from algorithm.VariableNeighbourhoodSearch import VariableNeighbourhoodSearch
from algorithm.GreedySolver import GreedySolver

## For now let's use one example for testing
instance = vrplib.read_instance("./data/Li/Li_24.vrp")
solution = vrplib.read_solution("./data/Li/Li_24.sol")

greedy_solver = GreedySolver()
our_solution = greedy_solver.solve(instance)
print("initial_solution " + str(our_solution.get_total_travel_distance()))
print("initial_solution " + str(our_solution.get_number_of_trucks()))
print("best result " + str(solution['cost']))
print("best result " + str(len(solution['routes'])))

greedy_pick = IteratedLocalSearch(our_solution)
new_solution = greedy_pick.solve()
print("new_solution " + str(new_solution.get_total_travel_distance()))
print("new_solution " + str(new_solution.get_number_of_trucks()))
