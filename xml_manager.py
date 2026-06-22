"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto - [Nombre 2]
Archivo: xml_manager.py
Descripcion: Carga y guardado en formato % delimitado. Trabaja directamente con objetos.
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
    def _linea_a_partes(
        linea: str,
        num_esperado: int,
        permitir_faltantes: int = 0,
    ) -> List[str] | None:
        """
        Parametros: linea (str), num_esperado (int), permitir_faltantes (int)
        Devuelve:   List[str] con las partes separadas, o None si la linea es invalida.
        Descripcion:
           Divide una linea separada por % en sus partes correspondientes.
        """
        partes = linea.split("%")
        min_campos = num_esperado - permitir_faltantes
        if len(partes) < min_campos or len(partes) > num_esperado:
            return None
        if len(partes) < num_esperado:
            partes += [""] * (num_esperado - len(partes))
        return partes

    # ----------------------------------------------------------
    # LIBROS
    # ----------------------------------------------------------

    def cargar_libros(self) -> List[Libro]:
        """
        Parametros: ninguno
        Devuelve:   List[Libro] con los datos de cada libro.
        Descripcion:
           Lee libros.xml en formato % y devuelve una lista de objetos Libro.
        """
        lineas = self._leer_lineas(self.ruta_libros)
        libros: List[Libro] = []
        for num, linea in enumerate(lineas, start=1):
            partes = self._linea_a_partes(linea, 6)
            if partes is None:
                print(f"[XMLManager] Linea {num} ignorada (libros): {linea}")
                continue
            try:
                libros.append(Libro(
                    codigo=int(partes[0]),
                    autor=partes[1],
                    titulo=partes[2],
                    anio=int(partes[3]),
                    editorial=partes[4],
                    area=partes[5],
                ))
            except ValueError:
                print(f"[XMLManager] Error de conversion en linea {num} (libros): {linea}")
        return libros

    def guardar_libros(self, libros: List[Libro]) -> None:
        """
        Parametros: libros (List[Libro])
        Devuelve:   None
        Descripcion:
           Guarda los objetos Libro en formato % delimitado.
        """
        Path(self.ruta_libros).parent.mkdir(parents=True, exist_ok=True)
        with open(self.ruta_libros, "w", encoding="utf-8") as f:
            for l in libros:
                partes = [str(l.codigo), l.autor, l.titulo, str(l.anio), l.editorial, l.area]
                f.write("%".join(partes) + "\n")

    # ----------------------------------------------------------
    # ESTUDIANTES
    # ----------------------------------------------------------

    def cargar_estudiantes(self) -> List[Estudiante]:
        """
        Parametros: ninguno
        Devuelve:   List[Estudiante] con los datos de cada estudiante.
        Descripcion:
           Lee estudiantes.xml en formato % y devuelve una lista de objetos Estudiante.
        """
        lineas = self._leer_lineas(self.ruta_estudiantes)
        estudiantes: List[Estudiante] = []
        for num, linea in enumerate(lineas, start=1):
            partes = self._linea_a_partes(linea, 6)
            if partes is None:
                print(f"[XMLManager] Linea {num} ignorada (estudiantes): {linea}")
                continue
            try:
                estudiantes.append(Estudiante(
                    carnet=int(partes[0]),
                    nombre=partes[1],
                    carrera=partes[2],
                    telefono=partes[3],
                    correo=partes[4],
                    direccion=partes[5],
                ))
            except ValueError:
                print(f"[XMLManager] Error de conversion en linea {num} (estudiantes): {linea}")
        return estudiantes

    def guardar_estudiantes(self, estudiantes: List[Estudiante]) -> None:
        """
        Parametros: estudiantes (List[Estudiante])
        Devuelve:   None
        Descripcion:
           Guarda los objetos Estudiante en formato % delimitado.
        """
        Path(self.ruta_estudiantes).parent.mkdir(parents=True, exist_ok=True)
        with open(self.ruta_estudiantes, "w", encoding="utf-8") as f:
            for e in estudiantes:
                partes = [str(e.carnet), e.nombre, e.carrera, e.telefono, e.correo, e.direccion]
                f.write("%".join(partes) + "\n")

    # ----------------------------------------------------------
    # PRESTAMOS
    # ----------------------------------------------------------

    def cargar_prestamos(self) -> List[Prestamo]:
        """
        Parametros: ninguno
        Devuelve:   List[Prestamo] con los datos de cada prestamo.
        Descripcion:
           Lee prestamos.xml en formato % y devuelve una lista de objetos Prestamo.
        """
        lineas = self._leer_lineas(self.ruta_prestamos)
        prestamos: List[Prestamo] = []
        for num, linea in enumerate(lineas, start=1):
            partes = self._linea_a_partes(linea, 4, permitir_faltantes=1)
            if partes is None:
                print(f"[XMLManager] Linea {num} ignorada (prestamos): {linea}")
                continue
            try:
                prestamos.append(Prestamo(
                    codigo_prestamo=int(partes[0]),
                    codigo_libro=int(partes[1]),
                    carnet_estudiante=int(partes[2]),
                    fecha_prestamo=partes[3],
                ))
            except ValueError:
                print(f"[XMLManager] Error de conversion en linea {num} (prestamos): {linea}")
        return prestamos

    def guardar_prestamos(self, prestamos: List[Prestamo]) -> None:
        """
        Parametros: prestamos (List[Prestamo])
        Devuelve:   None
        Descripcion:
           Guarda los objetos Prestamo en formato % delimitado.
        """
        Path(self.ruta_prestamos).parent.mkdir(parents=True, exist_ok=True)
        with open(self.ruta_prestamos, "w", encoding="utf-8") as f:
            for p in prestamos:
                if p.codigo_prestamo == p.carnet_estudiante:
                    print(
                        "[XMLManager] Aviso: codigo_prestamo y carnet_estudiante son iguales."
                    )
                partes = [str(p.codigo_prestamo), str(p.codigo_libro), str(p.carnet_estudiante), p.fecha_prestamo]
                while partes and partes[-1] == "":
                    partes.pop()
                f.write("%".join(partes) + "\n")

    # ----------------------------------------------------------
    # OPERACIONES CONJUNTAS
    # ----------------------------------------------------------

    def cargar_todo(self) -> tuple[List[Libro], List[Estudiante], List[Prestamo]]:
        """
        Parametros: ninguno
        Devuelve:   tuple (libros, estudiantes, prestamos) como listas de objetos.
        Descripcion:
           Carga los tres archivos en formato % y devuelve listas de objetos.
        """
        return (
            self.cargar_libros(),
            self.cargar_estudiantes(),
            self.cargar_prestamos(),
        )
