import json
from ..models import Nodes
from .. import db
import csv

def store_nodes_database():
    csv_file_path = '/SmartUP/csv-paths/Nodos iOS - FINAL.csv'
    with open(csv_file_path) as file:
        csvreader = csv.reader(file)

        next(csvreader)

        for row in csvreader:
            id_node = row[0]
            name = row[1]
            neighbors = row[2]
            cost = row[3]
            floor = row[5]

            neighbors = neighbors.split('-')
            cost = cost.split('-')

            neighbors = {key: value for key, value in zip(neighbors, cost)}

            node = Nodes(
                id_node=id_node,
                name=name,
                neighbors=json.dumps(neighbors),
                floor=int(floor),
                status=1
            )

            if Nodes.query.filter_by(id_node=id_node).first() is None:
                db.session.add(node)
                db.session.commit()


def return_all_nodes() -> list[dict]:
    all_nodes = Nodes.query.all()
    nodes_paths = []
    for node in all_nodes:
        nodes_paths.append(
            {
                'ID': node.id_node,
                'neighbors': json.loads(node.neighbors)
            }
        )

    return nodes_paths
