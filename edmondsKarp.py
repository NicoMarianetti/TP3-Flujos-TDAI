from constantes import INF
from constantes import EQUIPO_1, EQUIPO_2, PRIMO

class EdmondsKarp:
    def __init__(self, grafo, fuente, sumidero):
        self.grafo = grafo
        self.fuente = fuente
        self.sumidero = sumidero

    def resolve(self):
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

        tareas_equipo_1, tareas_equipo_2 = self.__obtener_tareas()
       

        return flujo, tareas_equipo_1, tareas_equipo_2
    

    def __buscar_camino_sat(self):
        caminos = { self.fuente: [] }
        cola_a_procesar = [ (self.fuente, self.fuente) ]
        visitados = { self.fuente: True }

        while cola_a_procesar:
            padre, vertice = cola_a_procesar.pop()
            camino_previo = caminos[padre]
            camino = camino_previo
            camino.append(vertice)
            caminos[vertice] = camino

            for vecino in self.grafo.vertices_adyacentes(vertice):
                if self.grafo.peso_arista(vertice, vecino) <= 0:
                    continue

                if vecino == self.sumidero: 
                   resultado = caminos[vertice]
                   resultado.append(vecino)
                   return resultado

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

    def __obtener_tareas(self):
         # Obtengo las tareas que me da el corte minimo:
        caminos_equipo_1 = self.grafo.adyacentes[EQUIPO_1].items()
        caminos_equipo_2 = [c for c in list(self.grafo.adyacentes.items()) if c[0].endswith(PRIMO)]
        
        # Las tareas cuya capacidad desde el equipo 1 (fuente) sea 0 seran trabajados por el equipo 1
        tareas_equipo_1 = list(
            map(lambda c: c[0],
                filter(lambda c: c[1] == 0, caminos_equipo_1)
            )
        )

        # Las tareas primadas cuya capacidad hacia el equipo 2 (sumidero) sean 0 seran tomadas por el equipo 2,
        # a menos que hayan que hayan sido tomadas por el equipo 1
        tareas_equipo_2 = list(
            filter(
                lambda c: c not in tareas_equipo_1,
                map(lambda c: c[0].replace(PRIMO, ''),
                    filter(lambda c: c[1][EQUIPO_2] == 0, caminos_equipo_2)
                )
            )
        )

        return tareas_equipo_1, tareas_equipo_2