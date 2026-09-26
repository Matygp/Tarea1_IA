class Mapa_evacuacion:
    def __init__(self, mapa_grilla, salida):

        self.mapa = mapa_grilla
        self.alto = len(mapa_grilla)
        self.ancho = len(mapa_grilla[0])
        self.salida = salida
        self.fuego = set()
        self.ocupacion = {} # diccionario para el numero de personas
        
    def es_valido(self, x, y):

        # Verifica límites, muros y celdas quemadas
        if 0 <= x < self.ancho and 0 <= y < self.alto:
            return self.mapa[y][x] == 0 and (x, y) not in self.fuego
        return False

    def obtener_costo(self, x, y):

        #Costo cuadrático por congestión de personas
        personas = self.ocupacion.get((x, y), 0)
        costo_base = 1.0
        alpha = 0.4  # Factor de penalización por saturación
        return costo_base + alpha * (personas ** 2)

    def propagar_fuego(self):

        # El fuego se propaga de forma irreversible cada k turnos
        nuevo_fuego = set()
        for fx, fy in self.fuego:
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = fx + dx, fy + dy
                if 0 <= nx < self.ancho and 0 <= ny < self.alto and self.mapa[ny][nx] == 0:
                    nuevo_fuego.add((nx, ny))
        self.fuego.update(nuevo_fuego)