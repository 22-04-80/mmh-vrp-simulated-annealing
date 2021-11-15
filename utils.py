import math
import random


def generate_initial_solution(node_seq, seed=None):
    if seed:
        random.seed(seed)
    else:
        random.seed(0)
    random.shuffle(node_seq)
    return node_seq