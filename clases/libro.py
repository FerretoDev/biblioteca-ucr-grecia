"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
Archivo: libro.py
"""

class Libro:
    """
    Descripción:
        Clase que representa un libro dentro de la biblioteca.
        Contiene todos los datos relevantes del material de lectura.
    """

    def __init__(self, codigo: int, autor: str, titulo: str, anio: int, editorial: str, area: str) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros:
            codigo (int): El número identificador único del libro.
            autor (str): Nombre de quien escribió el libro.
            titulo (str): El nombre del libro.
            anio (int): Año en que fue publicado.
            editorial (str): Empresa que imprimió o publicó el libro.
            area (str): Categoría o tema del libro (ej. Ciencias, Ficción).
        Devuelve: None
        Descripción:
            Constructora de la clase. Prepara un libro recién creado asignándole
            toda su información a sus variables internas (atributos).
        """
        # Guardamos la información que nos pasan en las variables del libro (self)
        self.codigo = codigo
        self.autor = autor
        self.titulo = titulo
        self.anio = anio
        self.editorial = editorial
        self.area = area

    def __str__(self) -> str:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: ninguno
        Devuelve: str - Un texto simple y amigable.
        Descripción:
            Genera un texto corto con el título, autor y año, pensado para que
            lo lea cualquier persona fácilmente (por ejemplo, en un mensaje de la pantalla).
        """
        # Se arma la oración resumen del libro
        return f"Libro: {self.titulo} por {self.autor} ({self.anio})"

    def __repr__(self) -> str:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: ninguno
        Devuelve: str - Un texto detallado para los programadores.
        Descripción:
            Devuelve el texto exacto que un programador escribiría para volver a
            crear este mismo libro en el código con todos sus datos.
        """
        # Representación técnica y completa del libro
        return f"Libro({self.codigo}, '{self.autor}', '{self.titulo}', {self.anio}, '{self.editorial}', '{self.area}')"
