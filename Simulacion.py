import random
from Mapa import Mapa_evacuacion
from Agente import Agente
from metricas.Metricas import GestorMetricas


def _posiciones_validas(mapa, salida):
    """Obtiene todas las celdas válidas (no muros) del mapa."""
    validas = []
    for y in range(len(mapa)):
        for x in range(len(mapa[0])):
            if mapa[y][x] == 0 and (x, y) != salida:
                validas.append((x, y))
    return validas


def ejecutar_simulacion(mapa, salida, posiciones_iniciales, focos_fuego_iniciales, k_fuego=5, algoritmo="a_star", max_turnos=300):
    # Validaciones básicas
    if not mapa or not mapa[0]:
        raise ValueError("El mapa no puede estar vacío")
    
    alto = len(mapa)
    ancho = len(mapa[0])
    
    sx, sy = salida
    if not (0 <= sx < ancho and 0 <= sy < alto):
        raise ValueError(f"La salida {salida} está fuera del mapa")
    if mapa[sy][sx] != 0:
        raise ValueError(f"La salida {salida} es un muro")
    
    for pos in posiciones_iniciales:
        px, py = pos
        if not (0 <= px < ancho and 0 <= py < alto):
            raise ValueError(f"Posición inicial {pos} fuera del mapa")
        if mapa[py][px] != 0:
            raise ValueError(f"Posición inicial {pos} es un muro")
    
    if algoritmo not in ("a_star", "ucs", "bfs", "greedy", "genetico"):
        raise ValueError(f"Algoritmo desconocido: {algoritmo}")

    entorno = Mapa_evacuacion(mapa, salida)
    entorno.fuego.update(focos_fuego_iniciales)
    
    agentes = [Agente(i, pos) for i, pos in enumerate(posiciones_iniciales)]
    
    turno = 0
    while turno < max_turnos:
        turno += 1
        
        # 1. Actualizar conteo de ocupación del entorno
        entorno.ocupacion.clear()
        vivos_restantes = 0
        for ag in agentes:
            if ag.estado == "vivo":
                vivos_restantes += 1
                entorno.ocupacion[ag.posicion] = entorno.ocupacion.get(ag.posicion, 0) + 1

        if vivos_restantes == 0:
            break

        # 2. Propagar fuego cada k turnos (ANTES de mover agentes)
        if turno % k_fuego == 0:
            entorno.propagar_fuego()

        # 3. Mover agentes
        for ag in agentes:
            if ag.estado == "vivo":
                if ag.posicion in entorno.fuego:
                    ag.estado = "atrapado"
                    continue
                
                ag.decidir_movimiento(entorno, algoritmo)
                
                if ag.posicion in entorno.fuego:
                    ag.estado = "atrapado"

    total_agentes = len(agentes)
    supervivientes = sum(1 for ag in agentes if ag.estado == "evacuado")
    tasa_supervivencia = (supervivientes / total_agentes) * 100.0 if total_agentes > 0 else 0.0
    
    return tasa_supervivencia, turno


def ejecutar_benchmarking(mapa, salida, posiciones_iniciales_base, focos_fuego_base, algoritmo="a_star", iteraciones=200, k_fuego=5, semilla=None):
 
    if semilla is not None:
        random.seed(semilla)
    
    gestor = GestorMetricas(algoritmo, iteraciones)
    
    posiciones_validas = _posiciones_validas(mapa, salida)
    num_agentes = len(posiciones_iniciales_base)
    num_focos = len(focos_fuego_base)
    
    for _ in range(iteraciones):
        # Generar posiciones iniciales aleatorias
        if len(posiciones_validas) >= num_agentes:
            posiciones = random.sample(posiciones_validas, num_agentes)
        else:
            posiciones = random.choices(posiciones_validas, k=num_agentes)
        
        # Generar focos de fuego aleatorios
        focos_fuego = set(random.sample(posiciones_validas, min(num_focos, len(posiciones_validas))))

        tasa, turnos = ejecutar_simulacion(
            mapa=mapa,
            salida=salida,
            posiciones_iniciales=posiciones,
            focos_fuego_iniciales=focos_fuego,
            k_fuego=k_fuego,
            algoritmo=algoritmo
        )

        gestor.registrar_ejecucion(tasa, turnos)

    return gestor
