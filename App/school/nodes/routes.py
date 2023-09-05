from flask import Blueprint, jsonify, Response
from ..nodes.utils import store_nodes_database, return_all_nodes, dijkstra

nodes = Blueprint('nodes', __name__)

@nodes.route('/update_nodes', methods=['GET'])
def find_path() -> tuple[Response, int]:

    store_nodes_database()

    return jsonify({
        'success': True,
        'message': 'Nodes added successfully to the database',
        'status_code': 200,
        'error': None,
        'code': 1
    }), 200

@nodes.route('/pathfinder/<string:start>/<string:goal>', methods=['GET'])
def get_nodes(start, goal) -> tuple[Response, int]:

    graph = return_all_nodes()
    path = dijkstra(graph, start=start, goal=goal)

    return jsonify({
        'success': True,
        'message': 'Nodes',
        'status_code': 200,
        'error': None,
        'code': 1,
        'data': path
    }), 200