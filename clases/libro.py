class Libro:

    def __init__(self, codigo: str, autor: str, titulo: str, anio: str, editorial: str, area: str) -> None:
        """
        Parámetros: codigo (str), autor (str), titulo (str), anio (str), editorial (str), area (str)
        Devuelve:   None
        Descripción:
            Inicializa un libro con los campos definidos para la entidad.
        """
        # TODO: Cambiar el tipo de codigo a int y anio a int
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
        return f"Libro('{self.codigo}', '{self.autor}', '{self.titulo}', '{self.anio}', '{self.editorial}', '{self.area}')"
