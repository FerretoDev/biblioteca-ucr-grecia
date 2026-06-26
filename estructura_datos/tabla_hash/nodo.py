"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
Archivo: nodo.py
"""

from typing import Optional
from clases.estudiante import Estudiante
class Nodo:
    """
    Clase que representa un nodo en una lista enlazada, la cual se utilizará 
    dentro de la tabla hash para manejar las colisiones (cuando dos elementos 
    caen en la misma posición).
    """
    def __init__(self, valor):
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Constructor de la clase Nodo.
        
        Parámetros:
        valor (Estudiante): El objeto Estudiante que se almacenará en este nodo.
        """
        # 'valor' guarda la información principal de este nodo, que en este caso es un Estudiante.
        self.valor: Optional[Estudiante] = valor
        
        # 'sig' (siguiente) es un apuntador o enlace al próximo nodo en la lista. 
        # Al crear un nodo nuevo, siempre empieza apuntando a nada (None).
        self.sig: Optional['Nodo'] = None
