from typing import List, Optional
from estructura_datos.tabla_hash.lista import Lista
from clases.estudiante import Estudiante

class TablaHash:
    def __init__(self, tam: int) -> None:
        """
        Parámetros: tam (int)
        Devuelve:   None
        Descripción: Inicializa la tabla hash con el tamaño indicado, creando una lista enlazada vacía en cada posición.
        """
        self.tam = tam
        self.tabla: List[Optional[Lista]] = [None] * tam
        for i in range(tam):
            self.tabla[i] = Lista()

    def calculo_hash(self, clave) -> int:
        """
        Parámetros: clave (int o str)
        Devuelve:   int (índice calculado)
        Descripción: Calcula el índice en la tabla usando el número de carnet y aplicando la función módulo.
        """
        # Usa el numero de carnet (4 digitos) para definir la posicion
        return int(clave) % self.tam
    
    def insertar(self, estudiante: Estudiante):
        """
        Parámetros: estudiante (Estudiante)
        Devuelve:   None
        Descripción: Inserta un nuevo objeto estudiante en la tabla hash en la posición correspondiente.
        """
        index = self.calculo_hash(estudiante.carnet)
        self.tabla[index].insertar(estudiante)

    def buscar_por_carnet(self, carnet):
        """
        Parámetros: carnet (int o str)
        Devuelve:   Estudiante o None
        Descripción: Busca a un estudiante por su número de carnet aplicando la función hash para ir a la lista exacta.
        """
        index = self.calculo_hash(carnet)
        return self.tabla[index].buscar_por_carnet(carnet)

    def buscar_por_nombre(self, nombre: str):
        """
        Parámetros: nombre (str)
        Devuelve:   Estudiante o None
        Descripción: Recorre todas las listas de la tabla hash buscando a un estudiante por su nombre.
        """
        # busca en todas las listas de la tabla
        for lista in self.tabla:
            encontrado = lista.buscar_por_nombre(nombre)
            if encontrado is not None:
                return encontrado
        return None
    
    def buscar_por_carrera(self, carrera: str):
        """
        Parámetros: carrera (str)
        Devuelve:   lista de nombres (List[str])
        Descripción: Recorre todas las listas de la tabla y devuelve los nombres de todos los estudiantes de una misma carrera.
        """
        # Recorre todo y junta los nombres de esa carrera
        resultado_nombres = []
        for lista in self.tabla:
            nombres = lista.buscar_por_carrera(carrera)
            if nombres:
                resultado_nombres.extend(nombres)
        return resultado_nombres

    def eliminar_estudiante(self, carnet):
        """
        Parámetros: carnet (int o str)
        Devuelve:   bool (True si se eliminó, False si no)
        Descripción: Elimina al estudiante por su carnet de la lista correspondiente (se debe validar externamente si tiene préstamos).
        """
        # Lo elimina de la lista correspondiente por carnet
        index = self.calculo_hash(carnet)
        return self.tabla[index].eliminar_por_carnet(carnet)

