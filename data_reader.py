import json
import os

from data_structs import Node, Model

def read_file(file_name):
    inputs_dir = os.path.join(os.path.abspath(os.path.curdir), 'inputs')
    file_path = os.path.join(inputs_dir, file_name)
    with open(file_path) as fp:
        data = json.load(fp)
    return data

def setup_model(data):
    depot = Node(
            data['fleet']['depot']['no'], 
            data['fleet']['depot']['name'],
            data['fleet']['depot']['demand'],
            data['fleet']['depot']['x_coord'],
            data['fleet']['depot']['y_coord']
        )
    model = Model(
        data['fleet']['each_vehicle_capacity'],
        depot,
        data['fleet']['vehicles_no'], 
    )
    for client in data['clients']:
        client = Node(
            client['no'], 
            client['name'],
            client['demand'],
            client['x_coord'],
            client['y_coord']
        )
        model.node_list.append(client)

    return model
    