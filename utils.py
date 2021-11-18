import json
import random
import copy


def chunker_list(seq, size):
    return (seq[i::size] for i in range(size))


def generate_initial_solution(model):
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


def strategy_one(model):
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


def prepare_solution(model, strategy):
    function = STRATEGIES[strategy]
    return function(model)


def prepare_output(model, output_file):
    res = []
    for result in model.results:
        row = {
            'epoch': result.epoch,
            'attempt': result.attempt,
            'temp': result.temp,
            'paths': [[{"city": node.name, "x": node.x_coord, "y": node.y_coord} for node in path] for path in result.result],
            'current_value': model.fitness(result.result),
            'current_best_known_value': model.fitness(result.current_best_known),
            'best_attempt_value': model.fitness(result.best_of_the_attempt),
        }
        res.append(row)
    print('Proszę czekać, trwa zapisywanie pliku')
    with open(output_file, 'wt', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False)
    print('Zakończono')
