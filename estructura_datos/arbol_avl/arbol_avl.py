"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
Archivo: arbol_avl.py
"""

from typing import Optional

from clases.libro import Libro
from estructura_datos.arbol_avl.nodo import Nodo


class ArbolAVL:
    """
    Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
    Descripción: 
        Clase principal que maneja un 'Árbol AVL'. Imagínatelo como un archivero
        muy inteligente que guarda los libros ordenados por su código, y además
        se acomoda solito para que las búsquedas sean siempre súper rápidas 
        (esto es lo que significa 'balanceado').
    """

    def __init__(self) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: ninguno
        Devuelve:   None
        Descripción:
            Constructor. Inicia nuestro "archivero" completamente vacío (sin libros).
        """
        # La raíz es el punto de inicio del árbol (el estante más alto). Empieza vacío (None).
        self.raiz: Optional[Nodo] = None

    def _altura(self, raiz_p: Optional[Nodo]) -> int:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: 
            raiz_p (Optional[Nodo]): El nodo (o caja) desde donde queremos empezar a medir.
        Devuelve:   
            int: La altura (cantidad de niveles) que tiene esa parte del árbol.
        Descripción:
            Calcula qué tan profundo o alto es una rama del árbol. 
            Si no hay nodo (None), la altura es 0.
        """
        # Si llegamos al final de la rama (vacío), la altura es cero
        if raiz_p is None:
            return 0

        # Preguntamos recursivamente (una y otra vez hacia abajo) la altura de la rama izquierda y derecha
        altura_izq: int = self._altura(raiz_p.izq)
        altura_der: int = self._altura(raiz_p.der)

        # Nos quedamos con la altura de la rama más larga y le sumamos 1 (por el nodo en el que estamos)
        if altura_izq > altura_der:
            return altura_izq + 1
        else:
            return altura_der + 1

    def calcular_fe(self, raiz_p: Optional[Nodo]) -> int:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: 
            raiz_p (Optional[Nodo]): El nodo al que le queremos revisar el balance.
        Devuelve:   
            int: El número que nos dice hacia dónde se inclina el árbol (Factor de Equilibrio).
        Descripción:
            Mide si la rama derecha pesa (mide) más que la izquierda, o al revés.
            Si el resultado es negativo, pesa más a la izquierda. Si es positivo, a la derecha.
            Idealmente debe dar -1, 0, o 1.
        """
        # Si no hay nodo, está en perfecto equilibrio (0)
        if raiz_p is None:
            return 0
        # Fórmula: Altura del lado derecho MENOS Altura del lado izquierdo
        return self._altura(raiz_p.der) - self._altura(raiz_p.izq)

    def insertar(self, raiz_p: Optional[Nodo], libro_nuevo: Libro) -> Nodo:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: 
            raiz_p (Optional[Nodo]): El nodo donde estamos revisando actualmente para meter el libro.
            libro_nuevo (Libro): El libro que queremos guardar en el árbol.
        Devuelve:   
            Nodo: El nodo que quedó en ese lugar (puede ser el mismo, o uno nuevo acomodado).
        Descripción:
            Agrega un libro nuevo al archivero buscando el lugar correcto según su código.
            Después de meterlo, revisa si el estante se desbalanceó y lo arregla si es necesario.
        """
        # Si encontramos un espacio vacío, ¡aquí metemos el libro nuevo creando un Nodo!
        if raiz_p is None:
            return Nodo(libro_nuevo)

        # Si el código del libro es MENOR, nos vamos por el lado IZQUIERDO
        if libro_nuevo.codigo < raiz_p.valor.codigo:
            raiz_p.izq = self.insertar(raiz_p.izq, libro_nuevo)
        # Si el código del libro es MAYOR, nos vamos por el lado DERECHO
        elif libro_nuevo.codigo > raiz_p.valor.codigo:
            raiz_p.der = self.insertar(raiz_p.der, libro_nuevo)
        else:
            # Si el código es IGUAL, el libro ya existe, no hacemos nada (evitamos duplicados)
            return raiz_p

        # Paso 1: Actualizamos la medida de inclinación (Factor de Equilibrio) de este nodo
        raiz_p.fe = self.calcular_fe(raiz_p)

        # Paso 2: Revisamos si está muy inclinado a la IZQUIERDA (factor de -2)
        if raiz_p.fe == -2:
            # Si el hijo izquierdo también tira a la izquierda o está balanceado...
            if self.calcular_fe(raiz_p.izq) <= 0:
                # Hacemos una rotación simple para arreglarlo
                return self.rotacion_ii(raiz_p)
            else:
                # Si es un caso cruzado (el hijo tira a la derecha), hacemos rotación doble
                return self.rotacion_id(raiz_p)

        # Paso 3: Revisamos si está muy inclinado a la DERECHA (factor de 2)
        if raiz_p.fe == 2:
            # Si el hijo derecho también tira a la derecha o está balanceado...
            if self.calcular_fe(raiz_p.der) >= 0:
                # Hacemos rotación simple
                return self.rotacion_dd(raiz_p)
            else:
                # Si es cruzado, hacemos rotación doble
                return self.rotacion_di(raiz_p)

        # Si todo está bien y balanceado, devolvemos el nodo como quedó
        return raiz_p

    def rotacion_ii(self, raiz_p: Nodo) -> Nodo:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: 
            raiz_p (Nodo): El nodo que está chueco y necesita arreglo.
        Devuelve:   
            Nodo: El nuevo nodo que quedó arriba (el nuevo "jefe" de esta parte).
        Descripción:
            (Rotación Izquierda-Izquierda) Cuando hay mucho peso a la izquierda en línea recta,
            giramos todo hacia la derecha para volver a equilibrarlo, como un sube y baja.
        """
        # Guardamos al hijo izquierdo, porque él será el nuevo "jefe" o raíz
        actual = raiz_p.izq
        # Guardamos lo que sea que tuviera el hijo a su derecha
        hijo = actual.der

        # Hacemos el giro: el hijo izquierdo (actual) sube, y el papá (raiz_p) baja a su derecha
        actual.der = raiz_p
        raiz_p.izq = hijo

        # Como se movieron, tenemos que volver a calcularles su inclinación
        raiz_p.fe = self.calcular_fe(raiz_p)
        actual.fe = self.calcular_fe(actual)
        
        # Devolvemos al nuevo nodo "jefe"
        return actual

    def rotacion_dd(self, raiz_p: Nodo) -> Nodo:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: 
            raiz_p (Nodo): El nodo desbalanceado.
        Devuelve:   
            Nodo: El nuevo nodo que queda arriba.
        Descripción:
            (Rotación Derecha-Derecha) Cuando hay mucho peso a la derecha en línea recta,
            giramos todo hacia la izquierda para que no se caiga. Es el espejo del anterior.
        """
        # Guardamos al hijo derecho, él subirá
        actual = raiz_p.der
        # Guardamos el lado izquierdo del hijo
        hijo = actual.izq

        # El giro: el papá baja a la izquierda, y el hijo toma su lugar arriba
        actual.izq = raiz_p
        raiz_p.der = hijo

        # Recalculamos la inclinación de ambos
        raiz_p.fe = self.calcular_fe(raiz_p)
        actual.fe = self.calcular_fe(actual)
        
        return actual

    def rotacion_id(self, raiz_p: Nodo) -> Nodo:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: 
            raiz_p (Nodo): El nodo desbalanceado.
        Devuelve:   
            Nodo: El nuevo nodo raíz de esta zona.
        Descripción:
            (Rotación Izquierda-Derecha) El árbol tiene forma de "zig-zag" (cayendo izq, luego der).
            Solución: Primero enderezamos la "rodilla" (hijo izquierdo) y luego giramos todo.
        """
        # Primero giramos al hijo izquierdo para enderezar el zig-zag
        raiz_p.izq = self.rotacion_dd(raiz_p.izq)
        # Ahora que está recto como una vara a la izquierda, usamos la rotación normal
        return self.rotacion_ii(raiz_p)

    def rotacion_di(self, raiz_p: Nodo) -> Nodo:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: 
            raiz_p (Nodo): El nodo desbalanceado.
        Devuelve:   
            Nodo: El nuevo nodo raíz de esta zona.
        Descripción:
            (Rotación Derecha-Izquierda) El árbol hace "zig-zag" hacia el otro lado.
            Es lo mismo pero al revés: enderezamos el hijo derecho y luego giramos todo.
        """
        # Enderezamos el hijo derecho
        raiz_p.der = self.rotacion_ii(raiz_p.der)
        # Hacemos la rotación normal hacia la izquierda
        return self.rotacion_dd(raiz_p)

    def buscar_codigo(self, raiz_p: Optional[Nodo], codigo: int) -> Optional[Libro]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: 
            raiz_p (Optional[Nodo]): El nodo por el que vamos buscando.
            codigo (int): El número de código del libro que queremos encontrar.
        Devuelve:   
            Optional[Libro]: El libro si lo encontramos, o 'None' (nada) si no existe.
        Descripción:
            Busca un libro súper rápido yendo por el camino correcto (derecha o izquierda) 
            según si el código buscado es mayor o menor que donde estamos.
        """
        # Si llegamos a un lugar vacío, el libro definitivamente no está
        if raiz_p is None:
            return None
        # ¡Bingo! Lo encontramos, devolvemos el libro
        elif raiz_p.valor.codigo == codigo:
            return raiz_p.valor
        # Si el código es MENOR, descartamos la mitad del árbol y nos vamos por la izquierda
        elif raiz_p.valor.codigo > codigo:
            return self.buscar_codigo(raiz_p.izq, codigo)
        # Si el código es MAYOR, descartamos la otra mitad y nos vamos por la derecha
        else:
            return self.buscar_codigo(raiz_p.der, codigo)

    def buscar_titulo(self, raiz_p: Optional[Nodo], titulo: str) -> Optional[Libro]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: 
            raiz_p (Optional[Nodo]): El nodo actual.
            titulo (str): El nombre del libro que queremos.
        Devuelve:   
            Optional[Libro]: El libro si lo encuentra, o None.
        Descripción:
            Como el árbol está ordenado por código y no por título, nos toca buscar "a pie"
            nodo por nodo (recorrido inorden) hasta toparnos con el título correcto.
        """
        # Si caemos en el vacío, no hay nada
        if raiz_p is None:
            return None

        # 1. Buscamos primero en toda la rama izquierda
        libro_izq = self.buscar_titulo(raiz_p.izq, titulo)
        # Si lo encontramos por ahí, lo devolvemos y dejamos de buscar
        if libro_izq is not None:
            return libro_izq

        # 2. Si no estaba a la izquierda, revisamos el nodo en el que estamos parados
        if raiz_p.valor.titulo == titulo:
            return raiz_p.valor

        # 3. Si tampoco es este, el último remedio es buscar por toda la rama derecha
        return self.buscar_titulo(raiz_p.der, titulo)

    def buscar_autor(self, raiz_p: Optional[Nodo], autor: str) -> list[Libro]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: 
            raiz_p (Optional[Nodo]): Nodo actual.
            autor (str): El nombre del autor del que queremos los libros.
        Devuelve:   
            list[Libro]: Una lista (como una bolsa) con todos los libros de ese autor.
        Descripción:
            Busca todos los libros escritos por una persona, recorriendo absolutamente 
            todo el árbol, porque un autor puede tener varios libros escondidos por ahí.
        """
        # Si estamos en un callejón sin salida, devolvemos una lista vacía
        if raiz_p is None:
            return []

        # 1. Recogemos en una lista todos los libros del autor que estén a la izquierda
        libros = self.buscar_autor(raiz_p.izq, autor)

        # 2. Revisamos nuestro nodo actual: si es del autor, ¡a la bolsa!
        if raiz_p.valor.autor == autor:
            libros.append(raiz_p.valor)

        # 3. Vamos a la rama derecha, buscamos, y lo que encontremos lo agregamos a nuestra bolsa
        libros.extend(self.buscar_autor(raiz_p.der, autor))

        return libros

    # mostrar_inorden
    def obtener_libros_inorden(self, raiz_p: Optional[Nodo]) -> list[Libro]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: 
            raiz_p (Optional[Nodo]): Nodo raíz por el que empezamos.
        Devuelve:   
            list[Libro]: Una lista de libros perfectamente ordenados del menor código al mayor.
        Descripción:
            Extrae TODOS los libros del árbol y los mete en una lista, pero lo hace 
            visitando primero la izquierda, luego el centro y luego la derecha.
            Esto mágicamente nos da los libros ordenados (Recorrido Inorden).
        """
        # Caso base: si está vacío, devolvemos lista vacía
        if raiz_p is None:
            return []

        libros = []
        # Obtenemos los menores (izquierda) y los metemos a la lista
        libros.extend(self.obtener_libros_inorden(raiz_p.izq))
        # Metemos el del medio (nodo actual)
        libros.append(raiz_p.valor)
        # Obtenemos los mayores (derecha) y los metemos a la lista
        libros.extend(self.obtener_libros_inorden(raiz_p.der))
        
        # Devolvemos la lista ya ordenadita
        return libros


    def _get_min_valor_nodo(self, nodo: Nodo) -> Nodo:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: 
            nodo (Nodo): Desde dónde empezamos a buscar.
        Devuelve:   
            Nodo: La "caja" que tiene el libro con el código numérico más chiquito.
        Descripción:
            En un árbol de este tipo, el número más pequeño SIEMPRE está yéndose a la 
            izquierda todo lo que se pueda. Esta función hace exactamente eso.
        """
        # Si no hay nodo, o ya no podemos ir más a la izquierda, ¡llegamos al mínimo!
        if nodo is None or nodo.izq is None:
            return nodo
        # Si podemos seguir a la izquierda, seguimos bajando
        return self._get_min_valor_nodo(nodo.izq)

    def eliminar_codigo(self, raiz_p: Optional[Nodo], codigo: int) -> Optional[Nodo]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: 
            raiz_p (Optional[Nodo]): El nodo donde estamos buscando para borrar.
            codigo (int): El número de código del libro a eliminar.
        Devuelve:   
            Optional[Nodo]: El árbol (la raíz) como quedó después de borrar y balancear.
        Descripción:
            Busca un libro, lo saca del árbol, y si por sacarlo el árbol queda cojo,
            hace malabares (rotaciones) para volver a dejarlo bien paradito.
        """
        # Si llegamos a la nada, significa que el libro ni siquiera existía
        if raiz_p is None:
            return None

        # PASO 1: Buscar al condenado libro
        # Si el código es menor, lo mandamos a buscar a la izquierda
        if codigo < raiz_p.valor.codigo:
            raiz_p.izq = self.eliminar_codigo(raiz_p.izq, codigo)
        # Si es mayor, a la derecha
        elif codigo > raiz_p.valor.codigo:
            raiz_p.der = self.eliminar_codigo(raiz_p.der, codigo)
        else:
            # ¡Lo encontramos! (raiz_p es el nodo a borrar)
            
            # Caso A: No tiene hijo izquierdo (solo tiene el derecho, o no tiene hijos)
            if raiz_p.izq is None:
                temp = raiz_p.der  # Rescatamos al hijo derecho
                raiz_p = None      # Borramos el nodo actual
                return temp        # Y ponemos al hijo en su lugar
            
            # Caso B: No tiene hijo derecho (solo tiene izquierdo)
            elif raiz_p.der is None:
                temp = raiz_p.izq  # Rescatamos al hijo izquierdo
                raiz_p = None      # Borramos el nodo actual
                return temp        # Y lo ponemos en su lugar

            # Caso C: ¡Tiene dos hijos! Es el caso complicado.
            # 1. Buscamos al "sucesor": el más pequeño de los mayores (el que esté más a la izq en la rama der)
            temp = self._get_min_valor_nodo(raiz_p.der)
            
            # 2. Le copiamos el valor del sucesor al nodo actual (es como si lo hubiéramos reemplazado)
            raiz_p.valor = temp.valor
            
            # 3. Ahora vamos a la rama derecha y le decimos que borre al sucesor original (porque ya lo copiamos aquí)
            raiz_p.der = self.eliminar_codigo(raiz_p.der, temp.valor.codigo)

        # Si tras borrar resulta que el árbol quedó completamente vacío, terminamos
        if raiz_p is None:
            return raiz_p

        # PASO 2: Recalcular la inclinación (Factor de Equilibrio)
        raiz_p.fe = self.calcular_fe(raiz_p)

        # PASO 3: Revisar si el árbol quedó chueco y hacer los "trucos" para arreglarlo
        
        # Si se inclinó mucho a la izquierda...
        if raiz_p.fe == -2:
            if self.calcular_fe(raiz_p.izq) <= 0:
                return self.rotacion_ii(raiz_p)
            else:
                return self.rotacion_id(raiz_p)

        # Si se inclinó mucho a la derecha...
        if raiz_p.fe == 2:
            if self.calcular_fe(raiz_p.der) >= 0:
                return self.rotacion_dd(raiz_p)
            else:
                return self.rotacion_di(raiz_p)

        # Devolvemos el árbol ya podado y balanceado
        return raiz_p
