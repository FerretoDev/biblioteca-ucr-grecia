class Estudiante:

    def __init__(self, carnet, nombre, carrera, telefono, correo, direccion):
        self.carnet = carnet
        self.nombre = nombre
        self.carrera = carrera
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion

    def __str__(self):
        return f"Estudiante: {self.nombre}, Carnet: {self.carnet}"
        # repr es casi lo mismo que str y se hace igual
    def __repr__(self):
        return f"Estudiante('{self.carnet}', '{self.nombre}', '{self.carrera}', '{self.telefono}', '{self.correo}', '{self.direccion}')"
