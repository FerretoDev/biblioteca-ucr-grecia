"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto - Paulo Anchía Correás
Archivo: test_sistema_prestamos.py
"""

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clases.libro import Libro
from clases.estudiante import Estudiante
from clases.prestamo import Prestamo
from estructura_datos.arbol_avl.arbol_avl import ArbolAVL
from estructura_datos.arbol_rojinegro.arbol_rojinegro import ArbolRojinegro
from estructura_datos.tabla_hash.tabla_hash import TablaHash
from xml_manager import XMLManager
from sistema_prestamos import SistemaPrestamos


def construir_sistema():
    avl = ArbolAVL()
    avl.raiz = avl.insertar(avl.raiz, Libro(101, "Autor A", "Titulo A", 2020, "Ed A", "CS"))
    avl.raiz = avl.insertar(avl.raiz, Libro(102, "Autor B", "Titulo B", 2021, "Ed B", "CS"))

    tabla = TablaHash(10)
    tabla.insertar(Estudiante(2023001, "Ana", "Informatica", "88881111", "ana@ucr.ac.cr", "Grecia"))
    tabla.insertar(Estudiante(2023002, "Luis", "Contabilidad", "88882222", "luis@ucr.ac.cr", "Grecia"))

    arbol_rb = ArbolRojinegro()
    xml = XMLManager()

    return SistemaPrestamos(avl, tabla, arbol_rb, xml)


def main():
    print("=" * 60)
    print("PRUEBAS SISTEMA DE PRESTAMOS")
    print("=" * 60)

    sp = construir_sistema()

    # 1. Prestar libro existente a estudiante existente
    ok, msg = sp.dar_prestamo(101, 2023001)
    print(f"\n1. Prestar libro 101 a estudiante 2023001: {'OK' if ok else 'FAIL'}")
    print(f"   {msg}")
    assert ok

    # 2. Intentar prestar el mismo libro dos veces
    ok, msg = sp.dar_prestamo(101, 2023002)
    print(f"\n2. Prestar libro 101 ya prestado: {'RECHAZADO' if not ok else 'ERROR'}")
    print(f"   {msg}")
    assert not ok

    # 3. Prestar libro que no existe
    ok, msg = sp.dar_prestamo(999, 2023001)
    print(f"\n3. Prestar libro 999 inexistente: {'RECHAZADO' if not ok else 'ERROR'}")
    print(f"   {msg}")
    assert not ok

    # 4. Prestar a estudiante que no existe
    ok, msg = sp.dar_prestamo(102, 9999999)
    print(f"\n4. Prestar a estudiante 9999999 inexistente: {'RECHAZADO' if not ok else 'ERROR'}")
    print(f"   {msg}")
    assert not ok

    # 5. Consultar libro prestado
    prestado = sp.libro_esta_prestado(101)
    print(f"\n5. libro_esta_prestado(101): {prestado}")
    assert prestado

    # 6. Consultar libro libre
    libre = sp.libro_esta_prestado(102)
    print(f"   libro_esta_prestado(102): {libre}")
    assert not libre

    # 7. Consultar si estudiante tiene prestamos
    tiene = sp.estudiante_tiene_prestamos(2023001)
    print(f"\n6. estudiante_tiene_prestamos(2023001): {tiene}")
    assert tiene

    no_tiene = sp.estudiante_tiene_prestamos(2023002)
    print(f"   estudiante_tiene_prestamos(2023002): {no_tiene}")
    assert not no_tiene

    # 8. Devolver libro
    prestamos = sp.listar_prestamos()
    codigo = prestamos[0].codigo_prestamo
    ok, msg = sp.devolver_libro(codigo)
    print(f"\n7. Devolver prestamo {codigo}: {'OK' if ok else 'FAIL'}")
    print(f"   {msg}")
    assert ok

    # 9. Ya no esta prestado
    sigue = sp.libro_esta_prestado(101)
    print(f"\n8. libro_esta_prestado(101) tras devolucion: {sigue}")
    assert not sigue

    # 10. Devolver prestamo que no existe
    ok, msg = sp.devolver_libro(9999)
    print(f"\n9. Devolver prestamo 9999 inexistente: {'RECHAZADO' if not ok else 'ERROR'}")
    print(f"   {msg}")
    assert not ok

    print("\n" + "=" * 60)
    print("TODAS LAS PRUEBAS PASARON")
    print("=" * 60)

if __name__ == "__main__":
    main()
