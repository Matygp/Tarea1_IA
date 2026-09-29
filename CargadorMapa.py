import json
import csv
import os


def cargar_mapa(ruta_archivo):

    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")
    
    extension = os.path.splitext(ruta_archivo)[1].lower()
    
    if extension == '.json':
        return _cargar_desde_json(ruta_archivo)
    elif extension == '.csv':
        return _cargar_desde_csv(ruta_archivo)
    elif extension == '.txt':
        return _cargar_desde_txt(ruta_archivo)
    else:
        raise ValueError(f"Formato no soportado: {extension}. Use .txt, .csv o .json")


def _cargar_desde_json(ruta_archivo):
    
    with open(ruta_archivo, 'r') as f:
        data = json.load(f)
    
    if isinstance(data, dict):
        mapa = data.get('mapa', data.get('grid', []))
        salida = tuple(data.get('salida', data.get('exit', [len(mapa[0])-1, len(mapa)-1])))
    else:
        mapa = data
        salida = (len(mapa[0])-1, len(mapa)-1)
    
    return mapa, salida


def _cargar_desde_csv(ruta_archivo):
   
    mapa = []
    with open(ruta_archivo, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # Ignorar líneas vacías
                mapa.append([int(x.strip()) for x in row])
    
    salida = (len(mapa[0])-1, len(mapa)-1)
    return mapa, salida


def _cargar_desde_txt(ruta_archivo):
   
    mapa = []
    with open(ruta_archivo, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Ignorar líneas vacías
                # Intentar separar por espacios o comas
                if ',' in line:
                    row = [int(x.strip()) for x in line.split(',')]
                else:
                    row = [int(x) for x in line.split()]
                mapa.append(row)
    
    salida = (len(mapa[0])-1, len(mapa)-1)
    return mapa, salida


def guardar_mapa(mapa, ruta_archivo, salida=None):
   
    extension = os.path.splitext(ruta_archivo)[1].lower()
    
    if extension == '.json':
        data = {
            'mapa': mapa,
            'salida': salida if salida else (len(mapa[0])-1, len(mapa)-1)
        }
        with open(ruta_archivo, 'w') as f:
            json.dump(data, f, indent=2)
    
    elif extension == '.csv':
        with open(ruta_archivo, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in mapa:
                writer.writerow(row)
    
    elif extension == '.txt':
        with open(ruta_archivo, 'w') as f:
            for row in mapa:
                f.write(' '.join(map(str, row)) + '\n')
    
    else:
        raise ValueError(f"Formato no soportado: {extension}")


def validar_mapa(mapa):
  
    if not mapa:
        return False, #El mapa está vacío
    
    if not isinstance(mapa, list):
        return False, #El mapa debe ser una lista de listas
    
    filas = len(mapa)
    if filas == 0:
        return False, #El mapa no tiene filas
    
    columnas = len(mapa[0])
    if columnas == 0:
        return False, #El mapa no tiene columnas
    
    # Verificar que todas las filas tengan el mismo número de columnas
    for i, fila in enumerate(mapa):
        if len(fila) != columnas:
            return False, f"Fila {i} tiene {len(fila)} columnas, se esperaban {columnas}"
        
        # Verificar que los valores sean 0 o 1
        for j, val in enumerate(fila):
            if val not in (0, 1):
                return False, f"Valor inválido en ({j},{i}): {val}. Debe ser 0 o 1"
    
    return True, "Mapa válido"


def obtener_celdas_validas(mapa):
    
    validas = []
    for y in range(len(mapa)):
        for x in range(len(mapa[0])):
            if mapa[y][x] == 0:
                validas.append((x, y))
    return validas


def obtener_celdas_fuego(mapa):
    
    return obtener_celdas_validas(mapa)


def imprimir_mapa(mapa, salida=None):
    
    print("\n=== MAPA ===")
    for y, fila in enumerate(mapa):
        linea = ""
        for x, val in enumerate(fila):
            if salida and (x, y) == salida:
                linea += "S "  # Salida
            elif val == 1:
                linea += "█ "  # Muro
            else:
                linea += ". "  # Espacio vacío
        print(linea)
    print(f"Dimensiones: {len(mapa[0])}x{len(mapa)}")
    if salida:
        print(f"Salida: {salida}")
    print()
