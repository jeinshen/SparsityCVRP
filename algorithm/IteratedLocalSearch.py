import random
from copy import deepcopy

from numpy.random import choice
import math

from algorithm.NeighbourhoodSearch import Relocate
from entities.Solution import Solution


def select_random_move_weight(candidate_list):
    delta_gain = [math.exp(-candidate.delta_gain) for candidate in candidate_list]
    total_weight = sum(delta_gain)
    norm_prob = [float(i) / total_weight for i in delta_gain]
    return choice(candidate_list, size=1, p=norm_prob)[0]

def select_random_move_reverse_weight(candidate_list):
    delta_gain = [math.exp(candidate.delta_gain) for candidate in candidate_list]
    ## total_weight = sum(delta_gain)
    norm_prob = [1 / len(delta_gain) for i in delta_gain]
    return choice(candidate_list, size=1, p=norm_prob)[0]

def temperature_schedule(iteration, max_iterations):
    return max(0.005, min(1, 1 - iteration / max_iterations))

class IteratedLocalSearch:

    def __init__(self, solution: Solution):
        self.solution = solution
        self.best_solution = deepcopy(self.solution)

    def __run_iteration(self):
        return

    def solve(self):
        relocate_search = Relocate()
        count = 0
        iteration = 0
        accepted_moves = []
        current_best_cost = 1000000000
        best_solution = deepcopy(self.solution)
        while True:
            if iteration == 30:
                print(iteration)
            temperature = temperature_schedule(iteration, 3000)
            if count >= 30:
                reversed_move_count = 0
                try_count = 0
                while reversed_move_count < 10:
                    move_to_be_reversed = select_random_move_reverse_weight(accepted_moves)
                    reversed_move = move_to_be_reversed.reverse_move()
                    try_count += 1
                    if reversed_move.is_local_move_feasible(self.solution):
                        accepted_moves.remove(move_to_be_reversed)
                        reversed_move.apply(self.solution)
                        count -= 1
                        reversed_move_count += 1
                    if try_count >= 100:
                        break
            if count < 3000:
                selected_move = relocate_search.find_best_feasible_local_move(self.solution)
                current_solution_cost = self.solution.get_total_travel_distance()
                new_solution_cost = current_solution_cost + selected_move.delta_gain
            else:
                all_local_candidates = relocate_search.find_feasible_local_moves(self.solution)
                selected_move = select_random_move_weight(all_local_candidates)
                current_solution_cost = self.solution.get_total_travel_distance()
                new_solution_cost = current_solution_cost + selected_move.delta_gain

            iteration += 1
            if new_solution_cost < current_solution_cost or random.random() < math.exp(
                    (current_solution_cost - new_solution_cost) / temperature):
                accepted_moves.append(selected_move)
                selected_move.apply(self.solution)
                count += 1
                if (self.solution.get_total_travel_distance() < current_best_cost):
                    current_best_cost = self.solution.get_total_travel_distance()
                    print(current_best_cost)
            if iteration > 3000: break

        return self.solution

