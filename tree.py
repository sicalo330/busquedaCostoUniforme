import heapq
import networkx as nx
import matplotlib.pyplot as plt
import random
import time

# --- Funciones para cargar el grafo desde archivo ---
def cargar_grafo_desde_archivo(nombre_archivo):
    grafo = {}
    niveles = {}  # Diccionario para reconstruir niveles: {nivel: [nodos]}
    
    with open(nombre_archivo, 'r') as archivo:#En este apartado se lee los datos que hay en el archivo
        lineas = archivo.readlines()#La variable lineas son los datos que obtiene del archivo, 1 2 5, 1 3 7...
        
        # Primera pasada: construir el grafo básico
        for linea in lineas:
            if linea.strip():
                origen, destino, peso = linea.strip().split()#Ya que hay una separación entre los numeros, se divide y se asignan a origen, destino y peso
                grafo.setdefault(origen, []).append((destino, int(peso)))
                grafo.setdefault(destino, [])  #Esto es sólo para asegurarse de que el destino también exista en el diccionario grafo, aunque no tenga hijos todavía
        
        # Segunda pasada: reconstruir niveles (asumiendo que el archivo está ordenado por niveles)
        niveles[0] = ['1']  # La raíz siempre es '1'
        for linea in lineas:
            origen, destino, _ = linea.strip().split()
            nivel_padre = next((k for k, v in niveles.items() if origen in v), None)#Lo que hace esto es recorrer cada hijo que tenga un nodo
            if nivel_padre is not None:#Luego entra al if, esto hace que el nivel del hijo sea 1 unidad mayor al del padre
                """
                Más o menos quedaría algo así
                    0: ['1'],
                    1: ['2', '3'],
                    2: ['4', '5', '6']
                """
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

    #La variable frontera tiene un 0, es el costo ya que de ahí se empieza y no nos hemos movido, si el nodo de inicio es 5, será frontera = [(0,'5')]
    #frontera es la referencia donde el algoritmo guarda todas las opciones de caminos abiertos, y permite saber por dónde seguir explorando para encontrar el camino más corto (menor coste acumulado).

    while frontera:
        costo_actual, nodo_actual = heapq.heappop(frontera)#La función heappop utiliza a frontera como un punto de inicio para así obtener el camino con menor volumen
        #Cabe aclarar que siempre al inicio va a sacar el nodo de inicio ya que es el único que conoce, después revisa el coste de sus vecinos y elige el que cueste menos
        """
        Es interesante como funciona el algoritmo de busque por costo uniforme, lo primero que hace es ponerse en un nodo de inicio la cual es elegido por un usuario, luego revisa sus vecinos y analiza cuál de ellos es el de menor coste,
        cuando encuenta el de menor costo, va hacia dicho nodo y repite el proceso
        Si encuentra algún nodo repetido lo ignora
        El nodo padre es el nodo anterior al que pasó, por ejemplo si se pasó de 2->9, el nodo padre sería 2

        Más o menos sería algo así
        Todos los nodos están sin visitar, por lo que el primer if nodo_actual not in visitados siempre entra inicialmente, el nodo actual pasa a ser vecino cuando se encontró el costo más barato
        Se calcula nuevo_costo = costo_actual + costo_arista,si el costo es mejor que el registrado (o es la primera vez que se visita), se actualiza
        Su costo mínimo (costos[vecino])
        Cuando el nodo actual es igual al destino entra al primer if, se reconstruye el camino desde el objetivo hasta el inicio usando el diccionario padres
        """

        if nodo_actual == objetivo:
            camino = [objetivo]#El nodo objetivo se asigna a la variable camino
            while objetivo in padres:
                objetivo = padres[objetivo]
                camino.insert(0, objetivo)
            return camino, costo_actual, arbol_busqueda

        if nodo_actual not in visitados:#Entra al if si el nodo que se encuentra actualmente no había sido analizado anteriormente, normalmente va a entrar aquí, el if de arriba es solo si se encontró el objetivo, es decir solo una vez
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
    inicio = input("Ingrese el nodo de inicio: ")
    objetivo = input("Ingrese el nodo ojetivo: ")
    inicio_tiempo = time.time()
    grafo, niveles = cargar_grafo_desde_archivo("datos.txt")

    hojas = [nodo for nodo in grafo if not grafo[nodo]]  # Nodos sin hijos

    print(f"\nNodo objetivo (aleatorio): {objetivo}")
    camino, costo, _ = busqueda_costo_uniforme(grafo, inicio, objetivo)

    if camino:
        print(f"Camino: {' -> '.join(camino)}")
        print(f"Costo total: {costo}")
        graficar_arbol_jerarquico(grafo, niveles, camino)
    else:
        print("No se encontró camino al objetivo.")