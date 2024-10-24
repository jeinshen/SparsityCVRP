import math


class Node:

    def __init__(self, x_coord, y_coord, demand):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.demand = demand

    def get_distance_to(self, other_node):
        return math.sqrt((self.x_coord - other_node.x_coord) ** 2 + (self.y_coord - other_node.y_coord) ** 2)

class Truck:

    def __init__(self, capacity, truck_id):
        self.capacity = capacity
        self.used_capacity = 0
        self.visited_node = [Node(0, 0, 0)]
        self.traveled_distance = 0
        self.truck_id = truck_id

    def get_remaining_capacity(self):
        return self.capacity - self.used_capacity

    def visit_node(self, node: Node):
        self.used_capacity += node.demand
        self.traveled_distance += node.get_distance_to(self.visited_node[-1])
        self.visited_node.append(node)

    def back_to_start_node(self):
        start_node = Node(0, 0, 0)
        self.traveled_distance += start_node.get_distance_to(self.visited_node[-1])
        self.visited_node.append(start_node)

    def feasible_to_pick_node(self, node: Node):
        return self.get_remaining_capacity() >= node.demand

    def get_distance_to_new_node(self, node: Node):
        return self.visited_node[-1].get_distance_to(node)