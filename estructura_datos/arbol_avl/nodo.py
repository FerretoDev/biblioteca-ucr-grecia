from clases.libro import Libro
from typing import Optional
class Nodo:
    """
        Parámetros: libro (Libro) — dato almacenado en el nodo.
        Descripción: Nodo del árbol AVL. Almacena un Libro, referencias
                     a hijos izquierdo y derecho, y su altura actual.
        """
    def __init__(self, libro: Libro) -> None:
        self.valor: Libro = libro # Es como decir self.libro = Libro
        self.izq: Optional[Nodo] = None
        self.der: Optional[Nodo] = None
        self.altura: int = 0 # No usar
        self.fe: int = 0