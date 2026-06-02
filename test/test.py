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

if __name__ == "__main__":

    test_buscar_codigo()
