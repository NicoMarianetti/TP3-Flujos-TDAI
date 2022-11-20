import sys
import csv

EQUIPO_1 = 'E1'
EQUIPO_2 = 'E2'
PRIMO = "'"
INF = 99999


def generar_grafo_dirigido(path_archivo_tareas):
    file = open(path_archivo_tareas)
    csvreader = csv.reader(file)

    grafo = Grafo(dirigido=True)

    fuente = EQUIPO_1
    sumidero = EQUIPO_2

    grafo.agregar_vertice(fuente)
    grafo.agregar_vertice(sumidero)

    for row in csvreader:
        nodo = row[0]
        nodo_prima = f"{nodo}{PRIMO}"

        grafo.agregar_vertice(nodo)
        grafo.agregar_vertice(nodo_prima)

        grafo.agregar_arista(fuente, nodo, int(row[1]))
        grafo.agregar_arista(nodo, nodo_prima, INF)
        grafo.agregar_arista(nodo_prima, sumidero, int(row[2]))

        dependencias = row[3:]

        for i, dependencia in enumerate(dependencias):
            if (i + 1) % 2 == 0:
                nodo_dependiente = dependencias[i - 1]
                nodo_prima_dependiente = f"{dependencias[i - 1]}{PRIMO}"

                grafo.agregar_vertice(nodo_dependiente)
                grafo.agregar_vertice(nodo_prima_dependiente)

                peso_dependencia = int(dependencias[i])

                grafo.agregar_arista(nodo, nodo_prima_dependiente, peso_dependencia)
                grafo.agregar_arista(nodo_dependiente, nodo_prima, peso_dependencia)

    return grafo


def minimum_cut(grafo):
    caminoSaT = buscar_camino_SaT(grafo)
    flujo = 0

    while caminoSaT:
        costo = buscar_cuello_botella(grafo, caminoSaT)
        flujo += costo

        # Actualizo grafo
        rango = range(1, len(caminoSaT))
        for i in rango:
            nodo_inicial = caminoSaT[i - 1]
            nodo_vecino = caminoSaT[i]
            peso = grafo.peso_arista(nodo_inicial, nodo_vecino)
            grafo.modificar_peso_arista(nodo_inicial, nodo_vecino, peso - costo)

            peso = grafo.peso_arista(nodo_vecino, nodo_inicial)
            grafo.modificar_peso_arista(nodo_vecino, nodo_inicial, peso + costo)

        caminoSaT = buscar_camino_SaT(grafo)

    return flujo, grafo


def buscar_camino_SaT(grafo):
    S = EQUIPO_1
    T = EQUIPO_2

    caminos = {S: []}
    cola_a_procesar = [(S, S)]
    visitados = {S: True}

    while cola_a_procesar:
        padre, vertice = cola_a_procesar.pop()
        camino_previo = caminos[padre]
        camino = camino_previo + [vertice]
        caminos[vertice] = camino

        for vecino in grafo.vertices_adyacentes(vertice):
            if grafo.peso_arista(vertice, vecino) <= 0:
                continue

            if vecino == T:
                return caminos[vertice] + [vecino]

            if not visitados.get(vecino, False):
                visitados[vecino] = True
                cola_a_procesar.append((vertice, vecino))

    return False


def buscar_cuello_botella(grafo, camino):
    rango = range(1, len(camino))
    min_camino = INF

    for i in rango:
        nodo_inicial = camino[i - 1]
        nodo_vecino = camino[i]
        costo = grafo.peso_arista(nodo_inicial, nodo_vecino)
        if costo < min_camino:
            min_camino = costo

    return min_camino


def resultado_tareas(grafo):
    equipo1 = []
    equipo2 = []

    nodos = grafo.obtener_vertices()
    en_solucion = {}
    for nodo in nodos:
        en_solucion[nodo] = False

    cola_a_procesar = [EQUIPO_1]
    visitados = {EQUIPO_1: True}

    while cola_a_procesar:

        vertice = cola_a_procesar.pop()

        for vecino in grafo.vertices_adyacentes(vertice):

            vertice_dual = obtener_dual(vertice)
            vecino_dual = obtener_dual(vecino)

            if en_solucion[vertice] or en_solucion[vertice_dual] or en_solucion[vecino_dual]:
                continue

            if grafo.peso_arista(vertice, vecino) == 0 and vertice == EQUIPO_1:
                en_solucion[vecino] = True
                en_solucion[vecino_dual] = True
                equipo1.append(vecino)

            elif grafo.peso_arista(vertice, vecino) == 0 and vecino == EQUIPO_2:
                en_solucion[vertice] = True
                en_solucion[vertice_dual] = True
                equipo2.append(vertice_dual)

            if not visitados.get(vecino, False):
                visitados[vecino] = True
                cola_a_procesar.append(vecino)

    return equipo1, equipo2


def obtener_dual(vertice):
    vertice_dual = f"{vertice}{PRIMO}"

    if vertice[-1] == PRIMO:
        vertice_dual = vertice[:-1]
    elif vertice == EQUIPO_1 or vertice == EQUIPO_2:
        vertice_dual = vertice

    return vertice_dual


def main():
    if len(sys.argv) != 2:
        print("Como user: tareas.py <rutaArchivo>")
        sys.exit(1)

    path_archivo_tareas = sys.argv[1]

    grafo = generar_grafo_dirigido(path_archivo_tareas)
    costo_minimo, grafo = minimum_cut(grafo)

    tareas_equipo1, tareas_equipo2 = resultado_tareas(grafo)

    print('Costo minimo: ', costo_minimo)
    print('Equipo 1: ', tareas_equipo1)
    print('Equipo 2: ', tareas_equipo2)


class Grafo:
    def __init__(self, dirigido):
        self.adyacentes = {}
        self.vertices = 0
        self.aristas = 0
        self.es_dirigido = dirigido

    def agregar_vertice(self, vertice):
        if self.adyacentes.get(vertice, False):
            return
        self.vertices += 1
        self.adyacentes[vertice] = self.adyacentes.get(vertice, {})

    def agregar_arista(self, vertice1, vertice2, peso):
        if (not self.es_dirigido):
            self.adyacentes[vertice2][vertice1] = peso
        self.adyacentes[vertice1][vertice2] = peso
        self.aristas += 1

    def peso_arista(self, vertice1, vertice2):
        return self.adyacentes[vertice1].get(vertice2, 0)

    def modificar_peso_arista(self, vertice1, vertice2, peso):
        if not self.adyacentes[vertice1].get(vertice2, False):
            self.agregar_arista(vertice1, vertice2, peso)
        self.adyacentes[vertice1][vertice2] = peso

    def obtener_vertices(self):
        return self.adyacentes.keys()

    def vertices_adyacentes(self, vertice):
        vertices_adyacentes = []
        for vert in self.adyacentes[vertice].keys():
            vertices_adyacentes.append(vert)
        return vertices_adyacentes


main()
