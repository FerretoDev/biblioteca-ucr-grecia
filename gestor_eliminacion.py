"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto - Paulo Anchía Correás
Archivo: gestor_eliminacion.py
Descripcion: Capa de reglas de negocio para eliminar libros y estudiantes.
"""

from typing import Tuple

from estructura_datos.arbol_avl.arbol_avl import ArbolAVL
from estructura_datos.tabla_hash.tabla_hash import TablaHash
from sistema_prestamos import SistemaPrestamos
from xml_manager import XMLManager


class GestorEliminacion:
    def __init__(
        self,
        avl: ArbolAVL,
        tabla_hash: TablaHash,
        sistema_prestamos: SistemaPrestamos,
        xml_manager: XMLManager,
    ) -> None:
        """
        Parametros: avl (ArbolAVL)                    — arbol de libros.
                    tabla_hash (TablaHash)             — tabla de estudiantes.
                    sistema_prestamos (SistemaPrestamos) — gestor de prestamos.
                    xml_manager (XMLManager)           — acceso a persistencia.
        Devuelve:   None
        Descripcion:
            Inicializa el gestor con referencias a las estructuras de datos
            ya cargadas. No carga datos propios; solo aplica reglas de negocio.
        """
        self.avl = avl
        self.tabla_hash = tabla_hash
        self.sistema_prestamos = sistema_prestamos
        self.xml_manager = xml_manager

    # ----------------------------------------------------------
    # LIBROS
    # ----------------------------------------------------------

    def eliminar_libro(self, codigo: int) -> Tuple[bool, str]:
        """
        Parametros: codigo (int) — codigo del libro a eliminar.
        Devuelve:   Tuple[bool, str] — (exito, mensaje descriptivo).
        Descripcion:
            Elimina un libro del AVL solo si no tiene un prestamo activo.
            Flujo:
              1. Verificar que el libro existe en el AVL.
              2. Verificar que el libro NO esta prestado.
              3. Eliminar del AVL (reasigna la raiz).
              4. Persistir libros.xml con la lista actualizada.
        """
        # 1. Verificar que el libro existe
        libro = self.avl.buscar_codigo(self.avl.raiz, codigo)
        if libro is None:
            return False, f"El libro {codigo} no existe en el sistema."

        # 2. Verificar que no esta prestado
        if self.sistema_prestamos.libro_esta_prestado(codigo):
            return False, "No se puede eliminar el libro: esta prestado."

        # 3. Eliminar del AVL — eliminar_codigo devuelve la nueva raiz
        self.avl.raiz = self.avl.eliminar_codigo(self.avl.raiz, codigo)

        # 4. Persistir: convertir todos los libros restantes a dict y guardar
        self._guardar_libros_xml()

        return True, "Libro eliminado correctamente."

    # ----------------------------------------------------------
    # ESTUDIANTES
    # ----------------------------------------------------------

    def eliminar_estudiante(self, carnet: int) -> Tuple[bool, str]:
        """
        Parametros: carnet (int) — carnet del estudiante a eliminar.
        Devuelve:   Tuple[bool, str] — (exito, mensaje descriptivo).
        Descripcion:
            Elimina un estudiante de la tabla hash solo si no tiene
            prestamos activos.
            Flujo:
              1. Verificar que el estudiante existe en la tabla hash.
              2. Verificar que no tiene prestamos activos.
              3. Eliminar de la tabla hash.
              4. Persistir estudiantes.xml con la lista actualizada.
        """
        # 1. Verificar que el estudiante existe
        estudiante = self.tabla_hash.buscar_por_carnet(carnet)
        if estudiante is None:
            return False, f"El estudiante con carnet {carnet} no existe."

        # 2. Verificar que no tiene prestamos activos
        if self.sistema_prestamos.estudiante_tiene_prestamos(carnet):
            return False, "No se puede eliminar el estudiante: tiene prestamos activos."

        # 3. Eliminar de la tabla hash
        eliminado = self.tabla_hash.eliminar_estudiante(carnet)
        if not eliminado:
            return False, "No se pudo eliminar el estudiante."

        # 4. Persistir
        self._guardar_estudiantes_xml()

        return True, "Estudiante eliminado correctamente."

    # ----------------------------------------------------------
    # PERSISTENCIA INTERNA
    # ----------------------------------------------------------

    def _guardar_libros_xml(self) -> None:
        """
        Parametros: ninguno
        Devuelve:   None
        Descripcion:
            Recorre el AVL en inorden y llama a xml_manager.guardar_libros().
        """
        libros = self.avl.obtener_libros_inorden(self.avl.raiz)
        self.xml_manager.guardar_libros(libros)

    def _guardar_estudiantes_xml(self) -> None:
        """
        Parametros: ninguno
        Devuelve:   None
        Descripcion:
            Recorre todos los buckets de la tabla hash, recopila los
            estudiantes y llama a xml_manager.guardar_estudiantes().
        """
        estudiantes = []
        for lista in self.tabla_hash.tabla_hash:
            actual = lista.primero  # nodo de la lista enlazada
            while actual is not None:
                estudiantes.append(actual.valor)
                actual = actual.sig
        self.xml_manager.guardar_estudiantes(estudiantes)
