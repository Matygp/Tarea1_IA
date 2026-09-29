import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import threading
import random
import json
import os
from datetime import datetime
from Simulacion import ejecutar_simulacion, ejecutar_benchmarking
from CargadorMapa import cargar_mapa, validar_mapa


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
        self.iteraciones = 200
        self.ejecutando = False
        self.pausado = False
        self.modo_benchmarking = False
        
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
        
        # Iteraciones
        tk.Label(frame_controles, text="Iteraciones:", bg=self.colores['panel'], 
                fg=self.colores['texto'], font=("Arial", 9)).pack(anchor=tk.W, pady=1)
        self.entry_iteraciones = tk.Entry(frame_controles, width=10)
        self.entry_iteraciones.insert(0, "200")
        self.entry_iteraciones.pack(fill=tk.X, pady=2)
        
        # Semilla
        tk.Label(frame_controles, text="Semilla (opcional):", bg=self.colores['panel'], 
                fg=self.colores['texto'], font=("Arial", 9)).pack(anchor=tk.W, pady=1)
        self.entry_semilla = tk.Entry(frame_controles, width=10)
        self.entry_semilla.insert(0, "42")
        self.entry_semilla.pack(fill=tk.X, pady=2)
        
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
        self.btn_iniciar = tk.Button(frame_controles, text="Iniciar Simulación", 
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
        
        self.btn_benchmarking = tk.Button(frame_controles, text="Ejecutar Benchmarking", 
                                         command=self._ejecutar_benchmarking,
                                         bg='#2196F3', fg='white', 
                                         font=("Arial", 10, "bold"))
        self.btn_benchmarking.pack(fill=tk.X, pady=2)
        
        self.btn_graficas = tk.Button(frame_controles, text="Gráficas", 
                                     command=self._generar_graficas,
                                     bg='#9C27B0', fg='white', 
                                     font=("Arial", 10, "bold"))
        self.btn_graficas.pack(fill=tk.X, pady=2)
        
        # Barra de progreso
        self.progreso = ttk.Progressbar(frame_controles, mode='indeterminate', length=200)
        self.progreso.pack(fill=tk.X, pady=10)
        
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
        
        # Panel central (Canvas del mapa con scrollbars)
        frame_canvas = tk.LabelFrame(frame_principal, text="Mapa", 
                                    font=("Arial", 12, "bold"), 
                                    bg=self.colores['panel'], fg=self.colores['texto'])
        frame_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para canvas con scrollbars
        frame_canvas_inner = tk.Frame(frame_canvas, bg=self.colores['panel'])
        frame_canvas_inner.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbars
        self.scroll_x = tk.Scrollbar(frame_canvas_inner, orient=tk.HORIZONTAL)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.scroll_y = tk.Scrollbar(frame_canvas_inner, orient=tk.VERTICAL)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas con scrollbars
        self.canvas = tk.Canvas(frame_canvas_inner, bg=self.colores['vacio'], 
                               highlightthickness=0,
                               xscrollcommand=self.scroll_x.set,
                               yscrollcommand=self.scroll_y.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scroll_x.config(command=self.canvas.xview)
        self.scroll_y.config(command=self.canvas.yview)
        
        # Panel inferior (Resultados)
        frame_resultados = tk.LabelFrame(frame_principal, text="Resultados", 
                                        font=("Arial", 12, "bold"), 
                                        bg=self.colores['panel'], fg=self.colores['texto'])
        frame_resultados.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.texto_resultados = ScrolledText(frame_resultados, height=8, 
                                            font=("Consolas", 10),
                                            bg=self.colores['fondo'], fg=self.colores['texto'])
        self.texto_resultados.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
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
            
            # Mostrar información
            self.texto_resultados.delete(1.0, tk.END)
            self.texto_resultados.insert(tk.END, f"Mapa cargado: {nombre_archivo}\n")
            self.texto_resultados.insert(tk.END, f"Dimensiones: {len(mapa[0])}x{len(mapa)}\n")
            self.texto_resultados.insert(tk.END, f"Salida: {salida}\n\n")
            
            self.label_estado.config(text=f"Mapa cargado: {nombre_archivo}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar mapa: {str(e)}")
    
    def _dibujar_mapa(self):
        """Dibuja el mapa en el canvas."""
        if not self.mapa:
            return
        
        self.canvas.delete("all")
        
        filas = len(self.mapa)
        columnas = len(self.mapa[0])
        
        # Tamaño de celda fijo según el tamaño del mapa
        if filas <= 15:
            celda = 40
        elif filas <= 25:
            celda = 30
        elif filas <= 35:
            celda = 20
        else:  # 50x50 o más
            celda = 15
        
        # Calcular dimensiones totales del mapa
        mapa_ancho = columnas * celda
        mapa_alto = filas * celda
        
        # Configurar región de scroll
        self.canvas.config(scrollregion=(0, 0, mapa_ancho, mapa_alto))
        
        # Centrar mapa inicialmente
        ancho_canvas = self.canvas.winfo_width()
        alto_canvas = self.canvas.winfo_height()
        
        if ancho_canvas > 1 and alto_canvas > 1:
            offset_x = max(0, (ancho_canvas - mapa_ancho) // 2)
            offset_y = max(0, (alto_canvas - mapa_alto) // 2)
        else:
            offset_x = 0
            offset_y = 0
        
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
        """Inicia la simulación visual."""
        if not self.mapa:
            messagebox.showwarning("Advertencia", "Carga un mapa primero")
            return
        
        if self.ejecutando:
            return
        
        self.ejecutando = True
        self.pausado = False
        self.turno = 0
        self.modo_benchmarking = False
        
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
        
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_resultados.insert(tk.END, f"Simulación iniciada con {self.algoritmo.upper()}\n")
        self.texto_resultados.insert(tk.END, f"Agentes: {num_agentes}\n")
        self.texto_resultados.insert(tk.END, f"K fuego: {self.k_fuego}\n\n")
        
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
            self.texto_resultados.insert(tk.END, f"Turno {self.turno}: Fuego propagado ({len(self.fuego)} celdas)\n")
            self.texto_resultados.see(tk.END)
        
        # Mover agentes
        for ag in self.agentes:
            if ag['estado'] != 'vivo':
                continue
            
            # Verificar si está en fuego
            if ag['posicion'] in self.fuego:
                ag['estado'] = 'atrapado'
                self.texto_resultados.insert(tk.END, f"Agente {ag['id']} atrapado por el fuego!\n")
                self.texto_resultados.see(tk.END)
                continue
            
            # Obtener camino si no tiene
            if not ag['camino'] or len(ag['camino']) <= 1:
                from Mapa import Mapa_evacuacion
                entorno = Mapa_evacuacion(self.mapa, self.salida)
                entorno.fuego = self.fuego
                
                if self.algoritmo == "a_star":
                    from algoritmos.A_estrella import busqueda_a_estrella
                    ag['camino'] = busqueda_a_estrella(ag['posicion'], self.salida, entorno)
                elif self.algoritmo == "ucs":
                    from algoritmos.Costo_uniforme import busqueda_ucs
                    ag['camino'] = busqueda_ucs(ag['posicion'], self.salida, entorno)
                elif self.algoritmo == "bfs":
                    from algoritmos.BFS import busqueda_bfs
                    ag['camino'] = busqueda_bfs(ag['posicion'], self.salida, entorno)
                elif self.algoritmo == "greedy":
                    from algoritmos.Greedy import busqueda_greedy
                    ag['camino'] = busqueda_greedy(ag['posicion'], self.salida, entorno)
                elif self.algoritmo == "genetico":
                    from algoritmos.Genetico import busqueda_genetico
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
                self.texto_resultados.insert(tk.END, f"Agente {ag['id']} evacuado!\n")
                self.texto_resultados.see(tk.END)
        
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
            self.texto_resultados.insert(tk.END, f"\nSimulación finalizada en {self.turno} turnos\n")
            self.texto_resultados.insert(tk.END, f"Supervivencia: {evacuados}/{len(self.agentes)} ({100*evacuados/len(self.agentes):.1f}%)\n")
            self.texto_resultados.see(tk.END)
            
            # Guardar datos
            self._guardar_datos()
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
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_resultados.insert(tk.END, "Simulación reiniciada\n")
    
    def _ejecutar_benchmarking(self):
        """Ejecuta el benchmarking con 200 iteraciones."""
        if not self.mapa:
            messagebox.showwarning("Advertencia", "Carga un mapa primero")
            return
        
        if self.ejecutando:
            return
        
        # Obtener configuración
        self.algoritmo = self.combo_algoritmo.get()
        self.k_fuego = int(self.entry_k_fuego.get())
        self.iteraciones = int(self.entry_iteraciones.get())
        
        semilla_str = self.entry_semilla.get()
        semilla = int(semilla_str) if semilla_str else None
        
        # Deshabilitar botón
        self.btn_benchmarking.config(state=tk.DISABLED)
        self.progreso.start()
        self.label_estado.config(text=f"Ejecutando {self.iteraciones} iteraciones...")
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_resultados.insert(tk.END, f"Ejecutando benchmarking con {self.iteraciones} iteraciones...\n")
        self.texto_resultados.see(tk.END)
        
        # Ejecutar en hilo separado
        hilo = threading.Thread(target=self._ejecutar_benchmarking_hilo, args=(semilla,))
        hilo.start()
    
    def _ejecutar_benchmarking_hilo(self, semilla):
        """Ejecuta el benchmarking en un hilo separado."""
        try:
            # Generar posiciones base
            posiciones_base = [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0), (0, 3)]
            focos_fuego_base = {(0, 9)}
            
            # Ejecutar benchmarking
            gestor = ejecutar_benchmarking(
                self.mapa, self.salida, posiciones_base, focos_fuego_base,
                algoritmo=self.algoritmo, iteraciones=self.iteraciones, 
                k_fuego=self.k_fuego, semilla=semilla
            )
            
            stats = gestor.calcular_estadisticas()
            
            # Obtener listas de datos individuales
            turnos_lista = gestor.tiempos_despeje
            supervivencia_lista = gestor.tasas_supervivencia
            
            # Guardar datos para gráficas
            self._guardar_datos_benchmarking(stats, turnos_lista, supervivencia_lista)
            
            # Actualizar UI
            self.root.after(0, self._mostrar_resultados_benchmarking, stats)
            
        except Exception as e:
            self.root.after(0, messagebox.showerror, "Error", str(e))
        finally:
            self.root.after(0, self._finalizar_benchmarking)
    
    def _mostrar_resultados_benchmarking(self, stats):
        """Muestra los resultados del benchmarking."""
        resultado_texto = f"""
{'='*50}
RESULTADOS DEL BENCHMARKING
{'='*50}

Algoritmo: {stats['algoritmo'].upper()}
Iteraciones: {stats['iteraciones']}

--- SUPERVIVENCIA ---
  Tasa de supervivencia media: {stats['supervivencia_media']:.2f}%
  Desviación estándar: {stats['supervivencia_std']:.2f}

--- TIEMPO (TURNOS) ---
  Media: {stats['tiempo_media']:.2f}
  Desviación estándar: {stats['tiempo_std']:.2f}
  Valor mínimo: {stats['tiempo_min']}
  Valor máximo: {stats['tiempo_max']}

{'='*50}
"""
        
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_resultados.insert(tk.END, resultado_texto)
        self.texto_resultados.see(tk.END)
    
    def _finalizar_benchmarking(self):
        """Habilita el botón al finalizar."""
        self.btn_benchmarking.config(state=tk.NORMAL)
        self.progreso.stop()
        self.label_estado.config(text="Benchmarking completado")
    
    def _generar_graficas(self):
        """Genera las gráficas desde los datos del juego."""
        try:
            from metricas.Graficas import generar_graficas_desde_juego, generar_diagrama_caja
            generar_graficas_desde_juego()
            generar_diagrama_caja()
            self.label_estado.config(text="Gráficas generadas en 'resultados/'")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráficas: {str(e)}")
    
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
        
        self.texto_resultados.insert(tk.END, f"\nDatos guardados en: {filename}\n")
        self.texto_resultados.see(tk.END)
        return filename
    
    def _guardar_datos_benchmarking(self, stats, turnos_lista, supervivencia_lista):
        """Guarda los datos del benchmarking para las gráficas."""
        os.makedirs('resultados', exist_ok=True)
        filename = f"resultados/benchmarking_{self.algoritmo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        datos = {
            'fecha': datetime.now().isoformat(),
            'algoritmo': self.algoritmo,
            'iteraciones': self.iteraciones,
            'turnos': turnos_lista,  # Lista de turnos de cada iteración
            'supervivencia': supervivencia_lista,  # Lista de supervivencia de cada iteración
            'agentes': [],
            'fuego_final': [],
            'salida': self.salida,
            'estadisticas': {
                'total_agentes': 6,
                'evacuados': int(stats['supervivencia_media'] / 100 * 6),
                'atrapados': 6 - int(stats['supervivencia_media'] / 100 * 6),
                'tasa_supervivencia': stats['supervivencia_media']
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(datos, f, indent=2)
        
        self.texto_resultados.insert(tk.END, f"Datos de benchmarking guardados en: {filename}\n")
        self.texto_resultados.see(tk.END)


def main():
    root = tk.Tk()
    app = JuegoEvacuacion(root)
    root.mainloop()


if __name__ == "__main__":
    main()
