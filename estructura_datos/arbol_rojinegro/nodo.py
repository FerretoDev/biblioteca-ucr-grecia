"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto - Paulo Anchía Correás
Archivo: nodo.py
"""

from typing import Optional

from clases.prestamo import Prestamo


class Nodo:
    """Nodo del árbol Rojinegro."""

    def __init__(self, prestamo: Prestamo) -> None:
        """Inicializa nodo. Padre se asigna externamente."""
        self.valor: Prestamo = prestamo
        self.izq: Optional[Nodo] = None
        self.der: Optional[Nodo] = None
        self.padre: Optional[Nodo] = None
        self.color: str = "Rojo"
