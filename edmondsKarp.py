from constantes import INF
from constantes import EQUIPO_1, EQUIPO_2, PRIMO


class EdmondsKarp:
    def __init__(self, grafo, fuente, sumidero):
        self.grafo = grafo
        self.fuente = fuente
        self.sumidero = sumidero

    def resolver(self, traduccion_nodos):
        caminoSaT = self.__buscar_camino_sat()
        flujo = 0

        while caminoSaT:
            costo = self.__buscar_cuello_botella(caminoSaT)
            flujo += costo

            # Actualizo grafo
            rango = range(1, len(caminoSaT))
            for i in rango:
                nodo_inicial = caminoSaT[i - 1]
                nodo_vecino = caminoSaT[i]
                peso = self.grafo.peso_arista(nodo_inicial, nodo_vecino)
                self.grafo.modificar_peso_arista(nodo_inicial, nodo_vecino, peso - costo)

                peso = self.grafo.peso_arista(nodo_vecino, nodo_inicial)
                self.grafo.modificar_peso_arista(nodo_vecino, nodo_inicial, peso + costo)

            caminoSaT = self.__buscar_camino_sat()
            
        nodos_e1 = self.__corte_minimo(traduccion_nodos)
        tareas_equipo_1, tareas_equipo_2 = self.__obtener_tareas(traduccion_nodos, nodos_e1)

        return flujo, tareas_equipo_1, tareas_equipo_2

    def __buscar_camino_sat(self):
        caminos = {self.fuente: []}
        cola_a_procesar = [(self.fuente, self.fuente)]
        visitados = {self.fuente: True}

        while cola_a_procesar:
            padre, vertice = cola_a_procesar.pop()
            nuevo_camino = caminos[padre].copy()
            nuevo_camino.append(vertice)
            caminos[vertice] = nuevo_camino

            for vecino in self.grafo.vertices_adyacentes(vertice):
                if self.grafo.peso_arista(vertice, vecino) <= 0:
                    continue

                if vecino == self.sumidero:
                    caminos[vertice].append(vecino)
                    return caminos[vertice]

                if not visitados.get(vecino, False):
                    visitados[vecino] = True
                    cola_a_procesar.append((vertice, vecino))

        return False

    def __buscar_cuello_botella(self, camino):
        rango = range(1, len(camino))
        min_camino = INF

        for i in rango:
            nodo_inicial = camino[i - 1]
            nodo_vecino = camino[i]
            costo = self.grafo.peso_arista(nodo_inicial, nodo_vecino)
            if costo < min_camino:
                min_camino = costo

        return min_camino

    def __corte_minimo(self, traduccion_nodos):
        caminos_de_S = []
        cola_a_procesar = [self.fuente]
        visitados = {self.fuente: True}

        while cola_a_procesar:
            vertice = cola_a_procesar.pop()
            caminos_de_S.append(vertice)

            for vecino in self.grafo.vertices_adyacentes(vertice):

                tarea_no_prima = traduccion_nodos.get(vecino, False)

                if self.grafo.peso_arista(vertice, vecino) <= 0 or (vecino == tarea_no_prima and vertice != tarea_no_prima):
                    continue
                
                if not visitados.get(vecino, False):
                    visitados[vecino] = True
                    cola_a_procesar.append( vecino )
        
        return caminos_de_S
    
    def __obtener_tareas(self, traduccion_nodos, nodos_e1):
        tareas_asignadas = {}

        caminos_equipo_1 = self.grafo.adyacentes[EQUIPO_1].keys()

        for tarea in caminos_equipo_1:
            tareas_asignadas[tarea] = EQUIPO_1

        for tarea in nodos_e1:

            tarea = traduccion_nodos.get(tarea, tarea)

            if tarea == EQUIPO_1:
                continue
            
            tareas_asignadas[tarea] = EQUIPO_2

        tareas_equipo1 = []
        tareas_equipo2 = []

        for tarea, equipo in tareas_asignadas.items():
            if equipo == EQUIPO_1:
                tareas_equipo1.append(tarea)
            else:
                tareas_equipo2.append(tarea)

        return tareas_equipo1, tareas_equipo2

