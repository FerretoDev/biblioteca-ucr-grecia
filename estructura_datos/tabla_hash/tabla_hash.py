"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto - Paulo Anchía Correás
Archivo: tabla_hash.py
"""

from typing import List, Optional

from clases.estudiante import Estudiante
from estructura_datos.tabla_hash.lista import Lista


class TablaHash:
    def __init__(self, tamanio: int) -> None:
        """
        Parametros: tamanio (int) — numero de buckets de la tabla.
        Devuelve:   None
        Descripcion:
            Inicializa la tabla con listas vacias en cada posicion.
        """
        self.tabla_hash: List[Lista] = [Lista() for _ in range(tamanio)]
        self.tamanio = tamanio

    def calculo_hash(self, clave: int) -> int:
        """
        Parametros: clave (int) — carnet del estudiante.
        Devuelve:   int — indice en la tabla.
        Descripcion:
            Calcula el indice usando modulo del carnet entre el tamanio.
        """
        return clave % self.tamanio

    def insertar(self, estudiante: Estudiante) -> None:
        """
        Parametros: estudiante (Estudiante) — estudiante a insertar.
        Devuelve:   None
        Descripcion:
            Calcula el indice con calculo_hash e inserta en la lista
            correspondiente.
        """
        index = self.calculo_hash(estudiante.carnet)
        self.tabla_hash[index].insertar(estudiante)

    def buscar_por_carnet(self, carnet: int) -> Optional[Estudiante]:
        """
        Parametros: carnet (int) — carnet a buscar.
        Devuelve:   Estudiante si existe, None si no.
        Descripcion:
            Busqueda O(1) promedio. Calcula indice y busca en esa lista.
        """
        index = self.calculo_hash(carnet)
        return self.tabla_hash[index].buscar_por_carnet(carnet)

    def buscar_por_nombre(self, nombre: str) -> Optional[Estudiante]:
        """
        Parametros: nombre (str) — nombre del estudiante.
        Devuelve:   Estudiante si existe, None si no.
        Descripcion:
            Recorre toda la tabla buscando por nombre. O(n).
        """
        for lista in self.tabla_hash:
            encontrado = lista.buscar_por_nombre(nombre)
            if encontrado is not None:
                return encontrado
        return None

    def buscar_por_carrera(self, carrera: str) -> List[Estudiante]:
        """
        Parametros: carrera (str) — carrera a buscar.
        Devuelve:   List[Estudiante] con todos los de esa carrera.
        Descripcion:
            Recorre toda la tabla acumulando estudiantes. O(n).
        """
        resultados: List[Estudiante] = []
        for lista in self.tabla_hash:
            nombres = lista.buscar_por_carrera(carrera)
            if nombres:
                resultados.extend(nombres)
        return resultados

    def eliminar_estudiante(self, carnet: int) -> bool:
        """
        Parametros: carnet (int) — carnet del estudiante a eliminar.
        Devuelve:   bool — True si se elimino, False si no existe.
        Descripcion:
            Calcula el indice y elimina de la lista correspondiente.
            Verificar externamente que no tenga prestamos activos.
        """
        index = self.calculo_hash(carnet)
        return self.tabla_hash[index].eliminar_por_carnet(carnet)
