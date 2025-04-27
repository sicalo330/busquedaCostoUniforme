import random

def ingresar_items():#Aqui se ingresan los valores de la mochila
    items = []#Se inicializa una lista
    num_items = int(input("Ingrese la cantidad de ítems: "))#Se ingresa la cantidad de items que tendrá la michila(no confundir con la capacidad)
    for i in range(1, num_items + 1):#Un ciclo que irá guardando los valores de costo y volumen de cada item
        costo = int(input(f"Costo del ítem {i}: "))
        volumen = int(input(f"Volumen del ítem {i}: "))
        items.append((i, costo, volumen))#Aquí se añaden los items(costo y volumen) uno por cada ciclo
    return items#Retorna la lista de items con los valores que se les haya dado

def heuristica_lineal(items, capacity, combinations):
    results = []#Se inicializa la lista results
    for idx,(k1, k2) in enumerate(combinations):#Enumerate es similar a len, es decir que cuenta la cantidad de datos en combinations, AÚN NO ENTIENDO POR QUÉ FOR k1,k2, por alguna razon debo dejar ahí el idx para que no falle
        puntuaciones = [(i, k1*c + k2*v, c, v) for i, c, v in items]# for i, c, v in items] bautiza cada item, por ejemplo si se tiene (1,10,5) entonces i=1 c=10 v=5 y luego hace los cálculos (i, k1*c + k2*v, c, v)
        """
        Este es un ejemplo de como se ve la lista puntuaciones
        puntuaciones = [
        (1, 5, 10, 5), 1 sería el número del item, 5 el costo, 10 el volumen y 5 el resultado de la combinación linea si k1=1 y k2=0
        (2, 4, 6, 2),
        (3, 7, 8, 4)
        ]
        """
        puntuaciones.sort(key=lambda x: x[1], reverse=True)#Ordena la lista de mayor a menor
        backPack = []
        totalCost = 0
        totalVolume = 0
        for i, p, c, v in puntuaciones:
            if totalVolume + v <= capacity:#Se empieza en 0 y si la suma del volumen a agregar supera la capacidad deja de iterar, creo que debería poner un else con un return
                backPack.append(i)
                totalCost += c
                totalVolume += v
        results.append((f"Lineal {idx}", backPack, totalCost, totalVolume))#Se devuelve los resultados
    return results

def heuristica_azar(items, capacidad):
    # Mezcla los ítems aleatoriamente
    items_mezclados = items.copy()#Se copia la lista para no modificar la original y evitar problemas a futuro
    random.shuffle(items_mezclados)#Mezcla la cantidad de elementos que haya en la lista como barajar una carta
    
    # Llena la mochila con el orden aleatorio generado
    mochila = []
    total_costo = 0
    total_volumen = 0
    
    for i, c, v in items_mezclados:
        if total_volumen + v <= capacidad:
            mochila.append(i)
            total_costo += c
            total_volumen += v
    return [("Azar", mochila, total_costo, total_volumen)]

def heuristica_alternancia(items, capacidad, orden):
    #Recordar que la estructura es la siguiente, 
    estrategias = {
        "valor": lambda x: x[1],
        "volumen": lambda x: -x[2],
        "relacion": lambda x: x[1]/x[2]
    }
    resultados = []
    for nombre in orden:#Itera sobre cada elemento de la lista orden En cada iteración, nombre toma lo asignado en valor,volumen o relacion dependiendo de la iteración y del orden del input
        items_ordenados = sorted(items, key=estrategias[nombre], reverse=True)
        """
        Reverse=true ordena de mayor a menor, estrategias[nombre] busca la estrategia a usar
        Es decir que si el input fue valor, buscará en estrategia posición valor y lambda x: x[1] obtendrá el mayor coste, recordar que si tenemos (2,8,2) y (1,10,5)  
        lambda lo ordenará con el mayor coste, en este caso el orden sería (1,10,5) y (2,8,2)

        Algo similar ocurre con volumen, solo que el lambda x: -x[2], pero lo hará de menos a mayor, (1, 10, 5) y (2, 8, 3), -3 > -5, por lo tanto el orden sería (2, 8, 3) y (1, 10, 5)

        Relación lo que hace es dividir el costo y volumen de cada dato y el resultado se ordena de mayor a menor, por ejemplo
        (1, 10, 5) => 10/5 = 2
        (2, 8, 2) => 8/2 = 4
        El órden sería (2, 8, 2) y (1, 10, 5) por que 4>2
        """
        mochila = []    
        total_costo = 0
        total_volumen = 0
        for i, c, v in items_ordenados:
            if total_volumen + v <= capacidad:
                mochila.append(i)
                total_costo += c
                total_volumen += v
        resultados.append((f"Alternancia: {nombre}", mochila, total_costo, total_volumen))
    return resultados

def heuristica_descomposicion(items, divisiones):
    print(divisiones)
    resultados = []
    for idx, (capacidad, heuristica, params) in enumerate(divisiones):#Se iteran, heuristica define qué tipo de heuristica (valga la redundancia) se va a usar
        if heuristica == "lineal":
            resultados += heuristica_lineal(items, capacidad, params)#En este caso paramas sería k1 y k2
        elif heuristica == "azar":
            resultados += heuristica_azar(items, capacidad)#En este caso, la semilla no es necesaria, pero todo el código se cae si se quita
        elif heuristica == "alternancia":
            resultados += heuristica_alternancia(items, capacidad, params)#En este caso paramas, sería valor, volumen o relación, quizas una dos o las tres juntas
    return resultados

