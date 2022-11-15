import networkx as nx
import sys
import csv
# import numpy
from networkx.algorithms.flow import maximum_flow, minimum_cut
# import matplotlib.pyplot as plt

EQUIPO_1 = 'E1'
EQUIPO_2 = 'E2'
PRIMO = "'"
INF = 99999


def generar_grafo_dirigido(path_archivo_tareas):
    G = nx.DiGraph()

    file = open(path_archivo_tareas)
    csvreader = csv.reader(file)

    fuente = EQUIPO_1
    sumidero = EQUIPO_2

    G.add_node(fuente)
    G.add_node(sumidero)

    for row in csvreader:
        nodo = row[0]
        nodo_prima = f"{nodo}{PRIMO}"
        G.add_edge(fuente, nodo, capacity=int(row[1]))
        # G.add_edge(nodo, nodo_prima, capacity=numpy.Inf)
        G.add_edge(nodo, nodo_prima, capacity=INF)
        G.add_edge(nodo_prima, sumidero, capacity=int(row[2]))
        dependencias = row[3:]

        for i, dependencia in enumerate(dependencias):
            if (i + 1) % 2 == 0:
                nodo_dependiente = dependencias[i - 1]
                nodo_prima_dependiente = f"{dependencias[i - 1]}{PRIMO}"
                peso_dependencia = int(dependencias[i])
                G.add_edge(nodo, nodo_prima_dependiente, capacity=peso_dependencia)
                G.add_edge(nodo_dependiente, nodo_prima, capacity=peso_dependencia)

    return G


def main():
    if len(sys.argv) != 2:
        print("Como user: tareas.py <rutaArchivo>")
        sys.exit(1)

    path_archivo_tareas = sys.argv[1]

    G = generar_grafo_dirigido(path_archivo_tareas)
    costo_minimo, corte = minimum_cut(G, EQUIPO_1, EQUIPO_2)
    tareas_equipo1, tareas_equipo2 = corte

    print('Costo minimo: ', costo_minimo)
    print('Equipo 1: ', [i for i in list(tareas_equipo2) if not i.endswith(PRIMO) and i != EQUIPO_2])
    print('Equipo 2: ', [i for i in list(tareas_equipo1) if not i.endswith(PRIMO) and i != EQUIPO_1])
    # plot_graph(G, tareas_equipo2)


def plot_graph(g, equipo_1, save=False, file_name=''):
    pos = {}

    labels = {node: node for node in g}
    cont = (len(g.nodes()) - 2) / 4
    y = 0
    yprima = 0

    for nodo in g.nodes():
        if not nodo.endswith(PRIMO) and nodo != EQUIPO_1 and nodo != EQUIPO_2:
            pos[nodo] = [0.25, y]
            y += cont/len(g.nodes())
        if nodo.endswith(PRIMO):
            pos[nodo] = [0.7, yprima]
            yprima += cont/len(g.nodes())

    pos[EQUIPO_1] = [0, 0.5]
    pos[EQUIPO_2] = [1, 0.5]

    plt.figure(figsize=(5, 5))
    plt.axis('off')
    plt.title('Tareas alcanzadas por los equipos', fontdict={'fontsize': 13})

    available_colors = {1: '#E9D758', 2: '#ff8552'}

    colors = [available_colors[2 if node in equipo_1 else 1] for node in g.nodes()]

    colors[0] = available_colors[2]
    colors[1] = available_colors[1]

    nx.draw_networkx_labels(g, pos, labels=labels)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=nx.get_edge_attributes(g, 'capacity'), label_pos=0.8, font_color='red', font_size=8, font_weight='bold')
    nx.draw_networkx_edges(g, pos, width=1, alpha=1)
    nx.draw_networkx_nodes(g, pos, nodelist=g.nodes(), node_color=colors, alpha=1, node_size=300, linewidths=1)

    if save:
        plt.savefig(file_name, format='svg', dpi=300)

    plt.show()


main()
