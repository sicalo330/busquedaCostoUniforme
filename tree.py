import heapq
import networkx as nx
import matplotlib.pyplot as plt
import random
import time

# --- Funciones para cargar el arbol desde archivo ---
def cargar_arbol_desde_archivo(nombre_archivo):
    arbol = {}
    niveles = {}  # Diccionario para reconstruir niveles: {nivel: [nodos]}
    
    with open(nombre_archivo, 'r') as archivo:#En este apartado se lee los datos que hay en el archivo
        lineas = archivo.readlines()#La variable lineas son los datos que obtiene del archivo, 1 2 5, 1 3 7...
        
        #construir el arbol básico
        for linea in lineas:
            if linea.strip():#Si la linea no está vacía, la cual no pasará porque enel archivo está lleno de líneas
                partes = linea.strip().split()
                origen = partes[0] #Es el nodo que se conecta a...
                destino = partes[1]#Es el nodo que está conectado a...
                #Por ejemplo 1->2, en este caso 1 es origen y 2 es destino
                peso = partes[2]#Este es el costo de viajar de 1->2 por ejemplo

                if origen not in arbol:#Si el nodo origen aún no existe en el arbol, este es añadido junto con su destino y peso
                    arbol[origen] = []#Cuando es la primera vez que existe un origen, se crea una lista vacía en esa posición para darle un "puesto" por así decirlo
                arbol[origen].append((destino, int(peso)))#Cuando ya tiene su "puesto" se le agrega el nodo destino y el peso de llegar hasta allí

                if destino not in arbol:
                    arbol[destino] = []#Cuando un destino es nuevo, se añade su "puesto" ya que cabe la posibilidad de que pueda tener hijos
                
                #Si algo falla quizás fue porque comenté este fragmento de código
                # origen, destino, peso = linea.strip().split()#Ya que hay una separación entre los numeros, se divide y se asignan a origen, destino y peso
                # arbol.setdefault(origen, []).append((destino, int(peso)))
                # arbol.setdefault(destino, [])  #Esto es sólo para asegurarse de que el destino también exista en el diccionario arbol, aunque no tenga hijos todavía

        # Segunda pasada: reconstruir niveles (asumiendo que el archivo está ordenado por niveles)
        # for linea in lineas:
        #     origen, destino, _ = linea.strip().split()
        #     nivel_padre = next((k for k, v in niveles.items() if origen in v), None)#Lo que hace esto es recorrer cada hijo que tenga un nodo
        #     if nivel_padre is not None:#Luego entra al if, esto hace que el nivel del hijo sea 1 unidad mayor al del padre
        #         """
        #         Más o menos quedaría algo así
        #             0: ['1'],
        #             1: ['2', '3'],
        #             2: ['4', '5', '6']
        #         """
        #         nivel_hijo = nivel_padre + 1
        #         niveles.setdefault(nivel_hijo, []).append(destino)
        niveles[0] = ['1']  # La raíz siempre es '1'
        #Este ciclo, se asignan los padres, estos son necesarios para conocer el camino que va a tomar
        for linea in lineas:
            if linea.strip():
                partes = linea.strip().split()
                origen = partes[0]
                destino = partes[1]
                # peso no se usa aquí

                nivel_padre = None
                for profundidad, posicion in niveles.items():#La primera vez que se hace el for, niveles = {0:['1']}, por lo que k=0 y v=['1']
                #Aquí se forman los niveles que va a tener el árbol
                    if origen in posicion:#¿El nodo actual se encuentra en alguna parte del árbol?
                        #De ser así, nivel_padre deja de ser none sino que se convierte en un número que corresponde al nivel que se encuentra actualmente
                        nivel_padre = profundidad
                        break
                if nivel_padre is not None:#En el caso de que el nodo actual esté en el arbol, se pasa este if
                    nivel_hijo = nivel_padre + 1#El nivel del hijo está una unidad más abajo del padre, por eso se suma uno
                    if nivel_hijo not in niveles:#Si el nivel del hijo no se encuentra creado, hay que hacerlo
                        niveles[nivel_hijo] = []#Aquí se le da un puesto al nuevo nivel, es decir 1 si es la primera vez
                    niveles[nivel_hijo].append(destino)#Después en dicho nivel se añade el nodo destino que corresponde al hijo del padre
                """
                Intentaré resumir todo lo anteriormente dicho,pero para ello se debe tener en cuenta algunos detalles
                Se empieza en el nivel 0 con un solo nodo (1)
                 
                Caso 1: Trae (1,2,5),dado la naturaleza del archivo externo sobre los nodos, conexiones y peso (1,2,5) pasa lo siguiente
                1 existe en el arbol actual de 0:['1'], pero dada la naturaleza del archivo, si existe es porque necesariamente va a hacer una conexión a otro nodo,
                por lo tanto se debe crear un nuevo nivel, en este caso el nivel 1 y se añade a la lista de nodos en el nivel 1.
                Como se está ciclando en 0:['1'], por ahora solo existe 0, eso significa que se itera una sola vez y profundidad es 0 al inicio, si este se suma 1, se da a entener que es nivel 1
                Caso 2: Trae (1,3,4), 1 como sí existe en el arbol se toma en cuenta la profundidad que es 0, se suma 1 para saber que en qué nivel estar  
                se está haciendo una conexión a un nodo 3 pero NO se crea otro nivel sino que se añade a la lista de niveles en el nivel 1 eso lo explica niveles[nivel_hijo].append(destino)
                como nivel_hijo = 1, se añade un nodo en el nivel 1
                Para que se cree otro nivel el origen NO puede existir al inicio, recordemos que se cicla en la lista de niveles que al comienzo es 0:['1'], pero con las iteraciones
                que se han hecho se ha vuelto algo así {0: ['1'], 1: ['2','3']}
                Caso 3: Trae (2,5,1), en el primer ciclo 0:['1'], como 2 NO es 1, se itera, por lo tanto se tiene esto 1:['2','3'] y la profundidad es 1,
                como 2 existe se debe crear otro nivel sumando en uno la profundidad, es decir 2, a la hora de crear un hijo, se añaden los valores pero en niveles[nivel_hijo].append(destino)
                tal que nivel_hijo = 2, por lo que se tendría algo así {0: ['1'], 1: ['2','3'],2['5']}
                """
    # Convertir el diccionario de niveles a una lista ordenada
    niveles_ordenados = []
    claves_ordenadas = sorted(niveles.keys())
    for i in claves_ordenadas:
        niveles_ordenados.append(niveles[i])
    return arbol, niveles_ordenados#Retorna el arbol y los nivelses, este ulitmo no como un diccionario sino como una lista


