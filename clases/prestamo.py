class Prestamo:

    def __init__(self, codigo_prestamo: int, codigo_libro: int, carnet_estudiante: int, fecha_prestamo: str = "") -> None:
        """
        Parámetros: codigo_prestamo (int), codigo_libro (int), carnet_estudiante (int), fecha_prestamo (str)
        Devuelve:   None
        Descripción:
            Inicializa un prestamo con los campos definidos en el archivo % delimitado.
        """
        self.codigo_prestamo = codigo_prestamo
        self.codigo_libro = codigo_libro
        self.carnet_estudiante = carnet_estudiante
        self.fecha_prestamo = fecha_prestamo

    def __str__(self) -> str:
        """
        Parámetros: ninguno
        Devuelve:   str con una representacion legible del prestamo
        Descripción:
            Devuelve un texto corto con datos del prestamo.
        """
        return f"Prestamo: {self.codigo_prestamo}, Libro: {self.codigo_libro}, Estudiante: {self.carnet_estudiante}"

    def __repr__(self) -> str:
        """
        Parámetros: ninguno
        Devuelve:   str con la representacion de depuracion del prestamo
        Descripción:
            Devuelve una representacion con todos los campos del prestamo.
        """
        return f"Prestamo({self.codigo_prestamo}, {self.codigo_libro}, {self.carnet_estudiante}, '{self.fecha_prestamo}')"
