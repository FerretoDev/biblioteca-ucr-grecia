from typing import Optional

from clases.prestamo import Prestamo


class Nodo:
    """
    Descripción: Nodo del árbol Rojinegro. Almacena un Prestamo, referencias
                 a hijos izquierdo y derecho, referencia al padre, y su color
                 (rojo o negro). Necesario para mantener las propiedades RB.
    """

    def __init__(self, prestamo: Prestamo) -> None:
        """
        Parámetros: prestamo (Prestamo) — el préstamo a almacenar en el nodo.
        Devuelve:   None
        Descripción:
            Inicializa un nodo del árbol Rojinegro. Todo nuevo nodo se inserta
            en color rojo por defecto. El padre se asigna externamente.
        """
        self.valor: Prestamo = prestamo
        self.izq: Optional[NodoRB] = None
        self.der: Optional[NodoRB] = None
        self.padre: Optional[NodoRB] = None
        self.color: str = "Rojo"  # Nuevo nodo siempre es rojo
