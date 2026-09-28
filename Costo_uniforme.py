import heapq


def busqueda_ucs(inicio, meta, entorno):
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (0, inicio))
    visitados = set()
    padres = {inicio: None}
    costos = {inicio: 0}

    while cola_prioridad:
        costo_acumulado, actual = heapq.heappop(cola_prioridad)

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
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:  # Incluye esperar (0,0)
            nx, ny = x + dx, y + dy
            vecino = (nx, ny)

            if entorno.es_valido(nx, ny) and vecino not in visitados:
                nuevo_costo = costo_acumulado + entorno.obtener_costo(nx, ny)
                if vecino not in costos or nuevo_costo < costos[vecino]:
                    costos[vecino] = nuevo_costo
                    padres[vecino] = actual
                    heapq.heappush(cola_prioridad, (nuevo_costo, vecino))
    return []
