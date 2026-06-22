"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto - Paulo Anchía Correás
Archivo: estudiante.py
"""

class Estudiante:

    def __init__(self, carnet: int, nombre: str, carrera: str, telefono: str, correo: str, direccion: str) -> None:
        """
        Parámetros: carnet (int), nombre (str), carrera (str), telefono (str), correo (str), direccion (str)
        Devuelve:   None
        Descripción:
            Inicializa un estudiante con los campos definidos en el archivo % delimitado.
        """
        self.carnet = carnet
        self.nombre = nombre
        self.carrera = carrera
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion

    def __str__(self) -> str:
        """
        Parámetros: ninguno
        Devuelve:   str con una representacion legible del estudiante
        Descripción:
            Devuelve un texto corto con nombre y carnet.
        """
        return f"Estudiante: {self.nombre}, Carnet: {self.carnet}"

    def __repr__(self) -> str:
        """
        Parámetros: ninguno
        Devuelve:   str con la representacion de depuracion del estudiante
        Descripción:
            Devuelve una representacion con todos los campos del estudiante.
        """
        return f"Estudiante({self.carnet}, '{self.nombre}', '{self.carrera}', '{self.telefono}', '{self.correo}', '{self.direccion}')"
