from xml_manager import XMLManager
from estructura_datos.arbol_avl.arbol_avl import ArbolAVL

def main():

    xml_manager = XMLManager()
    # Cargando datos
    libros, estudiantes, prestamos = xml_manager.cargar_todo()
    """-------------------------------------------------------------------------------------------"""

    mi_arbol_avl: ArbolAVL = ArbolAVL()

    for i in libros:
        libro = xml_manager.dict_a_libro(i)
        # TODO Hay que arreglar la linea de abajo, deberia ser mi_arbol_avl.insertar(mi_arbol_avl.raiz, libro)
        # BUG pero lo curioso es que sirve
        mi_arbol_avl.raiz = mi_arbol_avl.insertar(mi_arbol_avl.raiz, libro)

    mi_arbol_avl.mostrar(mi_arbol_avl.raiz)
    print(mi_arbol_avl.raiz)


    # Pruebas
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
