import numpy as np

class GestorMetricas:
    def __init__(self, algoritmo, iteraciones):
        self.algoritmo = algoritmo
        self.iteraciones = iteraciones
        self.tasas_supervivencia = []
        self.tiempos_despeje = []

    def registrar_ejecucion(self, tasa_supervivencia, turnos_totales):
        self.tasas_supervivencia.append(tasa_supervivencia)
        self.tiempos_despeje.append(turnos_totales)

    def calcular_estadisticas(self):
        """
        Calcula los estadísticos descriptivos obligatorios para el benchmarking.
        """
        if not self.tasas_supervivencia or not self.tiempos_despeje:
            return {}

        stats = {
            "algoritmo": self.algoritmo,
            "iteraciones": self.iteraciones,
            "supervivencia_media": float(np.mean(self.tasas_supervivencia)),
            "supervivencia_std": float(np.std(self.tasas_supervivencia)),
            "tiempo_media": float(np.mean(self.tiempos_despeje)),
            "tiempo_std": float(np.std(self.tiempos_despeje)),
            "tiempo_min": int(np.min(self.tiempos_despeje)),
            "tiempo_max": int(np.max(self.tiempos_despeje)),
        }
        return stats

    def imprimir_resultados(self):
        stats = self.calcular_estadisticas()
        print(f"\n--- Resultados de Benchmarking: {stats['algoritmo'].upper()} ---")
        print(f"  - Iteraciones evaluadas : {stats['iteraciones']}")
        print(f"  - Tasa Supervivencia Media: {stats['supervivencia_media']:.2f}% (±{stats['supervivencia_std']:.2f})")
        print(f"  - Tiempo (Turnos) Media : {stats['tiempo_media']:.2f}")
        print(f"  - Desviación Estándar   : {stats['tiempo_std']:.2f}")
        print(f"  - Valor Mínimo (Turnos) : {stats['tiempo_min']}")
        print(f"  - Valor Máximo (Turnos) : {stats['tiempo_max']}")