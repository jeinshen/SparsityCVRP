from algorithm.NeighbourhoodSearch import Relocate
from entities.Parameters import Parameters
from entities.Solution import Solution


class VariableNeighbourhoodSearch:

    def __init__(self):
        self.relocate_search = Relocate()

    def solve(self, solution: Solution, changes_allowed: int):
        count = 0
        while True:
            best_local_move = self.relocate_search.find_best_feasible_local_move(solution)
            if best_local_move is None: break
            best_local_move.apply(solution)
            count += 1
            if count >= changes_allowed: break

        return solution