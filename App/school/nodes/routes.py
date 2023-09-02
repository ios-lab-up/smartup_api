from flask import Blueprint, request, jsonify
import json


# recuerda dar de alta la blueprint en el archivo App/school/__init__.py
nodes = Blueprint('nodes', __name__)
# el import esta comentado para que no cause un error al momento de ejecutar el ciclo main



# No pueden haber variable globales en un archivo de rutas
# nodes = []
# esto es una variable global
# tienen que estar en el archivo utils.py de su respectivo módulo

nodes = [ # mueve esto a un archivo utils.py
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


# El simbolo / solo se utiliza cuando hay multiples rutas en un mismo archivo
# En este caso, el archivo nodes/routes.py solo tiene una ruta
@nodes.route('/find/path',method=['GET']) # hay que añadir el metodo POST, ya que por defecto es GET
# hay que renombrar la función a find_path, o algun parecido a lo que hace, como pathfinder
def find_path():

    # request.get_json() # esto es para obtener el json que se envia en el body de la petición
    return jsonify({"nodes": nodes}) # se esta regresando un json, no un diccionario
    # un endpoint siempre debe terminar con un return, ya sea un json, un string, un diccionario, etc.
    # tu diccionario solo tiene una llave, nodes, y su valor es una lista de diccionarios
    # por ende, es mejor regresar una lista de diccionarios, no un diccionario con una lista de diccionarios
    # return jsonify(nodes)


# borra lo que esta debajo de este comentario


# Esta funcion va a causar un error, ya que no se puede ejecutar el ciclo main en un archivo de rutas
# y estás borrando la blueprint al momento de declarar la variable nodes
if __name__ == '__main__':
    nodes.run(debug=True)

# El ciclo main nunca puede ser ejecutado en un archivo de rutas
# El ciclo main solo puede ser ejecutado en el archivo principal de la aplicación
# En este caso, el archivo principal de la aplicación es App/run.py
