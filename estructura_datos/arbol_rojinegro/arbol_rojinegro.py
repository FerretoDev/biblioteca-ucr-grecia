"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
Archivo: arbol_rojinegro.py
"""

from typing import List, Optional
from clases.prestamo import Prestamo
from estructura_datos.arbol_rojinegro.nodo import Nodo

class ArbolRojinegro:
    """
    Clase que representa un Árbol Rojinegro.
    Este árbol guarda los préstamos de la biblioteca ordenados por su código.
    Su característica principal es que se "balancea" (se acomoda) automáticamente 
    cada vez que agregamos o quitamos un préstamo, asegurando que las búsquedas 
    sean siempre súper rápidas.
    """
    def __init__(self) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Constructor del Árbol Rojinegro.
        Inicializa el árbol vacío, por lo que la raíz (el nodo principal) es nula (None).
        """
        self.raiz: Optional[Nodo] = None

    def esta_vacia(self) -> bool:
        """
        Verifica si el árbol no tiene ningún préstamo.
        Retorna True (verdadero) si está vacío, False (falso) si tiene al menos uno.
        """
        return self.raiz is None

    def buscar_codigo(self, raiz_p: Optional[Nodo], codigo_prestamo: int) -> Optional[Prestamo]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Busca un préstamo específico usando su código numérico.
        
        Parámetros:
        raiz_p (Nodo): Desde qué nodo empezamos a buscar (usualmente la raíz).
        codigo_prestamo (int): El número de código que queremos encontrar.
        
        Devuelve:
        Prestamo si lo encuentra, o None si no existe.
        """
        # Llamamos a una función interna auxiliar para encontrar el nodo
        nodo = self._buscar_nodo(raiz_p, codigo_prestamo)
        
        # Si encontró el nodo, devuelve el préstamo guardado adentro; sino, devuelve None
        return nodo.valor if nodo is not None else None

    def _buscar_nodo(self, raiz_p: Optional[Nodo], codigo_prestamo: int) -> Optional[Nodo]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Función interna (privada) que hace el trabajo pesado de buscar el nodo en el árbol.
        Navega por las ramas preguntando: "¿es mayor o menor?".
        """
        # Si llegamos a un nodo vacío, significa que el código no está en el árbol
        if raiz_p is None:
            return None
            
        # Si el código del nodo actual es exactamente el que buscamos, ¡Lo encontramos!
        if codigo_prestamo == raiz_p.valor.codigo_prestamo:
            return raiz_p
            
        # Si el código que buscamos es MENOR, bajamos por la rama izquierda
        elif codigo_prestamo < raiz_p.valor.codigo_prestamo:
            return self._buscar_nodo(raiz_p.izq, codigo_prestamo)
            
        # Si es MAYOR, bajamos por la rama derecha
        else:
            return self._buscar_nodo(raiz_p.der, codigo_prestamo)

    def rotacion_ii(self, raiz_p: Nodo) -> Nodo:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Realiza una rotación en el árbol para reacomodarlo.
        Se usa cuando el árbol se desbalancea (una rama crece más que la otra).
        Mueve los nodos como en un rompecabezas para mantenerlo rápido.
        """
        nuevo_raiz = raiz_p.izq
        raiz_p.izq = nuevo_raiz.der
        
        # Reconecta al hijo derecho del nuevo nodo raíz con el padre viejo
        if nuevo_raiz.der is not None:
            nuevo_raiz.der.padre = raiz_p
        
        # Conecta el nuevo nodo raíz con su abuelo
        nuevo_raiz.padre = raiz_p.padre
        
        # Si resulta que estábamos rotando la mismísima punta del árbol
        if raiz_p.padre is None:
            self.raiz = nuevo_raiz
        elif raiz_p == raiz_p.padre.izq:
            raiz_p.padre.izq = nuevo_raiz
        else:
            raiz_p.padre.der = nuevo_raiz
            
        # Termina de acomodar la rotación conectándolos entre sí
        nuevo_raiz.der = raiz_p
        raiz_p.padre = nuevo_raiz
        
        return nuevo_raiz

    def rotacion_dd(self, raiz_p: Nodo) -> Nodo:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Realiza otra rotación en el árbol (hacia el otro lado) para reacomodarlo.
        Sirve para el mismo propósito de balanceo, pero como un espejo.
        """
        nuevo_raiz = raiz_p.der
        raiz_p.der = nuevo_raiz.izq
        
        # Reconecta partes
        if nuevo_raiz.izq is not None:
            nuevo_raiz.izq.padre = raiz_p
            
        nuevo_raiz.padre = raiz_p.padre
        
        # Si rotamos en la punta
        if raiz_p.padre is None:
            self.raiz = nuevo_raiz
        elif raiz_p == raiz_p.padre.izq:
            raiz_p.padre.izq = nuevo_raiz
        else:
            raiz_p.padre.der = nuevo_raiz
            
        # Terminamos de entrelazarlos
        nuevo_raiz.izq = raiz_p
        raiz_p.padre = nuevo_raiz
        
        return nuevo_raiz

    def insertar(self, raiz_p: Optional[Nodo], prestamo_nuevo: Prestamo) -> Optional[Nodo]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Inserta un nuevo préstamo en el árbol rojinegro.
        Primero busca dónde debe ir (como un árbol binario normal) y luego 
        revisa los colores para asegurar que siga balanceado.
        """
        nuevo_nodo = Nodo(prestamo_nuevo)
        
        # Si el árbol está vacío, este será el primero (la raíz).
        # REGLA: La raíz de todo el árbol siempre tiene que ser de color Negro.
        if self.raiz is None:
            self.raiz = nuevo_nodo
            self.raiz.color = "Negro"
            return self.raiz

        if raiz_p is None:
            return None

        # Si el código es MENOR, debemos colocarlo a la IZQUIERDA
        if prestamo_nuevo.codigo_prestamo < raiz_p.valor.codigo_prestamo:
            # Si el lado izquierdo está vacío, lo colocamos ahí mismo
            if raiz_p.izq is None:
                nuevo_nodo.padre = raiz_p
                raiz_p.izq = nuevo_nodo

                # REGLA: No podemos tener un nodo Rojo pegado a un padre Rojo.
                # Si pasa eso, llamamos a 'cambio_color' para que lo repare.
                if raiz_p.color == "Rojo":
                    self.cambio_color(nuevo_nodo)

                return nuevo_nodo

            # Si el lado izquierdo ya está ocupado, seguimos bajando recursivamente
            return self.insertar(raiz_p.izq, prestamo_nuevo)

        # Si el código es MAYOR, debemos colocarlo a la DERECHA
        if prestamo_nuevo.codigo_prestamo > raiz_p.valor.codigo_prestamo:
            # Si el lado derecho está vacío, lo ponemos ahí
            if raiz_p.der is None:
                nuevo_nodo.padre = raiz_p
                raiz_p.der = nuevo_nodo

                # Chequeamos los colores por si hay dos Rojos juntos
                if raiz_p.color == "Rojo":
                    self.cambio_color(nuevo_nodo)

                return nuevo_nodo

            # Seguimos bajando por la derecha
            return self.insertar(raiz_p.der, prestamo_nuevo)

        # Si los códigos son iguales, no lo insertamos para evitar duplicados
        return raiz_p

    def cambio_color(self, hijo: Nodo) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Función que 'salva' el árbol cuando al insertar se rompe la regla de los colores
        (es decir, cuando un nodo Rojo quedó con un padre Rojo). 
        Usa 'tíos' y 'abuelos' para decidir si pintar nodos o hacer rotaciones.
        """
        # Mientras haya un problema (yo Rojo y mi padre Rojo)...
        while hijo != self.raiz and hijo.padre is not None and hijo.padre.color == "Rojo":
            actual = hijo.padre   # 'actual' es mi padre
            padre = actual.padre  # 'padre' es mi abuelo

            if padre is None:
                break

            # 1. Buscamos quién es el hermano de mi padre (mi Tío)
            if padre.izq == actual:
                hermano = padre.der # Mi tío está a la derecha
            else:
                hermano = padre.izq # Mi tío está a la izquierda

            # 2. CASO 1: Si mi Tío es Rojo (¡Es el caso más fácil!)
            if hermano is not None and hermano.color == "Rojo":
                # Solución: Pintamos a mi padre y a mi tío de Negro, y a mi abuelo de Rojo.
                actual.color = "Negro"
                hermano.color = "Negro"
                
                if padre == self.raiz:
                    padre.color = "Negro" # La raíz no puede ser Roja
                else:
                    padre.color = "Rojo"
                    
                # Subimos para ver si al pintar al abuelo de Rojo no arruinamos nada arriba
                hijo = padre
            else:
                # 3. CASOS 2 y 3: Mi Tío es Negro (o no existe). Esto requiere rotaciones.
                if padre.izq == actual:
                    # --- Mi padre está del lado Izquierdo ---
                    if hijo == actual.der:
                        # Hacemos un giro inicial si estamos en 'zig-zag'
                        hijo = actual
                        self.rotacion_dd(hijo)
                        actual = hijo.padre
                        padre = actual.padre
                    
                    # Pintamos y hacemos la rotación final para arreglarlo
                    actual.color = "Negro"
                    padre.color = "Rojo"
                    self.rotacion_ii(padre)
                else:
                    # --- Mi padre está del lado Derecho ---
                    if hijo == actual.izq:
                        # Giro inicial si estamos en 'zig-zag' al revés
                        hijo = actual
                        self.rotacion_ii(hijo)
                        actual = hijo.padre
                        padre = actual.padre
                        
                    # Pintamos y hacemos la rotación final
                    actual.color = "Negro"
                    padre.color = "Rojo"
                    self.rotacion_dd(padre)
                    
        # IMPORTANTE: Al final de cualquier relajo, la raíz de todo siempre termina Negra
        self.raiz.color = "Negro"

    def eliminar_codigo(self, raiz_p: Optional[Nodo], codigo_prestamo: int) -> Optional[Nodo]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Busca y elimina un préstamo del árbol según su código.
        Al igual que al insertar, primero lo elimina como en un árbol binario normal,
        y luego llama a una función reparadora si la eliminación arruinó el balance.
        """
        if raiz_p is None:
            return None

        # Buscamos el nodo navegando por izquierda o derecha
        if codigo_prestamo < raiz_p.valor.codigo_prestamo:
            self.eliminar_codigo(raiz_p.izq, codigo_prestamo)
        elif codigo_prestamo > raiz_p.valor.codigo_prestamo:
            self.eliminar_codigo(raiz_p.der, codigo_prestamo)

        else:
            # ¡Lo encontramos! Ahora a ver cómo lo borramos.
            if raiz_p.izq is not None and raiz_p.der is not None:
                # CASO DIFÍCIL: Tiene 2 hijos. 
                # Buscamos al sucesor (el más pequeño de los mayores) para que tome su lugar.
                temp = self._get_min_valor_nodo(raiz_p.der)
                raiz_p.valor = temp.valor
                # Ahora borramos al sucesor de su antigua posición
                self.eliminar_codigo(raiz_p.der, temp.valor.codigo_prestamo)
            else:
                # CASOS FÁCILES: Tiene 0 o 1 hijo
                color_original = raiz_p.color
                # 'actual' será el hijo que sube a reemplazar al borrado (o None si no hay)
                actual = raiz_p.izq if raiz_p.izq is not None else raiz_p.der
                padre = raiz_p.padre
                es_izq_de_padre = (padre is not None and raiz_p == padre.izq)

                if actual is None:
                    # CASO 0 HIJOS (es una hoja). 
                    # Usamos un nodo temporal "NIL" (invisible) para mantener la lógica de colores
                    actual = Nodo(Prestamo(-1, -1, -1, "")) 
                    actual.color = "Negro"
                    actual.padre = padre
                    
                    if padre is None:
                        self.raiz = actual
                    elif es_izq_de_padre:
                        padre.izq = actual
                    else:
                        padre.der = actual
                    
                    # Si borramos un nodo Negro, se altera el balance de caminos negros. Hay que reparar.
                    if color_original == "Negro":
                        self._reparar_eliminacion(actual)
                    
                    # Ya reparamos, ahora removemos el nodo temporal invisible
                    if actual.padre is None:
                        self.raiz = None
                    elif actual.padre.izq == actual:
                        actual.padre.izq = None
                    else:
                        actual.padre.der = None
                else:
                    # CASO 1 HIJO: El hijo sube y toma su lugar.
                    actual.padre = padre
                    if padre is None:
                        self.raiz = actual
                    elif es_izq_de_padre:
                        padre.izq = actual
                    else:
                        padre.der = actual

                    # Si borramos un Negro, hay que reparar la regla de los caminos negros
                    if color_original == "Negro":
                        self._reparar_eliminacion(actual)
                        
        return self.raiz

    def _get_min_valor_nodo(self, raiz_p: Nodo) -> Nodo:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Encuentra el nodo con el valor más pequeño a partir de un punto.
        Como los menores siempre van a la izquierda, basta con bajar 
        todo lo posible por la izquierda.
        """
        actual = raiz_p
        while actual.izq is not None:
            actual = actual.izq
        return actual
    def _reparar_eliminacion(self, actual: Nodo) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Se llama cuando al borrar un nodo Negro, una de las ramas queda con 
        "menos peso Negro" que las demás. Esta función pide prestado "peso" 
        a los hermanos (tíos) y hace rotaciones para equilibrar todo de nuevo.
        """
        # Mientras no estemos en la raíz y sigamos teniendo un "peso faltante" (nodo Negro)
        while actual != self.raiz and (actual is None or actual.color == "Negro"):
            padre = actual.padre
            
            # 1. Identificamos a nuestro hermano para pedirle ayuda
            es_hijo_izq = (actual == padre.izq)
            hermano = padre.der if es_hijo_izq else padre.izq
            
            # 2. CASO 1: Nuestro hermano es Rojo
            if hermano is not None and hermano.color == "Rojo":
                # Le robamos el color y rotamos para cambiar la estructura y caer en los otros casos
                hermano.color = "Negro"
                padre.color = "Rojo"
                if es_hijo_izq:
                    self.rotacion_dd(padre)
                    hermano = padre.der
                else:
                    self.rotacion_ii(padre)
                    hermano = padre.izq
                    
            # 3. CASO 2: Hermano es Negro y sus dos hijos (sobrinos) también son Negros
            if (hermano is not None and 
                (hermano.izq is None or hermano.izq.color == "Negro") and 
                (hermano.der is None or hermano.der.color == "Negro")):
                
                # Le quitamos el color Negro al hermano, y le pasamos el problema a nuestro padre
                hermano.color = "Rojo"
                actual = padre
                
            # 4. CASOS 3 y 4: Hermano es Negro, pero tiene al menos un sobrino Rojo que nos puede salvar
            else:
                if hermano is not None:
                    if es_hijo_izq:
                        # --- Resolviendo por la izquierda ---
                        # Si el sobrino derecho es Negro (y el izquierdo Rojo), ajustamos con un giro
                        if (hermano.der is None or hermano.der.color == "Negro"):
                            if hermano.izq is not None:
                                hermano.izq.color = "Negro"
                            hermano.color = "Rojo"
                            self.rotacion_ii(hermano)
                            hermano = padre.der
                            
                        # El sobrino derecho es Rojo: nos cede su color y giramos para balancear
                        hermano.color = padre.color
                        padre.color = "Negro"
                        if hermano.der is not None:
                            hermano.der.color = "Negro"
                        self.rotacion_dd(padre)
                        actual = self.raiz # ¡Problema resuelto!
                    else:
                        # --- Resolviendo por la derecha (espejo) ---
                        # Si el sobrino izquierdo es Negro, ajustamos
                        if (hermano.izq is None or hermano.izq.color == "Negro"):
                            if hermano.der is not None:
                                hermano.der.color = "Negro"
                            hermano.color = "Rojo"
                            self.rotacion_dd(hermano)
                            hermano = padre.izq
                            
                        # El sobrino izquierdo es Rojo, nos salva
                        hermano.color = padre.color
                        padre.color = "Negro"
                        if hermano.izq is not None:
                            hermano.izq.color = "Negro"
                        self.rotacion_ii(padre)
                        actual = self.raiz # ¡Problema resuelto!
                        
        # Al final, el nodo que subió queda Negro para compensar
        if actual is not None:
            actual.color = "Negro"
    def inorden(self, raiz_p: Optional[Nodo], lista: Optional[List[Prestamo]] = None) -> List[Prestamo]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Recorre todo el árbol para recolectar todos los préstamos.
        Como es un recorrido 'In-Orden' (Izquierda -> Centro -> Derecha),
        nos garantiza devolver la lista de préstamos ORDENADA por código, 
        de menor a mayor.
        """
        if lista is None:
            lista = []
            
        if raiz_p is not None:
            # Primero va por los más pequeños (Izquierda)
            self.inorden(raiz_p.izq, lista)
            
            # Luego guarda el actual (Centro)
            lista.append(raiz_p.valor)
            
            # Y al final va por los más grandes (Derecha)
            self.inorden(raiz_p.der, lista)
            
        return lista
