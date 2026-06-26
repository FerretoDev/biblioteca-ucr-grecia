"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto - Paulo Anchía Correás
Archivo: test.py
"""

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
    for libro in libros:
        mi_arbol_avl.raiz = mi_arbol_avl.insertar(mi_arbol_avl.raiz, libro)

    for libro in mi_arbol_avl.obtener_libros_inorden(mi_arbol_avl.raiz): print(libro)
    print("Buscar por codigo: ", end="")
    codigo: int = 1
    libro = mi_arbol_avl.buscar_codigo(mi_arbol_avl.raiz, codigo)
    if libro is not None:
        print(f"El libro con código {codigo} existe: {libro}")
    else:
        print(f"El libro con código {codigo} no existe")

    """-------------------------------------------------------------------------------------"""
    # Guardar datos al finalizar el programa
    xml_manager.guardar_libros(libros)

def test_buscar_titulo():
    xml_manager = XMLManager()
    libros = xml_manager.cargar_libros()
    mi_arbol_avl: ArbolAVL = ArbolAVL()

    for libro in libros:
        mi_arbol_avl.raiz = mi_arbol_avl.insertar(mi_arbol_avl.raiz, libro)

    for libro in mi_arbol_avl.obtener_libros_inorden(mi_arbol_avl.raiz): print(libro)
    print("Buscar por titulo: ", end="")
    titulo: str = "Estructuras de Datos"
    libro = mi_arbol_avl.buscar_titulo(mi_arbol_avl.raiz, titulo)
    if libro is not None:
        print(f"El libro '{titulo}' existe: {libro}")
    else:
        print(f"El libro '{titulo}' no existe")

    xml_manager.guardar_libros(libros)


def test_buscar_autor():
    xml_manager = XMLManager()
    libros = xml_manager.cargar_libros()
    mi_arbol_avl: ArbolAVL = ArbolAVL()

    for libro in libros:
        mi_arbol_avl.raiz = mi_arbol_avl.insertar(mi_arbol_avl.raiz, libro)

    for libro in mi_arbol_avl.obtener_libros_inorden(mi_arbol_avl.raiz): print(libro)
    print("Buscar por autor: ", end="")
    autor: str = "Silvia Guardi"
    libros_autor = mi_arbol_avl.buscar_autor(mi_arbol_avl.raiz, autor)
    if libros_autor:
        print(f"El autor '{autor}' tiene los siguientes libros: {[str(l) for l in libros_autor]}")
    else:
        print(f"El autor '{autor}' no existe o no tiene libros")

    xml_manager.guardar_libros(libros)


def test_eliminar_codigo():
    xml_manager = XMLManager()
    libros = xml_manager.cargar_libros()
    mi_arbol_avl: ArbolAVL = ArbolAVL()

    for libro in libros:
        mi_arbol_avl.raiz = mi_arbol_avl.insertar(mi_arbol_avl.raiz, libro)

    print("Arbol antes de eliminar:")
    for libro in mi_arbol_avl.obtener_libros_inorden(mi_arbol_avl.raiz): print(libro)

    codigo: int = 2
    mi_arbol_avl.raiz = mi_arbol_avl.eliminar_codigo(mi_arbol_avl.raiz, codigo)

    print(f"Arbol despues de eliminar codigo {codigo}:")
    for libro in mi_arbol_avl.obtener_libros_inorden(mi_arbol_avl.raiz): print(libro)

    xml_manager.guardar_libros(libros)

def test_rotacion_ii():
    """
    Parámetros: ninguno
    Devuelve:   None
    Descripción:
        Prueba el caso Izquierda-Izquierda (II) insertando [30, 20, 10]
        y verificando que se aplique la rotación simple a la derecha.
    """
    print("\n--- Test de Rotación II (Simple Derecha) ---")
    lista = [30, 20, 10]
    avl = ArbolAVL()
    for i in lista:
        avl.raiz = avl.insertar(avl.raiz, Libro(codigo=i, autor="", titulo="", anio=0, editorial="", area=""))
    print("Árbol final (debería tener 20 como raíz):")
    for libro in avl.obtener_libros_inorden(avl.raiz): print(libro)
    assert avl.raiz is not None
    assert avl.raiz.valor.codigo == 20, "Fallo: La raíz debería ser 20"
    assert avl.raiz.izq is not None and avl.raiz.izq.valor.codigo == 10, "Fallo: El hijo izquierdo debería ser 10"
    assert avl.raiz.der is not None and avl.raiz.der.valor.codigo == 30, "Fallo: El hijo derecho debería ser 30"
    print("ÉXITO: Rotación II funcionó correctamente")


def test_rotacion_dd():
    """
    Parámetros: ninguno
    Devuelve:   None
    Descripción:
        Prueba el caso Derecha-Derecha (DD) insertando [10, 20, 30]
        y verificando que se aplique la rotación simple a la izquierda.
    """
    print("\n--- Test de Rotación DD (Simple Izquierda) ---")
    lista = [10, 20, 30]
    avl = ArbolAVL()
    for i in lista:
        avl.raiz = avl.insertar(avl.raiz, Libro(codigo=i, autor="", titulo="", anio=0, editorial="", area=""))
    print("Árbol final (debería tener 20 como raíz):")
    for libro in avl.obtener_libros_inorden(avl.raiz): print(libro)
    assert avl.raiz is not None
    assert avl.raiz.valor.codigo == 20, "Fallo: La raíz debería ser 20"
    assert avl.raiz.izq is not None and avl.raiz.izq.valor.codigo == 10, "Fallo: El hijo izquierdo debería ser 10"
    assert avl.raiz.der is not None and avl.raiz.der.valor.codigo == 30, "Fallo: El hijo derecho debería ser 30"
    print("ÉXITO: Rotación DD funcionó correctamente")


def test_rotacion_id():
    """
    Parámetros: ninguno
    Devuelve:   None
    Descripción:
        Prueba el caso Izquierda-Derecha (ID) insertando [30, 10, 20]
        y verificando que se aplique la rotación doble izquierda-derecha.
    """
    print("\n--- Test de Rotación ID (Doble Izquierda-Derecha) ---")
    lista = [30, 10, 20]
    avl = ArbolAVL()
    for i in lista:
        avl.raiz = avl.insertar(avl.raiz, Libro(codigo=i, autor="", titulo="", anio=0, editorial="", area=""))
    print("Árbol final (debería tener 20 como raíz):")
    for libro in avl.obtener_libros_inorden(avl.raiz): print(libro)
    assert avl.raiz is not None
    assert avl.raiz.valor.codigo == 20, "Fallo: La raíz debería ser 20"
    assert avl.raiz.izq is not None and avl.raiz.izq.valor.codigo == 10, "Fallo: El hijo izquierdo debería ser 10"
    assert avl.raiz.der is not None and avl.raiz.der.valor.codigo == 30, "Fallo: El hijo derecho debería ser 30"
    print("ÉXITO: Rotación ID funcionó correctamente")


def test_rotacion_di():
    """
    Parámetros: ninguno
    Devuelve:   None
    Descripción:
        Prueba el caso Derecha-Izquierda (DI) insertando [10, 30, 20]
        y verificando que se aplique la rotación doble derecha-izquierda.
    """
    print("\n--- Test de Rotación DI (Doble Derecha-Izquierda) ---")
    lista = [10, 30, 20]
    avl = ArbolAVL()
    for i in lista:
        avl.raiz = avl.insertar(avl.raiz, Libro(codigo=i, autor="", titulo="", anio=0, editorial="", area=""))
    print("Árbol final (debería tener 20 como raíz):")
    for libro in avl.obtener_libros_inorden(avl.raiz): print(libro)
    assert avl.raiz is not None
    assert avl.raiz.valor.codigo == 20, "Fallo: La raíz debería ser 20"
    assert avl.raiz.izq is not None and avl.raiz.izq.valor.codigo == 10, "Fallo: El hijo izquierdo debería ser 10"
    assert avl.raiz.der is not None and avl.raiz.der.valor.codigo == 30, "Fallo: El hijo derecho debería ser 30"
    print("ÉXITO: Rotación DI funcionó correctamente")


def test_inorden():
    """
    Parámetros: ninguno
    Devuelve:   None
    Descripción:
        Prueba el recorrido inorden (impresión y retorno de lista) en el árbol AVL.
    """
    print("\n--- Test de Recorrido Inorden ---")
    lista = [50, 30, 70, 20, 40, 60, 80]
    avl = ArbolAVL()
    for i in lista:
        avl.raiz = avl.insertar(avl.raiz, Libro(codigo=i, autor="", titulo="", anio=0, editorial="", area=""))

    print("Imprimiendo árbol en inorden (debería salir de 20 a 80 en orden):")
    for libro in avl.obtener_libros_inorden(avl.raiz): print(libro)
    
    # Probar retorno de la lista para la GUI
    recorrido_lista = avl.obtener_libros_inorden(avl.raiz)
    codigos_resultado = [l.codigo for l in recorrido_lista]
    print(f"Lista para GUI obtenida: {codigos_resultado}")
    assert codigos_resultado == sorted(lista), f"Fallo: La lista debería ser {sorted(lista)}"
    print("ÉXITO: Recorrido inorden ejecutado y lista para GUI validada")


if __name__ == "__main__":
    test_buscar_codigo()
    test_buscar_titulo()
    test_buscar_autor()
    test_eliminar_codigo()
    test_inorden()
    """Test de rotaciones"""
    test_rotacion_ii()
    test_rotacion_dd()
    test_rotacion_id()
    test_rotacion_di()
