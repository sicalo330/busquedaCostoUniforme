import heapq
import networkx as nx
import matplotlib.pyplot as plt
import random
import time

# --- Funciones para cargar el grafo desde archivo ---
def cargar_grafo_desde_archivo(nombre_archivo):
    """
    Carga un grafo desde un archivo de texto y reconstruye su estructura jerárquica.
    Formato del archivo:
        origen destino peso
        origen destino peso
        ...
    """
    grafo = {}
    niveles = {}  # Diccionario para reconstruir niveles: {nivel: [nodos]}
    
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
        
        # Primera pasada: construir el grafo básico
        for linea in lineas:
            if linea.strip():
                origen, destino, peso = linea.strip().split()
                grafo.setdefault(origen, []).append((destino, int(peso)))
                grafo.setdefault(destino, [])  # Asegurar que los destinos existan
        
        # Segunda pasada: reconstruir niveles (asumiendo que el archivo está ordenado por niveles)
        niveles[0] = ['1']  # La raíz siempre es '1'
        for linea in lineas:
            origen, destino, _ = linea.strip().split()
            nivel_padre = next((k for k, v in niveles.items() if origen in v), None)
            if nivel_padre is not None:
                nivel_hijo = nivel_padre + 1
                niveles.setdefault(nivel_hijo, []).append(destino)
    
    # Convertir el diccionario de niveles a una lista ordenada
    niveles_ordenados = [niveles[i] for i in sorted(niveles.keys())]
    return grafo, niveles_ordenados


# --- Búsqueda de Costo Uniforme (sin cambios) ---
def busqueda_costo_uniforme(grafo, inicio, objetivo):
    frontera = [(0, inicio)]
    visitados = set()
    padres = {}
    costos = {inicio: 0}
    arbol_busqueda = nx.DiGraph()

    while frontera:
        costo_actual, nodo_actual = heapq.heappop(frontera)

        if nodo_actual == objetivo:
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

# --- Graficar árbol (con resaltado de camino) ---
def graficar_arbol_jerarquico(grafo, niveles, camino=None):
    G = nx.DiGraph()
    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos:
            G.add_edge(nodo, vecino, weight=peso)

    pos = {}
    y = 0
    for nivel in niveles:
        x_intervalo = 1 / (len(nivel) + 1)
        x = x_intervalo
        for nodo in nivel:
            pos[nodo] = (x, -y)
            x += x_intervalo
        y += 1

    # Colores para resaltar el camino
    edge_colors = ['red' if (u, v) in zip(camino[:-1], camino[1:]) else 'black' for u, v in G.edges()]
    node_colors = ['lightcoral' if nodo in camino else 'lightblue' for nodo in G.nodes()]

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors,
            node_size=800, font_size=10, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
    plt.title("Árbol desde archivo" + (" (camino resaltado)" if camino else ""))
    fin_tiempo = time.time()
    print(f"\nTiempo de ejecución: {fin_tiempo - inicio_tiempo:.4f} segundos")
    plt.show()

# --- Main ---
if __name__ == "__main__":
    nombre_archivo = input("Ingrese el nombre del archivo (ej: grafo): ")
    inicio = input("Ingrese el nodo de inicio: ")
    objetivo = input("Ingrese el nodo ojetivo: ")
    inicio_tiempo = time.time()
    grafo, niveles = cargar_grafo_desde_archivo(nombre_archivo + '.txt')

    hojas = [nodo for nodo in grafo if not grafo[nodo]]  # Nodos sin hijos

    print(f"\nNodo objetivo (aleatorio): {objetivo}")
    camino, costo, _ = busqueda_costo_uniforme(grafo, inicio, objetivo)

    if camino:
        print(f"Camino: {' -> '.join(camino)}")
        print(f"Costo total: {costo}")
        graficar_arbol_jerarquico(grafo, niveles, camino)
    else:
        print("No se encontró camino al objetivo.")