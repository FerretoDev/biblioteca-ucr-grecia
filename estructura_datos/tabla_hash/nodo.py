"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto - Paulo Anchía Correás
Archivo: nodo.py
"""

from typing import Optional
from clases.estudiante import Estudiante
class Nodo:

    def __init__(self, valor):
        self.valor: Optional[Estudiante] = valor
        self.sig: Optional[Nodo] = None
