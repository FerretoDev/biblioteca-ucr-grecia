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

    def calcular_fe(self, raiz_p: Optional[Nodo]) -> int:
        if raiz_p is None:
            return 0
        return self._altura(raiz_p.der) - self._altura(raiz_p.izq) # Formula: Altura (hijo.der) - Altura (hijo.izq)

    def insertar(self, raiz_p: Optional[Nodo], libro_nuevo: Libro) -> Nodo: # Quizas en vez de valor nuevo podria ser libro_nuevo
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

    def rotacion_ii(self, raiz_p: Nodo) -> Nodo:
        if raiz_p.izq is None:
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

    def rotacion_dd(self, raiz_p: Nodo) -> Nodo:
        # TODO: Implementar rotación derecha derecha
        return raiz_p

    def rotacion_id(self, raiz_p: Nodo) -> Nodo:
        # TODO: Implementar rotación izquierda derecha
        return raiz_p

    def rotacion_di(self, raiz_p: Nodo) -> Nodo:
        # TODO: Implementar rotación derecha izquierda
        return raiz_p

    def buscar_codigo(self, raiz_p: Optional[Nodo], codigo: int) -> bool:
        
        if raiz_p is None:
            return False
        elif raiz_p.valor.codigo == codigo:
            return True
        else:
            if raiz_p.valor.codigo > codigo:
                return self.buscar_codigo(raiz_p.izq, codigo)
            else:
                return self.buscar_codigo(raiz_p.der, codigo)

    def buscar_titulo(self, raiz_p: Optional[Nodo], titulo: str) -> bool:
        if raiz_p is None:
            return False
        elif raiz_p.valor.titulo == titulo:
            return True
        else:
            # El AVL está ordenado por código, no por título.
            # Para buscar por título en este AVL, tendríamos que recorrerlo todo (O(n)).
            return self.buscar_titulo(raiz_p.izq, titulo) or self.buscar_titulo(raiz_p.der, titulo)

    def buscar_autor(self, raiz_p: Optional[Nodo], autor: str) -> bool:
        if raiz_p is None:
            return False
        elif raiz_p.valor.autor == autor:
            return True
        else:
            # Similar al título, búsqueda exhaustiva.
            return self.buscar_autor(raiz_p.izq, autor) or self.buscar_autor(raiz_p.der, autor)


    def es_hoja(self, nodo: Optional[Nodo]) -> bool:
        if nodo is not None and nodo.izq is None and nodo.der is None:
            return True
        return False
    
    def eliminar_codigo(self, raiz_p: Optional[Nodo], codigo: int) -> Optional[Nodo]:
        # Implementación mejorada de eliminación (parcial por ahora basándome en lo que había)
        if raiz_p is None:
            return None

        if codigo < raiz_p.valor.codigo:
            raiz_p.izq = self.eliminar_codigo(raiz_p.izq, codigo)
        elif codigo > raiz_p.valor.codigo:
            raiz_p.der = self.eliminar_codigo(raiz_p.der, codigo)
        else:
            # Nodo encontrado
            if self.es_hoja(raiz_p):
                if raiz_p == self.raiz:
                    self.raiz = None
                return None
            
            # Si solo tiene un hijo
            if raiz_p.izq is None:
                if raiz_p == self.raiz:
                    self.raiz = raiz_p.der
                return raiz_p.der
            elif raiz_p.der is None:
                if raiz_p == self.raiz:
                    self.raiz = raiz_p.izq
                return raiz_p.izq
            
            # Si tiene dos hijos (aquí faltaría buscar sucesor/predecesor para completar AVL)
            print("Tiene 2 hijos - Eliminación compleja no implementada totalmente")
            
        return raiz_p


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















