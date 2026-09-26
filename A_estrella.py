import heapq

def heuristica(a, b):
    # Distancia Manhattan admisible
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def busqueda_a_estrella(inicio, meta, entorno):
    
    cola_prioridad = []
    h_inicial = heuristica(inicio, meta)
    heapq.heappush(cola_prioridad, (h_inicial, 0, inicio, [inicio]))
    visitados = set()

    while cola_prioridad:
        f, g, actual, camino = heapq.heappop(cola_prioridad)

        if actual == meta:
            return camino

        if actual in visitados:
            continue
        visitados.add(actual)

        x, y = actual
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (0,0)]:
            nx, ny = x + dx, y + dy
            vecino = (nx, ny)

            if entorno.es_valido(nx, ny):
                nuevo_g = g + entorno.obtener_costo(nx, ny)
                nuevo_f = nuevo_g + heuristica(vecino, meta)
                if vecino not in visitados:
                    heapq.heappush(cola_prioridad, (nuevo_f, nuevo_g, vecino, camino + [vecino]))
    return []