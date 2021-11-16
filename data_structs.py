class Node:
    def __init__(self, no, name, demand, x_coord, y_coord) -> None:
        self.no = no
        self.name = name
        self.demand = demand
        self.x_coord = x_coord
        self.y_coord = y_coord


class Model:
    def __init__(self, vehicle_cap, depot, no_of_vehicles) -> None:
        self.depot = depot
        self.vehicle_cap = vehicle_cap
        self.no_of_vehicles = no_of_vehicles
        self.node_list = []
