from data_reader import read_file, setup_model
import sys
from random import uniform

from utils import generate_initial_solution, prepare_solution

def start():
    TEMP = 100
    COOLING_FACTOR = 0.90
    EPOCHS = 1000
    ATTEMPTS = 500
    MINIMAL_TEMP = 5
    
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = 'input.json'
    data = read_file(file_name)
    model = setup_model(data)

    model.current_best_solution = generate_initial_solution(model)
    model.first_solution = model.current_best_solution

    for _ in range(EPOCHS):
        for _ in range(ATTEMPTS):

            candidate_list_of_paths = prepare_solution(model)
            
            if model.fitness(candidate_list_of_paths) < model.fitness(model.current_best_solution):
                model.current_best_solution = candidate_list_of_paths

            elif uniform(0, 1) < model.epsilon(candidate_list_of_paths, model.current_best_solution, TEMP):
                model.current_best_solution = candidate_list_of_paths
            
            print('.', sep='', end='', flush=True)
        
        if TEMP <= MINIMAL_TEMP:
            break
        TEMP *= COOLING_FACTOR
        print('current temp:', TEMP)
    
    print('first solution:', model.fitness(model.first_solution))
    print('current best distance:', model.fitness(model.current_best_solution))
    print('best known distance:', model.fitness(model.best_known_solution))
    print('TEMP:', TEMP)
    

if __name__ == '__main__':
    start()