
from xml_manager import XMLManager
def main():
    # Pasar xml a
    xmt_manager = XMLManager()

    lista_estudiantes = xmt_manager.cargar_estudiantes()
    print("Lista de estudiantes: ", lista_estudiantes)

    lista_libros = xmt_manager.cargar_libros()
    print("Lista de libros: ", lista_libros)

    lista_prestamos = xmt_manager.cargar_prestamos()
    print("Lista de prestamos: ", lista_prestamos)

if __name__ == "__main__":
    main()
