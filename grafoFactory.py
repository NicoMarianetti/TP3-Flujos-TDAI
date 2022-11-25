import csv
from grafo import Grafo
from constantes import EQUIPO_1, EQUIPO_2, PRIMO, INF, TAREA_INDEX, COSTO_EQUIPO_1_INDEX, COSTO_EQUIPO_2_INDEX, DEPENDENCIAS_INDEX

class GrafoDeFlujoFactory:
    def __init__(self):
        pass

    def generar_grafo_dirigido(self, path_archivo_tareas):
        file = open(path_archivo_tareas)
        csvreader = csv.reader(file)

        grafo = Grafo(dirigido=True)

        grafo.agregar_vertice(EQUIPO_1)
        grafo.agregar_vertice(EQUIPO_2)

        for row in csvreader:
            tarea = row[TAREA_INDEX]
            tarea_prima = f"{tarea}{PRIMO}"
            
            grafo.agregar_vertice(tarea)
            grafo.agregar_vertice(tarea_prima)

            grafo.agregar_arista(EQUIPO_1, tarea, int(row[COSTO_EQUIPO_1_INDEX]))
            grafo.agregar_arista(tarea, tarea_prima, INF)
            grafo.agregar_arista(tarea_prima, EQUIPO_2, int(row[COSTO_EQUIPO_2_INDEX]))

            dependencias = row[DEPENDENCIAS_INDEX:]
            for i, dependencia in enumerate(dependencias):
                if self.__es_costo_tarea(i):
                    tarea_dependiente = dependencias[i - 1]
                    tarea_prima_dependiente = f"{dependencias[i - 1]}{PRIMO}"

                    grafo.agregar_vertice(tarea_dependiente)
                    grafo.agregar_vertice(tarea_prima_dependiente)

                    peso_dependencia = int(dependencia)

                    grafo.agregar_arista(tarea, tarea_prima_dependiente, peso_dependencia)
                    grafo.agregar_arista(tarea_dependiente, tarea_prima, peso_dependencia)

        return grafo

    def __es_costo_tarea(self, i):
        return (i + 1) % 2 == 0