"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
Archivo: nodo.py
"""

from typing import Optional

from clases.prestamo import Prestamo


class Nodo:
    """
    Clase que representa un Nodo (o 'ramita') dentro de un Árbol Rojinegro.
    En este caso, cada nodo del árbol sirve para guardar un 'Préstamo' de libro.
    El árbol rojinegro es especial porque se auto-balancea usando colores (Rojo o Negro)
    para que buscar un préstamo siempre sea muy rápido.
    """

    def __init__(self, prestamo: Prestamo) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Constructor del Nodo para el árbol rojinegro.
        
        Parámetros:
        prestamo (Prestamo) — El objeto Préstamo que queremos guardar en este nodo.
        
        Devuelve:
        None (nada).
        
        Descripción:
        Prepara el nodo recién creado. Por regla general de los árboles rojinegros,
        todo nodo nuevo siempre nace siendo de color 'Rojo'.
        Sus conexiones a otros nodos (hijos y padre) nacen vacías (None).
        """
        # 'valor' guarda la información importante. Aquí es un Préstamo.
        self.valor: Prestamo = prestamo
        
        # 'izq' (hijo izquierdo) apuntará a un préstamo con código MENOR
        self.izq: Optional['Nodo'] = None
        
        # 'der' (hijo derecho) apuntará a un préstamo con código MAYOR
        self.der: Optional['Nodo'] = None
        
        # 'padre' apunta al nodo que está justo por encima de este en el árbol
        self.padre: Optional['Nodo'] = None
        
        # 'color' define si el nodo es "Rojo" o "Negro". Todo nodo nuevo empieza Rojo.
        self.color: str = "Rojo"
