
#Problema del Agente Viajero con el uso del Algoritmo de Hill Climbing Estocástico y grafos completos, así como de multigrafos

from itertools import permutations, product
import random
import time

def elegir_caminos(cantidad_nodos, recorridos):
    """
    Permite al usuario elegir una cantidad específica de caminos de una lista de recorridos posibles.
    La cantidad de caminos debe ser menor o igual a la cantidad de recorridos disponibles.

    Args:
        cantidad_nodos (int): El número de nodos en el grafo.
        recorridos (list): Lista de los caminos posibles entre los nodos.

    Returns:
        list: Una lista de caminos seleccionados aleatoriamente.
    """
    # Solicitar al usuario la cantidad de caminos a elegir
    cantidad_caminos = int(input("Ingrese la cantidad de caminos (Esta debe de ser máximo de): " + str(len(recorridos)) + " "))

    # Validar si la cantidad solicitada excede los caminos disponibles
    if cantidad_caminos > len(recorridos):
        print("La cantidad de caminos solicitada excede los disponibles.")
        return []

    try:
        # Elegir aleatoriamente los caminos seleccionados
        caminos_elegidos = random.sample(recorridos, cantidad_caminos)
        print("Caminos elegidos:")
        for camino in caminos_elegidos:
            print(camino)
        return caminos_elegidos
    except ValueError as e:
        print(f"Error al seleccionar caminos: {e}")
        return []


def calcular_distancias(grafo, caminos, multigrafo):
    """
    Calcula las distancias totales para cada uno de los caminos, considerando si el grafo es un multigrafo.

    Args:
        grafo (list): La matriz de adyacencia que representa el grafo.
        caminos (list): Lista de caminos a analizar.
        multigrafo (bool): Indica si el grafo es un multigrafo (puede haber múltiples caminos entre dos nodos).

    Returns:
        tuple: Dos listas, la primera contiene las distancias de los caminos y la segunda los caminos con sus respectivas distancias.
    """
    distancias = []
    caminos_distancias = []  # Para almacenar los caminos con sus distancias

    for camino in caminos:
        # Dividir el camino en nodos y convertirlos en enteros
        camino_split = camino.split(" → ")
        recorrido = [int(x) for x in camino_split]

        if multigrafo:
            # Recolectar las listas de pesos posibles para cada paso del camino
            opciones_por_paso = []
            for i in range(len(recorrido) - 1):
                pesos = grafo[recorrido[i]][recorrido[i + 1]]
                opciones_por_paso.append(pesos)

            # Generar todas las combinaciones posibles de un camino (una por cada opción de pesos)
            for combinacion in product(*opciones_por_paso):
                distancia = sum(combinacion)
                distancias.append(distancia)
                caminos_distancias.append(camino)
        else:
            # Grafo normal: solo hay un peso por arista
            distancia = 0
            for i in range(len(recorrido) - 1):
                distancia += grafo[recorrido[i]][recorrido[i + 1]]
            distancias.append(distancia)
            caminos_distancias.append(camino)

    return distancias, caminos_distancias


def generar_caminos(cantidad_nodos, nodo_inicio):
    """
    Genera todos los caminos posibles (permutaciones) desde un nodo de inicio, visitando todos los demás nodos.

    Args:
        cantidad_nodos (int): El número total de nodos en el grafo.
        nodo_inicio (int): El nodo de inicio desde donde comienza cada camino.

    Returns:
        list: Una lista de todos los caminos posibles en formato " → ".
    """
    nodos = [str(i) for i in range(cantidad_nodos)]
    nodos.remove(str(nodo_inicio))  # Eliminar el nodo de inicio de la lista de nodos
    permutaciones_nodos = permutations(nodos)  # Generar todas las permutaciones posibles de los nodos restantes

    recorridos = []
    for p in permutaciones_nodos:
        camino = [str(nodo_inicio)] + list(p) + [str(nodo_inicio)]
        recorrido_con_flechas = " → ".join(camino)
        recorridos.append(recorrido_con_flechas)

    return recorridos


