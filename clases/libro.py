"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto - Paulo Anchía Correás
Archivo: libro.py
"""

class Libro:

    def __init__(self, codigo: int, autor: str, titulo: str, anio: int, editorial: str, area: str) -> None:
        """
        Parámetros: codigo (int), autor (str), titulo (str), anio (int), editorial (str), area (str)
        Devuelve:   None
        Descripción:
            Inicializa un libro con los campos definidos para la entidad.
        """
        self.codigo = codigo
        self.autor = autor
        self.titulo = titulo
        self.anio = anio
        self.editorial = editorial
        self.area = area

    def __str__(self) -> str:
        """
        Parámetros: ninguno
        Devuelve:   str con una representacion legible del libro
        Descripción:
            Devuelve un texto corto con titulo, autor y anio.
        """
        return f"Libro: {self.titulo} por {self.autor} ({self.anio})"

    def __repr__(self) -> str:
        """
        Parámetros: ninguno
        Devuelve:   str con la representacion de depuracion del libro
        Descripción:
            Devuelve una representacion con todos los campos del libro.
        """
        return f"Libro({self.codigo}, '{self.autor}', '{self.titulo}', {self.anio}, '{self.editorial}', '{self.area}')"
