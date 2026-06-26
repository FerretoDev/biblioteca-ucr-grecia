"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
Archivo: prestamo.py
"""

class Prestamo:
    """
    Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
    Descripción:
        Clase que representa el acto de prestar un libro a un estudiante.
        Relaciona un estudiante (por su carnet) con un libro (por su código).
    """
    def __init__(
        self,
        codigo_prestamo: int,
        codigo_libro: int,
        carnet_estudiante: int,
        fecha_prestamo: str = "",
    ) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros:
            codigo_prestamo (int): Número único que identifica a este préstamo en particular.
            codigo_libro (int): El número único del libro que se está prestando.
            carnet_estudiante (int): El carnet del estudiante que se lleva el libro.
            fecha_prestamo (str): Fecha en la que se realizó el préstamo (opcional).
        Devuelve: None
        Descripción:
            Función constructora. Toma los datos del préstamo y los guarda en
            la memoria interna del objeto (atributos).
        """
        # Almacenamos los identificadores necesarios para saber qué libro tiene qué estudiante
        self.codigo_prestamo = codigo_prestamo
        self.codigo_libro = codigo_libro
        self.carnet_estudiante = carnet_estudiante
        self.fecha_prestamo = fecha_prestamo

    def __str__(self) -> str:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: ninguno
        Devuelve: str - Un texto corto y fácil de entender.
        Descripción:
            Crea un mensaje resumido que muestra el número de préstamo,
            qué libro es y qué estudiante lo tiene.
        """
        # Formateo básico para mostrar información clave a simple vista
        return f"Prestamo: {self.codigo_prestamo}, Libro: {self.codigo_libro}, Estudiante: {self.carnet_estudiante}"

    def __repr__(self) -> str:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: ninguno
        Devuelve: str - Texto exacto con todos los datos técnicos.
        Descripción:
            Genera una representación detallada (ideal para los programadores)
            con todos los valores que componen este préstamo.
        """
        # Código que serviría para recrear exactamente esta misma variable de préstamo
        return f"Prestamo({self.codigo_prestamo}, {self.codigo_libro}, {self.carnet_estudiante}, '{self.fecha_prestamo}')"
