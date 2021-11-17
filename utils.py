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


def strategy_two(model: Model):
    """Losowe przenoszenie miast między ścieżkami"""
    paths = copy.deepcopy(model.current_best_solution)
    random_origin_path = paths[random.randint(0, len(paths) - 1)]
    while len(random_origin_path) <= 3:
        # nie wyciągamy miasta ze ścieżki jeśli jest jedynym klientem
        random_origin_path = paths[random.randint(0, len(paths) - 1)]
    random_origin_node = random_origin_path.pop(random.randint(1, len(random_origin_path) - 2))
    
    while True:
        random_target_path = paths[random.randint(0, len(paths) - 1)]
        if len(random_target_path) == 2:
            # to oznacza że tylko baza jest w tej ścieżce
            index = 1
        else:
            index = random.randint(1, len(random_target_path) - 2)
        random_target_path.insert(index, random_origin_node)

        if validate_capacity(random_target_path, model.vehicle_cap):
            return paths
        else:
            random_target_path.pop(index)


STRATEGIES = [strategy_one, strategy_two]


def prepare_solution(model: Model, strategy):
    function = STRATEGIES[strategy]
    return function(model)
