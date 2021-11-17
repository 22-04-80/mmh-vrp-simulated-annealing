import math
from itertools import tee


class Node:
    def __init__(self, no, name, demand, x_coord, y_coord) -> None:
        self.no = no
        self.name = name
        self.demand = demand
        self.x_coord = x_coord
        self.y_coord = y_coord


class Model:
    def __init__(self, vehicle_cap, depot, no_of_vehicles) -> None:
        self.depot = depot
        self.vehicle_cap = vehicle_cap
        self.no_of_vehicles = no_of_vehicles
        self.node_list = []
        self.best_known_solution = None
        self.__current_best_solution = None
        self.first_solution = None
    
    @property
    def current_best_solution(self):
        return self.__current_best_solution

    @current_best_solution.setter
    def current_best_solution(self, solution):
        self.__current_best_solution = solution
        if self.best_known_solution is None:
            self.best_known_solution = solution
        elif self.fitness(solution) < self.fitness(self.best_known_solution):
            self.best_known_solution = solution
    
    @staticmethod
    def distance(node1, node2):
        x1, y1 = node1.x_coord, node1.y_coord
        x2, y2 = node2.x_coord, node2.y_coord
        return math.sqrt((x1-x2)**2+(y1-y2)**2)

    @staticmethod
    def fitness(list_of_paths):
        res = 0
        for path in list_of_paths:
            path_dist = 0
            left, right = tee(path)
            for node1, node2 in zip(left, list(right)[1:]):
                path_dist += Model.distance(node1, node2)
            res += path_dist
        
        return res

    @staticmethod
    def epsilon(candidate_list_of_paths, best_list_of_path, temperature):
        return math.exp((Model.fitness(candidate_list_of_paths) - Model.fitness(best_list_of_path)) / temperature)