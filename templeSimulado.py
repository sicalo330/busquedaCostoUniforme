import math
import random
import matplotlib.pyplot as plt
import time

#Función a minimizar, en este caso x^2
def funcion_objetivo(x):
    return x**2

#Generar vecinos
def generar_vecino(x):#En esta función se tomará la posición actual y se le sumará o se le restará un número aleatorio entre -1 y 1
    return x + random.uniform(-1, 1)

# Temple Simulado con registro para graficar
#temple_simulado(funcion_objetivo, x_inicial, 1000, 0.01, 0.98)
#T_inicial es la temperatura con la que se va a comenzar el algoritmo, t_final es lo que se convertirá a medida que se reduzca la temperatura
#Alfa es la cantidad de temperatura que se va a disminuir, esto es algo complejo por lo tanto lo pondré abajo
"""

"""
def temple_simulado(funcion_objetivo, x_inicial, T_inicial, T_final, alfa, max_iteraciones):
    x_actual = x_inicial#Es el valor inicial y lo que se va a elevar al cuadrado
    f_actual = funcion_objetivo(x_actual)#f_actual será el resultado de la función, en este caso si x=8, 8^2=64, por lo tanto f_actual=64
    Ti = T_inicial#Al menos incialmente la temperatura inicial será mucho más grande que la temperatura final
    Tf = T_final#La temperatura final será constante

    historial_funcion = []
    historial_temperatura = []

    iteraciones = 0

    while Ti > Tf and iteraciones < max_iteraciones:
        x_nuevo = generar_vecino(x_actual)#Se genera un vecino(Valor cercano a la posición inicial)
        """
        Si delta es negativo es porque se resto al x_atual, es decir que se está acercando a la solución más optima,
        en el caso de que fuera positivo se haría una probabilidad a ver si entra o no dependiendo de la temperatura, 
        pero a medida que pasa el tiempo ya no irá aceptando tantas soluciones positivas
        """
        f_nuevo = funcion_objetivo(x_nuevo)
        delta = f_nuevo - f_actual

        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / Ti):
            #Se reeemplazan los valores y se sigue iterandp
            x_actual = x_nuevo
            f_actual = f_nuevo

        #Ambos historiales se usan para poder usarlos en la gráfica
        historial_funcion.append(f_actual)
        historial_temperatura.append(Ti)

        Ti *= alfa
        iteraciones += 1  # Aumentamos el contador de iteraciones

    return x_actual, f_actual, historial_funcion, historial_temperatura

# Ejecutar
x_inicial = random.uniform(-10, 10)
max_iteraciones = 5000  # Número máximo de iteraciones
#Solución es el x_actual más óptimo para el algoritmo
#valor es el f_actual del algoritmo, es decir el resultado del valor óptimo elevado al cuadrado
start_time = time.perf_counter()#En teoria perf_counter es más preciso que time.time()
solucion, valor, historial_funcion, historial_temperatura = temple_simulado(funcion_objetivo, x_inicial, 1000, 0.01, 0.98, max_iteraciones)
#Al parecer es una buena práctica devolver todos los datos aunque no se usen de nada
end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"El tiempo de ejecución fue: {execution_time * 1000:.6f} milisegundos.")#Se multipliza por 1000 para volverlo milisegundos

print(f"Mejor solución: x = {solucion}, f(x) = {valor}")

"""
Si asumimos que el algoritmo realiza una iteración en cada ciclo y cada iteración tiene un costo constante (O(1))
entonces la complejidad general del algoritmo de temple simulado se puede aproximar a O(n) donde n es el número de iteraciones
Cada vez que el algoritmo genera un nuevo "vecino" se hace una operación aritmética, la cual no tiene mucho peso en términos de rendimiento
En general el algoritmo no hace uso de tantas operaciones más allá de las aritméticas, por lo tanto en teoría no es poco eficiente
A la hora de medir el tiempo, este daba 0 sin importar a cuantos decimales redondeara, se tuvo que usar perf_counter para mayor precisión y convertirlo a milisegundos
"""

# Graficar
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(historial_funcion)
plt.title("Función objetivo vs iteraciones")
plt.xlabel("Iteración")
plt.ylabel("f(x)")

plt.subplot(1, 2, 2)
plt.plot(historial_temperatura)
plt.title("Temperatura vs iteraciones")
plt.xlabel("Iteración")
plt.ylabel("Temperatura")

plt.tight_layout()
plt.show()
