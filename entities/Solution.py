from typing import List

from entities.NetworkEntities import Truck, Node


def remove_node_visit(truck: Truck, node: Node):
    return truck.remove_node(node)


class Solution:


    def __init__(self):
        self.all_truck = []

    def add_truck(self, truck):
        self.all_truck.append(truck)

    def get_trucks(self) -> List[Truck]:
        return self.all_truck

    def get_total_travel_distance(self):
        return sum(truck.traveled_distance for truck in self.all_truck)

    def get_number_of_trucks(self):
        return len(self.all_truck)

