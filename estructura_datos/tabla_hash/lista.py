from nodo import Nodo
from typing import Optional, List
class Lista:
    
    def __init__(self):
        self.primero: Optional[Nodo] = None
        
    def esta_vacia(self):
        return self.primero is None
    
    def insertar(self, valor_nuevo):
        nodo_nuevo: Optional[Nodo] = Nodo(valor_nuevo)
        if self.esta_vacia():
            self.primero = nodo_nuevo
        else:
            temp = self.primero
            while temp.sig:
                if str(temp.valor.carnet) == str(estudiante.carnet):
                    return # No inserta si el carnet ya existe
                temp = temp.sig
            if str(temp.valor.carnet) == str(estudiante.carnet):
                return
            temp.sig = nodo_nuevo

    def buscar_por_carnet(self, carnet):
        # Busca y retorna el estudiante por su carnet
        temp = self.primero
        while temp:
            if str(temp.valor.carnet) == str(carnet):
                return temp.valor
            temp = temp.sig
        return None

    def buscar_por_nombre(self, nombre):
        # Busca y retorna el estudiante por su nombre
        temp = self.primero
        while temp:
            if temp.valor.nombre.lower() == nombre.lower():
                return temp.valor
            temp = temp.sig
        return None

    def buscar_por_carrera(self, carrera):
        # Devuelve una lista con nombres de los que cursan la carrera
        nombres = []
        temp = self.primero
        while temp:
            if temp.valor.carrera.lower() == carrera.lower():
                nombres.append(temp.valor.nombre)
            temp = temp.sig
        return nombres

    def eliminar_por_carnet(self, carnet):
        # Elimina al estudiante si coincide el carnet
        if self.esta_vacia():
            return False

        if str(self.primero.valor.carnet) == str(carnet):
            self.primero = self.primero.sig
            return True

        temp = self.primero
        while temp.sig:
            if str(temp.sig.valor.carnet) == str(carnet):
                temp.sig = temp.sig.sig
                return True
            temp = temp.sig
        return False