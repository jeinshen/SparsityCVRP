import os

import pandas as pd
import vrplib

from algorithm.IteratedLocalSearch import IteratedLocalSearch
from algorithm.VariableNeighbourhoodSearch import VariableNeighbourhoodSearch
from algorithm.GreedySolver import GreedySolver

def find_all_run_cases(folder_path, extension):
    # Ensure the extension starts with a dot
    if not extension.startswith('.'):
        extension = '.' + extension

    # Use a list comprehension to find all matching files
    matching_files = [
        os.path.join(root, filename)
        for root, _, files in os.walk(folder_path)
        for filename in files
        if filename.endswith(extension)
    ]

    return [os.path.splitext(file)[0] for file in matching_files]

instances = find_all_run_cases("./data/Li/", "vrp" )
result_df = pd.DataFrame(columns=["instance", "initial solution", "greedy pick solution", "ILS solution"])

for instance in instances:

    print("solve for instance " + instance)

    ## For now let's use one example for testing
    instance_definition = vrplib.read_instance(instance + ".vrp")
    solution = vrplib.read_solution(instance + ".sol")

    greedy_solver = GreedySolver()
    greedy_solution = greedy_solver.solve(instance_definition)
    initial_solution_cost = greedy_solution.get_total_travel_distance()

    greedy_pick = VariableNeighbourhoodSearch(greedy_solution)
    greedy_pick_solution = greedy_pick.solve()
    greedy_pick_solution_cost = greedy_pick_solution.get_total_travel_distance()

    ils_pick = IteratedLocalSearch(greedy_solution)
    iterated_local_search_solution = ils_pick.solve()
    ils_solution_cost = iterated_local_search_solution.get_total_travel_distance()
    result_df.loc[len(result_df)] = pd.Series({"instance": instance, "initial solution" : initial_solution_cost,
                                  "greedy pick solution" : greedy_pick_solution_cost,
                                  "ILS solution" : ils_solution_cost})

result_df.to_csv("./data/Li/result_df.csv")