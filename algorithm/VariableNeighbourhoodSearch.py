from algorithm.NeighbourhoodSearch import Relocate
from entities.Solution import Solution


class VariableNeighbourhoodSearch:

    def __init__(self, solution: Solution):
        self.solution = solution

    def solve(self):
        relocate_search = Relocate()
        count = 0
        while True:
            best_local_move = relocate_search.find_best_feasible_local_move(self.solution)
            if best_local_move is None: break
            best_local_move.apply(self.solution)
            count += 1
            if count > 30: break

        return self.solution