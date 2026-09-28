import heapq


def heuristica(a, b):
    # Distancia Manhattan admisible
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def busqueda_a_estrella(inicio, meta, entorno):
    cola_prioridad = []
    h_inicial = heuristica(inicio, meta)
    heapq.heappush(cola_prioridad, (h_inicial, 0, inicio))
    visitados = set()
    padres = {inicio: None}
    costos = {inicio: 0}

    while cola_prioridad:
        f, g, actual = heapq.heappop(cola_prioridad)

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
                nuevo_g = g + entorno.obtener_costo(nx, ny)
                if vecino not in costos or nuevo_g < costos[vecino]:
                    costos[vecino] = nuevo_g
                    padres[vecino] = actual
                    nuevo_f = nuevo_g + heuristica(vecino, meta)
                    heapq.heappush(cola_prioridad, (nuevo_f, nuevo_g, vecino))
    return []
