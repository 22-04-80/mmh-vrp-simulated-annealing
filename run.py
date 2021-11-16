from data_reader import read_file, setup_model
import sys
from random import uniform

from utils import generate_initial_solution, epsilon, fitness

def start():
    TEMP = 100
    COOLING_FACTOR = 0.9
    EPOCHS = 1000
    ATTEMPTS = 500
    
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = 'input.json'
    data = read_file(file_name)
    model = setup_model(data)

    best_list_of_path = generate_initial_solution(model)

    for _ in range(EPOCHS):
        for _ in range(ATTEMPTS):

            candidate_list_of_paths = [[]]
            
            if fitness(candidate_list_of_paths) < fitness(best_list_of_path):
                best_list_of_path = candidate_list_of_paths

            elif uniform(0, 1) < epsilon(candidate_list_of_paths, best_list_of_path, TEMP):
                best_list_of_path = candidate_list_of_paths

        TEMP *= COOLING_FACTOR
    

if __name__ == '__main__':
    start()