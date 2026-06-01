"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto - [Nombre 2]
Archivo: xml_manager.py
Descripción: Módulo encargado de cargar y guardar los datos
             de libros, estudiantes y préstamos en archivos XML.
"""


from typing import List
import xmltodict

from clases import prestamo
from clases.libro import Libro
from clases.estudiante import Estudiante
from clases.prestamo import Prestamo


class XMLManager:

    def __init__(self):
        self.ruta_libros = "datos/libros.xml"
        self.ruta_estudiantes = "datos/estudiantes.xml"
        self.ruta_prestamos = "datos/prestamos.xml"

    @staticmethod
    def _asegurar_lista(datos):
        """
        Convierte un diccionario en lista si solo existe un elemento.
        """
        if isinstance(datos, list):
            return datos

        if datos is None:
            return []

        return [datos]

    def cargar_libros(self) -> List[Libro]:
        """
        Lee libros.xml y devuelve una lista de objetos Libro.
        """

        with open(self.ruta_libros, "r", encoding="utf-8") as archivo:
            datos = xmltodict.parse(archivo.read())

        libros_xml = datos.get("libros", {}).get("libro", [])
        libros_xml = self._asegurar_lista(libros_xml)

        libros = []

        for libro in libros_xml:
            libros.append(
                Libro(
                    codigo=libro.get("codigo", ""),
                    autor=libro.get("autor", ""),
                    titulo=libro.get("titulo", ""),
                    anio=int(libro.get("anio", 0)),
                    editorial=libro.get("editorial", "N/A"),
                    areas=libro.get("areas", "N/A")
                )
            )

        return libros

    def cargar_estudiantes(self) -> List[Estudiante]:
        """
        Lee estudiantes.xml y devuelve una lista de objetos Estudiante.
        """

        with open(self.ruta_estudiantes, "r", encoding="utf-8") as archivo:
            datos = xmltodict.parse(archivo.read())

        estudiantes_xml = datos.get("estudiantes", {}).get(
            "estudiante", []
        )

        estudiantes_xml = self._asegurar_lista(estudiantes_xml)

        estudiantes = []

        for estudiante in estudiantes_xml:
            estudiantes.append(
                Estudiante(
                    carnet=estudiante.get("carnet", ""),
                    nombre=estudiante.get("nombre", ""),
                    carrera=estudiante.get("carrera", ""),
                    telefono=estudiante.get("telefono", ""),
                    correo=estudiante.get("correo", ""),
                    direccion=estudiante.get("direccion", "")
                )
            )

        return estudiantes

    def cargar_prestamos(self) -> List[Prestamo]:
        """
        Lee prestamos.xml y devuelve una lista de objetos Prestamo.
        """

        with open(self.ruta_prestamos, "r", encoding="utf-8") as archivo:
            datos = xmltodict.parse(archivo.read())

        prestamos_xml = datos.get("prestamos", {}).get(
            "prestamo", []
        )

        prestamos_xml = self._asegurar_lista(prestamos_xml)

        prestamos = []

        for prestamo in prestamos_xml:
            # Soporte tanto para 'carnet' como 'carnet_estudiante'
            # y para 'codigo_prestamo' o 'id'
            carnet = prestamo.get("carnet_estudiante") or prestamo.get("carnet", "")
            codigo_p = prestamo.get("codigo_prestamo") or prestamo.get("id", "")

            prestamos.append(
                Prestamo(
                    codigo_prestamo=codigo_p,
                    codigo_libro=prestamo.get("codigo_libro", ""),
                    carnet_estudiante=carnet,
                    fecha_prestamo=prestamo.get("fecha_prestamo", ""),
                )
            )

        return prestamos

    def guardar_libros(self, libros: List[Libro]):
        """
        Guarda la lista de libros en libros.xml.
        """

        datos = {
            "libros": {
                "libro": [
                    {
                        "codigo": libro.codigo,
                        "autor": libro.autor,
                        "titulo": libro.titulo,
                        "anio": libro.anio,
                        "editorial": libro.editorial,
                        "areas": libro.areas,
                    }
                    for libro in libros
                ]
            }
        }

        with open(self.ruta_libros, "w", encoding="utf-8") as archivo:
            archivo.write(xmltodict.unparse(datos, pretty=True))

    def guardar_estudiantes(self,estudiantes: List[Estudiante]):
        """
        Guarda la lista de estudiantes en estudiantes.xml.
        """

        datos = {
            "estudiantes": {
                "estudiante": [
                    {
                        "carnet": estudiante.carnet,
                        "nombre": estudiante.nombre,
                        "carrera": estudiante.carrera,
                        "telefono": estudiante.telefono,
                        "correo": estudiante.correo,
                        "direccion": estudiante.direccion,
                    }
                    for estudiante in estudiantes
                ]
            }
        }

        with open(
                self.ruta_estudiantes,
                "w",
                encoding="utf-8"
        ) as archivo:
            archivo.write(xmltodict.unparse(datos, pretty=True))

    def guardar_prestamos(self,prestamos: List[Prestamo]
    ):
        """
        Guarda la lista de préstamos en prestamos.xml.
        """

        datos = {
            "prestamos": {
                "prestamo": [
                    {
                        "codigo_prestamo": prestamo.codigo_prestamo,
                        "codigo_libro": prestamo.codigo_libro,
                        "carnet_estudiante": prestamo.carnet_estudiante,
                        "fecha_prestamo": prestamo.fecha_prestamo,
                    }
                    for prestamo in prestamos
                ]
            }
        }

        with open(
                self.ruta_prestamos,
                "w",
                encoding="utf-8"
        ) as archivo:
            archivo.write(xmltodict.unparse(datos, pretty=True))