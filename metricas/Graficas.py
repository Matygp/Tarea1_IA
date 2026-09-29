import matplotlib
matplotlib.use('Agg')  # Modo sin display para guardar gráficas
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import sys
from glob import glob

# Agregar directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Simulacion import ejecutar_benchmarking


def generar_graficas(mapa, salida, posiciones_base, focos_fuego_base, k_fuego=4, iteraciones=200, semilla=42):
    

    algoritmos = ["a_star", "ucs", "bfs", "greedy", "genetico"]
    nombres = ["A*", "UCS", "BFS", "Greedy", "Genético"]
    colores = ["#2196F3", "#4CAF50", "#FF9800", "#F44336", "#9C27B0"]
    
    # Ejecutar benchmarking para todos los algoritmos
    resultados = {}
    for alg in algoritmos:
        gestor = ejecutar_benchmarking(
            mapa, salida, posiciones_base, focos_fuego_base,
            algoritmo=alg, iteraciones=iteraciones, k_fuego=k_fuego, semilla=semilla
        )
        resultados[alg] = gestor.calcular_estadisticas()
    
    # Crear figura con 4 subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Benchmarking Comparativo - Algoritmos de Evacuación', fontsize=16, fontweight='bold')
    
    # 1. Tasa de Supervivencia (Barras)
    ax1 = axes[0, 0]
    supervivencia = [resultados[alg]["supervivencia_media"] for alg in algoritmos]
    bars1 = ax1.bar(nombres, supervivencia, color=colores, edgecolor='black', linewidth=1.2)
    ax1.set_ylabel('Supervivencia (%)', fontsize=11)
    ax1.set_title('Tasa de Supervivencia Media', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 100)
    ax1.grid(axis='y', alpha=0.3)
    # Agregar valores sobre las barras
    for bar, val in zip(bars1, supervivencia):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{val:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 2. Tiempo Promedio (Barras)
    ax2 = axes[0, 1]
    tiempos = [resultados[alg]["tiempo_media"] for alg in algoritmos]
    bars2 = ax2.bar(nombres, tiempos, color=colores, edgecolor='black', linewidth=1.2)
    ax2.set_ylabel('Turnos', fontsize=11)
    ax2.set_title('Tiempo de Despeje Promedio', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars2, tiempos):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, 
                f'{val:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 3. Desviación Estándar (Barras)
    ax3 = axes[1, 0]
    stds = [resultados[alg]["tiempo_std"] for alg in algoritmos]
    bars3 = ax3.bar(nombres, stds, color=colores, edgecolor='black', linewidth=1.2)
    ax3.set_ylabel('Desviación Estándar', fontsize=11)
    ax3.set_title('Consistencia (Menos es Mejor)', fontsize=12, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars3, stds):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
                f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 4. Rango Min-Max (Barras agrupadas)
    ax4 = axes[1, 1]
    x = np.arange(len(nombres))
    width = 0.35
    mins = [resultados[alg]["tiempo_min"] for alg in algoritmos]
    maxs = [resultados[alg]["tiempo_max"] for alg in algoritmos]
    bars_min = ax4.bar(x - width/2, mins, width, label='Mínimo', color='#81C784', edgecolor='black')
    bars_max = ax4.bar(x + width/2, maxs, width, label='Máximo', color='#E57373', edgecolor='black')
    ax4.set_ylabel('Turnos', fontsize=11)
    ax4.set_title('Rango de Tiempo (Mín - Máx)', fontsize=12, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(nombres)
    ax4.legend()
    ax4.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('benchmarking_resultados.png', dpi=150, bbox_inches='tight')
    print("Gráfica guardada como 'benchmarking_resultados.png'")
    plt.show()
    
    return resultados


def generar_grafica_distribucion(mapa, salida, posiciones_base, focos_fuego_base, k_fuego=4, iteraciones=200, semilla=42):
    """Genera gráfico de caja (boxplot) con la distribución de turnos."""
    
    algoritmos = ["a_star", "ucs", "bfs", "greedy", "genetico"]
    nombres = ["A*", "UCS", "BFS", "Greedy", "Genético"]
    
    # Obtener datos de turnos para cada algoritmo
    datos_turnos = []
    for alg in algoritmos:
        gestor = ejecutar_benchmarking(
            mapa, salida, posiciones_base, focos_fuego_base,
            algoritmo=alg, iteraciones=iteraciones, k_fuego=k_fuego, semilla=semilla
        )
        datos_turnos.append(gestor.tiempos_despeje)
    
    # Crear boxplot
    fig, ax = plt.subplots(figsize=(10, 6))
    bp = ax.boxplot(datos_turnos, tick_labels=nombres, patch_artist=True)
    
    colores = ["#2196F3", "#4CAF50", "#FF9800", "#F44336", "#9C27B0"]
    for patch, color in zip(bp['boxes'], colores):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.set_ylabel('Turnos', fontsize=12)
    ax.set_title('Distribución de Tiempo de Despeje por Algoritmo', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('distribucion_turnos.png', dpi=150, bbox_inches='tight')
    print("Gráfica guardada como 'distribucion_turnos.png'")
    plt.show()


def cargar_datos_juego(carpeta='resultados'):
    """Carga los datos de las simulaciones guardadas por Juego.py."""
    datos = []
    patron = os.path.join(carpeta, '*.json')
    
    for archivo in glob(patron):
        try:
            with open(archivo, 'r') as f:
                datos.append(json.load(f))
        except Exception as e:
            print(f"Error cargando {archivo}: {e}")
    
    return datos


def generar_graficas_desde_juego(carpeta='resultados'):
    """Genera gráficas usando los datos guardados por Juego.py."""
    datos = cargar_datos_juego(carpeta)
    
    if not datos:
        print("No se encontraron datos de simulaciones en la carpeta 'resultados'")
        print("Ejecuta Juego.py primero para generar datos")
        return
    
    # Agrupar por algoritmo
    por_algoritmo = {}
    for d in datos:
        alg = d.get('algoritmo', 'desconocido')
        if alg not in por_algoritmo:
            por_algoritmo[alg] = []
        por_algoritmo[alg].append(d)
    
    algoritmos = list(por_algoritmo.keys())
    nombres = [alg.upper() for alg in algoritmos]
    colores = ["#2196F3", "#4CAF50", "#FF9800", "#F44336", "#9C27B0", "#00BCD4"]
    
    # Crear figura con 2 subplots
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f'Resultados del Juego ({len(datos)} simulaciones)', fontsize=16, fontweight='bold')
    
    # 1. Tasa de supervivencia por algoritmo
    ax1 = axes[0]
    supervivencia = []
    for alg in algoritmos:
        stats = [d['estadisticas']['tasa_supervivencia'] for d in por_algoritmo[alg]]
        supervivencia.append(np.mean(stats))
    
    bars1 = ax1.bar(nombres, supervivencia, color=colores[:len(algoritmos)], 
                   edgecolor='black', linewidth=1.2)
    ax1.set_ylabel('Supervivencia (%)', fontsize=11)
    ax1.set_title('Tasa de Supervivencia por Algoritmo', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 100)
    ax1.grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars1, supervivencia):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{val:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 2. Turnos por algoritmo
    ax2 = axes[1]
    turnos = []
    for alg in algoritmos:
        t = [d['turnos'] for d in por_algoritmo[alg]]
        turnos.append(np.mean(t))
    
    bars2 = ax2.bar(nombres, turnos, color=colores[:len(algoritmos)], 
                   edgecolor='black', linewidth=1.2)
    ax2.set_ylabel('Turnos', fontsize=11)
    ax2.set_title('Turnos Promedio por Algoritmo', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars2, turnos):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                f'{val:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('resultados/graficas_juego.png', dpi=150, bbox_inches='tight')
    print(f"Gráfica guardada en 'resultados/graficas_juego.png'")
    plt.close()


def generar_grafica_historial(carpeta='resultados'):
    """Genera un gráfico de línea con el historial de simulaciones."""
    datos = cargar_datos_juego(carpeta)
    
    if not datos:
        print("No se encontraron datos de simulaciones")
        return
    
    # Ordenar por fecha
    datos.sort(key=lambda x: x.get('fecha', ''))
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Historial de Simulaciones', fontsize=16, fontweight='bold')
    
    # Extraer datos
    supervivencia = [d['estadisticas']['tasa_supervivencia'] for d in datos]
    turnos = [d['turnos'] for d in datos]
    algoritmos = [d.get('algoritmo', 'desconocido') for d in datos]
    
    # Colores por algoritmo
    colores = {"a_star": "#2196F3", "ucs": "#4CAF50", "bfs": "#FF9800", 
               "greedy": "#F44336", "genetico": "#9C27B0"}
    puntos = [colores.get(alg, "#888888") for alg in algoritmos]
    
    # 1. Supervivencia en el tiempo
    ax1 = axes[0]
    ax1.scatter(range(len(datos)), supervivencia, c=puntos, s=100, alpha=0.7, edgecolors='black')
    ax1.set_xlabel('Simulación', fontsize=11)
    ax1.set_ylabel('Supervivencia (%)', fontsize=11)
    ax1.set_title('Supervivencia por Simulación', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 100)
    ax1.grid(alpha=0.3)
    
    # 2. Turnos en el tiempo
    ax2 = axes[1]
    ax2.scatter(range(len(datos)), turnos, c=puntos, s=100, alpha=0.7, edgecolors='black')
    ax2.set_xlabel('Simulación', fontsize=11)
    ax2.set_ylabel('Turnos', fontsize=11)
    ax2.set_title('Turnos por Simulación', fontsize=12, fontweight='bold')
    ax2.grid(alpha=0.3)
    
    # Leyenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color, edgecolor='black', label=alg.upper()) 
                      for alg, color in colores.items() if alg in algoritmos]
    ax1.legend(handles=legend_elements, loc='lower right')
    
    plt.tight_layout()
    plt.savefig('resultados/historial_simulaciones.png', dpi=150, bbox_inches='tight')
    print(f"Gráfica guardada en 'resultados/historial_simulaciones.png'")
    plt.close()


def generar_diagrama_caja(carpeta='resultados'):
    """Genera diagramas de caja (boxplot) con los datos del benchmarking."""
    datos = cargar_datos_juego(carpeta)
    
    if not datos:
        print("No se encontraron datos de simulaciones")
        print("Ejecuta el benchmarking primero desde Juego.py")
        return
    
    # Agrupar por algoritmo - usar TODOS los datos disponibles
    por_algoritmo = {}
    for d in datos:
        alg = d.get('algoritmo', 'desconocido')
        if alg not in por_algoritmo:
            por_algoritmo[alg] = {'turnos': [], 'supervivencia': []}
        
        # Si hay listas de datos individuales, usarlas
        if isinstance(d.get('turnos'), list):
            por_algoritmo[alg]['turnos'].extend(d['turnos'])
        if isinstance(d.get('supervivencia'), list):
            por_algoritmo[alg]['supervivencia'].extend(d['supervivencia'])
        
        # Si no hay listas, usar los datos individuales de la simulación
        if not isinstance(d.get('turnos'), list) and 'estadisticas' in d:
            # Usar el turno de la simulación individual
            if 'turnos' in d:
                por_algoritmo[alg]['turnos'].append(d['turnos'])
            if 'estadisticas' in d and 'tasa_supervivencia' in d['estadisticas']:
                por_algoritmo[alg]['supervivencia'].append(d['estadisticas']['tasa_supervivencia'])
    
    # Filtrar algoritmos con datos
    algoritmos = [alg for alg in por_algoritmo if por_algoritmo[alg]['turnos'] or por_algoritmo[alg]['supervivencia']]
    
    if not algoritmos:
        print("No se encontraron datos para generar diagramas de caja")
        return
    
    nombres = [alg.upper() for alg in algoritmos]
    colores = ["#2196F3", "#4CAF50", "#FF9800", "#F44336", "#9C27B0"]
    
    # Crear figura con 2 subplots
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Diagramas de Caja - Resultados del Benchmarking', fontsize=16, fontweight='bold')
    
    # 1. Diagrama de caja de turnos
    ax1 = axes[0]
    datos_turnos = [por_algoritmo[alg]['turnos'] for alg in algoritmos if por_algoritmo[alg]['turnos']]
    if datos_turnos:
        bp1 = ax1.boxplot(datos_turnos, tick_labels=nombres[:len(datos_turnos)], patch_artist=True)
        for patch, color in zip(bp1['boxes'], colores):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
    ax1.set_ylabel('Turnos', fontsize=11)
    ax1.set_title('Distribución de Tiempo de Despeje', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # 2. Diagrama de caja de supervivencia
    ax2 = axes[1]
    datos_supervivencia = [por_algoritmo[alg]['supervivencia'] for alg in algoritmos if por_algoritmo[alg]['supervivencia']]
    if datos_supervivencia:
        bp2 = ax2.boxplot(datos_supervivencia, tick_labels=nombres[:len(datos_supervivencia)], patch_artist=True)
        for patch, color in zip(bp2['boxes'], colores):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
    ax2.set_ylabel('Supervivencia (%)', fontsize=11)
    ax2.set_title('Distribución de Tasa de Supervivencia', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, 100)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('resultados/diagrama_caja.png', dpi=150, bbox_inches='tight')
    print(f"Diagrama de caja guardado en 'resultados/diagrama_caja.png'")
    plt.close()
