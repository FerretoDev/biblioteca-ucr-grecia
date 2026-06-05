from typing import List, Optional
from estructura_datos.tabla_hash.lista import Lista
class TablaHash:
    def __init__(self, tamanio: int) -> None:
        self.tabla_hash: List[Optional[Lista]] = [None] * tamanio
        for i in range(tamanio):
            self.tabla_hash[i] = Lista()

    def calculo_hash(self, clave: int , tam) -> int:
        suma = 0
        for char in clave:
            suma += ord(char)
        return suma % tam
    
    def agregar(self, nombre, tam):
        index = self.calculo_hash(nombre, tam)
        self.tabla_hash[index].insertar(nombre)

    def buscar(self, clave, tam):
        index = self.calculo_hash(clave, tam)
        return self.tabla_hash[index].buscar(clave)
    def buscar_por_nombre(self, nombre):
        # busca en todas las listas de la tabla
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
        # Lo elimina de la lista correspondiente por carnet
        index = self.calculo_hash(carnet)
        return self.tabla[index].eliminar_por_carnet(carnet)

