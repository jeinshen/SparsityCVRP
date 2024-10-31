import random
from copy import deepcopy

import numpy as np
from numpy.random import choice
import math

from algorithm.NeighbourhoodSearch import Relocate
from entities.Solution import Solution


def select_random_move_weight(candidate_list):
    delta_gain = [np.exp(-candidate.delta_gain + 0.001) for candidate in candidate_list]
    total_weight = sum(delta_gain)
    norm_prob = [float(i) / total_weight for i in delta_gain]
    return choice(candidate_list, size=1, p=norm_prob)[0]

def select_random_move_reverse_weight(candidate_list):
    delta_gain = [np.exp(candidate.delta_gain) for candidate in candidate_list]
    ## total_weight = sum(delta_gain)
    norm_prob = [1 / len(delta_gain) for i in delta_gain]
    return choice(candidate_list, size=1, p=norm_prob)[0]

def temperature_schedule(iteration, max_iterations):
    return max(0.005, min(1, 1 - iteration / max_iterations))

class IteratedLocalSearch:

    def __init__(self, solution: Solution):
        self.current_solution = solution
        self.best_solution = deepcopy(self.current_solution)
        self.best_solution_accepted_moves = []

    def __run_iteration(self, iteration, count_current_changes):
        relocate_search = Relocate()
        temperature = temperature_schedule(iteration, 3000)
        if count_current_changes >= 30:
            reversed_move_count = 0
            try_count = 0
            while reversed_move_count < 10:
                move_to_be_reversed = select_random_move_reverse_weight(self.best_solution_accepted_moves)
                reversed_move = move_to_be_reversed.reverse_move()
                try_count += 1
                if reversed_move.is_local_move_feasible(self.current_solution):
                    self.best_solution_accepted_moves.remove(move_to_be_reversed)
                    reversed_move.apply(self.current_solution)
                    count_current_changes -= 1
                    reversed_move_count += 1
                if try_count >= 100:
                    break
        while count_current_changes < 30:
            if iteration < 100:
                selected_move = relocate_search.find_best_feasible_local_move(self.current_solution)
            else:
                all_local_candidates = relocate_search.find_feasible_local_moves(self.current_solution)
                if len(all_local_candidates) == 0:
                    break
                selected_move = select_random_move_weight(all_local_candidates)

            self.best_solution_accepted_moves.append(selected_move)
            selected_move.apply(self.current_solution)
            count_current_changes += 1

        new_solution_cost = self.current_solution.get_total_travel_distance()
        current_solution_cost = self.best_solution.get_total_travel_distance()
        if new_solution_cost < current_solution_cost or random.random() < math.exp(
                (current_solution_cost - new_solution_cost) / temperature):
            if self.current_solution.get_total_travel_distance() < self.best_solution.get_total_travel_distance():
                self.best_solution = deepcopy(self.current_solution)
        iteration += 1
        return iteration, count_current_changes

    def solve(self):
        count = 0
        iteration = 0
        while True:
            iteration, count = self.__run_iteration(iteration, count)
            if iteration > 3000: break

        return self.best_solution
