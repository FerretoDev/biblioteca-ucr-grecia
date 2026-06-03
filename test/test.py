from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from xml_manager import XMLManager
from estructura_datos.arbol_avl.arbol_avl import ArbolAVL
from clases.libro import Libro
"""
def main():
    xml_manager: XMLManager = XMLManager()
    libros = xml_manager.cargar_todo()

    #codigo = input("Ingrese el código del libro: ") # El codigo es de tres dijitos
    #autor = input("Ingrese el nombre del autor:")
    #titulo = input("Ingrese el titulo del libro: ")
    #anio = input("Ingrese el año del libro: ")
    #editorial = input("Ingrese la editorial del libro: ")
    #area = input("Ingrese el area del libro: ")

    codigo: int =1
    autor:str ="Marcos Ferreto"
    titulo: str = "Pepo"
    anio: int = 2026
    editorial: str = "Poe"
    area: str = "Mate"


    libro: list = [{
        "codigo": codigo,
        "autor": autor,
        "titulo": titulo,
        "anio": anio,
        "editorial": editorial,
        "area": area
    }]


    xml_manager.guardar_libros(libro)
"""
def test_buscar_codigo():
    # Este objeto es el que se encarga de toda la logia, tanto para leer, escribir, validar un .xml, tambien con un json y tambien es utilizado para pasar de .xml a un objeto en python
    xml_manager = XMLManager()
    # Carga de los datos
    libros = xml_manager.cargar_libros()
    """-------------------------------------------------------------------------------------------"""
    # TODO: Implementación del main, por ahora en consola, después hacia GUI
    mi_arbol_avl: ArbolAVL = ArbolAVL()

    # Recorre y va insertando los objetos tipo libros en el arbol avl que están almacenados en /datos/libros.json
    for i in libros:
        # dict_a_libro pasa los libros que estan en un diccionario y los pasa a un objeto tipo libro
        libro: Libro = xml_manager.dict_a_libro(i)
        # TODO: Hay que arreglar la linea de abajo, debería ser mi_arbol_avl.insertar(mi_arbol_avl.raiz, libro)
        # BUG pero lo curioso es que sirve
        mi_arbol_avl.raiz = mi_arbol_avl.insertar(mi_arbol_avl.raiz, libro)

    mi_arbol_avl.mostrar(mi_arbol_avl.raiz)
    print("Buscar por codigo: ", end="")
    codigo: int = 1 # TODO: Cambiar la logica de xml_manager para que trabaje con enteros
    if mi_arbol_avl.buscar_codigo(mi_arbol_avl.raiz, codigo):
        print(f"El libro con código {codigo} existe")
    else:
        print(f"El libro con código {codigo} no existe")




    """-------------------------------------------------------------------------------------"""
    # Guardar datos al finalizar el programa
    xml_manager.guardar_libros(libros)

def test_buscar_titulo():
    xml_manager = XMLManager()
    libros = xml_manager.cargar_libros()
    mi_arbol_avl: ArbolAVL = ArbolAVL()

    for i in libros:
        libro: Libro = xml_manager.dict_a_libro(i)
        mi_arbol_avl.raiz = mi_arbol_avl.insertar(mi_arbol_avl.raiz, libro)

    mi_arbol_avl.mostrar(mi_arbol_avl.raiz)
    print("Buscar por titulo: ", end="")
    titulo: str = "Estructuras de Datos"
    if mi_arbol_avl.buscar_titulo(mi_arbol_avl.raiz, titulo):
        print(f"El libro '{titulo}' existe")
    else:
        print(f"El libro '{titulo}' no existe")

    xml_manager.guardar_libros(libros)


def test_buscar_autor():
    xml_manager = XMLManager()
    libros = xml_manager.cargar_libros()
    mi_arbol_avl: ArbolAVL = ArbolAVL()

    for i in libros:
        libro: Libro = xml_manager.dict_a_libro(i)
        mi_arbol_avl.raiz = mi_arbol_avl.insertar(mi_arbol_avl.raiz, libro)

    mi_arbol_avl.mostrar(mi_arbol_avl.raiz)
    print("Buscar por autor: ", end="")
    autor: str = "Silvia Guardi"
    if mi_arbol_avl.buscar_autor(mi_arbol_avl.raiz, autor):
        print(f"El autor '{autor}' existe")
    else:
        print(f"El autor '{autor}' no existe")

    xml_manager.guardar_libros(libros)


def test_eliminar_codigo():
    xml_manager = XMLManager()
    libros = xml_manager.cargar_libros()
    mi_arbol_avl: ArbolAVL = ArbolAVL()

    for i in libros:
        libro: Libro = xml_manager.dict_a_libro(i)
        mi_arbol_avl.raiz = mi_arbol_avl.insertar(mi_arbol_avl.raiz, libro)

    print("Arbol antes de eliminar:")
    mi_arbol_avl.mostrar(mi_arbol_avl.raiz)

    codigo: int = 2
    mi_arbol_avl.eliminar_codigo(mi_arbol_avl.raiz, codigo)

    print(f"Arbol despues de eliminar codigo {codigo}:")
    mi_arbol_avl.mostrar(mi_arbol_avl.raiz)

    xml_manager.guardar_libros(libros)


if __name__ == "__main__":
    #test_buscar_codigo()
    test_buscar_titulo()
    #test_buscar_autor()
    #test_eliminar_codigo()
