"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
Archivo: estudiante.py
"""

class Estudiante:
    """
    Descripción:
        Clase que representa a un estudiante dentro del sistema de la biblioteca.
        Guarda toda su información personal y académica.
    """

    def __init__(self, carnet: int, nombre: str, carrera: str, telefono: str, correo: str, direccion: str) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros:
            carnet (int): El número de identificación único del estudiante.
            nombre (str): El nombre completo del estudiante.
            carrera (str): La carrera que estudia.
            telefono (str): Número de teléfono para contactarlo.
            correo (str): Correo electrónico.
            direccion (str): Lugar donde vive.
        Devuelve: None
        Descripción:
            Función constructora. Se llama automáticamente cuando creamos un nuevo 'Estudiante'
            para guardar todos sus datos en la memoria (variables internas).
        """
        # Asignamos el valor recibido a las variables internas del objeto (self)
        self.carnet = carnet
        self.nombre = nombre
        self.carrera = carrera
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion

    def __str__(self) -> str:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: ninguno
        Devuelve: str - Un texto amigable para el usuario normal.
        Descripción:
            Devuelve un resumen fácil de leer con el nombre y el carnet del estudiante.
            Esto es lo que se ve si hacemos print() del estudiante.
        """
        # Formateamos un texto simple y directo
        return f"Estudiante: {self.nombre}, Carnet: {self.carnet}"

    def __repr__(self) -> str:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Parámetros: ninguno
        Devuelve: str - Un texto con fines técnicos o de programación (depuración).
        Descripción:
            Devuelve cómo se vería el código exacto para volver a crear a este estudiante
            con todos sus datos actuales.
        """
        # Creamos una cadena de texto que imita cómo se crea un Estudiante en Python
        return f"Estudiante({self.carnet}, '{self.nombre}', '{self.carrera}', '{self.telefono}', '{self.correo}', '{self.direccion}')"
