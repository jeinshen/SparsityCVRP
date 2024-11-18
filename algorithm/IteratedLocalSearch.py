from copy import deepcopy

import numpy as np
import math

from algorithm.NeighbourhoodSearch import Relocate
from entities.Parameters import Parameters
from entities.Solution import Solution


def select_random_move_weight(candidate_list):
    delta_gain = [np.exp(-candidate.delta_gain/100 + 0.001) + 1 for candidate in candidate_list]
    total_weight = sum(delta_gain)
    norm_prob = [float(i) / total_weight for i in delta_gain]
    return np.random.choice(candidate_list, size=1, p=norm_prob)[0]

def select_random_move_reverse_weight(candidate_list):
    # delta_gain = [np.exp(candidate.delta_gain/100) for candidate in candidate_list]
    # total_weight = sum(delta_gain)
    norm_prob = [1 / len(candidate_list) for _ in candidate_list]
    return np.random.choice(candidate_list, size=1, p=norm_prob)[0]

def temperature_schedule(iteration, max_iterations):
    return max(0.005, min(1, 1 - iteration / max_iterations))

class IteratedLocalSearch:

    def __init__(self, solution: Solution, logging, changes_allowed: int):
        self.current_solution = solution
        self.changes_allowed = changes_allowed
        self.best_solution = deepcopy(self.current_solution)
        self.best_solution_accepted_moves = []
        np.random.seed(Parameters.random_seed)
        self.iteration_without_improvement = 0
        self.logging = logging

    def __run_iteration(self, iteration):
        relocate_search = Relocate()
        temperature = temperature_schedule(iteration, Parameters.max_ils_iterations)
        accepted_moves = list(self.best_solution_accepted_moves)
        count_current_changes = len(accepted_moves)
        if count_current_changes >= self.changes_allowed:
            reversed_move_count = 0
            try_count = 0
            while reversed_move_count < 10:
                move_to_be_reversed = select_random_move_reverse_weight(accepted_moves)
                reversed_move = move_to_be_reversed.reverse_move()
                try_count += 1
                if reversed_move.is_local_move_feasible(self.current_solution):
                    accepted_moves.remove(move_to_be_reversed)
                    reversed_move.apply(self.current_solution)
                    count_current_changes -= 1
                    reversed_move_count += 1
                if try_count >= 100:
                    break
        while count_current_changes < self.changes_allowed:
            try_count = 0
            if iteration < 2000:
                selected_move = relocate_search.find_best_feasible_local_move(self.current_solution)
            else:
                all_local_candidates = relocate_search.find_feasible_local_moves(self.current_solution)
                all_local_candidates_filtered = [x for x in all_local_candidates if not np.isnan(x.delta_gain)]
                if len(all_local_candidates_filtered) == 0:
                    break
                selected_move = select_random_move_weight(all_local_candidates_filtered)

            if isinstance(selected_move, type(None)):
                break
            accepted_moves.append(selected_move)
            selected_move.apply(self.current_solution)
            count_current_changes += 1
            try_count += 1
            if try_count >= 100:
                break

        new_solution_cost = self.current_solution.get_total_travel_distance()
        current_solution_cost = self.best_solution.get_total_travel_distance()
        if new_solution_cost < current_solution_cost or np.random.random() < math.exp(
                (current_solution_cost - new_solution_cost) / temperature):
            if new_solution_cost < current_solution_cost:
                self.best_solution = deepcopy(self.current_solution)
                self.best_solution_accepted_moves = accepted_moves
            self.iteration_without_improvement = 0
        else:
            self.iteration_without_improvement += 1
            if self.iteration_without_improvement >= 30:
                self.current_solution = deepcopy(self.best_solution)
        iteration += 1
        return iteration

    def solve(self):
        iteration = 0
        while True:
            if iteration % 100 == 0:
                self.logging.info("current {} iterations of ils, best solution at {}".format(
                    iteration, self.best_solution.get_total_travel_distance()))
            iteration = self.__run_iteration(iteration)
            if iteration > Parameters.max_ils_iterations: break

        return self.best_solution

