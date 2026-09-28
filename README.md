# Escape de la Torre - Simulación de Evacuación

Proyecto de Inteligencia Artificial: Sistema de navegación y toma de decisiones para evacuación en un edificio con propagación de fuego.

## Integrantes

- Matías Ignacio García Padilla

## Descripción

Simulación de agentes que deben escapar de un edificio en llamas utilizando diferentes algoritmos de búsqueda y optimización.

## Estructura del Proyecto

```
Tarea1_IA/
├── algoritmos/           # Algoritmos de búsqueda
│   ├── A_estrella.py
│   ├── BFS.py
│   ├── Costo_uniforme.py
│   ├── Genetico.py
│   └── Greedy.py
├── metricas/             # Métricas y visualización
│   ├── Graficas.py
│   └── Metricas.py
├── mapas/                # Mapas de ejemplo
│   ├── mapa_ejemplo.csv
│   ├── mapa_ejemplo.json
│   └── mapa_ejemplo.txt
├── Agente.py             # Clase del agente
├── CargadorMapa.py       # Cargador de mapas
├── Juego.py              # Interfaz tipo juego
├── Mapa.py               # Clase del mapa
└── Simulacion.py         # Motor de simulación
```

## Requisitos

```bash
pip install numpy matplotlib
```

## Ejecución

### Juego principal
```bash
python Juego.py
```

### Generar gráficas desde datos del juego
```bash
python -c "from metricas.Graficas import generar_graficas_desde_juego; generar_graficas_desde_juego()"
```

## Algoritmos Implementados

| Tipo | Algoritmo | Archivo |
|------|-----------|---------|
| No informado | BFS | `algoritmos/BFS.py` |
| No informado | UCS | `algoritmos/Costo_uniforme.py` |
| Informado | A* | `algoritmos/A_estrella.py` |
| Informado | Greedy | `algoritmos/Greedy.py` |
| Bioinspirado | Genético | `algoritmos/Genetico.py` |

## Agregar Nuevos Mapas

Para agregar un nuevo mapa, coloca el archivo en la carpeta `mapas/` con extensión `.txt`, `.csv` o `.json`. Luego, desde la interfaz del juego, haz clic en **"Cargar Mapa"** y selecciona el archivo.

**Importante:** El archivo del mapa debe estar ubicado en la carpeta `mapas/` para que el juego lo encuentre correctamente.

## Formato de Mapas

### TXT
```
0 0 0 0 0
0 1 1 0 0
0 0 0 0 0
```

### CSV
```
0,0,0,0,0
0,1,1,0,0
0,0,0,0,0
```

### JSON
```json
{
  "mapa": [[0,0,0,0,0], [0,1,1,0,0], [0,0,0,0,0]],
  "salida": [4, 4]
}
```

## Métricas

- Tasa de supervivencia
- Tiempo de despeje (turnos)
- Desviación estándar
- Valor mínimo y máximo
