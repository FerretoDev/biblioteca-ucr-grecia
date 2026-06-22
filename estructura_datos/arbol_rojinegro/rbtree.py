from typing import List, Optional
from clases.prestamo import Prestamo
from estructura_datos.arbol_rojinegro.nodo import NodoRB


class RBTree:
    """
    Descripción: Árbol Binario de Búsqueda Rojinegro (Red-Black Tree) para
    gestionar préstamos ordenados por código de préstamo.
    Mantiene las 5 propiedades esenciales del árbol RB:
        1. Todo nodo es rojo o negro.
        2. La raíz es siempre negra.
        3. Las hojas NIL son negras.
        4. Si un nodo es rojo, sus hijos son negros.
        5. Todos los caminos desde un nodo a sus hojas NIL tienen
           el mismo número de nodos negros (altura negra).
    """

    def __init__(self) -> None:
        """
        Parámetros: ninguno
        Devuelve:   None
        Descripción:
            Inicializa un árbol Rojinegro vacío con la raíz establecida en None.
        """
        self.raiz: Optional[NodoRB] = None

    # ========== BÚSQUEDA ==========

    def buscar_codigo(self, raiz_p: Optional[NodoRB], codigo_prestamo: int) -> Optional[Prestamo]:
        """
        Parámetros: raiz_p (Optional[NodoRB]) — nodo inicial de búsqueda.
                    codigo_prestamo (int) — código del préstamo a buscar.
        Devuelve:   Optional[Prestamo] — el préstamo encontrado o None si no existe.
        Descripción:
            Busca un préstamo en el árbol Rojinegro por su código de forma recursiva.
            Complejidad: O(log n) en el mejor caso, O(n) en el peor.
        """
        if raiz_p is None:
            return None

        if codigo_prestamo == raiz_p.valor.codigo_prestamo:
            return raiz_p.valor
        elif codigo_prestamo < raiz_p.valor.codigo_prestamo:
            return self.buscar_codigo(raiz_p.izq, codigo_prestamo)
        else:
            return self.buscar_codigo(raiz_p.der, codigo_prestamo)

    def _buscar_nodo(self, raiz_p: Optional[NodoRB], codigo_prestamo: int) -> Optional[NodoRB]:
        """
        Parámetros: raiz_p (Optional[NodoRB]) — nodo inicial de búsqueda.
                    codigo_prestamo (int) — código del préstamo a buscar.
        Devuelve:   Optional[NodoRB] — el nodo que contiene el préstamo o None.
        Descripción:
            Busca y retorna el nodo que contiene un préstamo específico.
            Método auxiliar para operaciones internas del árbol.
        """
        if raiz_p is None:
            return None

        if codigo_prestamo == raiz_p.valor.codigo_prestamo:
            return raiz_p
        elif codigo_prestamo < raiz_p.valor.codigo_prestamo:
            return self._buscar_nodo(raiz_p.izq, codigo_prestamo)
        else:
            return self._buscar_nodo(raiz_p.der, codigo_prestamo)

    # ========== ROTACIONES ==========

    def rotar_izq(self, nodo_p: NodoRB) -> NodoRB:
        """
        Parámetros: nodo_p (NodoRB) — nodo sobre el cual rotar.
        Devuelve:   NodoRB — la nueva raíz del subárbol después de la rotación.
        Descripción:
            Realiza una rotación simple a la izquierda. El hijo derecho de nodo_p
            sube para ocupar su lugar, y nodo_p desciende como hijo izquierdo.
            Estructura: antes de rotación:    después de rotación:
                           nodo_p                      derecho
                          /      \\                    /       \\
                        izq    derecho     =>      nodo_p    der_der
                              /     \\            /     \\
                          der_izq  der_der      izq   der_izq
        """

        nuevo_raiz = nodo_p.der
        
        if nuevo_raiz is None:
            return nodo_p
        
        # conecta el subárbol izquierdo del hijo derecho como derecho de nodo_p
        nodo_p.der = nuevo_raiz.izq
        if nuevo_raiz.izq is not None:
            nuevo_raiz.izq.padre = nodo_p
        
        # conecta el padre de nodo_p con nuevo_raiz
        nuevo_raiz.padre = nodo_p.padre
        
        # conecta nodo_p como hijo izquierdo de nuevo_raiz
        nuevo_raiz.izq = nodo_p
        nodo_p.padre = nuevo_raiz
        
        return nuevo_raiz

    def rotar_der(self, nodo_p: NodoRB) -> NodoRB:
        """
        Parámetros: nodo_p (NodoRB) — nodo sobre el cual rotar.
        Devuelve:   NodoRB — la nueva raíz del subárbol después de la rotación.
        Descripción:
            Realiza una rotación simple a la derecha. El hijo izquierdo de nodo_p
            sube para ocupar su lugar, y nodo_p desciende como hijo derecho.
            Estructura: antes de rotación:    después de rotación:
                           nodo_p                      izquierdo
                          /      \\                    /       \\
                      izquierdo   der     =>      izq_izq    nodo_p
                      /     \\                              /     \\
                  izq_izq  izq_der                    izq_der    der
        """
        # Obtener el hijo izquierdo
        nuevo_raiz = nodo_p.izq
        
        if nuevo_raiz is None:
            return nodo_p
        
        # conecta el subárbol derecho del hijo izquierdo como izquierdo de nodo_p
        nodo_p.izq = nuevo_raiz.der
        if nuevo_raiz.der is not None:
            nuevo_raiz.der.padre = nodo_p
        
        # conecta el padre de nodo_p con nuevo_raiz
        nuevo_raiz.padre = nodo_p.padre
        
        # conecta nodo_p como hijo derecho de nuevo_raiz
        nuevo_raiz.der = nodo_p
        nodo_p.padre = nuevo_raiz
        
        return nuevo_raiz

    # ========== INSERCIÓN ==========

    def insertar(self, prestamo_nuevo: Prestamo) -> None:
        """
        Parámetros: prestamo_nuevo (Prestamo) — el préstamo a insertar.
        Devuelve:   None
        Descripción:
            Inserta un nuevo préstamo en el árbol Rojinegro de manera ordenada
            por código de préstamo. Si el código ya existe, no se inserta (sin duplicados).
            Luego realiza recoloración y rotaciones para mantener las propiedades RB.
        """
        nuevo_nodo = NodoRB(prestamo_nuevo)
        
        if self.raiz is None:
            self.raiz = nuevo_nodo
            self.raiz.color = "Negro"
            return
        
        actual = self.raiz
        padre = None
        
        while actual is not None:
            padre = actual
            if prestamo_nuevo.codigo_prestamo < actual.valor.codigo_prestamo:
                actual = actual.izq
            elif prestamo_nuevo.codigo_prestamo > actual.valor.codigo_prestamo:
                actual = actual.der
            else:
                # Código duplicado
                return
        
        # conecta el nuevo nodo con su padre
        nuevo_nodo.padre = padre
        
        if prestamo_nuevo.codigo_prestamo < padre.valor.codigo_prestamo:
            padre.izq = nuevo_nodo
        else:
            padre.der = nuevo_nodo
        
        self._reparar_insercion(nuevo_nodo)

    def _reparar_insercion(self, nodo_p: NodoRB) -> None:
        """
        Parámetros: nodo_p (NodoRB) — el nodo recién insertado (siempre rojo).
        Devuelve:   None
        Descripción:
            Repara las propiedades del árbol Rojinegro después de una inserción.
            Resuelve violaciones de la propiedad 4: "si un nodo es rojo, sus hijos
            deben ser negros" mediante recoloración y rotaciones.
        """
        while nodo_p != self.raiz and nodo_p.padre is not None and nodo_p.padre.color == "Rojo":
            if nodo_p.padre == nodo_p.padre.padre.izq:
                # El padre es hijo izquierdo del abuelo
                tio = nodo_p.padre.padre.der
                
                if tio is not None and tio.color == "Rojo":
                    # Caso 1: Tío es rojo -> recolorar
                    nodo_p.padre.color = "Negro"
                    tio.color = "Negro"
                    nodo_p.padre.padre.color = "Rojo"
                    nodo_p = nodo_p.padre.padre
                else:
                    # Caso 2 y 3: Tío es negro -> rotar
                    if nodo_p == nodo_p.padre.der:
                        # Caso 2: nodo es hijo derecho -> rotar padre a izquierda
                        nodo_p = nodo_p.padre
                        self.raiz = self._rotar_izq_interna(self.raiz, nodo_p)
                    
                    # Caso 3: nodo es hijo izquierdo -> recolorar y rotar abuelo a derecha
                    nodo_p.padre.color = "Negro"
                    nodo_p.padre.padre.color = "Rojo"
                    self.raiz = self._rotar_der_interna(self.raiz, nodo_p.padre.padre)
            else:
                # El padre es hijo derecho del abuelo (simétricamente opuesto)
                tio = nodo_p.padre.padre.izq
                
                if tio is not None and tio.color == "Rojo":
                    # Caso 1: Tío es rojo -> recolorar
                    nodo_p.padre.color = "Negro"
                    tio.color = "Negro"
                    nodo_p.padre.padre.color = "Rojo"
                    nodo_p = nodo_p.padre.padre
                else:
                    # Caso 2 y 3: Tío es negro -> rotar
                    if nodo_p == nodo_p.padre.izq:
                        # Caso 2: nodo es hijo izquierdo -> rotar padre a derecha
                        nodo_p = nodo_p.padre
                        self.raiz = self._rotar_der_interna(self.raiz, nodo_p)
                    
                    # Caso 3: nodo es hijo derecho -> recolorar y rotar abuelo a izquierda
                    nodo_p.padre.color = "Negro"
                    nodo_p.padre.padre.color = "Rojo"
                    self.raiz = self._rotar_izq_interna(self.raiz, nodo_p.padre.padre)
        
        # Asegurar que la raíz sea negra
        self.raiz.color = "Negro"

    def _rotar_izq_interna(self, raiz: Optional[NodoRB], nodo_p: NodoRB) -> Optional[NodoRB]:
        """
        Parámetros: raiz (Optional[NodoRB]) — raíz actual del árbol.
                    nodo_p (NodoRB) — nodo a rotar.
        Devuelve:   Optional[NodoRB] — nueva raíz después de la rotación.
        Descripción:
            Método auxiliar interno que realiza una rotación a la izquierda
            manteniendo la referencia correcta a la raíz del árbol.
        """
        padre = nodo_p.padre
        if padre is None:
            raiz = self.rotar_izq(nodo_p)
        else:
            es_izq = (nodo_p == padre.izq)
            nueva_raiz = self.rotar_izq(nodo_p)
            if es_izq:
                padre.izq = nueva_raiz
            else:
                padre.der = nueva_raiz
        return raiz

    def _rotar_der_interna(self, raiz: Optional[NodoRB], nodo_p: NodoRB) -> Optional[NodoRB]:
        """
        Parámetros: raiz (Optional[NodoRB]) — raíz actual del árbol.
                    nodo_p (NodoRB) — nodo a rotar.
        Devuelve:   Optional[NodoRB] — nueva raíz después de la rotación.
        Descripción:
            Método auxiliar interno que realiza una rotación a la derecha
            manteniendo la referencia correcta a la raíz del árbol.
        """
        padre = nodo_p.padre
        if padre is None:
            raiz = self.rotar_der(nodo_p)
        else:
            es_izq = (nodo_p == padre.izq)
            nueva_raiz = self.rotar_der(nodo_p)
            if es_izq:
                padre.izq = nueva_raiz
            else:
                padre.der = nueva_raiz
        return raiz

    # ========== ELIMINACIÓN ==========

    def eliminar_codigo(self, codigo_prestamo: int) -> bool:
        """
        Parámetros: codigo_prestamo (int) — código del préstamo a eliminar.
        Devuelve:   bool — True si se eliminó, False si no existe.
        Descripción:
            Elimina un préstamo del árbol Rojinegro por su código, manteniendo
            las propiedades RB mediante rebalanceo. Devuelve True si se eliminó
            exitosamente, False si el código no existe.
        """
        nodo_a_eliminar = self._buscar_nodo(self.raiz, codigo_prestamo)
        
        if nodo_a_eliminar is None:
            return False
        
        self._eliminar_nodo_interno(nodo_a_eliminar)
        return True

    def _eliminar_nodo_interno(self, nodo_p: NodoRB) -> None:
        """
        Parámetros: nodo_p (NodoRB) — el nodo a eliminar.
        Devuelve:   None
        Descripción:
            Método auxiliar que realiza la eliminación del nodo y repara
            el árbol Rojinegro después de la operación.
        """
        color_original = nodo_p.color
        x: Optional[NodoRB] = None
        x_padre: Optional[NodoRB] = None
        es_izq_de_padre = False
        
        # Caso 1: Nodo sin hijo izquierdo
        if nodo_p.izq is None:
            x = nodo_p.der
            x_padre = nodo_p.padre
            es_izq_de_padre = (nodo_p.padre is not None and nodo_p == nodo_p.padre.izq)
            self._trasplantar(nodo_p, nodo_p.der)
        # Caso 2: Nodo sin hijo derecho
        elif nodo_p.der is None:
            x = nodo_p.izq
            x_padre = nodo_p.padre
            es_izq_de_padre = (nodo_p.padre is not None and nodo_p == nodo_p.padre.izq)
            self._trasplantar(nodo_p, nodo_p.izq)
        # Caso 3: Nodo con dos hijos
        else:
            # Encontrar el sucesor (mínimo en el subárbol derecho)
            sucesor = self._obtener_minimo(nodo_p.der)
            color_original = sucesor.color
            x = sucesor.der
            
            if sucesor.padre == nodo_p:
                x_padre = sucesor
                es_izq_de_padre = False
            else:
                x_padre = sucesor.padre
                es_izq_de_padre = True
                self._trasplantar(sucesor, sucesor.der)
                sucesor.der = nodo_p.der
                sucesor.der.padre = sucesor
            
            self._trasplantar(nodo_p, sucesor)
            sucesor.izq = nodo_p.izq
            sucesor.izq.padre = sucesor
            sucesor.color = nodo_p.color
        
        # Reparar el árbol si se eliminó un nodo negro
        if color_original == "Negro":
            if x is None:
                # Nodo temporal para jugar el rol de NIL
                temp = NodoRB(Prestamo(-1, -1, -1, ""))
                temp.color = "Negro"
                temp.padre = x_padre
                if x_padre is None:
                    self.raiz = temp
                elif es_izq_de_padre:
                    x_padre.izq = temp
                else:
                    x_padre.der = temp
                
                self._reparar_eliminacion(temp)
                
                # Quitar el nodo temporal
                if temp.padre is None:
                    self.raiz = None
                elif temp == temp.padre.izq:
                    temp.padre.izq = None
                else:
                    temp.padre.der = None
            else:
                self._reparar_eliminacion(x)

    def _trasplantar(self, nodo_p: NodoRB, nodo_reemplazo: Optional[NodoRB]) -> None:
        """
        Parámetros: nodo_p (NodoRB) — nodo a ser reemplazado.
                    nodo_reemplazo (Optional[NodoRB]) — nodo que lo reemplaza.
        Devuelve:   None
        Descripción:
            Reemplaza un nodo con otro en el árbol, actualizando referencias de padres.
        """
        if nodo_p.padre is None:
            self.raiz = nodo_reemplazo
        elif nodo_p == nodo_p.padre.izq:
            nodo_p.padre.izq = nodo_reemplazo
        else:
            nodo_p.padre.der = nodo_reemplazo
        
        if nodo_reemplazo is not None:
            nodo_reemplazo.padre = nodo_p.padre

    def _obtener_minimo(self, nodo_p: NodoRB) -> NodoRB:
        """
        Parámetros: nodo_p (NodoRB) — nodo raíz desde el cual buscar.
        Devuelve:   NodoRB — el nodo con el menor valor en el subárbol.
        Descripción:
            Encuentra y retorna el nodo más a la izquierda (con el menor código)
            en un subárbol dado.
        """
        actual = nodo_p
        while actual.izq is not None:
            actual = actual.izq
        return actual

    def _reparar_eliminacion(self, nodo_p: NodoRB) -> None:
        """
        Parámetros: nodo_p (NodoRB) — el nodo donde comenzar la reparación.
        Devuelve:   None
        Descripción:
            Repara las propiedades del árbol Rojinegro después de eliminar un nodo negro.
            Resuelve violaciones de altura negra mediante recoloración y rotaciones.
        """
        actual = nodo_p
        
        while actual != self.raiz and self._obtener_color(actual) == "Negro":
            if actual == actual.padre.izq:
                # actual es hijo izquierdo
                hermano = actual.padre.der
                
                # Caso 1: Hermano es rojo
                if hermano is not None and hermano.color == "Rojo":
                    hermano.color = "Negro"
                    actual.padre.color = "Rojo"
                    self.raiz = self._rotar_izq_interna(self.raiz, actual.padre)
                    hermano = actual.padre.der
                
                # Caso 2: Hermano y sus hijos son negros
                if (hermano is not None and 
                    self._obtener_color(hermano.izq) == "Negro" and 
                    self._obtener_color(hermano.der) == "Negro"):
                    if hermano is not None:
                        hermano.color = "Rojo"
                    actual = actual.padre
                else:
                    # Caso 3: Hermano es negro, hijo izquierdo rojo, hijo derecho negro
                    if hermano is not None:
                        if self._obtener_color(hermano.der) == "Negro":
                            if hermano.izq is not None:
                                hermano.izq.color = "Negro"
                            hermano.color = "Rojo"
                            self.raiz = self._rotar_der_interna(self.raiz, hermano)
                            hermano = actual.padre.der
                        
                        # Caso 4: Hermano es negro, hijo derecho rojo
                        hermano.color = actual.padre.color
                        actual.padre.color = "Negro"
                        if hermano.der is not None:
                            hermano.der.color = "Negro"
                        self.raiz = self._rotar_izq_interna(self.raiz, actual.padre)
                        actual = self.raiz
            else:
                # actual es hijo derecho (simétricamente opuesto)
                hermano = actual.padre.izq
                
                # Caso 1: Hermano es rojo
                if hermano is not None and hermano.color == "Rojo":
                    hermano.color = "Negro"
                    actual.padre.color = "Rojo"
                    self.raiz = self._rotar_der_interna(self.raiz, actual.padre)
                    hermano = actual.padre.izq
                
                # Caso 2: Hermano y sus hijos son negros
                if (hermano is not None and 
                    self._obtener_color(hermano.izq) == "Negro" and 
                    self._obtener_color(hermano.der) == "Negro"):
                    if hermano is not None:
                        hermano.color = "Rojo"
                    actual = actual.padre
                else:
                    # Caso 3: Hermano es negro, hijo derecho rojo, hijo izquierdo negro
                    if hermano is not None:
                        if self._obtener_color(hermano.izq) == "Negro":
                            if hermano.der is not None:
                                hermano.der.color = "Negro"
                            hermano.color = "Rojo"
                            self.raiz = self._rotar_izq_interna(self.raiz, hermano)
                            hermano = actual.padre.izq
                        
                        # Caso 4: Hermano es negro, hijo izquierdo rojo
                        hermano.color = actual.padre.color
                        actual.padre.color = "Negro"
                        if hermano.izq is not None:
                            hermano.izq.color = "Negro"
                        self.raiz = self._rotar_der_interna(self.raiz, actual.padre)
                        actual = self.raiz
        
        actual.color = "Negro"

    def _obtener_color(self, nodo: Optional[NodoRB]) -> str:
        """
        Parámetros: nodo (Optional[NodoRB]) — nodo del cual obtener el color.
        Devuelve:   str — el color del nodo ("Rojo" o "Negro"), "Negro" si es None.
        Descripción:
            Método auxiliar que retorna el color de un nodo. Considera las hojas NIL como negras.
        """
        if nodo is None:
            return "Negro"
        return nodo.color

    # ========== RECORRIDOS ==========

    def inOrden(self, raiz_p: Optional[NodoRB]) -> None:
        """
        Parámetros: raiz_p (Optional[NodoRB]) — nodo inicial para el recorrido.
        Devuelve:   None
        Descripción:
            Recorre el árbol Rojinegro en inorden (izquierda -> nodo -> derecha)
            imprimiendo los códigos de préstamo en orden ascendente.
        """
        if raiz_p is not None:
            self.inOrden(raiz_p.izq)
            
            prestamo = raiz_p.valor
            print(f"Código: {prestamo.codigo_prestamo} | Color: {raiz_p.color} | "
                  f"Libro: {prestamo.codigo_libro} | Estudiante: {prestamo.carnet_estudiante}")
            
            self.inOrden(raiz_p.der)

    def preOrden(self, raiz_p: Optional[NodoRB]) -> None:
        """
        Parámetros: raiz_p (Optional[NodoRB]) — nodo inicial para el recorrido.
        Devuelve:   None
        Descripción:
            Recorre el árbol Rojinegro en preorden (nodo -> izquierda -> derecha),
            mostrando la estructura del árbol y sus colores.
        """
        if raiz_p is not None:
            prestamo = raiz_p.valor
            print(f"Código: {prestamo.codigo_prestamo} | Color: {raiz_p.color} | "
                  f"Libro: {prestamo.codigo_libro} | Estudiante: {prestamo.carnet_estudiante}")
            
            self.preOrden(raiz_p.izq)
            self.preOrden(raiz_p.der)

    def postOrden(self, raiz_p: Optional[NodoRB]) -> None:
        """
        Parámetros: raiz_p (Optional[NodoRB]) — nodo inicial para el recorrido.
        Devuelve:   None
        Descripción:
            Recorre el árbol Rojinegro en postorden (izquierda -> derecha -> nodo),
            útil para operaciones que requieren procesar hijos antes que padres.
        """
        if raiz_p is not None:
            self.postOrden(raiz_p.izq)
            self.postOrden(raiz_p.der)
            
            prestamo = raiz_p.valor
            print(f"Código: {prestamo.codigo_prestamo} | Color: {raiz_p.color} | "
                  f"Libro: {prestamo.codigo_libro} | Estudiante: {prestamo.carnet_estudiante}")

    def obtener_prestamos_inorden(self, raiz_p: Optional[NodoRB]) -> List[Prestamo]:
        """
        Parámetros: raiz_p (Optional[NodoRB]) — nodo raíz del subárbol.
        Devuelve:   List[Prestamo] — lista de préstamos ordenados por código.
        Descripción:
            Recorre el árbol en inorden y retorna una lista de objetos Prestamo.
            Fundamental para que la interfaz gráfica obtenga y muestre los datos.
        """
        if raiz_p is None:
            return []
        
        prestamos = []
        prestamos.extend(self.obtener_prestamos_inorden(raiz_p.izq))
        prestamos.append(raiz_p.valor)
        prestamos.extend(self.obtener_prestamos_inorden(raiz_p.der))
        return prestamos

    # ========== VERIFICACIÓN DE PROPIEDADES RB ==========

    def verificar_propiedades_rb(self) -> dict:
        """
        Parámetros: ninguno
        Devuelve:   dict — diccionario con el estado de cada propiedad RB.
        Descripción:
            Verifica que el árbol cumpla con las 5 propiedades del árbol Rojinegro:
            1. Todo nodo es rojo o negro.
            2. La raíz es negra.
            3. Las hojas NIL son negras (implícito).
            4. Si un nodo es rojo, sus hijos son negros.
            5. Todos los caminos desde un nodo a sus hojas tienen igual altura negra.
            Retorna un diccionario con los resultados de cada verificación.
        """
        resultado = {
            "propiedad_1_colores": self._verificar_colores(self.raiz),
            "propiedad_2_raiz_negra": self._verificar_raiz_negra(),
            "propiedad_4_rojo_hijos_negros": self._verificar_rojo_padre_negro(self.raiz),
            "propiedad_5_altura_negra": self._verificar_altura_negra(self.raiz) >= 0,
            "arbol_valido": True
        }
        
        # Validar que todas las propiedades se cumplan
        if not all([resultado["propiedad_1_colores"], 
                   resultado["propiedad_2_raiz_negra"],
                   resultado["propiedad_4_rojo_hijos_negros"],
                   resultado["propiedad_5_altura_negra"]]):
            resultado["arbol_valido"] = False
        
        return resultado

    def _verificar_colores(self, nodo: Optional[NodoRB]) -> bool:
        """
        Parámetros: nodo (Optional[NodoRB]) — nodo a verificar.
        Devuelve:   bool — True si todos los nodos son rojo o negro.
        Descripción:
            Verifica la propiedad 1: Todo nodo es rojo o negro.
        """
        if nodo is None:
            return True
        
        if nodo.color not in ["Rojo", "Negro"]:
            return False
        
        return (self._verificar_colores(nodo.izq) and 
                self._verificar_colores(nodo.der))

    def _verificar_raiz_negra(self) -> bool:
        """
        Parámetros: ninguno
        Devuelve:   bool — True si la raíz es negra.
        Descripción:
            Verifica la propiedad 2: La raíz es negra.
        """
        if self.raiz is None:
            return True
        return self.raiz.color == "Negro"

    def _verificar_rojo_padre_negro(self, nodo: Optional[NodoRB]) -> bool:
        """
        Parámetros: nodo (Optional[NodoRB]) — nodo a verificar.
        Devuelve:   bool — True si se cumple la propiedad 4.
        Descripción:
            Verifica la propiedad 4: Si un nodo es rojo, sus hijos son negros.
        """
        if nodo is None:
            return True
        
        if nodo.color == "Rojo":
            if nodo.izq is not None and nodo.izq.color == "Rojo":
                return False
            if nodo.der is not None and nodo.der.color == "Rojo":
                return False
        
        return (self._verificar_rojo_padre_negro(nodo.izq) and 
                self._verificar_rojo_padre_negro(nodo.der))

    def _verificar_altura_negra(self, nodo: Optional[NodoRB]) -> int:
        """
        Parámetros: nodo (Optional[NodoRB]) — nodo desde el cual calcular.
        Devuelve:   int — altura negra del subárbol, o -1 si hay violación.
        Descripción:
            Verifica la propiedad 5: Todos los caminos desde un nodo a sus hojas NIL
            contienen el mismo número de nodos negros. Retorna -1 si hay violación.
        """
        if nodo is None:
            return 1  # Las hojas NIL son negras
        
        altura_izq = self._verificar_altura_negra(nodo.izq)
        altura_der = self._verificar_altura_negra(nodo.der)
        
        # Si hay violación en alguno de los subárboles
        if altura_izq == -1 or altura_der == -1:
            return -1
        
        # Si las alturas negras son diferentes
        if altura_izq != altura_der:
            return -1
        
        # Retornar la altura negra aumentada si este nodo es negro
        if nodo.color == "Negro":
            return altura_izq + 1
        else:
            return altura_izq

    def mostrar(self, raiz_p: Optional[NodoRB]) -> None:
        """
        Parámetros: raiz_p (Optional[NodoRB]) — nodo inicial para mostrar.
        Devuelve:   None
        Descripción:
            Muestra el árbol en preorden para debug, mostrando códigos y colores.
        """
        if raiz_p is not None:
            prestamo = raiz_p.valor
            print(f"[{prestamo.codigo_prestamo}({raiz_p.color[0]})]", end=" ")
            
            self.mostrar(raiz_p.izq)
            self.mostrar(raiz_p.der)

    def esta_vacio(self) -> bool:
        """
        Parámetros: ninguno
        Devuelve:   bool — True si el árbol está vacío, False en caso contrario.
        Descripción:
            Verifica si el árbol Rojinegro está vacío (sin nodos).
        """
        return self.raiz is None
