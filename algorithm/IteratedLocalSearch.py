import random

from numpy.random import choice
import math

from algorithm.NeighbourhoodSearch import Relocate
from entities.Solution import Solution


def select_random_move_weight(candidate_list):
    delta_gain = [math.exp(-candidate.delta_gain) for candidate in candidate_list]
    norm_prob = [float(i) / sum(delta_gain) for i in delta_gain]
    return choice(candidate_list, size=1, p=norm_prob)[0]

def select_random_move_reverse_weight(candidate_list):
    delta_gain = [math.exp(candidate.delta_gain) for candidate in candidate_list]
    norm_prob = [float(i) / sum(delta_gain) for i in delta_gain]
    return choice(candidate_list, size=1, p=norm_prob)[0]

def temperature_schedule(iteration, max_iterations):
    return max(0.005, min(1, 1 - iteration / max_iterations))

class IteratedLocalSearch:

    def __init__(self, solution: Solution):
        self.solution = solution

    def solve(self):
        relocate_search = Relocate()
        count = 0
        iteration = 0
        accepted_moves = []
        while True:
            temperature = temperature_schedule(iteration, 500)
            if count >= 100:
                while True:
                    move_to_be_reversed = select_random_move_reverse_weight(accepted_moves)
                    reversed_move = move_to_be_reversed.reverse_move()
                    if reversed_move.is_local_move_feasible(self.solution):
                        reversed_move.apply(self.solution)
                        count -= 1
                        break
            if count < 90:
                selected_move = relocate_search.find_best_feasible_local_move(self.solution)
                current_solution_cost = self.solution.get_total_travel_distance()
                new_solution_cost = current_solution_cost + selected_move.delta_gain
                iteration += 1
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
                print(count)
                print(iteration)
                print(self.solution.get_total_travel_distance())
            if iteration > 500: break

        return self.solution

