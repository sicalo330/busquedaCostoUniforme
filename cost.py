import heapq
import networkx as nx
import matplotlib.pyplot as plt

def busqueda_costo_uniforme(grafo, inicio, objetivo):
    """
    Realiza una búsqueda de costo uniforme (Uniform Cost Search) en el grafo dado.

    Args:
        grafo (dict): Grafo representado como un diccionario donde las llaves son nodos
                      y los valores son listas de tuplas (vecino, costo).
        inicio (str): Nodo de inicio.
        objetivo (str): Nodo objetivo.

    Returns:
        tuple: (camino encontrado como lista de nodos, costo total del camino,
                árbol de búsqueda como un DiGraph de NetworkX).
    """
    frontera = [(0, inicio)]  # Cola de prioridad (min-heap) con tuplas (costo acumulado, nodo)
    visitados = set()         # Conjunto de nodos ya visitados
    padres = {}               # Diccionario para reconstruir el camino
    costos = {inicio: 0}       # Diccionario de costos mínimos conocidos a cada nodo
    arbol_busqueda = nx.DiGraph()  # Grafo dirigido que representa el árbol de búsqueda

    while frontera:
        costo_actual, nodo_actual = heapq.heappop(frontera)

        if nodo_actual == objetivo:
            # Reconstrucción del camino desde el objetivo hasta el inicio
            camino = [objetivo]
            while objetivo in padres:
                objetivo = padres[objetivo]
                camino.insert(0, objetivo)
            return camino, costo_actual, arbol_busqueda

        if nodo_actual not in visitados:
            visitados.add(nodo_actual)

            for vecino, costo in grafo.get(nodo_actual, []):
                nuevo_costo = costo_actual + costo
                if vecino not in costos or nuevo_costo < costos[vecino]:
                    costos[vecino] = nuevo_costo
                    heapq.heappush(frontera, (nuevo_costo, vecino))
                    padres[vecino] = nodo_actual
                    arbol_busqueda.add_edge(nodo_actual, vecino, weight=costo)

    return None, None, arbol_busqueda

def graficar_arbol(arbol):
    """
    Grafica el árbol de búsqueda utilizando NetworkX y Matplotlib.

    Args:
        arbol (nx.DiGraph): Árbol de búsqueda generado por la búsqueda de costo uniforme.
    """
    pos = nx.spring_layout(arbol)  # Posicionamiento de los nodos
    edge_labels = nx.get_edge_attributes(arbol, 'weight')  # Pesos de las aristas

    plt.figure(figsize=(8, 6))
    nx.draw(arbol, pos, with_labels=True, node_color='lightblue',
            node_size=1500, font_size=12, font_weight='bold', arrows=True)
    nx.draw_networkx_edge_labels(arbol, pos, edge_labels=edge_labels)
    plt.title("Árbol de Búsqueda")
    plt.show()

def toma_datos():
    """
    Solicita al usuario los nodos del grafo y las conexiones (pesos) entre ellos.

    Returns:
        tuple: (lista de nodos, lista de listas de pesos, lista de conexiones como pares de nodos)
    """
    conexiones_num = []
    conexiones_vertices = []
    nodos_grafo = input("Ingrese los nodos del grafo, separados por comas: ")
    nodos_grafo = nodos_grafo.split(",")
    print("Los nodos son los siguientes: " + str(nodos_grafo))

    for i in range(len(nodos_grafo)):
        for j in range(i+1, len(nodos_grafo)):
            pesos = input(f"Ingrese el peso de la conexión entre {nodos_grafo[i]} y {nodos_grafo[j]} (puedes ingresar varios separados por comas): ")
            pesos = pesos.split(",")
            pesos_int = []
            for peso in pesos:
                try:
                    pesos_int.append(int(peso))
                except ValueError:
                    print(f"Valor inválido '{peso}', se ignorará.")
            if len(pesos_int) == 0:
                pesos_int.append(0)  # Si no se ingresó ningún peso válido, se asigna 0
            conexiones_num.append(pesos_int)
            conexiones_vertices.append((nodos_grafo[i], nodos_grafo[j]))

    return nodos_grafo, conexiones_num, conexiones_vertices

def construir_grafo(nodos_grafo, conexiones_num, conexiones_vertices):
    """
    Construye un grafo no dirigido a partir de los nodos y las conexiones.

    Args:
        nodos_grafo (list): Lista de nodos del grafo.
        conexiones_num (list): Lista de listas de pesos para cada conexión.
        conexiones_vertices (list): Lista de pares de nodos que representan conexiones.

    Returns:
        dict: Grafo representado como un diccionario.
    """
    grafo = {nodo: [] for nodo in nodos_grafo}
    for (nodo1, nodo2), pesos in zip(conexiones_vertices, conexiones_num):
        for peso in pesos:
            if peso != 0:
                grafo[nodo1].append((nodo2, peso))
                grafo[nodo2].append((nodo1, peso))  # Agregamos también la conexión inversa (no dirigido)
    return grafo

def mostrar_conexiones(conexiones_num, conexiones_vertices):
    """
    Muestra en pantalla las conexiones entre nodos y sus respectivos pesos.

    Args:
        conexiones_num (list): Lista de listas de pesos de las conexiones.
        conexiones_vertices (list): Lista de pares de nodos que representan conexiones.
    """
    print("\nConexiones entre nodos:")
    for (nodo1, nodo2), pesos in zip(conexiones_vertices, conexiones_num):
        print(f"Conexión {nodo1}-{nodo2}: Pesos -> {pesos}")

def main():
    """
    Función principal que orquesta la toma de datos, construcción del grafo,
    ejecución de la búsqueda de costo uniforme y graficación del árbol de búsqueda.
    """
    nodos_grafo, conexiones_num, conexiones_vertices = toma_datos()
    mostrar_conexiones(conexiones_num, conexiones_vertices)
    grafo = construir_grafo(nodos_grafo, conexiones_num, conexiones_vertices)
    print("\nGrafo construido:", grafo)

    inicio = input("Ingrese el nodo de inicio: ")
    objetivo = input("Ingrese el nodo objetivo: ")
    camino, costo_total, arbol_busqueda = busqueda_costo_uniforme(grafo, inicio, objetivo)

    if camino:
        print("Camino encontrado:", camino)
        print("Costo total:", costo_total)
        graficar_arbol(arbol_busqueda)
    else:
        print("No se encontró un camino entre los nodos.")

if __name__ == "__main__":
    main()
