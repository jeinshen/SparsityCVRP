from dataclasses import dataclass

from entities.NetworkEntities import Truck, Node

@dataclass
class LocalChange:
    truckCurrent: Truck
    originalIndex: int
    node: Node
    truckNew: Truck
    position: int

class LocalMove:

    def __init__(self):
        self.local_changes_in_order = []

    def add_local_change(self, local_change: LocalChange):
        self.local_changes_in_order.append(local_change)

    def apply(self, solution) -> bool:
        for local_change in self.local_changes_in_order:
            if (local_change.truckCurrent not in solution.get_trucks() or
                    local_change.truckNew not in solution.get_trucks()) :
                return False
            local_change.truckCurrent.remove_node(local_change.node)
            local_change.truckNew.insert_node(local_change.node, local_change.position)
            return True
