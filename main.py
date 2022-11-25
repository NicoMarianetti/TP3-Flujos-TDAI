import sys
from grafoFactory import GrafoDeFlujoFactory
from constantes import EQUIPO_1, EQUIPO_2, PRIMO
from edmondsKarp import EdmondsKarp

def main():
    if len(sys.argv) != 2:
        print("Como user: tareas.py <rutaArchivo>")
        sys.exit(1)

    path_archivo_tareas = sys.argv[1]
    grafo, traduccion_nodos = GrafoDeFlujoFactory().generar_grafo_dirigido(path_archivo_tareas)
    costo_minimo, tareas_equipo1, tareas_equipo2 = EdmondsKarp(grafo, EQUIPO_1, EQUIPO_2).resolver(traduccion_nodos)

    print('Costo minimo: ', costo_minimo)
    print('Equipo 1: ', [i for i in list(tareas_equipo1) if not i.endswith(PRIMO) and i != EQUIPO_1])
    print('Equipo 2: ', [i for i in list(tareas_equipo2) if not i.endswith(PRIMO) and i != EQUIPO_2])


main()
