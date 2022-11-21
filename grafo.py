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

    def borrar_vertice(self, a_borrar):
        self.vertices -= 1
        del self.adyacentes[a_borrar]
        for vertice in self.adyacentes.keys():
            del self.adyacentes[vertice][a_borrar]

    def borrar_arista(self, vertice1, vertice2):
        if (not self.es_dirigido):
            del self.adyacentes[vertice2][vertice1]
        self.aristas -= 1
        del self.adyacentes[vertice1][vertice2]

    def vertices_conectados(self, vertice1, vertice2):
        for vertice in self.adyacentes[vertice1].keys():
            if vertice == vertice2:
                return True
        return False

    def ver_si_exite_vertice(self, vert):
        if vert in self.adyacentes.keys():
            return True
        return False

    def peso_arista(self, vertice1, vertice2):
        return self.adyacentes[vertice1].get(vertice2, 0)

    def modificar_peso_arista(self, vertice1, vertice2, peso):
        if not self.adyacentes[vertice1].get(vertice2, False):
            self.agregar_arista(vertice1, vertice2, peso)
        self.adyacentes[vertice1][vertice2] = peso

    def obtener_vertices(self):
        claves = []
        for vertice in self.adyacentes.keys():
            claves.append(vertice)
        return claves

    def cantidad_de_vertices(self):
        return self.vertices

    def cantidad_de_aristas(self):
        return self.aristas

    def vertices_adyacentes(self, vertice):
        vertices_adyacentes = []
        for vert in self.adyacentes[vertice].keys():
            vertices_adyacentes.append(vert)
        return vertices_adyacentes

    