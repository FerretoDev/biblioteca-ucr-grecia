from lista import Lista
from typing import Optional, List
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
        self.tablaHash[index].insertar(nombre)

    def buscar(self, clave, tam):
        index = self.calculo_hash(clave, tam)
        return self.tablaHash[index].buscar(clave)

    def indexado(self, clave, tam):
        return self.calculo_hash(clave, tam)

#que cada campo de la tabla tenga una lista
#clase nodo clase lista clase tabla y clase main





