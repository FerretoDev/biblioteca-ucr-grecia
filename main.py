from xml_manager import XMLManager
from estructura_datos.arbol_avl.arbol_avl import ArbolAVL
from clases.libro import Libro
def main():
    # Este objeto es el que se encarga de toda la logia, tanto para leer, escribir, validar un .xml, tambien con un json y tambien es utilizado para pasar de .xml a un objeto en python
    xml_manager = XMLManager()
    # Carga de los datos
    libros, estudiantes, prestamos = xml_manager.cargar_todo()
    """-------------------------------------------------------------------------------------------"""


    """-------------------------------------------------------------------------------------"""
    # Guardar datos al finalizar el programa
    xml_manager.guardar_todo(libros, estudiantes, prestamos)
    xml_manager.guardar_json(libros, estudiantes, prestamos)



if __name__ == "__main__":
    main()
