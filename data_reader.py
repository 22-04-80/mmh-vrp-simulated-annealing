import json
import os

from data_structs import Node, Model, Nodes

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
        data['each_vehicle_capacity'],
        depot
    )
    nodes = Nodes()
    for client in data['clients']:
        client = Node(
            client['no'], 
            client['name'],
            client['demand'],
            client['x_coord'],
            client['y_coord']
        )
        nodes.add_client(client)
        nodes.add_seq_no(client.seq_no)

    model.node_list = nodes
    model.node_seq_no_list = nodes.seq_no_list
    return model
    