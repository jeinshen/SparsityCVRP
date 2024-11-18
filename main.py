import math
import os
from copy import deepcopy

import pandas as pd
import vrplib

from algorithm.IteratedLocalSearch import IteratedLocalSearch
from algorithm.VariableNeighbourhoodSearch import VariableNeighbourhoodSearch
from algorithm.GreedySolver import GreedySolver
from entities.Parameters import Parameters
from writers.SolutionWriter import SolutionWriter

import logging

folder_path = './data/result/'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
logging.basicConfig(filename='./data/result/run.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


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

## Initialise env
instances = find_all_run_cases("./data/Li/", "vrp" )
result_df = pd.DataFrame(columns=["instance", "initial solution", "greedy pick solution", "ILS solution"])
greedy_solver = GreedySolver()
vnd_solver = VariableNeighbourhoodSearch()

for instance in instances:

    logging.info("solve for instance {}".format(instance))
    ## Step 1: read in instance and best solution
    instance_definition = vrplib.read_instance(instance + ".vrp")
    best_solution = vrplib.read_solution(instance + ".sol")
    instance_size = instance_definition['dimension']
    changes_allowed = math.floor(instance_size * Parameters.max_changes)

    ## Step 2: build the initial solution
    logging.info("solve for instance {} using greedy to build initial solution".format(instance))
    greedy_solution = greedy_solver.solve(instance_definition)
    initial_solution_cost = greedy_solution.get_total_travel_distance()
    SolutionWriter().write(greedy_solution, instance, "initial_solution")

    ## Step 3: solve for vnd pick
    logging.info("solve for instance {} using vnd".format(instance))
    initial_solution = deepcopy(greedy_solution)
    vnd_solution = vnd_solver.solve(initial_solution, changes_allowed)
    vnd_solution_cost = vnd_solution.get_total_travel_distance()
    SolutionWriter().write(vnd_solution, instance, "vnd_solution")
    logging.info("solved for instance {} using vnd, at total cost of {}".format(instance, vnd_solution_cost))

    ## Step 4: solve for ils
    logging.info("solve for instance {} using ils".format(instance))
    initial_solution_ils = deepcopy(greedy_solution)
    ils_pick = IteratedLocalSearch(initial_solution_ils, logging, instance_size)
    iterated_local_search_solution = ils_pick.solve()
    ils_solution_cost = iterated_local_search_solution.get_total_travel_distance()
    SolutionWriter().write(iterated_local_search_solution, instance, "ils_solution")
    result_df.loc[len(result_df)] = pd.Series({"instance": instance, "initial solution" : initial_solution_cost,
                                  "greedy pick solution" : vnd_solution_cost,
                                  "ILS solution" : ils_solution_cost})

    ## ongoing writing to monitor the finished instances
    result_df.to_csv("./data/result/result_df.csv")