def main():
    items = ingresar_items()
    capacidad_total = int(input("Ingrese la capacidad de la mochila: "))#Esta sí es la capacidad de la mochila

    print("\nSeleccione el tipo de metaheurística:")
    print("1. Constructiva")
    print("2. De reducción")
    print("3. De descomposición")
    type = int(input("Opcion: "))

    results = []

    if type == 1 or type == 2:# Si se eligió la metaheuristica constructiva o reductiva entrará al if, esto porque utilizan las mismas funciones
        print("\nSeleccione la heurística de sensibilidad:")
        print("1. Combinación lineal")
        print("2. Alternancia")
        print("3. Azar")
        heur = int(input("Opcion: "))#En esta opción se debería elegir el número de la heurística a usar mas que poner el nombre en sí

        if heur == 1:#Aquí entra en la combinación lineal
            n = int(input("Cuántas combinaciones desea ingresar?: "))
            combinaciones = []#Se inicializan la lista combinaciones
            for i in range(n):#Aquí se agregan las constantes que se van a usar
                k1 = float(input(f"K1 para combinación {i+1}: "))
                k2 = float(input(f"K2 para combinación {i+1}: "))
                combinaciones.append((k1, k2))#Aquí se guardan las constantes en la lista llamada combinaciones
            results = heuristica_lineal(items, capacidad_total, combinaciones)#Aquí se hacen los cálculos para la combinación lineal

        elif heur == 2:#Aquí usará alternancia
            orden = input("Ingrese las heurísticas a alternar ejemplo: valor, volumen, relacion separadas por comas: ").split(',')
            orden = [o.strip() for o in orden]#Esta linea limpia los espacios blancos que pudo haber tenido el input anterior
            results = heuristica_alternancia(items, capacidad_total, orden)#Si dos soluciones tienen exactamente el mismo costo y volumen, imprimirá el primero y ya

        elif heur == 3:#Aquí elegirá items al azar siempre y cuando no supere la capacidad
            results = heuristica_azar(items, capacidad_total)

    elif type == 3:  # Metaheurística de descomposición
        capacidad_restante = capacidad_total  # Capacidad disponible inicial
        n = int(input("¿Cuántas submochilas desea crear?: "))
        
        divisiones = []
        for i in range(n):
            print(f"\n--- Submochila {i+1} ---")
            capacidad = int(input(f"Capacidad de la submochila {i+1}: "))#Aquí se añade la capacidad de cada submochila
            
            # Validación de capacidad
            if capacidad <= 0:#Si hay algún chistoso que ponga un número negativo, el programa acaba
                print("Error: La capacidad debe ser mayor que 0.")
                return
            if capacidad > capacidad_restante:#Si la mochila tiene una capacidad de 10 y se pone 20, el programa se acaba
                print(f"Error: No hay suficiente capacidad. Capacidad restante: {capacidad_restante}")
                return
            
            capacidad_restante -= capacidad #Actualiza la capacidad restante
            #Básicamente en cada submochila se hará uso de una heuristica e inmediatamente empezara otra, no sé si me hago entender
            # Selección de heurística
            heur = input("Heurística para esta submochila (lineal, alternancia, azar): ").strip().lower()#En este apartado, sí se debe poner la palabra
            if heur == "lineal":
                k1 = float(input("K1: "))
                k2 = float(input("K2: "))
                divisiones.append((capacidad, heur, [(k1, k2)]))
            elif heur == "azar":
                semilla = int(input("Semilla: "))#Lamentablemente no sé cómo sacar el input de semilla sin que se dañe el código, al inicio lo necesitaba pero ahora no
                divisiones.append((capacidad, heur, semilla))
            elif heur == "alternancia":
                orden = input("Heurísticas a alternar (valor, volumen, relacion): ").split(',')
                orden = [o.strip() for o in orden]#Esta linea limpia los espacios blancos que pudo haber tenido el input anterior
                divisiones.append((capacidad, heur, orden))
            else:
                print("Error: Heurística no válida.")
                return
        
        results = heuristica_descomposicion(items, divisiones)

    print("\nResultados:")
    mejor = max(results, key=lambda x: x[2])#recordar que resultados para el caso de heuristica_lineal es Lineal 1, backPack, totalCost, totalVolume x: x[2] indica que busca el mayor costo, esto evita que si dos datos tienen mismo volumen pero costos diferentes se elija el de mayor costo
    for nombre, mochila, costo, volumen in results:# Se imprimen todos los items, el costo y volumen total y los items seleccionados sacados
        print(f"\nHeurística: {nombre}")
        print(f"Items seleccionados: {mochila}")
        print(f"Costo total: {costo}")
        print(f"Volumen usado: {volumen}")
    print(f"\n>> Mejor solución: {mejor[0]} con costo {mejor[2]} y volumen {mejor[3]}")#Aquí se imprime el mejor resultado

if __name__ == "__main__":#Todo empieza desde aquí, se llama la función main que tiene todas las funciones de la mochila
    main()