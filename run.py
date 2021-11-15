from data_reader import read_file, setup_model
import sys

from data_structs import Solution
from utils import generate_initial_solution

def start():
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = 'input.json'
    data = read_file(file_name)
    model = setup_model(data)
    
    solution = Solution()
    solution.nodes_seq = generate_initial_solution(model.node_seq_no_list)
    

if __name__ == '__main__':
    start()