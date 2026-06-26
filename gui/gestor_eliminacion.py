"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
Archivo: gestor_eliminacion.py
"""

from typing import Tuple

from estructura_datos.arbol_avl.arbol_avl import ArbolAVL
from estructura_datos.tabla_hash.tabla_hash import TablaHash
from gui.sistema_prestamos import SistemaPrestamos
from gui.xml_manager import XMLManager


class GestorEliminacion:
    """
    Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
    Propósito: Clase que administra las reglas especiales al momento de intentar eliminar un estudiante o un libro.
               Funciona como un policía: no te deja eliminar cosas si tienen alguna cuenta o préstamo pendiente.
    """
    def __init__(
        self,
        avl: ArbolAVL,
        tabla_hash: TablaHash,
        sistema_prestamos: SistemaPrestamos,
        xml_manager: XMLManager,
    ) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Inicializar el gestor conectándolo a las diferentes estructuras de datos del programa.
        Parámetros: 
            avl (ArbolAVL) - Árbol principal que guarda todos los libros disponibles.
            tabla_hash (TablaHash) - El diccionario/tabla de todos los estudiantes registrados.
            sistema_prestamos (SistemaPrestamos) - El cerebro que maneja quién tiene libros prestados.
            xml_manager (XMLManager) - Herramienta para guardar en disco cualquier cambio tras borrar algo.
        Devuelve:   None
        Descripción:
            Asigna las herramientas externas a variables internas de la clase (self) para que podamos
            accederlas fácilmente más adelante al momento de hacer las eliminaciones.
        """
        # Guardamos en variables internas quién es quién
        self.avl = avl
        self.tabla_hash = tabla_hash
        self.sistema_prestamos = sistema_prestamos
        self.xml_manager = xml_manager

    # ----------------------------------------------------------
    # LIBROS
    # ----------------------------------------------------------

    def eliminar_libro(self, codigo: int) -> Tuple[bool, str]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Tratar de eliminar un libro del sistema de forma segura, verificando que nadie lo tenga prestado.
        Parámetros: codigo (int) — El código numérico único del libro a borrar.
        Devuelve:   Tuple[bool, str] — Pareja: (Verdadero o Falso sobre el éxito, Mensaje explicativo para mostrar).
        Descripción:
            Sigue una receta muy estricta:
              1. Ve que el libro sea real y esté en la base.
              2. Comprueba que el libro no esté volando en un préstamo.
              3. Recorta el libro del árbol AVL de memoria.
              4. Salva la información final en el archivo de texto.
        """
        # 1. Verificar que el libro existe
        # Buscamos en el árbol de libros (AVL) a ver si existe el que queremos borrar
        libro = self.avl.buscar_codigo(self.avl.raiz, codigo)
        # Si la búsqueda devuelve None, significa que ese libro ni siquiera está registrado
        if libro is None:
            return False, f"El libro {codigo} no existe en el sistema."

        # 2. Verificar que el libro no esté prestado
        # Le preguntamos al sistema de préstamos si alguien anda con ese libro en sus manos
        if self.sistema_prestamos.libro_esta_prestado(codigo):
            # No podemos borrar de la base un libro que físicamente alguien tiene, así que abortamos
            return False, "No se puede eliminar el libro: esta prestado."

        # 3. Eliminar del AVL
        # Llamamos a eliminar_codigo, que borra el libro y nos devuelve la nueva estructura reparada del árbol
        self.avl.raiz = self.avl.eliminar_codigo(self.avl.raiz, codigo)

        # 4. Persistir o Guardar
        # Le decimos al sistema interno que actualice el disco duro sin ese libro que acabamos de matar
        self._guardar_libros_xml()

        # Final feliz, notificamos que se eliminó
        return True, "Libro eliminado correctamente."

    # ----------------------------------------------------------
    # ESTUDIANTES
    # ----------------------------------------------------------

    def eliminar_estudiante(self, carnet: int) -> Tuple[bool, str]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Intentar remover a un estudiante de la biblioteca de manera segura y controlada.
        Parámetros: carnet (int) — El carnet del muchacho o muchacha que queremos eliminar.
        Devuelve:   Tuple[bool, str] — Retorna (exito True/False, mensaje al usuario).
        Descripción:
            Receta estricta de borrado:
              1. Ver que el estudiante exista de verdad en nuestra tabla.
              2. Vigilar que el estudiante no nos deba ningún libro (no préstamos activos).
              3. Sacarlo completamente de la tabla hash.
              4. Guardar los cambios finales en los archivos de estudiantes para que se mantenga el borrado.
        """
        # 1. Verificar que el estudiante existe consultando en la tabla hash de memoria
        estudiante = self.tabla_hash.buscar_por_carnet(carnet)
        # Si la tabla dice que no hay nada ahí (None), abortamos, no podemos borrar fantasmas
        if estudiante is None:
            return False, f"El estudiante con carnet {carnet} no existe."

        # 2. Verificar que el estudiante no tiene deudas activas
        # Le preguntamos al sistema de préstamos si este carnet en particular debe algo
        if self.sistema_prestamos.estudiante_tiene_prestamos(carnet):
            # Si nos debe un libro, detenemos la eliminación para obligarlo a que lo devuelva primero
            return False, "No se puede eliminar el estudiante: tiene prestamos activos."

        # 3. Eliminar de la tabla hash
        # Le indicamos a la tabla hash que proceda a borrar a la persona, nos devolverá True si funcionó
        eliminado = self.tabla_hash.eliminar_estudiante(carnet)
        # Por si pasara algún error rarísimo donde no se pudo borrar de la memoria
        if not eliminado:
            return False, "No se pudo eliminar el estudiante."

        # 4. Persistir y confirmar cambios
        # Actualizamos nuestro archivo estudiantes.xml para que el borrado quede firme en el disco
        self._guardar_estudiantes_xml()

        # Todo salió súper bien, devolvemos un True
        return True, "Estudiante eliminado correctamente."

    # ----------------------------------------------------------
    # PERSISTENCIA INTERNA
    # ----------------------------------------------------------

    def _guardar_libros_xml(self) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Función interna para agrupar los libros vivos y grabarlos en disco duro.
        Parámetros: ninguno
        Devuelve:   None
        Descripción:
            Manda a pedir la lista plana de libros en orden a partir del árbol (AVL) y los 
            envía al gestor de archivos (XMLManager) para reemplazar el archivo viejo.
        """
        # Convertimos nuestro árbol en una lista sencilla y ordenada de objetos Libro
        libros = self.avl.obtener_libros_inorden(self.avl.raiz)
        # Tomamos esa lista y le pedimos al gestor XML que sobrescriba el archivo físico
        self.xml_manager.guardar_libros(libros)

    def _guardar_estudiantes_xml(self) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Función interna que empaqueta todos los estudiantes que quedaron y los guarda.
        Parámetros: ninguno
        Devuelve:   None
        Descripción:
            Tiene que ir buscando en todas y cada una de las cajitas (buckets) de la tabla hash,
            extraer los estudiantes y mandarlos todos juntos al gestor de archivos.
        """
        # Preparamos una lista en blanco que se llenará de estudiantes
        estudiantes = []
        # La tabla hash es una gran lista que por dentro tiene listas enlazadas (cajitas). Las recorremos todas.
        for lista in self.tabla_hash.tabla_hash:
            # Empezamos por el primer elemento de la lista enlazada (nodo) dentro de la cajita actual
            actual = lista.primero
            # Mientras el nodo no esté vacío (None), lo procesamos
            while actual is not None:
                # Sacamos el valor real del estudiante de adentro del nodo y lo metemos a nuestra lista recolectora
                estudiantes.append(actual.valor)
                # Nos movemos hacia el siguiente nodo de la lista enlazada
                actual = actual.sig
        # Cuando terminamos de peinar toda la tabla, enviamos la recolección al XMLManager para que la guarde
        self.xml_manager.guardar_estudiantes(estudiantes)
