"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto - Paulo Anchía Correás
Archivo: criterio_aceptacion_arbol_avl.py
"""

from pathlib import Path
import sys

# Asegurar que la raíz del proyecto esté en el PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from clases.libro import Libro
from estructura_datos.arbol_avl.arbol_avl import ArbolAVL


def ejecutar_criterio_aceptacion():
    """
    Parámetros: ninguno
    Devuelve:   None
    Descripción:
        Ejecuta el criterio de aceptación del AVL de libros:
        1. Inserta 10+ libros.
        2. Realiza búsquedas por código (O log n), título (recorrido inorden) y autor.
        3. Realiza la eliminación de un libro que provoca un desbalance.
        4. Verifica que el árbol se rebalancee correctamente tras la eliminación.
    """
    print("==================================================")
    print("      CRITERIO DE ACEPTACIÓN: ÁRBOL AVL")
    print("==================================================\n")

    # 1. Instanciar el árbol e insertar 10 libros
    # Insertamos en el orden: [50, 30, 70, 20, 40, 60, 85, 10, 80, 90]
    avl = ArbolAVL()
    libros = [
        Libro(50, "Autor Principal", "Estructuras de Datos", 2026, "UCR", "Computación"),
        Libro(30, "Silvia Guardi", "Matemáticas Discretas", 2006, "McGrawHill", "Matemáticas"),
        Libro(70, "Francisco Sevilla", "Algoritmos Complejos", 2018, "O'Reilly", "Computación"),
        Libro(20, "Silvia Guardi", "Álgebra Lineal", 2010, "Pearson", "Matemáticas"),
        Libro(40, "Veronica Rojas", "Introducción a Python", 2022, "Alfaomega", "Programación"),
        Libro(60, "Francisco Sevilla", "Bases de Datos", 2015, "Springer", "Computación"),
        Libro(85, "Silvia Guardi", "Cálculo I", 2012, "Pearson", "Matemáticas"),
        Libro(10, "Marcos Ferreto", "Compiladores", 2024, "UCR", "Computación"),
        Libro(80, "Paulo Anchia", "Redes de Computadoras", 2021, "UCR", "Computación"),
        Libro(90, "Veronica Rojas", "Inteligencia Artificial", 2025, "Springer", "Computación"),
    ]

    print("--- 1. Insertando 10 libros en el AVL ---")
    for libro in libros:
        avl.raiz = avl.insertar(avl.raiz, libro)
    print("Libros insertados con éxito.\n")

    # Mostrar árbol en preorder
    print("Árbol en Preorder (Raíz -> Izq -> Der):")
    avl.mostrar(avl.raiz)
    print()

    # Mostrar árbol en inorden
    print("Árbol en Inorden (Ordenado por código de menor a mayor):")
    avl.inorden(avl.raiz)
    print()

    # 2. Búsquedas
    print("--- 2. Probando Búsquedas ---")
    
    # Búsqueda por código (O log n)
    print("\n* Búsqueda por Código (70):")
    libro_cod = avl.buscar_codigo(avl.raiz, 70)
    if libro_cod:
        print(f"  ENCONTRADO: {libro_cod}")
    else:
        print("  ERROR: Libro no encontrado por código.")
    assert libro_cod is not None and libro_cod.codigo == 70

    # Búsqueda por título (Inorden)
    print("\n* Búsqueda por Título ('Introducción a Python'):")
    libro_tit = avl.buscar_titulo(avl.raiz, "Introducción a Python")
    if libro_tit:
        print(f"  ENCONTRADO: {libro_tit}")
    else:
        print("  ERROR: Libro no encontrado por título.")
    assert libro_tit is not None and libro_tit.titulo == "Introducción a Python"

    # Búsqueda por autor (Muestra todos los libros del autor)
    print("\n* Búsqueda por Autor ('Silvia Guardi'):")
    libros_autor = avl.buscar_autor(avl.raiz, "Silvia Guardi")
    print(f"  Encontrados {len(libros_autor)} libros:")
    for l in libros_autor:
        print(f"  - {l}")
    assert len(libros_autor) == 3

    # 3. Eliminación con Rebalanceo
    print("\n--- 3. Probando Eliminación con Rebalanceo ---")
    # Para provocar un desbalance en el nodo 30, eliminamos el nodo 40.
    # Antes de eliminar, 30 tiene:
    #   Hijo izquierdo 20 (altura 2, pues tiene al 10)
    #   Hijo derecho 40 (altura 1, es hoja)
    # Tras borrar 40, el factor de equilibrio de 30 se convierte en fe = 0 - 2 = -2.
    # El hijo izquierdo 20 tiene fe = -1 (tiene al 10 en izq).
    # Esto activará la rotación simple a la derecha (rotacion_ii) en el nodo 30,
    # haciendo que 20 sea la nueva raíz del subárbol izquierdo, con 10 a la izq y 30 a la der.
    
    print("Eliminando el libro con código 40 (Introducción a Python)...")
    avl.raiz = avl.eliminar_codigo(avl.raiz, 40)
    print("Eliminación completada.\n")

    # 4. Verificar Rebalanceo
    print("--- 4. Verificando el Rebalanceo ---")
    print("Árbol en Preorder tras la eliminación:")
    avl.mostrar(avl.raiz)
    print()

    # Validamos la estructura rebalanceada
    # La raíz sigue siendo 50
    assert avl.raiz is not None and avl.raiz.valor.codigo == 50
    # El hijo izquierdo de 50 ahora debe ser 20 (en vez de 30) debido a la rotación II
    assert avl.raiz.izq is not None and avl.raiz.izq.valor.codigo == 20, "Fallo: La raíz del subárbol izquierdo debería ser 20"
    # El hijo izquierdo de 20 debe ser 10
    assert avl.raiz.izq.izq is not None and avl.raiz.izq.izq.valor.codigo == 10
    # El hijo derecho de 20 debe ser 30
    assert avl.raiz.izq.der is not None and avl.raiz.izq.der.valor.codigo == 30

    print("¡ÉXITO: El árbol se rebalanceó correctamente después de la eliminación!")
    print("==================================================")


if __name__ == "__main__":
    ejecutar_criterio_aceptacion()
