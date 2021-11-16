import random
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


def strategy_one(model: Model):
    """Mieszanie miast tylko w ramach jednej ścieżki"""
    paths = copy.deepcopy(model.current_best_solution)
    result = []
    for path in paths:
        path = path[1:-1]
        random.shuffle(path)
        path = [model.depot] + path + [model.depot]
        result.append(path)
    return result


def strategy_two(model):
    """Mieszanie miast między ścieżkami"""
    pass


def strategy_three(model):
    """Losowe przenoszenie miast"""
    pass


STRATEGIES = [strategy_one, strategy_two, strategy_three]

def prepare_solution(model: Model, strategy=0):
    function = STRATEGIES[strategy]
    return function(model)
