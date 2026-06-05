from .lista import Lista

class TablaHash:
    def __init__(self, tam=97):
        # Guarda el tamano y crea listas vacias
        self.tam = tam
        self.tabla = [None] * tam
        for i in range(tam):
            self.tabla[i] = Lista()

    def calculo_hash(self, carnet):
        # Usa el numero de carnet (4 digitos) para definir la posicion
        return int(carnet) % self.tam
    
    def insertar(self, estudiante):
        # Metemos el estudiante en la lista de acuerdo a su hash
        index = self.calculo_hash(estudiante.carnet)
        self.tabla[index].insertar(estudiante)

    def buscar_por_carnet(self, carnet):
        # Vamos directo al indice y buscamos el carnet
        index = self.calculo_hash(carnet)
        return self.tabla[index].buscar_por_carnet(carnet)

    def buscar_por_nombre(self, nombre):
        # Toca buscar en todas las listas de la tabla
        for lista in self.tabla:
            encontrado = lista.buscar_por_nombre(nombre)
            if encontrado is not None:
                return encontrado
        return None
    
    def buscar_por_carrera(self, carrera):
        # Recorre todo y junta los nombres de esa carrera
        resultado_nombres = []
        for lista in self.tabla:
            nombres = lista.buscar_por_carrera(carrera)
            if nombres:
                resultado_nombres.extend(nombres)
        return resultado_nombres

    def eliminar_estudiante(self, carnet):
        # Lo eliminamos de la lista correspondiente por carnet
        index = self.calculo_hash(carnet)
        return self.tabla[index].eliminar_por_carnet(carnet)