# --- Búsqueda de Costo Uniforme (sin cambios) ---
def busqueda_costo_uniforme(arbol, inicio, objetivo):
    frontera = [(0, inicio)]
    visitados = set()
    padres = {}
    costos = {inicio: 0}
    arbol_busqueda = nx.DiGraph()

    #La variable frontera tiene un 0, es el costo ya que de ahí se empieza y no nos hemos movido, si el nodo de inicio es 5, será frontera = [(0,'5')]
    #frontera es la referencia donde el algoritmo guarda todas las opciones de caminos abiertos, y permite saber por dónde seguir explorando para encontrar el camino más corto (menor coste acumulado).

    while frontera:
        elemento = heapq.heappop(frontera)#La función heappop utiliza a frontera como un punto de inicio para así obtener el camino con menor volumen
        costo_actual = elemento[0]
        nodo_actual = elemento[1]
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
        if nodo_actual == objetivo:#Por lo general no va a pasar de este if, ya que solo lo hará cuando se alcance el objetivo
            camino = []
            camino.append(objetivo)

            while objetivo in padres:
                padre = padres[objetivo]
                camino.insert(0, padre)
                objetivo = padre

            return camino, costo_actual, arbol_busqueda
        #Entra al if si el nodo que se encuentra actualmente no había sido analizado anteriormente, normalmente va a entrar aquí, el if de arriba es solo si se encontró el objetivo, es decir solo una vez
        #Si el nodo actual no ha sido visitado todavía
        if nodo_actual not in visitados: #Este if fallará en dos casos, si el arbol está mal construido o si el objetivo es un nodo que no existe en el arbol
            #Por lo general va a entrar a este if hasta que se alcance el objetivo
            visitados.add(nodo_actual)

            #Recorrer todos los vecinos del nodo actual
            if nodo_actual in arbol:#Se va a iterar en cada nivel del arbol
                vecinos = arbol[nodo_actual]#Si el nodo actual no es el objetivo, se convierte en vecino ya que moverá a otro nodo
            
                for vecino_y_costo in vecinos:
                    vecino = vecino_y_costo[0]
                    costo_arista = vecino_y_costo[1]

                    nuevo_costo = costo_actual + costo_arista

                    #Si el vecino no tiene registrado un costo o encontramos un camino más barato
                    if vecino not in costos or nuevo_costo < costos[vecino]:#Si no conocemos aún un coste para el vecino o si encontramos un camino mejor (más barato) que el que conocíamos
                        costos[vecino] = nuevo_costo
                        heapq.heappush(frontera, (nuevo_costo, vecino))
                        padres[vecino] = nodo_actual#Aquí el nodo que no era el objetivo se convierte en padre
                        arbol_busqueda.add_edge(nodo_actual, vecino, weight=costo_arista)#Esta línea añade una arista dirigida al grafo arbol busqueda, desde nodo_actual hacia vecino
    return None, None, arbol_busqueda

# --- Graficar árbol (con resaltado de camino) ---
def graficar_arbol_jerarquico(arbol, niveles, camino=None):
    G = nx.DiGraph()
    for nodo, vecinos in arbol.items():
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

    #El camino del inicio al objetivo se marca en rojo, lo demás en negro
    edge_colors = []
    if camino:
        pares_camino = list(zip(camino[:-1], camino[1:]))  # Crear los pares de nodos consecutivos del camino

        for u, v in G.edges():
            if (u, v) in pares_camino:
                edge_colors.append('red')
            else:
                edge_colors.append('black')
    else:
        #Si no hay camino, todas las aristas en negro
        for _ in G.edges():
            edge_colors.append('black')
    node_colors = []
    for nodo in G.nodes():
        if camino and nodo in camino:
            node_colors.append('lightcoral')
        else:
            node_colors.append('lightblue')


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
    inicio_tiempo = time.time()#Comienza a medir el tiempo
    arbol, niveles = cargar_arbol_desde_archivo("test.txt")#Se crea el árbol y se utiliza el archivo llamado datos.txt

    # hojas = [nodo for nodo in arbol if not arbol[nodo]]  #Nodos sin hijos
    hojas = []
    for nodo in arbol:
        if not arbol[nodo]:
            hojas.append(nodo)

    print(f"\nNodo objetivo: {objetivo}")
    #Arbol son todos los nodos que se han creado hasta el momento, inicio es el nodo de inicio y objetivo es el destino que se busca llegar
    camino, costo, _ = busqueda_costo_uniforme(arbol, inicio, objetivo)

    if camino:
        print(f"Camino: {' -> '.join(camino)}")
        print(f"Costo total: {costo}")
        graficar_arbol_jerarquico(arbol, niveles, camino)
    else:
        print("No se encontró camino al objetivo.")