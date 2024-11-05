import os

import vrplib


class SolutionWriter:
    def __init__(self):
        self.folder_path = './data/result/'
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

    def write(self, solution, instance_name, solution_type):
        instance_name_without_path = os.path.basename(os.path.normpath(instance_name))
        solution_loc = "{}{}_{}{}".format(self.folder_path, instance_name_without_path, solution_type, '.sol')
        routes = []
        vehicle_types = []

        for truck in solution.get_trucks():
            vehicle_types.append(truck.truck_id)
            truck_route = []
            for node in truck.visited_node:
                truck_route.append(node.node_id)
            routes.append(truck_route)
        solution_data = {"Cost": solution.get_total_travel_distance(), "Vehicle types": vehicle_types}
        vrplib.write_solution(solution_loc, routes, solution_data)



