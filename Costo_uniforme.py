import heapq

def busqueda_ucs(inicio, meta, entorno):
   
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (0, inicio, [inicio]))
    visitados = set()

    while cola_prioridad:
        costo_acumulado, actual, camino = heapq.heappop(cola_prioridad)

        if actual == meta:
            return camino

        if actual in visitados:
            continue
        visitados.add(actual)

        x, y = actual
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (0,0)]: # Incluye esperar (0,0)
            nx, ny = x + dx, y + dy
            vecino = (nx, ny)

            if entorno.es_valido(nx, ny):
                nuevo_costo = costo_acumulado + entorno.obtener_costo(nx, ny)
                if vecino not in visitados:
                    heapq.heappush(cola_prioridad, (nuevo_costo, vecino, camino + [vecino]))
    return []