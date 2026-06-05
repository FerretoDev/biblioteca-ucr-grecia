from typing import List, Optional
from clases.estudiante import Estudiante
class Nodo:

    def __init__(self, valor):
        self.valor: Optional[Estudiante] = valor
        self.sig: Optional[Nodo] = None
