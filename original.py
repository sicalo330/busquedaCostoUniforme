import heapq
import networkx as nx
import matplotlib.pyplot as plt
import random

# --- Funciones para construir un árbol jerárquico ---
def generar_arbol_jerarquico(profundidad, hijos_minimos):
    grafo = {}
    contador_nodos = 1#Se empieza con el nodo 1
    niveles = [[str(contador_nodos)]]
    grafo[str(contador_nodos)] = []

    for nivel in range(profundidad):#Iterará la misma cantidad de veces de la profundidad seleccionada
        nuevo_nivel = []
        for nodo in niveles[-1]:#Este ciclo lo que hace es almacenar una lista de datos en donde estarán los numeros de cada nivel ['1'],['2','3','4','5'] en el caso de que la cantidad de hijos por nodo fueran 4
            # num_hijos = random.randint(hijos_minimos, hijos_minimos + 2)#Aquí se generan los hijos
            for i in range(hijos_minimos):#Lo que hará el for es darle hijos al nodo que esté seleccionado
                #El contador de hijos aumenta en uno, es decir que si se empezó en 1, se incrementa a 2, y con este número se bautiza el siguiente nodo
                contador_nodos += 1
                hijo = str(contador_nodos)
                peso = random.randint(1, 10)
                grafo[nodo].append((hijo, peso))#Aún no entiendo del todo qué hace esto
                print(nodo)
                print(grafo[nodo])
                grafo[hijo] = []
                nuevo_nivel.append(hijo)#Esta parte es importante ya que almacena los números que tendrá cada nivel de esta forma ['2','3','4'] esto si el número de hijos por nodo es 3
        niveles.append(nuevo_nivel)
    return grafo, niveles

# --- Búsqueda de Costo Uniforme ---
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

# --- Funciones para graficar de forma jerárquica ---
def graficar_arbol_jerarquico(grafo, niveles, camino=None):
    arbol = nx.DiGraph()
    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos:
            arbol.add_edge(nodo, vecino, weight=peso)

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
    edge_colors = []
    node_colors = []
    
    if camino:
        aristas_camino = set(zip(camino[:-1], camino[1:]))  # Pares de nodos del camino
    else:
        aristas_camino = set()

    for edge in arbol.edges():
        if edge in aristas_camino:
            edge_colors.append('red')
        else:
            edge_colors.append('black')

    for node in arbol.nodes():
        if camino and node in camino:
            node_colors.append('lightcoral')
        else:
            node_colors.append('lightblue')

    edge_labels = nx.get_edge_attributes(arbol, 'weight')
    plt.figure(figsize=(16, 12))
    nx.draw(arbol, pos, with_labels=True, node_color=node_colors,
            node_size=800, font_size=10, arrows=True, edge_color=edge_colors)
    nx.draw_networkx_edge_labels(arbol, pos, edge_labels=edge_labels)
    plt.title("Árbol Jerárquico" + (" (camino resaltado)" if camino else ""))
    plt.show()

def cargar_grafo_desde_archivo(nombre_archivo):
    grafo = {}
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            partes = linea.strip().split()
            if len(partes) == 3:
                origen, destino, peso = partes
                grafo.setdefault(origen, []).append((destino, int(peso)))
                grafo.setdefault(destino, [])  # Asegurar que el destino también esté en el grafo
    return grafo


# --- Main ---
if __name__ == "__main__":
    profundidad = int(input("Ingrese la cantidad de la profundidad del árbol: ")) 
    hijos_minimos = int(input("Ingrese la cantidad de hijos por nodo: ")) 
    grafo, niveles = generar_arbol_jerarquico(profundidad, hijos_minimos)

    inicio = '1'
    hojas = [nodo for nodo, vecinos in grafo.items() if len(vecinos) == 0]
    objetivo = random.choice(hojas)

    print(f"\nNodo de inicio: {inicio}")
    print(f"Nodo objetivo (hoja aleatoria): {objetivo}")

    camino, costo_total, arbol_busqueda = busqueda_costo_uniforme(grafo, inicio, objetivo)

    if camino:
        print("\nCamino encontrado:", camino)
        print("Costo total:", costo_total)
        graficar_arbol_jerarquico(grafo, niveles, camino)  # ¡Aquí pasamos el camino!
    else:
        print("No se encontró un camino entre los nodos.")