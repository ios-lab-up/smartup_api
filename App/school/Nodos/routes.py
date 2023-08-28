from flask import flask, request, jsonify

nodos = Flask(__name__)

def encontrar_ruta(nodo_inicio, nodo_destino):
    # Si los nodos son iguales, la ruta será solo ese nodo
    if nodo_inicio == nodo_destino:
        return [nodo_inicio]

    visitados = set() # Lista de nodos visitados
    cola = [(nodo_inicio, [nodo_destino])] # Inicializar una cola

    # Creando bucle para visitar cada nodo
    while cola:
        nodo_actual, ruta_actual = cola.pop(0) # Saca el primer elemento de la cola

        if nodo_actual in visitados:
            continue # Si el noso ya ha sido visitado, omite este ciclo

        vecinos = nodos.get(nodo_actual, []) # Obtiene los vecinos del nodo actual

        for vecino in vecinos:
            nueva_ruta = list(ruta_actual)  # Crea una copia nueva de la ruta actual
            nueva_ruta.append(vecino)  # Agrega el vecino a la ruta
            cola.append((vecino, nueva_ruta))  # Agrega el vecino y su ruta a la cola

            if vecino == nodo_destino:
                return nueva_ruta  # Si se encuentra el nodo del destino, devuelve la ruta

        visitados.add(nodo_actual)

    return None  # Si no se encuentra una ruta, devuelve None


#Nuevo punto de conexión utilizando el método (GET)
@nodos.route('/ruta-nodo', methods=['GET'])
def bucar_ruta():
    try:
        #Obtiene los IDs de lo nodos (inicio/destino) de los parámetros
        nodo_inicio = request.args.get('nodo_inicio')
        nodo_destino = request.args.get('nodo_destino')

        # Verificar si ambo IDs de nodos se proporcionaron
        if nodo_inicio is None or nodo_destino is None:
            return jsonify({'error': "Se requieren los parámetro nodo_inicio y nodo_destino"}), 400

        ruta = encontrar_ruta(nodo_inicio, nodo_destino)

        if not ruta:
            return jsonify({"menaje": "No se encontró ruta entre los nodos."}), 404

        #Devuelve la ruta encontrada en forma de lista
        return jsonify({"ruta": ruta}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500