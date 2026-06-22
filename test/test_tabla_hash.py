import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clases.estudiante import Estudiante
from estructura_datos.tabla_hash.tabla_hash import TablaHash


@pytest.fixture
def tabla():
    """
    Criterio de Aceptación: Configuración de la Tabla e Inserción con Colisiones.
    Dado que se inicializa la clase TablaHash con un tamaño pequeño (2),
    cuando se insertan estudiantes que generan el mismo hash (ej. 1001, 1003, 1005),
    entonces deben alojarse en la misma lista enlazada simulando colisiones.
    """
    t = TablaHash(tamanio=2)

    estudiantes = [
        Estudiante(1001, "Ana Garcia", "Informatica", "1111", "a@a.com", "Grecia"),
        Estudiante(
            1003, "Carlos Perez", "Administracion", "2222", "c@a.com", "San Jose"
        ),
        Estudiante(1005, "Beto Gomez", "Informatica", "3333", "b@a.com", "Alajuela"),
        Estudiante(1002, "Diana Rojas", "Diseno", "4444", "d@a.com", "Heredia"),
    ]

    for est in estudiantes:
        t.insertar(est)

    return t


def test_insertar_y_buscar_por_carnet(tabla):
    """
    Criterio de Aceptación: Búsqueda Directa por Carnet.
    Dado que existen estudiantes en la tabla (con colisiones en el mismo índice),
    cuando se busca por un carnet específico,
    entonces la tabla retorna los datos exactos del estudiante correcto iterando su sublista.
    """
    estudiante = tabla.buscar_por_carnet(1003)
    assert estudiante is not None
    assert estudiante.nombre == "Carlos Perez"
    assert estudiante.carnet == 1003


def test_buscar_inexistente(tabla):
    """
    Criterio de Aceptación: Búsqueda de Carnet Inexistente.
    Cuando se busca un carnet que no ha sido registrado,
    entonces debe retornar None de manera controlada.
    """
    assert tabla.buscar_por_carnet(9999) is None


def test_buscar_por_nombre(tabla):
    """
    Criterio de Aceptación: Búsqueda Transversal por Nombre.
    Dado que se realiza una búsqueda por nombre,
    cuando el estudiante existe en cualquier sublista de la tabla,
    entonces debe retornar sus datos completos sin importar si hay mayúsculas o minúsculas.
    """
    estudiante1 = tabla.buscar_por_nombre("Ana Garcia")
    assert estudiante1 is not None
    assert estudiante1.carnet == 1001

    estudiante2 = tabla.buscar_por_nombre("Beto gomez")
    assert estudiante2 is not None
    assert estudiante2.carnet == 1005


def test_buscar_por_carrera(tabla):
    """
    Criterio de Aceptación: Búsqueda Transversal por Carrera.
    Dado que se realiza una búsqueda por carrera,
    cuando se ejecuta la consulta,
    entonces debe retornar una lista únicamente con los nombres de todos los estudiantes en ella.
    """
    nombres = tabla.buscar_por_carrera("Informatica")
    assert len(nombres) == 2
    assert "Ana Garcia" in nombres
    assert "Beto Gomez" in nombres

    assert tabla.buscar_por_carrera("Arquitectura") == []


def test_eliminar_estudiante(tabla):
    """
    Criterio de Aceptación: Eliminación por Carnet.
    Dado que un estudiante no tiene préstamos activos,
    cuando se solicita su eliminación mediante el carnet,
    entonces debe ser borrado correctamente de la lista enlazada a la que pertenece
    y las búsquedas posteriores deben retornar None.
    """
    assert tabla.buscar_por_carnet(1003) is not None

    eliminado = tabla.eliminar_estudiante(1003)
    assert eliminado is True

    assert tabla.buscar_por_carnet(1003) is None

    assert tabla.eliminar_estudiante(1003) is False

