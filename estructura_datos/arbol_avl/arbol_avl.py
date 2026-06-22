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
        """
        Parámetros: ninguno
        Devuelve:   None
        Descripción:
            Inicializa un árbol AVL vacío con la raíz establecida en None.
        """
        self.raiz: Optional[Nodo] = None

    def _altura(self, raiz_p: Optional[Nodo]) -> int:
        """
        Parámetros: raiz_p (Optional[Nodo]) — nodo raíz del subárbol.
        Devuelve:   int — la altura del subárbol.
        Descripción:
            Calcula recursivamente la altura de un subárbol, devolviendo 0 si el nodo es None.
        """
        if raiz_p is None:
            return 0

        altura_izq: int = self._altura(raiz_p.izq)
        altura_der: int = self._altura(raiz_p.der)

        if altura_izq > altura_der:
            return altura_izq + 1
        else:
            return altura_der + 1

    def calcular_fe(self, raiz_p: Optional[Nodo]) -> int:
        """
        Parámetros: raiz_p (Optional[Nodo]) — nodo al que se le calculará el factor de equilibrio.
        Devuelve:   int — factor de equilibrio (altura subárbol derecho - altura subárbol izquierdo).
        Descripción:
            Calcula el factor de equilibrio de un nodo basándose en la altura de sus hijos.
        """
        if raiz_p is None:
            return 0
        return self._altura(raiz_p.der) - self._altura(raiz_p.izq) # Formula: Altura (hijo.der) - Altura (hijo.izq)

    def insertar(self, raiz_p: Optional[Nodo], libro_nuevo: Libro) -> Nodo:
        """
        Parámetros: raiz_p (Optional[Nodo]) — nodo inicial para insertar.
                    libro_nuevo (Libro) — libro a insertar en el árbol.
        Devuelve:   Nodo — la raíz (posiblemente nueva/balanceada) del subárbol.
        Descripción:
            Inserta un nuevo libro en el árbol AVL de manera ordenada por código y realiza
            los rebalanceos necesarios (rotaciones) si se detecta un desbalance.
        """
        if raiz_p is None:
            return Nodo(libro_nuevo)

        if libro_nuevo.codigo < raiz_p.valor.codigo:
            raiz_p.izq = self.insertar(raiz_p.izq, libro_nuevo)
        elif libro_nuevo.codigo > raiz_p.valor.codigo:
            raiz_p.der = self.insertar(raiz_p.der, libro_nuevo)
        else:
            return raiz_p # Código duplicado

        # Actualizar factor de equilibrio
        raiz_p.fe = self.calcular_fe(raiz_p)

        # Balancear el árbol
        # Caso Izquierda-Izquierda (II) o Izquierda-Derecha (ID)
        if raiz_p.fe == -2:
            if self.calcular_fe(raiz_p.izq) <= 0:
                return self.rotacion_ii(raiz_p)
            else:
                return self.rotacion_id(raiz_p)

        # Caso Derecha-Derecha (DD) o Derecha-Izquierda (DI)
        if raiz_p.fe == 2:
            if self.calcular_fe(raiz_p.der) >= 0:
                return self.rotacion_dd(raiz_p)
            else:
                return self.rotacion_di(raiz_p)

        return raiz_p

    def rotacion_ii(self, raiz_p: Nodo) -> Nodo: # Rotación simple a la derecha
        """
        Parámetros: raiz_p (Nodo) — nodo que presenta el desbalance.
        Devuelve:   Nodo — la nueva raíz del subárbol después de la rotación simple a la derecha.
        Descripción:
            Realiza una rotación simple a la derecha (caso Izquierda-Izquierda, II) para restaurar el balance.
        """
        actual = raiz_p.izq
        hijo = actual.der

        actual.der = raiz_p
        raiz_p.izq = hijo

        raiz_p.fe = self.calcular_fe(raiz_p)
        actual.fe = self.calcular_fe(actual)
        return actual

    def rotacion_dd(self, raiz_p: Nodo) -> Nodo: # Rotación simple a la izquierda
        """
        Parámetros: raiz_p (Nodo) — nodo que presenta el desbalance.
        Devuelve:   Nodo — la nueva raíz del subárbol después de la rotación simple a la izquierda.
        Descripción:
            Realiza una rotación simple a la izquierda (caso Derecha-Derecha, DD) para restaurar el balance.
        """
        actual = raiz_p.der
        hijo = actual.izq

        actual.izq = raiz_p
        raiz_p.der = hijo

        raiz_p.fe = self.calcular_fe(raiz_p)
        actual.fe = self.calcular_fe(actual)
        return actual

    def rotacion_id(self, raiz_p: Nodo) -> Nodo:
        """
        Parámetros: raiz_p (Nodo) — nodo que presenta el desbalance.
        Devuelve:   Nodo — la nueva raíz del subárbol después de la rotación doble izquierda-derecha.
        Descripción:
            Realiza una rotación doble izquierda-derecha (caso Izquierda-Derecha, ID) para restaurar el balance.
        """
        raiz_p.izq = self.rotacion_dd(raiz_p.izq)
        return self.rotacion_ii(raiz_p)

    def rotacion_di(self, raiz_p: Nodo) -> Nodo:
        """
        Parámetros: raiz_p (Nodo) — nodo que presenta el desbalance.
        Devuelve:   Nodo — la nueva raíz del subárbol después de la rotación doble derecha-izquierda.
        Descripción:
            Realiza una rotación doble derecha-izquierda (caso Derecha-Izquierda, DI) para restaurar el balance.
        """
        raiz_p.der = self.rotacion_ii(raiz_p.der)
        return self.rotacion_dd(raiz_p)

    def buscar_codigo(self, raiz_p: Optional[Nodo], codigo: int) -> Optional[Libro]:
        """
        Parámetros: raiz_p (Optional[Nodo]) — nodo inicial de búsqueda.
                    codigo (int) — código del libro a buscar.
        Devuelve:   Optional[Libro] — el libro encontrado o None si no existe.
        Descripción:
            Busca un libro por su código utilizando búsqueda binaria en el árbol AVL.
        """
        if raiz_p is None:
            return None
        elif raiz_p.valor.codigo == codigo:
            return raiz_p.valor
        elif raiz_p.valor.codigo > codigo:
            return self.buscar_codigo(raiz_p.izq, codigo)
        else:
            return self.buscar_codigo(raiz_p.der, codigo)

    def buscar_titulo(self, raiz_p: Optional[Nodo], titulo: str) -> Optional[Libro]:
        """
        Parámetros: raiz_p (Optional[Nodo]) — nodo inicial de búsqueda.
                    titulo (str) — título del libro a buscar.
        Devuelve:   Optional[Libro] — el libro encontrado o None si no existe.
        Descripción:
            Recorre el árbol en inorden para buscar un libro por su título.
        """
        if raiz_p is None:
            return None

        # 1. Buscar en el subárbol izquierdo (Inorden)
        libro_izq = self.buscar_titulo(raiz_p.izq, titulo)
        if libro_izq is not None:
            return libro_izq

        # 2. Evaluar el nodo actual
        if raiz_p.valor.titulo == titulo:
            return raiz_p.valor

        # 3. Buscar en el subárbol derecho
        return self.buscar_titulo(raiz_p.der, titulo)

    def buscar_autor(self, raiz_p: Optional[Nodo], autor: str) -> list[Libro]:
        """
        Parámetros: raiz_p (Optional[Nodo]) — nodo inicial de búsqueda.
                    autor (str) — autor del libro a buscar.
        Devuelve:   list[Libro] — lista de libros del autor.
        Descripción:
            Recorre el árbol en inorden para buscar y listar todos los libros de un autor.
        """
        if raiz_p is None:
            return []

        # 1. Buscar en el subárbol izquierdo (Inorden)
        libros = self.buscar_autor(raiz_p.izq, autor)

        # 2. Evaluar el nodo actual
        if raiz_p.valor.autor == autor:
            libros.append(raiz_p.valor)

        # 3. Buscar en el subárbol derecho y extender la lista
        libros.extend(self.buscar_autor(raiz_p.der, autor))

        return libros

    def inorden(self, raiz_p) -> None: # Funcion que se encarga de mostrar de manera inorden

        """
        Parámetros: raiz_p (Optional[Nodo]) — nodo inicial para el recorrido.
        Devuelve:   None
        Descripción:
            Recorre el árbol AVL en inorden (izq -> nodo -> der) imprimiendo los códigos de los libros.
        """
        if raiz_p is not None:
            self.inorden(raiz_p.izq)

            libro: Libro = raiz_p.valor
            print(f"Código {libro.codigo}")
            # print(f"Autor {libro.autor}")
            # print(f"Titulo {libro.titulo}")
            # print(f"Año {libro.anio}")
            # print(f"Editorial {libro.editorial}")
            # print(f"Areas {libro.area}")

            self.inorden(raiz_p.der)

    def obtener_libros_inorden(self, raiz_p: Optional[Nodo]) -> list[Libro]:
        """
        Parámetros: raiz_p (Optional[Nodo]) — nodo raíz del subárbol.
        Devuelve:   list[Libro] — lista de objetos Libro ordenados por código.
        Descripción:
            Recorre el árbol AVL en inorden y retorna la lista de libros ordenados.
            Este método es fundamental para que la interfaz gráfica (GUI) obtenga
            los datos y los pueda mostrar en una tabla o lista.
        """
        if raiz_p is None:
            return []

        libros = []
        libros.extend(self.obtener_libros_inorden(raiz_p.izq))
        libros.append(raiz_p.valor)
        libros.extend(self.obtener_libros_inorden(raiz_p.der))
        return libros


    def _get_min_valor_nodo(self, nodo: Nodo) -> Nodo:
        """
        Parámetros: nodo (Nodo) — nodo raíz desde el cual buscar.
        Devuelve:   Nodo — el nodo con el menor código de libro en ese subárbol.
        Descripción:
            Busca y retorna el nodo más a la izquierda de un subárbol, el cual contiene el menor valor.
        """
        if nodo is None or nodo.izq is None:
            return nodo
        return self._get_min_valor_nodo(nodo.izq)

    def eliminar_codigo(self, raiz_p: Optional[Nodo], codigo: int) -> Optional[Nodo]:
        """
        Parámetros: raiz_p (Optional[Nodo]) — nodo raíz del subárbol del cual eliminar.
                    codigo (int) — código del libro a eliminar.
        Devuelve:   Optional[Nodo] — la raíz (posiblemente balanceada) del subárbol tras la eliminación.
        Descripción:
            Elimina un libro del árbol AVL por su código, rebalanceando el árbol si es necesario.
            Nota: la validación de si el libro está prestado se debe realizar externamente.
        """
        if raiz_p is None:
            return None

        if codigo < raiz_p.valor.codigo:
            raiz_p.izq = self.eliminar_codigo(raiz_p.izq, codigo)
        elif codigo > raiz_p.valor.codigo:
            raiz_p.der = self.eliminar_codigo(raiz_p.der, codigo)
        else:
            # Nodo encontrado
            if raiz_p.izq is None:
                temp = raiz_p.der
                raiz_p = None
                return temp
            elif raiz_p.der is None:
                temp = raiz_p.izq
                raiz_p = None
                return temp

            # Nodo con dos hijos: obtener el sucesor (mínimo en el subárbol derecho)
            temp = self._get_min_valor_nodo(raiz_p.der)
            raiz_p.valor = temp.valor
            raiz_p.der = self.eliminar_codigo(raiz_p.der, temp.valor.codigo)

        if raiz_p is None:
            return raiz_p

        # Actualizar factor de equilibrio
        raiz_p.fe = self.calcular_fe(raiz_p)

        # Balancear el árbol
        if raiz_p.fe == -2:
            if self.calcular_fe(raiz_p.izq) <= 0:
                return self.rotacion_ii(raiz_p)
            else:
                return self.rotacion_id(raiz_p)

        if raiz_p.fe == 2:
            if self.calcular_fe(raiz_p.der) >= 0:
                return self.rotacion_dd(raiz_p)
            else:
                return self.rotacion_di(raiz_p)

        return raiz_p

    def mostrar(self, raiz_p) -> None: # Este muestra el arbol en posorden y es para debug
        """
        Parámetros: raiz_p (Optional[Nodo]) — nodo inicial para mostrar.
        Devuelve:   None
        Descripción:
            Muestra el contenido del árbol imprimiendo los códigos en recorrido preorden.
        """
        if raiz_p is not None:
            libro: Libro = raiz_p.valor

            print(f"Código {libro.codigo}")

            self.mostrar(raiz_p.izq)
            self.mostrar(raiz_p.der)
