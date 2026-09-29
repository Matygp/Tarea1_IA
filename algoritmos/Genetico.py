import random


def _generar_ruta_aleatoria(inicio, meta, entorno, max_pasos=50):
   
    ruta = [inicio]
    actual = inicio
    visitados = {inicio}

    for _ in range(max_pasos):
        if actual == meta:
            return ruta

        x, y = actual
        movimientos = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x, y)]
        validos = [(nx, ny) for nx, ny in movimientos 
                   if entorno.es_valido(nx, ny) and (nx, ny) not in visitados]

        if not validos:
            break

        actual = random.choice(validos)
        ruta.append(actual)
        visitados.add(actual)

    return ruta


def _fitness(ruta, entorno):
 
    if not ruta:
        return -10000

    puntaje = 0

    #  Bonus por llegar a la salida
    if ruta[-1] == entorno.salida:
        puntaje += 1000

    # Penalización por pasar por fuego
    for pos in ruta:
        if pos in entorno.fuego:
            puntaje -= 500

    # Penalización por longitud (rutas más cortas son mejores)
    puntaje -= len(ruta) * 10

    # Penalización por congestión
    for pos in ruta:
        personas = entorno.ocupacion.get(pos, 0)
        puntaje -= personas * 5

    # Bonus por distancia a la salida (más cerca = mejor)
    if ruta:
        distancia = abs(ruta[-1][0] - entorno.salida[0]) + abs(ruta[-1][1] - entorno.salida[1])
        puntaje -= distancia * 20

    return puntaje


def _seleccionar(poblacion, fitnesses):
   
    idx1, idx2 = random.sample(range(len(poblacion)), 2)
    if fitnesses[idx1] > fitnesses[idx2]:
        return poblacion[idx1]
    return poblacion[idx2]


def _cruzar(padre1, padre2):
    
    puntos_comunes = set(padre1) & set(padre2)
    if puntos_comunes and len(padre1) > 2 and len(padre2) > 2:
        punto_cruce = random.choice(list(puntos_comunes))
        idx1 = padre1.index(punto_cruce)
        idx2 = padre2.index(punto_cruce)
        hijo = padre1[:idx1] + padre2[idx2:]
        # Eliminar duplicados consecutivos
        hijo_limpio = [hijo[0]] if hijo else []
        for i in range(1, len(hijo)):
            if hijo[i] != hijo[i-1]:
                hijo_limpio.append(hijo[i])
        return hijo_limpio
    return padre1.copy()


def _mutar(ruta, entorno, probabilidad=0.1):
   
    if len(ruta) <= 2:
        return ruta.copy()

    nueva_ruta = [ruta[0]]  # Mantener inicio

    for i in range(1, len(ruta) - 1):
        if random.random() < probabilidad:
            # Cambia el movimiento por uno aleatorio válido
            x, y = ruta[i]
            movimientos = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x, y)]
            validos = [(nx, ny) for nx, ny in movimientos if entorno.es_valido(nx, ny)]
            if validos:
                nueva_ruta.append(random.choice(validos))
            else:
                nueva_ruta.append(ruta[i])
        else:
            nueva_ruta.append(ruta[i])

    nueva_ruta.append(ruta[-1])  # Mantener fin
    return nueva_ruta


def busqueda_genetico(inicio, meta, entorno, tamano_poblacion=30, generaciones=50, prob_mutacion=0.1):
    
    #  Generar población inicial
    poblacion = [_generar_ruta_aleatoria(inicio, meta, entorno) for _ in range(tamano_poblacion)]

    mejor_ruta = []
    mejor_fitness = -10000

    for generacion in range(generaciones):
        #  Evaluar fitness
        fitnesses = [_fitness(ruta, entorno) for ruta in poblacion]

        # Encontrar mejor ruta de esta generación
        for i, fit in enumerate(fitnesses):
            if fit > mejor_fitness:
                mejor_fitness = fit
                mejor_ruta = poblacion[i]

        # Crear nueva generación
        nueva_poblacion = []

        # Elitismo: mantener los mejores 2
        indices_ordenados = sorted(range(len(fitnesses)), key=lambda i: fitnesses[i], reverse=True)
        nueva_poblacion.append(poblacion[indices_ordenados[0]])
        if len(indices_ordenados) > 1:
            nueva_poblacion.append(poblacion[indices_ordenados[1]])

        # 5. Selección, cruce y mutación
        while len(nueva_poblacion) < tamano_poblacion:
            padre1 = _seleccionar(poblacion, fitnesses)
            padre2 = _seleccionar(poblacion, fitnesses)
            hijo = _cruzar(padre1, padre2)
            hijo = _mutar(hijo, entorno, prob_mutacion)
            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

    # Evaluar última generación
    fitnesses = [_fitness(ruta, entorno) for ruta in poblacion]
    for i, fit in enumerate(fitnesses):
        if fit > mejor_fitness:
            mejor_fitness = fit
            mejor_ruta = poblacion[i]

    return mejor_ruta
