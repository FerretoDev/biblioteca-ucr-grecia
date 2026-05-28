class Prestamo:

    def __init__(self, codigo_prestamo, codigo_libro, carnet_estudiante, fecha_prestamo):
        self.codigo_prestamo = codigo_prestamo
        self.codigo_libro = codigo_libro
        self.carnet_estudiante = carnet_estudiante
        self.fecha_prestamo = fecha_prestamo

    def __str__(self):
        return f"Prestamo: {self.codigo_prestamo}, Libro: {self.codigo_libro}, Estudiante: {self.carnet_estudiante}"

    def __repr__(self):
        return f"Prestamo('{self.codigo_prestamo}', '{self.codigo_libro}', '{self.carnet_estudiante}', '{self.fecha_prestamo}')"
