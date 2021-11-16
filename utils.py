import math
import random
from itertools import tee
import copy

from data_structs import Model

def chunker_list(seq, size):
    return (seq[i::size] for i in range(size))

def generate_initial_solution(model: Model):
    clients = copy.deepcopy(model.node_list)
    random.shuffle(clients)
    groups = list(chunker_list(clients, model.no_of_vehicles))

    if all([validate_capacity(path, model.vehicle_cap) for path in groups]):
        return [[model.depot] + group + [model.depot] for group in groups]
    else:
        return generate_initial_solution(model)


def validate_capacity(path, available_capacity):
    demand = 0
    for client in path:
        demand += client.demand

    return demand <= available_capacity


def epsilon(candidate_list_of_paths, best_list_of_path, temperature):
    return math.exp((fitness(candidate_list_of_paths) - fitness(best_list_of_path)) / temperature)


def fitness(list_of_paths):
    res = 0
    for path in list_of_paths:
        path_dist = 0
        left, right = tee(path)
        for node1, node2 in zip(left, list(right)[1:]):
            path_dist += distance(node1, node2)
        res += path_dist
    
    return res


def distance(node1, node2):
    x1, y1 = node1.x_coord, node1.y_coord
    x2, y2 = node2.x_coord, node2.y_coord
    return math.sqrt((x1-x2)**2+(y1-y2)**2)
