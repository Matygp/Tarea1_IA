import json
import os
import glob

archivos = glob.glob('resultados/benchmarking_*.json')
print(f'Archivos de benchmarking: {len(archivos)}')

for f in archivos[:3]:
    data = json.load(open(f))
    nombre = os.path.basename(f)
    turnos = data.get('turnos', [])
    supervivencia = data.get('supervivencia', [])
    print(f'{nombre}:')
    print(f'  turnos: {len(turnos)} datos')
    print(f'  supervivencia: {len(supervivencia)} datos')
    if turnos:
        print(f'  primeros turnos: {turnos[:5]}')
    if supervivencia:
        print(f'  primeras supervivencias: {supervivencia[:5]}')
    print()
