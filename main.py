import itertools
import math
import os
from copy import deepcopy
import multiprocessing

import pandas as pd
import vrplib

from algorithm.IteratedLocalSearch import IteratedLocalSearch
from algorithm.VariableNeighbourhoodSearch import VariableNeighbourhoodSearch
from algorithm.GreedySolver import GreedySolver
from writers.SolutionWriter import SolutionWriter

import logging

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

def extend_instance(instances, testing_change_size):
    return list(itertools.product(instances, testing_change_size))


def run_one_instance(instance_name_and_change_size):
    instance_name = instance_name_and_change_size[0]
    logging.info("solve for instance {}".format(instance_name))
    ## Step 1: read in instance and best solution
    instance_definition = vrplib.read_instance(instance_name + ".vrp")
    instance_size = instance_definition['dimension']
    change_size = instance_name_and_change_size[1]
    changes_allowed = math.floor(instance_size * change_size)

    ## Step 2: build the initial solution
    logging.info("solve for instance {} using greedy to build initial solution".format(instance_name))
    greedy_solver = GreedySolver()
    vnd_solver = VariableNeighbourhoodSearch()
    greedy_solution = greedy_solver.solve(instance_definition)
    initial_solution_cost = greedy_solution.get_total_travel_distance()
    SolutionWriter().write(greedy_solution, instance_name, "initial_solution")

    ## Step 3: solve for vnd pick
    logging.info("solve for instance {} using vnd".format(instance_name))
    initial_solution = deepcopy(greedy_solution)
    vnd_solution = vnd_solver.solve(initial_solution, changes_allowed)
    vnd_solution_cost = vnd_solution.get_total_travel_distance()
    SolutionWriter().write(vnd_solution, instance_name, "vnd_solution")
    logging.info("solved for instance {} using vnd, at total cost of {}".format(instance_name, vnd_solution_cost))

    ## Step 4: solve for ils
    logging.info("solve for instance {} using ils".format(instance_name))
    initial_solution_ils = deepcopy(greedy_solution)
    ils_pick = IteratedLocalSearch(initial_solution_ils, changes_allowed, change_size)
    iterated_local_search_solution = ils_pick.solve()
    ils_solution_cost = iterated_local_search_solution.get_total_travel_distance()
    SolutionWriter().write(iterated_local_search_solution, instance_name, "ils_solution")
    return pd.Series({"instance": instance_name, "instance_size": instance_size,
                      "change_size": change_size,
                      "initial solution" : initial_solution_cost, "greedy pick solution" : vnd_solution_cost,
                      "ILS solution" : ils_solution_cost})


if __name__ == '__main__':

    folder_path = './data/result/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    logging.basicConfig(filename='./data/result/run.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    testing_change_size = [0.05, 0.1, 0.15]

    ## Initialise env
    instances = find_all_run_cases("./data/Li/", "vrp" )
    all_run_instances = extend_instance(instances, testing_change_size)
    result_df = pd.DataFrame(columns=["instance", "instance_size", "change_size", "initial solution",
                                      "greedy pick solution", "ILS solution"])
    with multiprocessing.Pool(processes=len(all_run_instances)) as pool:
        results = pool.map(run_one_instance, all_run_instances)
        for result_row in results:
            result_df.loc[len(result_df)] = result_row

    ## ongoing writing to monitor the finished instances
    result_df.to_csv("./data/result/result_df.csv")



