from data_reader import read_file, setup_model
import sys
from random import uniform, randint
import random

from utils import generate_initial_solution, prepare_solution, prepare_output


def start():
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = 'input.json'
    data = read_file(file_name)

    if not data['parameters']['random_seed']:
        random.seed(0)

    epochs = data['parameters']['epochs']
    attempts = data['parameters']['attempts']
    minimal_temp = data['parameters']['minimal_temp']
    cooling_factor = data['parameters']['cooling_factor']
    temp = data['parameters']['initial_temperature']

    model = setup_model(data)
    model.current_best_solution = generate_initial_solution(model)
    model.first_solution = model.current_best_solution

    for e in range(epochs):
        print('Epoch:', e+1)
        for a in range(attempts):
            if (a+1) % 50 == 0:
                print('\tAttempt:', a+1)
            strategy = randint(0, 1)
            candidate_list_of_paths = prepare_solution(model, strategy)
            
            if model.fitness(candidate_list_of_paths) < model.fitness(model.current_best_solution):
                model.current_best_solution = candidate_list_of_paths

            elif uniform(0, 1) < model.epsilon(candidate_list_of_paths, model.current_best_solution, temp):
                model.current_best_solution = candidate_list_of_paths

        if temp <= minimal_temp:
            break
        temp *= cooling_factor
        print('Najlepsze rozwiązanie epoki:', model.fitness(model.current_best_solution))
        print('New temperature:', temp)

    print()
    print('==========')
    print()
    print('Ostatnia temperatura:', temp)
    print('Pierwszy wynik:', model.fitness(model.first_solution))
    print('Pierwsze rozwiązanie:', [[node.name for node in path] for path in model.first_solution])
    print('Pierwsze rozwiązanie (zapotrzebowania):', [sum([node.demand for node in path]) for path in model.first_solution])
    print('Pierwsze rozwiązanie:', [sum([node.demand for node in path]) for path in model.first_solution])
    print('Najlepszy wynik:', model.fitness(model.best_known_solution))
    print('Najlepsze rozwiązanie:', [[node.name for node in path] for path in model.best_known_solution])
    print('Najlepsze rozwiązanie (zapotrzebowania):', [sum([node.demand for node in path]) for path in model.best_known_solution])

    prepare_output(model, 'results.json')


if __name__ == '__main__':
    start()