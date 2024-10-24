from abc import ABC, abstractmethod

from algorithm.LocalMove import LocalMove, LocalChange
from entities import Solution
from entities.NetworkEntities import Node


def if_node_is_start_point(node: Node):
    return node.demand == 0 and node.x_coord == 0 and node.y_coord == 0


class NeighbourhoodSearch(ABC):

    @abstractmethod
    def find_best_feasible_local_moves(self, solution: Solution):
        pass

class Relocate(NeighbourhoodSearch):
    def find_best_feasible_local_moves(self, solution: Solution):
        best_relocate = None
        best_saving = None
        for truck in solution.get_trucks():
            for node in truck.visited_node:
                node_index = truck.visited_node.index(node)
                if if_node_is_start_point(node): continue
                additional_distance_remove = truck.additional_distance_if_remove(node)
                Solution.remove_node_visit(truck, node)
                for new_truck in solution.get_trucks():
                    if not new_truck.feasible_to_pick_node(node): continue
                    total_visited_nodes = len(new_truck.visited_node)
                    for insert_index in range(1, total_visited_nodes):
                        additional_distance_add = new_truck.additional_distance_if_visit(node, insert_index)
                        distance_saving = additional_distance_add + additional_distance_remove
                        if (distance_saving < 0) and (best_saving is None or best_saving > distance_saving):
                            local_move = LocalMove()
                            local_move.add_local_change(LocalChange(truck, node_index, node, new_truck, insert_index))
                            best_relocate = local_move
                            best_saving = distance_saving
                truck.insert_node(node, node_index)
        return best_relocate
