from collections import deque


def busqueda_bfs(inicio, meta, entorno):
   
    cola = deque([inicio])
    visitados = {inicio}
    padres = {inicio: None}

    while cola:
        actual = cola.popleft()

        if actual == meta:
            # Reconstruir camino
            camino = []
            nodo = actual
            while nodo is not None:
                camino.append(nodo)
                nodo = padres[nodo]
            return camino[::-1]

        x, y = actual
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:  # Incluye esperar
            nx, ny = x + dx, y + dy
            vecino = (nx, ny)

            if entorno.es_valido(nx, ny) and vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = actual
                cola.append(vecino)

    return []  # No se encontró camino
