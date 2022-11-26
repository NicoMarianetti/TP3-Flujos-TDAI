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
        if not self.es_dirigido:
            self.adyacentes[vertice2][vertice1] = peso
        self.adyacentes[vertice1][vertice2] = peso
        self.aristas += 1

    def peso_arista(self, vertice1, vertice2):
        return self.adyacentes[vertice1].get(vertice2, 0)

    def modificar_peso_arista(self, vertice1, vertice2, peso):
        if not self.adyacentes[vertice1].get(vertice2, False):
            self.agregar_arista(vertice1, vertice2, peso)
        self.adyacentes[vertice1][vertice2] = peso

    def vertices_adyacentes(self, vertice):
        vertices_adyacentes = []
        for vert in self.adyacentes[vertice].keys():
            vertices_adyacentes.append(vert)
        return vertices_adyacentes

    