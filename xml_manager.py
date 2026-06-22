"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto - [Nombre 2]
Archivo: xml_manager.py
Descripcion: Carga y guardado en formato % delimitado. Trabaja con diccionarios de Python en memoria.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from clases.estudiante import Estudiante
from clases.libro import Libro
from clases.prestamo import Prestamo


class XMLManager:
    def __init__(self) -> None:
        """
        Parametros: ninguno
        Devuelve:   None
        Descripcion:
           Inicializa las rutas de los archivos de datos.
        """
        self.ruta_libros = "datos/libros.xml"
        self.ruta_estudiantes = "datos/estudiantes.xml"
        self.ruta_prestamos = "datos/prestamos.xml"

    # ----------------------------------------------------------
    # HELPERS GENERICOS
    # ----------------------------------------------------------

    def _leer_lineas(self, ruta: str) -> List[str]:
        """
        Parametros: ruta (str)
        Devuelve:   List[str] con lineas validas del archivo.
        Descripcion:
           Lee el archivo y devuelve lineas no vacias.
        """
        archivo = Path(ruta)
        if not archivo.exists():
            print(f"[XMLManager] '{ruta}' no encontrado.")
            return []

        lineas: List[str] = []
        with archivo.open("r", encoding="utf-8") as f:
            for linea in f:
                cruda = linea.strip()
                if cruda:
                    lineas.append(cruda)
        return lineas

    @staticmethod
    def _linea_a_dict(
        linea: str,
        campos: List[str],
        permitir_faltantes: int = 0,
    ) -> dict | None:
        """
        Parametros: linea (str), campos (List[str]), permitir_faltantes (int)
        Devuelve:   dict con los campos, o None si la linea es invalida.
        Descripcion:
           Convierte una linea separada por % en un diccionario de Python.
        """
        partes = linea.split("%")
        min_campos = len(campos) - permitir_faltantes
        if len(partes) < min_campos or len(partes) > len(campos):
            return None
        if len(partes) < len(campos):
            partes += [""] * (len(campos) - len(partes))
        return dict(zip(campos, partes))

    @staticmethod
    def _dict_a_linea(
        d: dict,
        campos: List[str],
        omitir_vacios_finales: bool = False,
    ) -> str:
        """
        Parametros: d (dict), campos (List[str]), omitir_vacios_finales (bool)
        Devuelve:   str con los campos separados por %.
        Descripcion:
           Serializa un diccionario de Python a una linea en formato % delimitado.
        """
        valores = [str(d.get(campo, "")) for campo in campos]
        if omitir_vacios_finales:
            while valores and valores[-1] == "":
                valores.pop()
        return "%".join(valores) + "\n"

    # ----------------------------------------------------------
    # CONVERSORES dict → objeto
    # ----------------------------------------------------------

    @staticmethod
    def dict_a_libro(d: dict) -> Libro:
        """
        Parametros: d (dict) — diccionario con claves codigo, autor, titulo,
                    anio, editorial, area.
        Devuelve:   Libro con los datos del diccionario.
        Descripcion:
           Convierte un diccionario de Python en un objeto Libro.
           Usado para poblar el AVL desde los datos cargados del XML.
        """
        return Libro(
            codigo=int(d["codigo"]),
            autor=d["autor"],
            titulo=d["titulo"],
            anio=int(d["anio"]),
            editorial=d["editorial"],
            area=d["area"],
        )

    @staticmethod
    def dict_a_estudiante(d: dict) -> Estudiante:
        """
        Parametros: d (dict) — diccionario con claves carnet, nombre, carrera,
                    telefono, correo, direccion.
        Devuelve:   Estudiante con los datos del diccionario.
        Descripcion:
           Convierte un diccionario de Python en un objeto Estudiante.
           Usado para poblar la Tabla Hash desde los datos cargados del XML.
        """
        return Estudiante(
            carnet=int(d["carnet"]),
            nombre=d["nombre"],
            carrera=d["carrera"],
            telefono=d["telefono"],
            correo=d["correo"],
            direccion=d["direccion"],
        )

    @staticmethod
    def dict_a_prestamo(d: dict) -> Prestamo:
        """
        Parametros: d (dict) — diccionario con claves codigo_prestamo,
                    codigo_libro, carnet_estudiante, fecha_prestamo.
        Devuelve:   Prestamo con los datos del diccionario.
        Descripcion:
           Convierte un diccionario de Python en un objeto Prestamo.
           Usado para poblar el Arbol Rojinegro desde los datos del XML.
        """
        return Prestamo(
            codigo_prestamo=int(d["codigo_prestamo"]),
            codigo_libro=int(d["codigo_libro"]),
            carnet_estudiante=int(d["carnet_estudiante"]),
            fecha_prestamo=d.get("fecha_prestamo", ""),
        )

    # ----------------------------------------------------------
    # LIBROS
    # ----------------------------------------------------------

    def cargar_libros(self) -> List[dict]:
        """
        Parametros: ninguno
        Devuelve:   List[dict] con los datos de cada libro.
        Descripcion:
           Lee libros.xml en formato % y devuelve una lista de diccionarios.
        """
        campos = ["codigo", "autor", "titulo", "anio", "editorial", "area"]
        lineas = self._leer_lineas(self.ruta_libros)
        libros: List[dict] = []
        for num, linea in enumerate(lineas, start=1):
            d = self._linea_a_dict(linea, campos)
            if d is None:
                print(f"[XMLManager] Linea {num} ignorada (libros): {linea}")
                continue
            libros.append(d)
        return libros

    def guardar_libros(self, libros: List[dict]) -> None:
        """
        Parametros: libros (List[dict])
        Devuelve:   None
        Descripcion:
           Guarda los libros en formato % delimitado.
        """
        Path(self.ruta_libros).parent.mkdir(parents=True, exist_ok=True)
        campos = ["codigo", "autor", "titulo", "anio", "editorial", "area"]
        with open(self.ruta_libros, "w", encoding="utf-8") as f:
            for d in libros:
                f.write(self._dict_a_linea(d, campos))

    # ----------------------------------------------------------
    # ESTUDIANTES
    # ----------------------------------------------------------

    def cargar_estudiantes(self) -> List[dict]:
        """
        Parametros: ninguno
        Devuelve:   List[dict] con los datos de cada estudiante.
        Descripcion:
           Lee estudiantes.xml en formato % y devuelve una lista de diccionarios.
        """
        campos = ["carnet", "nombre", "carrera", "telefono", "correo", "direccion"]
        lineas = self._leer_lineas(self.ruta_estudiantes)
        estudiantes: List[dict] = []
        for num, linea in enumerate(lineas, start=1):
            d = self._linea_a_dict(linea, campos)
            if d is None:
                print(f"[XMLManager] Linea {num} ignorada (estudiantes): {linea}")
                continue
            estudiantes.append(d)
        return estudiantes

    def guardar_estudiantes(self, estudiantes: List[dict]) -> None:
        """
        Parametros: estudiantes (List[dict])
        Devuelve:   None
        Descripcion:
           Guarda los estudiantes en formato % delimitado.
        """
        Path(self.ruta_estudiantes).parent.mkdir(parents=True, exist_ok=True)
        campos = ["carnet", "nombre", "carrera", "telefono", "correo", "direccion"]
        with open(self.ruta_estudiantes, "w", encoding="utf-8") as f:
            for d in estudiantes:
                f.write(self._dict_a_linea(d, campos))

    # ----------------------------------------------------------
    # PRESTAMOS
    # ----------------------------------------------------------

    def cargar_prestamos(self) -> List[dict]:
        """
        Parametros: ninguno
        Devuelve:   List[dict] con los datos de cada prestamo.
        Descripcion:
           Lee prestamos.xml en formato % y devuelve una lista de diccionarios.
        """
        campos = [
            "codigo_prestamo",
            "codigo_libro",
            "carnet_estudiante",
            "fecha_prestamo",
        ]
        lineas = self._leer_lineas(self.ruta_prestamos)
        prestamos: List[dict] = []
        for num, linea in enumerate(lineas, start=1):
            d = self._linea_a_dict(linea, campos, permitir_faltantes=1)
            if d is None:
                print(f"[XMLManager] Linea {num} ignorada (prestamos): {linea}")
                continue
            prestamos.append(d)
        return prestamos

    def guardar_prestamos(self, prestamos: List[dict]) -> None:
        """
        Parametros: prestamos (List[dict])
        Devuelve:   None
        Descripcion:
           Guarda los prestamos en formato % delimitado.
        """
        Path(self.ruta_prestamos).parent.mkdir(parents=True, exist_ok=True)
        campos = [
            "codigo_prestamo",
            "codigo_libro",
            "carnet_estudiante",
            "fecha_prestamo",
        ]
        with open(self.ruta_prestamos, "w", encoding="utf-8") as f:
            for d in prestamos:
                if d.get("codigo_prestamo") == d.get("carnet_estudiante"):
                    print(
                        "[XMLManager] Aviso: codigo_prestamo y carnet_estudiante son iguales."
                    )
                f.write(self._dict_a_linea(d, campos, omitir_vacios_finales=True))

    # ----------------------------------------------------------
    # OPERACIONES CONJUNTAS
    # ----------------------------------------------------------

    def cargar_todo(self) -> tuple[List[dict], List[dict], List[dict]]:
        """
        Parametros: ninguno
        Devuelve:   tuple (libros, estudiantes, prestamos) como listas de diccionarios.
        Descripcion:
           Carga los tres archivos en formato % y devuelve listas de diccionarios.
        """
        return (
            self.cargar_libros(),
            self.cargar_estudiantes(),
            self.cargar_prestamos(),
        )

