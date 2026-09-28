import heapq


def heuristica(a, b):
    # Distancia Manhattan admisible
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def busqueda_greedy(inicio, meta, entorno):
    
    cola_prioridad = []
    h_inicial = heuristica(inicio, meta)
    heapq.heappush(cola_prioridad, (h_inicial, inicio))
    visitados = set()
    padres = {inicio: None}

    while cola_prioridad:
        h, actual = heapq.heappop(cola_prioridad)

        if actual == meta:
            # Reconstruir camino
            camino = []
            nodo = actual
            while nodo is not None:
                camino.append(nodo)
                nodo = padres[nodo]
            return camino[::-1]

        if actual in visitados:
            continue
        visitados.add(actual)

        x, y = actual
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
            nx, ny = x + dx, y + dy
            vecino = (nx, ny)

            if entorno.es_valido(nx, ny) and vecino not in visitados:
                padres[vecino] = actual
                h_vecino = heuristica(vecino, meta)
                heapq.heappush(cola_prioridad, (h_vecino, vecino))

    return []
