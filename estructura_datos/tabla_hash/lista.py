"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto - Paulo Anchía Correás
Archivo: lista.py
"""

from estructura_datos.tabla_hash.nodo import Nodo
from typing import Optional, List
class Lista:
    
    def __init__(self):
        """
        Parámetros: ninguno
        Devuelve:   None
        Descripción: Inicializa una lista enlazada simple vacía para el manejo de colisiones de la tabla hash.
        """
        self.primero = None
        
    def esta_vacia(self):
        """
        Parámetros: ninguno
        Devuelve:   bool
        Descripción: Retorna True si la lista se encuentra vacía, False en caso contrario.
        """
        return self.primero is None
    
    def insertar(self, estudiante):
        """
        Parámetros: estudiante (Estudiante)
        Devuelve:   None
        Descripción: Inserta un nuevo nodo con el estudiante al final de la lista, validando que el carnet no esté duplicado.
        """
        # Agrega un nuevo estudiante al final
        nodo_nuevo = Nodo(estudiante)
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
        """
        Parámetros: carnet (int o str)
        Devuelve:   Estudiante o None
        Descripción: Recorre la lista y retorna el estudiante cuyo carnet coincida, si no lo encuentra retorna None.
        """
        # Busca y retorna el estudiante por su carnet
        temp = self.primero
        while temp:
            if str(temp.valor.carnet) == str(carnet):
                return temp.valor
            temp = temp.sig
        return None

    def buscar_por_nombre(self, nombre):
        """
        Parámetros: nombre (str)
        Devuelve:   Estudiante o None
        Descripción: Recorre la lista y retorna el estudiante cuyo nombre coincida de forma exacta (sin diferenciar mayúsculas), o None.
        """
        # Busca y retorna el estudiante por su nombre
        temp = self.primero
        while temp:
            if temp.valor.nombre.lower() == nombre.lower():
                return temp.valor
            temp = temp.sig
        return None

    def buscar_por_carrera(self, carrera):
        """
        Parámetros: carrera (str)
        Devuelve:   lista de strings (List[str])
        Descripción: Retorna una lista con los nombres de todos los estudiantes que cursan la carrera indicada.
        """
        # Devuelve una lista con nombres de los que cursan la carrera
        nombres = []
        temp = self.primero
        while temp:
            if temp.valor.carrera.lower() == carrera.lower():
                nombres.append(temp.valor.nombre)
            temp = temp.sig
        return nombres

    def eliminar_por_carnet(self, carnet):
        """
        Parámetros: carnet (int o str)
        Devuelve:   bool
        Descripción: Elimina de la lista al estudiante que tenga el carnet especificado. Retorna True si lo logró, False si no.
        """
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

