from xml_manager import XMLManager
from estructura_datos.arbol_avl.arbol_avl import ArbolAVL
from clases.libro import Libro
def main():
    # Este objeto es el que se encarga de toda la logia, tanto para leer, escribir, validar un .xml, tambien con un json y tambien es utilizado para pasar de .xml a un objeto en python
    xml_manager = XMLManager()
    # Carga de los datos
    libros, estudiantes, prestamos = xml_manager.cargar_todo()
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
    # print(mi_arbol_avl.raiz)
    print("Buscar por codigo: ", end="")
    codigo: int = 4
    if mi_arbol_avl.buscar_codigo(mi_arbol_avl.raiz, codigo):
        print(f"El libro con código {codigo} existe")
    else:
        print(f"El libro con código {codigo} no existe")

    # Pruebas que hice para comprobar si los hijos de las raiz_p existían
    #print("Pruebas")
    #print(mi_arbol_avl.raiz)
    #print(mi_arbol_avl.raiz.izq)
    #print(mi_arbol_avl.raiz.der)


    """-------------------------------------------------------------------------------------"""
    # Guardar datos al finalizar el programa
    xml_manager.guardar_todo(libros, estudiantes, prestamos)
    xml_manager.guardar_json(libros, estudiantes, prestamos)



if __name__ == "__main__":
    main()
