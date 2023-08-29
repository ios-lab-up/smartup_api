from flask import Blueprint, request, jsonify

nodes = Blueprint('nodes',__name__)

@nodes.route('/find_path',method=['GET'])
def find_path():
    pass