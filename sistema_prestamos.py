"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Archivo: sistema_prestamos.py
Descripcion: Capa de reglas de negocio para gestionar prestamos.
             Valida condiciones antes de tocar el arbol rojinegro o el XML.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from clases.prestamo import Prestamo
from estructura_datos.arbol_avl.arbol_avl import ArbolAVL
from estructura_datos.arbol_rojinegro.arbol_rojinegro import ArbolRojinegro
from estructura_datos.tabla_hash.tabla_hash import TablaHash
from xml_manager import XMLManager

DURACION_PRESTAMO_DIAS = 15


class SistemaPrestamos:
    def __init__(
        self,
        avl_libros: ArbolAVL,
        hash_estudiantes: TablaHash,
        arbol_prestamos: ArbolRojinegro,
        xml_manager: XMLManager,
    ) -> None:
        """
        Parametros: avl_libros (ArbolAVL), hash_estudiantes (TablaHash),
                    arbol_prestamos (ArbolRojinegro), xml_manager (XMLManager)
        Devuelve:   None
        Descripcion:
            Inicializa el gestor con referencias a las estructuras de datos
            ya cargadas. No carga datos propios; solo aplica reglas de negocio.
        """
        self.avl_libros = avl_libros
        self.hash_estudiantes = hash_estudiantes
        self.arbol_prestamos = arbol_prestamos
        self.xml_manager = xml_manager

    # ----------------------------------------------------------
    # CONSULTAS
    # ----------------------------------------------------------

    def libro_esta_prestado(self, codigo_libro: int) -> bool:
        """
        Parametros: codigo_libro (int) — codigo del libro a consultar.
        Devuelve:   bool — True si el libro tiene un prestamo activo.
        Descripcion:
            Recorre todos los prestamos en inorden y verifica si alguno
            corresponde al libro dado.
        """
        prestamos = self.arbol_prestamos.inorden(self.arbol_prestamos.raiz)
        for prestamo in prestamos:
            if prestamo.codigo_libro == codigo_libro:
                return True
        return False

    def estudiante_tiene_prestamos(self, carnet: int) -> bool:
        """
        Parametros: carnet (int) — carnet del estudiante a consultar.
        Devuelve:   bool — True si el estudiante tiene al menos un prestamo activo.
        Descripcion:
            Recorre todos los prestamos en inorden y verifica si alguno
            pertenece al estudiante dado.
        """
        prestamos = self.arbol_prestamos.inorden(self.arbol_prestamos.raiz)
        for prestamo in prestamos:
            if prestamo.carnet_estudiante == carnet:
                return True
        return False

    def listar_prestamos(self) -> List[Prestamo]:
        """
        Parametros: ninguno
        Devuelve:   List[Prestamo] con todos los prestamos activos en orden.
        Descripcion:
            Devuelve todos los prestamos del arbol rojinegro en recorrido
            inorden (orden ascendente por codigo de prestamo).
        """
        return self.arbol_prestamos.inorden(self.arbol_prestamos.raiz)

    def _generar_codigo(self) -> int:
        """
        Parametros: ninguno
        Devuelve:   int — codigo de prestamo unico de 4 digitos.
        Descripcion:
            Genera un codigo incremental basado en el maximo existente.
            Garantiza que no se repita mientras el arbol este en memoria.
        """
        prestamos = self.arbol_prestamos.inorden(self.arbol_prestamos.raiz)
        if not prestamos:
            return 1000
        maximo = max(p.codigo_prestamo for p in prestamos)
        siguiente = maximo + 1
        if siguiente > 9999:
            raise ValueError("Se alcanzo el limite de 9999 prestamos.")
        return siguiente

    # ----------------------------------------------------------
    # OPERACIONES
    # ----------------------------------------------------------

    def dar_prestamo(
        self, codigo_libro: int, carnet_estudiante: int
    ) -> Tuple[bool, str]:
        """
        Parametros: codigo_libro (int) — codigo del libro a prestar.
                    carnet_estudiante (int) — carnet del estudiante que pide el libro.
        Devuelve:   Tuple[bool, str] — (exito, mensaje descriptivo).
        Descripcion:
            Valida que el libro exista en el AVL, que el estudiante exista
            en la tabla hash, y que el libro no este ya prestado.
            Si todo es valido, crea el prestamo, lo inserta en el arbol
            rojinegro y lo persiste en el XML.
        """
        # 1. Verificar que el libro existe
        libro = self.avl_libros.buscar_codigo(self.avl_libros.raiz, codigo_libro)
        if libro is None:
            return False, f"El libro {codigo_libro} no existe en el sistema."

        # 2. Verificar que el estudiante existe
        estudiante = self.hash_estudiantes.buscar_por_carnet(carnet_estudiante)
        if estudiante is None:
            return False, f"El estudiante con carnet {carnet_estudiante} no existe."

        # 3. Verificar que el libro no esta ya prestado
        if self.libro_esta_prestado(codigo_libro):
            return False, f"El libro {codigo_libro} ya esta prestado."

        # 4. Crear el prestamo
        codigo_prestamo = self._generar_codigo()
        fecha_prestamo = datetime.now().strftime("%Y-%m-%d")

        nuevo_prestamo = Prestamo(
            codigo_prestamo=codigo_prestamo,
            codigo_libro=codigo_libro,
            carnet_estudiante=carnet_estudiante,
            fecha_prestamo=fecha_prestamo,
        )

        # 5. Insertar en el arbol rojinegro
        self.arbol_prestamos.insertar(self.arbol_prestamos.raiz, nuevo_prestamo)

        # 6. Persistir en XML
        self._guardar_prestamos_xml()

        fecha_devolucion = (
            datetime.strptime(fecha_prestamo, "%Y-%m-%d")
            + timedelta(days=DURACION_PRESTAMO_DIAS)
        ).strftime("%Y-%m-%d")

        return (
            True,
            f"Prestamo {codigo_prestamo} registrado. Devolucion: {fecha_devolucion}.",
        )

    def devolver_libro(self, codigo_prestamo: int) -> Tuple[bool, str]:
        """
        Parametros: codigo_prestamo (int) — codigo del prestamo a cerrar.
        Devuelve:   Tuple[bool, str] — (exito, mensaje descriptivo).
        Descripcion:
            Busca el prestamo en el arbol rojinegro y lo elimina.
            Persiste los cambios en el XML.
        """
        prestamo = self.arbol_prestamos.buscar_codigo(
            self.arbol_prestamos.raiz, codigo_prestamo
        )
        if prestamo is None:
            return False, f"No existe un prestamo con codigo {codigo_prestamo}."

        self.arbol_prestamos.eliminar_codigo(
            self.arbol_prestamos.raiz, codigo_prestamo
        )
        self._guardar_prestamos_xml()

        return True, f"Libro {prestamo.codigo_libro} devuelto correctamente."

    # ----------------------------------------------------------
    # PERSISTENCIA
    # ----------------------------------------------------------

    def _guardar_prestamos_xml(self) -> None:
        """
        Parametros: ninguno
        Devuelve:   None
        Descripcion:
            Convierte todos los prestamos del arbol a dicts y los guarda
            en el archivo XML usando el XMLManager.
        """
        prestamos = self.arbol_prestamos.inorden(self.arbol_prestamos.raiz)
        prestamos_dict = [
            {
                "codigo_prestamo": str(p.codigo_prestamo),
                "codigo_libro": str(p.codigo_libro),
                "carnet_estudiante": str(p.carnet_estudiante),
                "fecha_prestamo": p.fecha_prestamo,
            }
            for p in prestamos
        ]
        self.xml_manager.guardar_prestamos(prestamos_dict)
