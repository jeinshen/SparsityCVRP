from dataclasses import dataclass

from entities.NetworkEntities import Truck, Node

@dataclass
class LocalChange:
    truck_current: Truck
    original_index: int
    node: Node
    truck_new: Truck
    position: int

class LocalMove:

    def __init__(self):
        self.local_changes_in_order = []
        self.delta_gain = 0

    def add_local_change(self, local_change: LocalChange):
        self.local_changes_in_order.append(local_change)

    def set_delta_gain(self, delta_gain: float):
        self.delta_gain = delta_gain

    def apply(self, solution) -> bool:
        for local_change in self.local_changes_in_order:
            if (local_change.truck_current not in solution.get_trucks() or
                    local_change.truck_new not in solution.get_trucks()) :
                return False
            local_change.truck_current.remove_node(local_change.node)
            local_change.truck_new.insert_node(local_change.node, local_change.position)
            return True

    def reverse_move(self):
        reversed_change = LocalMove()
        for local_change in self.local_changes_in_order[::-1]:
            reversed_local_move = LocalChange(local_change.truck_new, local_change.position, local_change.node,
                                              local_change.truck_current, local_change.original_index)
            reversed_change.add_local_change(reversed_local_move)
        return reversed_change

    def is_local_move_feasible(self, solution) -> bool:
        for local_change in self.local_changes_in_order:
            if (local_change.truck_current not in solution.get_trucks()
                    or local_change.truck_new not in solution.get_trucks()):
                return False
            if (local_change.node not in local_change.truck_current.visited_node
                    or len(local_change.truck_new.visited_node) <= local_change.position+2):
                return False
        return True