from flask import Blueprint, request, jsonify
import json

nodes = Blueprint('nodes', __name__)

nodes = [
    {
        "ID": str,
        "ID_Nodo": "AS0",
        "ID_Nombre": "Entrada / Anexo",
        "ID_Vecinos": [
            {
                "ID": str,
                "ID_Nodo": "AP1",
                "Codto": int,
            }
        ],
        "Piso": 1,
        "Status": bool
    },
    {
        "ID": str,
        "ID_Nodo": "AP1",
        "ID_Nombre": "Pasillo",
        "ID_Vecinos": [
            {
                "ID": str,
                "ID_Nodo": "AS0",
                "Costo": int,
            },
            {
                "ID": str,
                "ID_Nodo": "AS1",
                "Costo": int,
            },
            {
              "ID": str,
              "ID_Nodo": "AP2",
              "Costo": int,
            }
        ],
        "Piso": 1,
        "Status": bool
    }
]

@nodes.route('/find/path',method=['GET'])
def find_path():
    return jsonify({"nodes": nodes})

if __name__ == '__main__':
    nodes.run(debug=True)