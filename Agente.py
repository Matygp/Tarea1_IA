from A_estrella import busqueda_a_estrella
from Costo_uniforme import busqueda_ucs


class Agente:
    def __init__(self, id_agente, posicion_inicial):
        self.id = id_agente
        self.posicion = posicion_inicial
        self.estado = "vivo"  # "vivo", "evacuado", "atrapado"
        self.camino_actual = []

    def decidir_movimiento(self, entorno, algoritmo="a_star"):
        if self.estado != "vivo":
            return

        # Replanificación: Si no hay camino o el siguiente paso está bloqueado por fuego/obstáculo
        necesita_replanificar = False
        if not self.camino_actual or len(self.camino_actual) <= 1:
            necesita_replanificar = True
        else:
            siguiente_paso = self.camino_actual[1]
            if not entorno.es_valido(siguiente_paso[0], siguiente_paso[1]):
                necesita_replanificar = True

        if necesita_replanificar:
            if algoritmo == "a_star":
                self.camino_actual = busqueda_a_estrella(self.posicion, entorno.salida, entorno)
            elif algoritmo == "ucs":
                self.camino_actual = busqueda_ucs(self.posicion, entorno.salida, entorno)
            else:
                raise ValueError(f"Algoritmo desconocido: {algoritmo}")

        # Ejecutar movimiento si hay ruta válida
        if len(self.camino_actual) > 1:
            self.camino_actual.pop(0)
            nueva_pos = self.camino_actual[0]
            
            if entorno.es_valido(nueva_pos[0], nueva_pos[1]):
                self.posicion = nueva_pos
        
        # Verificar si llegó a la salida (y la salida no está en fuego)
        if self.posicion == entorno.salida and self.posicion not in entorno.fuego:
            self.estado = "evacuado"
