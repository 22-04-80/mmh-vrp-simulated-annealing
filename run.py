from data_reader import read_file, setup_model
import sys
from random import uniform, randint
import random

from utils import generate_initial_solution, prepare_solution


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

    for _ in range(epochs):
        for _ in range(attempts):
            strategy = randint(0, 1)
            candidate_list_of_paths = prepare_solution(model, strategy)
            
            if model.fitness(candidate_list_of_paths) < model.fitness(model.current_best_solution):
                model.current_best_solution = candidate_list_of_paths

            elif uniform(0, 1) < model.epsilon(candidate_list_of_paths, model.current_best_solution, temp):
                model.current_best_solution = candidate_list_of_paths
            
            print('.', sep='', end='', flush=True)
        
        if temp <= minimal_temp:
            break
        temp *= cooling_factor
        print('current temp:', temp)
    
    print()
    print('first solution:', model.fitness(model.first_solution))
    print('current best distance:', model.fitness(model.current_best_solution))
    print('best known distance:', model.fitness(model.best_known_solution))
    print('temp:', temp)
    

if __name__ == '__main__':
    start()