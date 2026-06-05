import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clases.estudiante import Estudiante
from estructura_datos.tabla_hash.tabla_hash import TablaHash

"""
esta parte de arriba la hice la ia porque no me funcionaba
"""


def main():
    # tabla con un tamaño muy pequeño para forzar colisiones
    tabla = TablaHash(tam=2)

    # Crear estudiantes
    estudiante1 = Estudiante(1001, "Ana Garcia", "Informatica", "1111", "a@a.com", "Grecia")
    estudiante2 = Estudiante(1003, "Carlos Perez", "Administracion", "2222", "c@a.com",
                             "San Jose")  # 1001 % 2 = 1, 1003 % 2 = 1 (falla)
    estudiante3 = Estudiante(1005, "Beto Gomez", "Informatica", "3333", "b@a.com", "Alajuela")  # 1005 % 2 = 1 (falla)
    estudiante4 = Estudiante(1002, "Diana Rojas", "Diseno", "4444", "d@a.com", "Heredia")  # 1002 % 2 = 0

    # Insertar
    tabla.insertar(estudiante1)
    tabla.insertar(estudiante2)
    tabla.insertar(estudiante3)
    tabla.insertar(estudiante4)

    # Busqueda por carnet
    print("Buscar por carnet (1003):", tabla.buscar_por_carnet(1003))

    # Busqueda por nombre
    print("Buscar por nombre 'Ana Garcia':", tabla.buscar_por_nombre("Ana Garcia"))
    print("Buscar por nombre 'Beto gomez':", tabla.buscar_por_nombre("Beto gomez"))

    # Busqueda por carrera
    print("Buscar por carrera 'Informatica':", tabla.buscar_por_carrera("Informatica"))

    # Eliminar carnet 1003
    print("Eliminando 1003:", tabla.eliminar_estudiante(1003))
    print("Buscar por carnet 1003 después de eliminar:", tabla.buscar_por_carnet(1003))


if __name__ == "__main__":
    main()