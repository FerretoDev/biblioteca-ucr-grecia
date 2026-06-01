from typing import Optional

from clases.libro import Libro
from estructura_datos.arbol_avl.nodo import Nodo
class ArbolAVL:
    """
        Descripción: Árbol binario de búsqueda balanceado (AVL) para
                     gestionar libros. Se ordena por el código del libro.
                     Garantiza O(log n) en inserción, eliminación y búsqueda.
        """

    def __init__(self) -> None:
        self.raiz: Optional[Nodo] = None

    def _altura(self, raiz_p: Optional[Nodo]) -> int:
        if raiz_p is None:
            return 0

        altura_izq: int = self._altura(raiz_p.izq)
        altura_der: int = self._altura(raiz_p.der)

        if altura_izq > altura_der:
            return altura_izq + 1
        else:
            return altura_der + 1

    def calcular_fe(self,raiz_p) -> int:
        if raiz_p is None:
            return 0
        return self._altura(raiz_p.der) - self._altura(raiz_p.izq) # Formula: Altura (hijo.der) - Altura (hijo.izq)

    def insertar(self, raiz_p: Optional[Nodo], libro_nuevo: Libro) -> Nodo | None: # Quizas en vez de valor nuevo podria ser libro_nuevo
        # Pre-orden
        if self.raiz is None:
            self.raiz = Nodo(libro_nuevo)
            return self.raiz

        if raiz_p is None:
            return Nodo(libro_nuevo)


        #-------
        if libro_nuevo.codigo < raiz_p.valor.codigo: # raiz_p es lo mismo que raiz_p.libro
            # Conecta el hijo izquierdo
            raiz_p.izq = self.insertar(raiz_p.izq, libro_nuevo)

        elif libro_nuevo.codigo > raiz_p.valor.codigo:
            raiz_p.der = self.insertar(raiz_p.der, libro_nuevo)

        else:
            return raiz_p # .codigo duplicado

        raiz_p.fe = self.calcular_fe(raiz_p)

        return raiz_p

    def rotacion_ii(self, raiz_p):
        if raiz_p is None or raiz_p.izq in None:
            return raiz_p

        actual = raiz_p.izq
        hijo = actual.der

        # Conecta raiz_p como hijo derecho de actual
        actual.der = raiz_p
        # Conecta el hijo derecho de actual como hijo izquierdo raiz_p
        raiz_p.izq = hijo

        # Se aplica el cálculo del factor de equibrio
        raiz_p.fe = self.calcular_fe(raiz_p)
        actual.fe = self.calcular_fe(actual)
        return actual

    def rotacion_dd(self, raiz_p):
        # TODO: Implementar rotación derecha derecha
        ...

    def rotacion_id(self, raiz_p):
        # TODO: Implementar rotación izquierda derecha
        ...

    def rotacion_di(self,rai_p):
        # TODO: Implementar rotación derecha izquierda
        ...

    def buscar_codigo(self, raiz_p, codigo):
        
        if raiz_p is None:
            return False
        elif raiz_p.valor == codigo:
            return True
        elif raiz_p is None:
            print("No existe")
        else:
            if raiz_p.valor > codigo:
                return self.buscar(raiz_p.izq, codigo)
            else:
                return self.buscar(raiz_p.der, codigo)
    def buscar_titulo(self, raiz_p, titulo):
        # TODO: Implementar buscar por titulo
        ...

    def buscar_autor(self, raiz_p, autor):
        # TODO: Implementar buscar por autor
        ...

    def eliminar_codigo(self, raiz_p, codigo):
        # TODO: Implementar eliminar por codigo
        ...

    def mostrar(self, raiz_p)-> None:
        if raiz_p is not None:
            libro: Libro = raiz_p.valor

            print(f"Código {libro.codigo}")
            # print(f"Autor {libro.autor}")
            #print(f"Titulo {libro.titulo}")
            #print(f"Año {libro.anio}")
            #print(f"Editorial {libro.editorial}")
            #print(f"Areas {libro.area}")

            self.mostrar(raiz_p.izq)
            self.mostrar(raiz_p.der)















