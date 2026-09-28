import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import threading
import random
import json
import os
from datetime import datetime
from Simulacion import ejecutar_simulacion
from CargadorMapa import cargar_mapa, validar_mapa
from algoritmos.A_estrella import busqueda_a_estrella
from algoritmos.Costo_uniforme import busqueda_ucs
from algoritmos.BFS import busqueda_bfs
from algoritmos.Greedy import busqueda_greedy
from algoritmos.Genetico import busqueda_genetico


class JuegoEvacuacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Escape de la Torre - Simulación de Evacuación")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        
        # Variables del juego
        self.mapa = None
        self.salida = None
        self.agentes = []
        self.fuego = set()
        self.ocupacion = {}
        self.turno = 0
        self.k_fuego = 4
        self.algoritmo = "a_star"
        self.ejecutando = False
        self.pausado = False
        
        # Colores del juego
        self.colores = {
            'vacio': '#16213e',
            'muro': '#0f3460',
            'salida': '#00ff00',
            'fuego': '#ff4500',
            'agente': '#00d4ff',
            'agente_evacuado': '#00ff88',
            'agente_atrapado': '#ff0000',
            'texto': '#ffffff',
            'fondo': '#1a1a2e',
            'panel': '#16213e',
            'boton': '#0f3460',
            'boton_hover': '#1a4a7a'
        }
        
        self._crear_widgets()
    
    def _crear_widgets(self):
        # Título
        titulo = tk.Label(self.root, text="ESCAPE DE LA TORRE", 
                         font=("Arial", 20, "bold"), bg=self.colores['fondo'], 
                         fg=self.colores['texto'])
        titulo.pack(pady=10)
        
        # Frame principal
        frame_principal = tk.Frame(self.root, bg=self.colores['fondo'])
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Panel izquierdo (Controles)
        frame_controles = tk.LabelFrame(frame_principal, text="Controles", 
                                        font=("Arial", 12, "bold"), 
                                        bg=self.colores['panel'], fg=self.colores['texto'])
        frame_controles.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Cargar mapa
        tk.Label(frame_controles, text="Mapa:", bg=self.colores['panel'], 
                fg=self.colores['texto'], font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=2)
        
        self.btn_cargar = tk.Button(frame_controles, text="Cargar Mapa", 
                                   command=self._cargar_mapa,
                                   bg='#ff9800', fg='white', 
                                   font=("Arial", 10, "bold"))
        self.btn_cargar.pack(fill=tk.X, pady=2)
        
        self.label_mapa = tk.Label(frame_controles, text="No cargado", 
                                  bg=self.colores['panel'], fg='gray', 
                                  font=("Arial", 8))
        self.label_mapa.pack(anchor=tk.W, pady=2)
        
        # Separador
        ttk.Separator(frame_controles, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Configuración
        tk.Label(frame_controles, text="Configuración:", bg=self.colores['panel'], 
                fg=self.colores['texto'], font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=2)
        
        # Algoritmo
        tk.Label(frame_controles, text="Algoritmo:", bg=self.colores['panel'], 
                fg=self.colores['texto'], font=("Arial", 9)).pack(anchor=tk.W, pady=1)
        self.combo_algoritmo = ttk.Combobox(frame_controles, 
                                           values=["a_star", "ucs", "bfs", "greedy", "genetico"], 
                                           state="readonly", width=15)
        self.combo_algoritmo.set("a_star")
        self.combo_algoritmo.pack(fill=tk.X, pady=2)
        
        # K fuego
        tk.Label(frame_controles, text="K (fuego):", bg=self.colores['panel'], 
                fg=self.colores['texto'], font=("Arial", 9)).pack(anchor=tk.W, pady=1)
        self.entry_k_fuego = tk.Entry(frame_controles, width=10)
        self.entry_k_fuego.insert(0, "4")
        self.entry_k_fuego.pack(fill=tk.X, pady=2)
        
        # Velocidad
        tk.Label(frame_controles, text="Velocidad:", bg=self.colores['panel'], 
                fg=self.colores['texto'], font=("Arial", 9)).pack(anchor=tk.W, pady=1)
        self.scale_velocidad = tk.Scale(frame_controles, from_=1, to=10, 
                                       orient=tk.HORIZONTAL, bg=self.colores['panel'],
                                       fg=self.colores['texto'], highlightthickness=0)
        self.scale_velocidad.set(5)
        self.scale_velocidad.pack(fill=tk.X, pady=2)
        
        # Separador
        ttk.Separator(frame_controles, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Botones de control
        self.btn_iniciar = tk.Button(frame_controles, text="Iniciar", 
                                    command=self._iniciar_simulacion,
                                    bg='#4CAF50', fg='white', 
                                    font=("Arial", 10, "bold"))
        self.btn_iniciar.pack(fill=tk.X, pady=2)
        
        self.btn_pausar = tk.Button(frame_controles, text="Pausar", 
                                   command=self._pausar_simulacion,
                                   bg='#FFC107', fg='black', 
                                   font=("Arial", 10, "bold"), state=tk.DISABLED)
        self.btn_pausar.pack(fill=tk.X, pady=2)
        
        self.btn_reiniciar = tk.Button(frame_controles, text="Reiniciar", 
                                      command=self._reiniciar_simulacion,
                                      bg='#f44336', fg='white', 
                                      font=("Arial", 10, "bold"))
        self.btn_reiniciar.pack(fill=tk.X, pady=2)
        
        # Separador
        ttk.Separator(frame_controles, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Estadísticas en vivo
        tk.Label(frame_controles, text="Estadísticas:", bg=self.colores['panel'], 
                fg=self.colores['texto'], font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=2)
        
        self.label_turno = tk.Label(frame_controles, text="Turno: 0", 
                                   bg=self.colores['panel'], fg=self.colores['texto'], 
                                   font=("Arial", 9))
        self.label_turno.pack(anchor=tk.W, pady=1)
        
        self.label_vivos = tk.Label(frame_controles, text="Vivos: 0", 
                                    bg=self.colores['panel'], fg=self.colores['texto'], 
                                    font=("Arial", 9))
        self.label_vivos.pack(anchor=tk.W, pady=1)
        
        self.label_evacuados = tk.Label(frame_controles, text="Evacuados: 0", 
                                       bg=self.colores['panel'], fg=self.colores['texto'], 
                                       font=("Arial", 9))
        self.label_evacuados.pack(anchor=tk.W, pady=1)
        
        self.label_atrapados = tk.Label(frame_controles, text="Atrapados: 0", 
                                       bg=self.colores['panel'], fg=self.colores['texto'], 
                                       font=("Arial", 9))
        self.label_atrapados.pack(anchor=tk.W, pady=1)
        
        # Panel central (Canvas del mapa)
        frame_canvas = tk.LabelFrame(frame_principal, text="Mapa", 
                                    font=("Arial", 12, "bold"), 
                                    bg=self.colores['panel'], fg=self.colores['texto'])
        frame_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(frame_canvas, bg=self.colores['vacio'], 
                               highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel inferior (Log)
        frame_log = tk.LabelFrame(frame_principal, text="Log de Eventos", 
                                 font=("Arial", 12, "bold"), 
                                 bg=self.colores['panel'], fg=self.colores['texto'])
        frame_log.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.texto_log = ScrolledText(frame_log, height=6, 
                                     font=("Consolas", 9),
                                     bg=self.colores['fondo'], fg=self.colores['texto'])
        self.texto_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Mensaje de estado
        self.label_estado = tk.Label(self.root, text="Carga un mapa para comenzar", 
                                    bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                    font=("Arial", 9), bg=self.colores['panel'], 
                                    fg=self.colores['texto'])
        self.label_estado.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _cargar_mapa(self):
        """Carga un mapa desde un archivo."""
        try:
            ruta = filedialog.askopenfilename(
                title="Seleccionar mapa",
                filetypes=[
                    ("Todos los soportados", "*.txt *.csv *.json"),
                    ("Archivos JSON", "*.json"),
                    ("Archivos CSV", "*.csv"),
                    ("Archivos TXT", "*.txt"),
                    ("Todos los archivos", "*.*")
                ]
            )
            
            if not ruta:
                return
            
            mapa, salida = cargar_mapa(ruta)
            es_valido, mensaje = validar_mapa(mapa)
            
            if not es_valido:
                messagebox.showerror("Error", f"Mapa inválido: {mensaje}")
                return
            
            self.mapa = mapa
            self.salida = salida
            
            # Actualizar etiqueta
            nombre_archivo = ruta.split("/")[-1].split("\\")[-1]
            self.label_mapa.config(text=nombre_archivo, fg='#00ff00')
            
            # Dibujar mapa
            self._dibujar_mapa()
            
            # Log
            self._log(f"Mapa cargado: {nombre_archivo}")
            self._log(f"Dimensiones: {len(mapa[0])}x{len(mapa)}")
            self._log(f"Salida: {salida}")
            
            self.label_estado.config(text=f"Mapa cargado: {nombre_archivo}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar mapa: {str(e)}")
    
    def _dibujar_mapa(self):
        """Dibuja el mapa en el canvas."""
        if not self.mapa:
            return
        
        self.canvas.delete("all")
        
        # Calcular tamaño de celda
        ancho_canvas = self.canvas.winfo_width()
        alto_canvas = self.canvas.winfo_height()
        
        # Si el canvas aún no tiene tamaño, usar valores por defecto
        if ancho_canvas <= 1 or alto_canvas <= 1:
            ancho_canvas = 600
            alto_canvas = 500
        
        filas = len(self.mapa)
        columnas = len(self.mapa[0])
        
        celda_ancho = ancho_canvas // columnas
        celda_alto = alto_canvas // filas
        celda = min(celda_ancho, celda_alto)
        
        # Asegurar que las celdas sean visibles (mínimo 10px para mapas grandes)
        celda = max(celda, 10)
        
        # Centrar mapa
        offset_x = (ancho_canvas - columnas * celda) // 2
        offset_y = (alto_canvas - filas * celda) // 2
        
        self.celda_size = celda
        self.offset_x = offset_x
        self.offset_y = offset_y
        
        # Dibujar celdas
        for y in range(filas):
            for x in range(columnas):
                x1 = offset_x + x * celda
                y1 = offset_y + y * celda
                x2 = x1 + celda
                y2 = y1 + celda
                
                if self.mapa[y][x] == 1:
                    color = self.colores['muro']
                elif (x, y) == self.salida:
                    color = self.colores['salida']
                else:
                    color = self.colores['vacio']
                
                self.canvas.create_rectangle(x1, y1, x2, y2, 
                                            fill=color, outline='#333333', width=1)
        
        # Dibujar agentes
        for ag in self.agentes:
            self._dibujar_agente(ag)
        
        # Dibujar fuego
        for f in self.fuego:
            self._dibujar_fuego(f)
    
    def _dibujar_agente(self, agente):
        """Dibuja un agente en el canvas."""
        if not hasattr(self, 'celda_size'):
            return
        
        x, y = agente['posicion']
        celda = self.celda_size
        offset_x = self.offset_x
        offset_y = self.offset_y
        
        x1 = offset_x + x * celda + celda // 4
        y1 = offset_y + y * celda + celda // 4
        x2 = x1 + celda // 2
        y2 = y1 + celda // 2
        
        if agente['estado'] == 'vivo':
            color = self.colores['agente']
        elif agente['estado'] == 'evacuado':
            color = self.colores['agente_evacuado']
        else:
            color = self.colores['agente_atrapado']
        
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline='white', width=2)
    
    def _dibujar_fuego(self, pos):
        """Dibuja fuego en una posición."""
        if not hasattr(self, 'celda_size'):
            return
        
        x, y = pos
        celda = self.celda_size
        offset_x = self.offset_x
        offset_y = self.offset_y
        
        x1 = offset_x + x * celda
        y1 = offset_y + y * celda
        x2 = x1 + celda
        y2 = y1 + celda
        
        self.canvas.create_rectangle(x1, y1, x2, y2, 
                                    fill=self.colores['fuego'], outline='#ff6600', width=1)
    
    def _iniciar_simulacion(self):
        """Inicia la simulación."""
        if not self.mapa:
            messagebox.showwarning("Advertencia", "Carga un mapa primero")
            return
        
        if self.ejecutando:
            return
        
        self.ejecutando = True
        self.pausado = False
        self.turno = 0
        
        # Obtener configuración
        self.algoritmo = self.combo_algoritmo.get()
        self.k_fuego = int(self.entry_k_fuego.get())
        
        # Generar posiciones iniciales aleatorias
        posiciones_validas = []
        for y in range(len(self.mapa)):
            for x in range(len(self.mapa[0])):
                if self.mapa[y][x] == 0 and (x, y) != self.salida:
                    posiciones_validas.append((x, y))
        
        num_agentes = min(6, len(posiciones_validas))
        posiciones_iniciales = random.sample(posiciones_validas, num_agentes)
        
        # Crear agentes
        self.agentes = []
        for i, pos in enumerate(posiciones_iniciales):
            self.agentes.append({
                'id': i,
                'posicion': pos,
                'estado': 'vivo',
                'camino': []
            })
        
        # Fuego inicial
        self.fuego = set()
        if len(posiciones_validas) > num_agentes:
            focos = random.sample(posiciones_validas[num_agentes:], 
                                min(1, len(posiciones_validas) - num_agentes))
            self.fuego = set(focos)
        
        # Actualizar UI
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_pausar.config(state=tk.NORMAL)
        self.label_estado.config(text="Simulación en curso...")
        
        self._log(f"Simulación iniciada con {self.algoritmo.upper()}")
        self._log(f"Agentes: {num_agentes}")
        self._log(f"K fuego: {self.k_fuego}")
        
        # Iniciar hilo de simulación
        hilo = threading.Thread(target=self._ejecutar_turno)
        hilo.start()
    
    def _ejecutar_turno(self):
        """Ejecuta un turno de la simulación."""
        if not self.ejecutando or self.pausado:
            return
        
        self.turno += 1
        
        # Propagar fuego
        if self.turno % self.k_fuego == 0:
            nuevo_fuego = set()
            for fx, fy in self.fuego:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = fx + dx, fy + dy
                    if (0 <= nx < len(self.mapa[0]) and 
                        0 <= ny < len(self.mapa) and 
                        self.mapa[ny][nx] == 0):
                        nuevo_fuego.add((nx, ny))
            self.fuego.update(nuevo_fuego)
            self._log(f"Turno {self.turno}: Fuego propagado ({len(self.fuego)} celdas)")
        
        # Mover agentes
        for ag in self.agentes:
            if ag['estado'] != 'vivo':
                continue
            
            # Verificar si está en fuego
            if ag['posicion'] in self.fuego:
                ag['estado'] = 'atrapado'
                self._log(f"Agente {ag['id']} atrapado por el fuego!")
                continue
            
            # Obtener camino si no tiene
            if not ag['camino'] or len(ag['camino']) <= 1:
                from Mapa import Mapa_evacuacion
                entorno = Mapa_evacuacion(self.mapa, self.salida)
                entorno.fuego = self.fuego
                
                if self.algoritmo == "a_star":
                    ag['camino'] = busqueda_a_estrella(ag['posicion'], self.salida, entorno)
                elif self.algoritmo == "ucs":
                    ag['camino'] = busqueda_ucs(ag['posicion'], self.salida, entorno)
                elif self.algoritmo == "bfs":
                    ag['camino'] = busqueda_bfs(ag['posicion'], self.salida, entorno)
                elif self.algoritmo == "greedy":
                    ag['camino'] = busqueda_greedy(ag['posicion'], self.salida, entorno)
                elif self.algoritmo == "genetico":
                    ag['camino'] = busqueda_genetico(ag['posicion'], self.salida, entorno)
            
            # Mover
            if len(ag['camino']) > 1:
                ag['camino'].pop(0)
                nueva_pos = ag['camino'][0]
                
                # Verificar validez
                if (0 <= nueva_pos[0] < len(self.mapa[0]) and 
                    0 <= nueva_pos[1] < len(self.mapa) and 
                    self.mapa[nueva_pos[1]][nueva_pos[0]] == 0):
                    ag['posicion'] = nueva_pos
            
            # Verificar si llegó a la salida
            if ag['posicion'] == self.salida and ag['posicion'] not in self.fuego:
                ag['estado'] = 'evacuado'
                self._log(f"Agente {ag['id']} evacuado!")
        
        # Actualizar estadísticas
        vivos = sum(1 for ag in self.agentes if ag['estado'] == 'vivo')
        evacuados = sum(1 for ag in self.agentes if ag['estado'] == 'evacuado')
        atrapados = sum(1 for ag in self.agentes if ag['estado'] == 'atrapado')
        
        self.label_turno.config(text=f"Turno: {self.turno}")
        self.label_vivos.config(text=f"Vivos: {vivos}")
        self.label_evacuados.config(text=f"Evacuados: {evacuados}")
        self.label_atrapados.config(text=f"Atrapados: {atrapados}")
        
        # Redibujar
        self._dibujar_mapa()
        
        # Verificar fin
        if vivos == 0:
            self.ejecutando = False
            self.btn_iniciar.config(state=tk.NORMAL)
            self.btn_pausar.config(state=tk.DISABLED)
            self.label_estado.config(text="Simulación finalizada")
            self._log(f"Simulación finalizada en {self.turno} turnos")
            self._log(f"Supervivencia: {evacuados}/{len(self.agentes)} ({100*evacuados/len(self.agentes):.1f}%)")
            
            # Guardar datos de la simulación
            filename = self._guardar_datos()
            if filename:
                self._log(f"Resultados guardados en: {filename}")
            
            return
        
        # Programar siguiente turno
        velocidad = 11 - self.scale_velocidad.get()
        self.root.after(velocidad * 50, self._ejecutar_turno)
    
    def _pausar_simulacion(self):
        """Pausa o reanuda la simulación."""
        self.pausado = not self.pausado
        if self.pausado:
            self.btn_pausar.config(text="Reanudar")
            self.label_estado.config(text="Simulación pausada")
        else:
            self.btn_pausar.config(text="Pausar")
            self.label_estado.config(text="Simulación en curso...")
            self._ejecutar_turno()
    
    def _reiniciar_simulacion(self):
        """Reinicia la simulación."""
        self.ejecutando = False
        self.pausado = False
        self.turno = 0
        self.agentes = []
        self.fuego = set()
        
        self.btn_iniciar.config(state=tk.NORMAL)
        self.btn_pausar.config(state=tk.DISABLED, text="Pausar")
        self.label_estado.config(text="Simulación reiniciada")
        
        self.label_turno.config(text="Turno: 0")
        self.label_vivos.config(text="Vivos: 0")
        self.label_evacuados.config(text="Evacuados: 0")
        self.label_atrapados.config(text="Atrapados: 0")
        
        self._dibujar_mapa()
        self._log("Simulación reiniciada")
    
    def _log(self, mensaje):
        """Agrega un mensaje al log."""
        self.texto_log.insert(tk.END, f"{mensaje}\n")
        self.texto_log.see(tk.END)
    
    def _guardar_datos(self):
        """Guarda los datos de la simulación en un archivo JSON."""
        if not self.agentes:
            return
        
        # Crear estructura de datos
        datos = {
            'fecha': datetime.now().isoformat(),
            'algoritmo': self.algoritmo,
            'k_fuego': self.k_fuego,
            'turnos': self.turno,
            'agentes': [],
            'fuego_final': list(self.fuego),
            'salida': self.salida
        }
        
        # Guardar datos de cada agente
        for ag in self.agentes:
            datos['agentes'].append({
                'id': ag['id'],
                'posicion_inicial': ag.get('posicion_inicial', ag['posicion']),
                'posicion_final': ag['posicion'],
                'estado': ag['estado'],
                'turnos': self.turno
            })
        
        # Calcular estadísticas
        total = len(self.agentes)
        evacuados = sum(1 for ag in self.agentes if ag['estado'] == 'evacuado')
        atrapados = sum(1 for ag in self.agentes if ag['estado'] == 'atrapado')
        
        datos['estadisticas'] = {
            'total_agentes': total,
            'evacuados': evacuados,
            'atrapados': atrapados,
            'tasa_supervivencia': (evacuados / total * 100) if total > 0 else 0
        }
        
        # Guardar en archivo
        os.makedirs('resultados', exist_ok=True)
        filename = f"resultados/simulacion_{self.algoritmo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(datos, f, indent=2)
        
        self._log(f"Datos guardados en: {filename}")
        return filename


def main():
    root = tk.Tk()
    app = JuegoEvacuacion(root)
    root.mainloop()


if __name__ == "__main__":
    main()