def grafo_completo():
    """
    Solicita al usuario los datos para construir un grafo completo, incluyendo los pesos de las aristas.

    Returns:
        tuple: Contiene el grafo, el número de nodos y si el grafo es un multigrafo.
    """
    cantidad_nodos = int(input("Ingrese el número de nodos del grafo: "))
    es_multigrafo = input("¿El grafo es multigrafo? (S/N): ").strip().upper() == "S"

    grafo = []

    # Solicitar los pesos de las aristas del grafo
    for i in range(cantidad_nodos):
        fila = []
        for j in range(cantidad_nodos):
            if i == j:
                fila.append([] if es_multigrafo else 0)
            elif j > i:
                if es_multigrafo:
                    caminos = int(input(f"Ingrese cuántos caminos hay de {i} a {j}: "))
                    pesos = [int(input(f"  Peso del camino {k+1} entre {i} y {j}: ")) for k in range(caminos)]
                    fila.append(pesos)
                else:
                    peso = int(input(f"Ingrese el peso entre {i} y {j}: "))
                    fila.append(peso)
            else:
                fila.append(grafo[j][i])  # La matriz es simétrica
        grafo.append(fila)
    return grafo, cantidad_nodos, es_multigrafo


def main():
    """
    Función principal que gestiona el flujo del programa:
    1. Construye el grafo con los datos ingresados por el usuario.
    2. Genera los caminos posibles desde un nodo de inicio.
    3. Permite al usuario elegir caminos aleatoriamente.
    4. Calcula las distancias de los caminos seleccionados y muestra los resultados.
    """
    grafo, cantidad_nodos, es_multigrafo = grafo_completo()
    print("\nGrafo generado:")
    for fila in grafo:
        print(fila)

    nodo_inicio = int(input("\nIngrese el nodo de inicio: "))
    recorridos = generar_caminos(cantidad_nodos, nodo_inicio)

    eleccion = elegir_caminos(cantidad_nodos, recorridos)

    # Calcular distancias para todos los caminos y para los caminos elegidos
    distancias_recorridos_totales, caminos_distancias_totales = calcular_distancias(grafo, recorridos, es_multigrafo)
    distancias_recorridos, caminos_distancias = calcular_distancias(grafo, eleccion, es_multigrafo)

    print("\nDistancias para los diferentes recorridos:")
    for distancia, camino in zip(distancias_recorridos, caminos_distancias):
        print(f"Camino: {camino}, Distancia: {distancia}")

    # Obtener la menor distancia y el camino correspondiente
    menor_distancia = min(distancias_recorridos)
    indice_menor = distancias_recorridos.index(menor_distancia)
    camino_menor = caminos_distancias[indice_menor]

    print(f"\nLa menor distancia fue: {menor_distancia}  para los caminos elegidos")
    print(f"El camino recorrido para obtener esta menor distancia fue: {camino_menor}\n")

    # Imprimir todas las distancias con los respectivos caminos que se hubieran podido obtener
    for distancia, camino in zip(distancias_recorridos_totales, caminos_distancias_totales):
        print(f"Camino: {camino}, Distancia: {distancia}")

    menor_distancia_total = min(distancias_recorridos_totales)
    indice_menor_total = distancias_recorridos_totales.index(menor_distancia_total)
    camino_menor_total = caminos_distancias_totales[indice_menor_total]

    print(f"\nLa menor distancia fue: {menor_distancia_total} en general")
    print(f"El camino recorrido para obtener esta menor distancia fue: {camino_menor_total}")

    if menor_distancia==menor_distancia_total:
      print("Se llegó a la menor distancia posible!")
    else:
      print("No se llegó a la menor distancia posible")

if __name__ == "__main__":
   #Calculo del tiempo de ejecución
    inicio = time.time()
    main()
    fin = time.time()
    print(f"\nTiempo total de ejecución: {fin - inicio:.4f} segundos")