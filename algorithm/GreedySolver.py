from entities.NetworkEntities import Node, Truck
from entities.Solution import Solution


class GreedySolver:

    global_truck_id = 1

    def solve(self, instance):
        self.instance = instance
        self.solution = Solution()
        self.truck_capacity = self.instance['capacity']
        self.not_visited_node = []
        self.__build_all_nodes()
        self.__visit_node_in_greedy()
        return self.solution

    def __visit_node_in_greedy(self):
        while len(self.not_visited_node) != 0:
            new_truck = Truck(capacity=self.truck_capacity, truck_id=self.global_truck_id)
            self.global_truck_id += 1
            while True:
                best_node = self.__find_node_to_visit_in_greedy_way(new_truck)
                if best_node is None:
                    new_truck.back_to_start_node()
                    self.solution.add_truck(new_truck)
                    break
                new_truck.visit_node(best_node)
                self.not_visited_node.remove(best_node)


    def __build_all_nodes(self):
        for node_index in range(len(self.instance['node_coord'])):
            coord = self.instance['node_coord'][node_index]
            demand = self.instance['demand'][node_index]
            if demand == 0.0: continue
            self.not_visited_node.append(Node(coord[0], coord[1], demand, node_index + 1))

    def __find_node_to_visit_in_greedy_way(self, truck):
        best_node_to_visit = None
        best_node_distance = None
        for node in self.not_visited_node:
            if not truck.feasible_to_pick_node(node): continue
            distance = truck.get_distance_to_new_node(node)
            if best_node_distance is None or distance < best_node_distance:
                best_node_distance = distance
                best_node_to_visit = node
        return best_node_to_visit

