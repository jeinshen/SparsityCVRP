import math

class Node:

    def __init__(self, x_coord, y_coord, demand, node_id):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.demand = demand
        self.node_id = node_id
        self.hashcode = hash((self.x_coord, self.y_coord, self.demand))

    def get_distance_to(self, other_node):
        return math.sqrt((self.x_coord - other_node.x_coord) ** 2 + (self.y_coord - other_node.y_coord) ** 2)

    def __hash__(self):
        return self.hashcode

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.__hash__() == other.__hash__()

class Truck:

    def __init__(self, capacity, truck_id):
        self.capacity = capacity
        self.used_capacity = 0
        self.visited_node = [Node(0, 0, 0, 1)]
        self.traveled_distance = 0
        self.truck_id = truck_id
        self.hashcode = hash(self.truck_id)
    def __hash__(self):
        return self.hashcode

    def __eq__(self, other):
        if not isinstance(other, Truck):
            return False
        return self.__hash__() == other.__hash__()

    def get_remaining_capacity(self):
        return self.capacity - self.used_capacity

    def visit_node(self, node: Node):
        self.used_capacity += node.demand
        self.traveled_distance += node.get_distance_to(self.visited_node[-1])
        self.visited_node.append(node)

    def back_to_start_node(self):
        start_node = Node(0, 0, 0, 1)
        self.traveled_distance += start_node.get_distance_to(self.visited_node[-1])
        self.visited_node.append(start_node)

    def feasible_to_pick_node(self, node: Node):
        return self.get_remaining_capacity() >= node.demand

    def get_distance_to_new_node(self, node: Node):
        return self.visited_node[-1].get_distance_to(node)

    def remove_node(self, node: Node) -> bool:
        index = self.visited_node.index(node)
        ## we can't remove a node if (1) it is not in the visited node or (2) it is the start node.
        if index == -1 or index == 0 or index == len(self.visited_node): return False
        self.used_capacity -= node.demand
        pre_distance_leg_1 = self.visited_node[index - 1].get_distance_to(node)
        pre_distance_leg_2 = self.visited_node[index + 1].get_distance_to(node)
        self.traveled_distance -= (pre_distance_leg_1 + pre_distance_leg_2)
        self.traveled_distance += self.visited_node[index - 1].get_distance_to(self.visited_node[index + 1])
        self.visited_node.remove(node)

    def insert_node(self, node: Node, index: int) -> bool:
        self.used_capacity += node.demand
        new_distance_leg_1 = self.visited_node[index - 1].get_distance_to(node)
        new_distance_leg_2 = self.visited_node[index].get_distance_to(node)
        self.traveled_distance += (new_distance_leg_1 + new_distance_leg_2)
        self.traveled_distance -= self.visited_node[index - 1].get_distance_to(self.visited_node[index])
        self.visited_node.insert(index, node)

    def additional_distance_if_visit(self, node: Node, index: int):
        new_distance_leg_1 = self.visited_node[index - 1].get_distance_to(node)
        new_distance_leg_2 = self.visited_node[index].get_distance_to(node)
        old_distance = self.visited_node[index - 1].get_distance_to(self.visited_node[index])
        return new_distance_leg_1 + new_distance_leg_2 - old_distance

    def additional_distance_if_remove(self, node: Node):
        index = self.visited_node.index(node)
        if index == -1: return 0
        old_distance_leg_1 = self.visited_node[index - 1].get_distance_to(node)
        old_distance_leg_2 = self.visited_node[index + 1].get_distance_to(node)
        new_distance = self.visited_node[index - 1].get_distance_to(self.visited_node[index + 1])
        return new_distance - old_distance_leg_1 - old_distance_leg_2