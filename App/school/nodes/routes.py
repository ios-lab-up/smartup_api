from flask import Blueprint, jsonify, Response
from ..nodes.utils import store_nodes_database, return_all_nodes

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

@nodes.route('/nodes', methods=['GET'])
def get_nodes() -> tuple[Response, int]:

    nodes_paths = return_all_nodes()

    return jsonify({
        'success': True,
        'message': 'Nodes',
        'status_code': 200,
        'error': None,
        'code': 1,
        'data': nodes_paths
    }), 200