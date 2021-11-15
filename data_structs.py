class Nodes:
    def __init__(self) -> None:
        self.nodes = []
        self.seq_no_list = []
    
    def add_client(self, client):
        self.nodes.append(client)
    
    def add_seq_no(self, seq_no):
        self.seq_no_list.append(seq_no)


class Node:
    def __init__(self, no, name, demand, x_coord, y_coord) -> None:
        self.no = no
        self.name = name
        self.demand = demand
        self.x_coord = x_coord
        self.y_coord = y_coord
    
    @property
    def seq_no(self):
        return self.no - 1


class Model:
    def __init__(self, vehicle_cap, depot) -> None:
        self.__node_list = []
        self.__depot = depot
        self.__vehicle_cap = vehicle_cap
        self.__node_seq_no_list = None
        self.__best_sol = None
    
    @property
    def node_list(self):
        return self.__node_list
    
    @node_list.setter
    def node_list(self, nodes):
        self.__node_list = nodes
    
    @property
    def number_of_nodes(self):
        return len(self.__node_list)
    
    @property
    def depot(self):
        return self.__depot
    
    @property
    def vehicle_cap(self):
        return self.__vehicle_cap

    @property
    def node_seq_no_list(self):
        return self.__node_seq_no_list
    
    @node_seq_no_list.setter
    def node_seq_no_list(self, seq_list):
        self.__node_seq_no_list = seq_list
    

class Solution:
    def __init__(self) -> None:
        self.obj = None
        self.routes = []