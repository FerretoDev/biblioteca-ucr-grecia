from xml_manager import XMLManager


def test():
    """
    Parámetros: ninguno
    Devuelve:   None
    Descripción:

    """
    xml_manager = XMLManager()
    print("Cargando datos delimitados por % desde .xml a JSON...")
    libros, estudiantes, prestamos = xml_manager.cargar_todo()

    print("Trabajando con JSON en memoria...")
    print("Libros (JSON):", libros)
    print("Estudiantes (JSON):", estudiantes)
    print("Prestamos (JSON):", prestamos)

    print("Guardando JSON a .xml con delimitacion %...")
    xml_manager.guardar_todo(libros, estudiantes, prestamos)
    print("Guardando JSON a .json para inspeccion...")
    xml_manager.guardar_json(libros, estudiantes, prestamos)


def main():
    ...
if __name__ == "__main__":
    test()
