import json
from typing import Any
from ..models import Nodes
from .. import db
import csv
import sys

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


def return_all_nodes() -> dict[Any, Any]:
    all_nodes = Nodes.query.all()
    graph = {}
    for node in all_nodes:
        graph[node.id_node] = json.loads(node.neighbors)


    return graph


def dijkstra(graph, start, goal) -> dict[str, Any]:
    if start not in graph:
        return {
            'distance': f'{start} not in graph',
            'path': []
        }
    if goal not in graph:
        return {
            'distance': f'{goal} not in graph',
            'path': []
        }
    shortest_distance = {}
    predecessor = {}
    unseenNodes = graph
    infinity = sys.maxsize
    path = []
    for node in unseenNodes:
        shortest_distance[node] = infinity
    shortest_distance[start] = 0
    while unseenNodes:
        minNode = None
        for node in unseenNodes:
            if minNode is None:
                minNode = node
            elif shortest_distance[node] < shortest_distance[minNode]:
                minNode = node
        for childNode, weight in graph[minNode].items():
            if int(weight) + int(shortest_distance[minNode]) < shortest_distance[childNode]:
                shortest_distance[childNode] = int(weight) + int(shortest_distance[minNode])
                predecessor[childNode] = minNode
        unseenNodes.pop(minNode)
    currentNode = goal
    while currentNode != start:
        try:
            path.insert(0, currentNode)
            currentNode = predecessor[currentNode]
        except KeyError:
            print('Path not reachable')
            break
    path.insert(0, start)
    if shortest_distance[goal] != infinity:
        return {
            'distance': shortest_distance[goal],
            'path': path
        }
    else:
        return {
            'distance': 'No path found',
            'path': []
        }

