import heapq

# Definir un grafo con las rutas del sistema de transporte masivo
grafo = {
    'A': {'B': 5, 'C': 10},
    'B': {'A': 5, 'C': 3, 'D': 7},
    'C': {'A': 10, 'B': 3, 'D': 1, 'E': 4},
    'D': {'B': 7, 'C': 1, 'E': 2},
    'E': {'C': 4, 'D': 2}
}

# Función para evaluar heurística (distancia estimada hasta el objetivo)
def heuristica(nodo, objetivo):
    distancias_heuristicas = {
        'A': 7,
        'B': 6,
        'C': 2,
        'D': 1,
        'E': 0  # Distancia al objetivo es 0
    }
    return distancias_heuristicas.get(nodo, float('inf'))

# Algoritmo A* para encontrar la mejor ruta
def encontrar_mejor_ruta(grafo, inicio, objetivo):
    # La cola de prioridad con el formato (costo_acumulado, nodo_actual, camino_recorrido)
    cola_prioridad = [(0, inicio, [])]
    visitados = set()

    while cola_prioridad:
        (costo, nodo_actual, camino) = heapq.heappop(cola_prioridad)

        if nodo_actual in visitados:
            continue

        # Añadir el nodo al conjunto de visitados
        visitados.add(nodo_actual)
        camino = camino + [nodo_actual]

        # Si llegamos al objetivo, devolvemos el costo y el camino
        if nodo_actual == objetivo:
            return costo, camino

        # Explorar los vecinos
        for vecino, peso in grafo.get(nodo_actual, {}).items():
            if vecino not in visitados:
                # Calcular el costo acumulado y agregarlo a la cola con la heurística
                costo_total = costo + peso
                prioridad = costo_total + heuristica(vecino, objetivo)
                heapq.heappush(cola_prioridad, (prioridad, vecino, camino))

    return float('inf'), []

# Base de conocimiento con reglas lógicas (esto es una representación básica)
def evaluar_reglas(nodo, hora_pico=False):
    # Por ejemplo, en horas pico algunas rutas pueden ser evitadas
    reglas = {
        'A': 'evitar' if hora_pico else 'permitido',
        'B': 'permitido',
        'C': 'permitido',
        'D': 'evitar' if hora_pico else 'permitido',
        'E': 'permitido'
    }
    return reglas.get(nodo, 'permitido')

# Aplicar el sistema
inicio = 'A'
objetivo = 'E'
hora_pico = True  # Ejemplo de condición basada en reglas

# Filtrar nodos basados en las reglas
grafo_filtrado = {
    nodo: {vecino: peso for vecino, peso in vecinos.items() if evaluar_reglas(vecino, hora_pico) == 'permitido'}
    for nodo, vecinos in grafo.items()
    if evaluar_reglas(nodo, hora_pico) == 'permitido' or nodo == inicio
}

# Verificar si el nodo de inicio tiene vecinos después del filtrado
if not grafo_filtrado.get(inicio):
    print(f"No hay rutas disponibles desde {inicio}.")
else:
    # Encontrar la mejor ruta
    costo, ruta = encontrar_mejor_ruta(grafo_filtrado, inicio, objetivo)
    if ruta:
        print(f"Mejor ruta: {ruta} con un costo total de {costo}")
    else:
        print(f"No se encontró una ruta válida desde {inicio} hasta {objetivo}.")
