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

    def buscar_codigo(self, raiz_p:Optional[Nodo], codigo: int):
        
        if raiz_p is None:
            return False
        elif raiz_p.valor.codigo == codigo:
            return True
        elif raiz_p is None:
            return False
        else:
            if raiz_p.valor.codigo > codigo:
                return self.buscar_codigo(raiz_p.izq, codigo)
            else:
                return self.buscar_codigo(raiz_p.der, codigo)

    def buscar_titulo(self, raiz_p:Optional[Nodo], titulo: int):
        if raiz_p is None:
            return False
        elif raiz_p.valor.codigo == titulo:
            return True
        elif raiz_p is None:
            return False
        else:
            if raiz_p.valor.codigo > titulo:
                return self.buscar_codigo(raiz_p.izq, titulo)
            else:
                return self.buscar_codigo(raiz_p.der, titulo)

    def buscar_autor(self, raiz_p: Optional[Nodo], autor: int):
        if raiz_p is None:
            return False
        elif raiz_p.valor.codigo == autor:
            return True
        elif raiz_p is None:
            return False
        else:
            if raiz_p.valor.codigo > autor:
                return self.buscar_codigo(raiz_p.izq, autor)
            else:
                return self.buscar_codigo(raiz_p.der, autor)


    def es_hoja(self, nodo):
        if nodo is not None and nodo.izq is None and nodo.der is None:
            return True
        return False
    
    def eliminar_codigo(self, raiz_p, codigo):
        # 1. pregunta si self.raiz es el nodo buscado y si es hoja
        if self.raiz is not None and self.raiz.valor == codigo:
            if self.es_hoja(self.raiz):
                self.raiz = None

        elif codigo < raiz_p.valor:
            # pregunta por el hijo izquierdo
            if raiz_p.izq is not None and codigo == raiz_p.izq.valor:
                if self.es_hoja(raiz_p.izq):
                    raiz_p.izq = None
                else:
                    # si solo tiene una hijo izquierdo
                    if raiz_p.izq.der is None:
                        raiz_p.izq = raiz_p.izq.izq

                    # si solo tiene un hijo derecho
                    elif raiz_p.izq.izq is None:
                        raiz_p.izq = raiz_p.izq.der

                    else:
                        print("Tiene 2 hijos")
            else:
                self.eliminar_codigo(raiz_p.izq, codigo)

        elif codigo > raiz_p.valor:
            # Preguntamos por el hijo derecho
            if raiz_p.der is not None and codigo == raiz_p.der.valor:
                if self.es_hoja(raiz_p.der):
                    raiz_p.der = None
                else:
                    # aca la misma historia, solo uno izq
                    if raiz_p.der.der is None:
                        raiz_p.der = raiz_p.der.izq
                    
                    # solo un der
                    elif raiz_p.der.izq is None:
                        raiz_p.der = raiz_p.der.der
                    
                    else:
                        print("Tiene dos hijos")
            else:
                self.eliminar_codigo(raiz_p.der, codigo)


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















