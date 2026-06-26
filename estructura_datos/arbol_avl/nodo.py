"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
Archivo: nodo.py
"""

from clases.libro import Libro
from typing import Optional
class Nodo:
    """
    Descripción:
        Clase que representa un "pedacito" o bloque básico de nuestro Árbol AVL (una estructura de datos).
        Cada 'Nodo' es como una caja que guarda un libro adentro, y tiene dos "brazos" (izquierdo y derecho)
        para agarrarse de otras cajas (otros nodos).
    """
    def __init__(self, libro: Libro) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros:
            libro (Libro): El objeto de tipo Libro que queremos guardar dentro de esta "caja" (nodo).
        Devuelve: None
        Descripción:
            Constructor de la clase Nodo. Prepara la "caja" guardando el libro,
            dejando los brazos vacíos (sin conectar a otros nodos todavía), y poniendo su balance en 0.
        """
        # 'self.valor' es el dato real que estamos guardando (el libro)
        self.valor: Libro = libro 
        
        # 'self.izq' apunta al nodo que quede a la izquierda (por ahora vacío)
        self.izq: Optional[Nodo] = None
        
        # 'self.der' apunta al nodo que quede a la derecha (por ahora vacío)
        self.der: Optional[Nodo] = None
        
        # Atributo altura reservado pero no usado, lo marcamos como 0
        self.altura: int = 0 
        
        # 'self.fe' significa "Factor de Equilibrio". Nos dice si el árbol está inclinado 
        # a la derecha o a la izquierda. 0 significa que está perfectamente balanceado.
        self.fe: int = 0