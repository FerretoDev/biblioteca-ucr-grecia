"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto - Paulo Anchía Correás
Archivo: test_arbol_rojinegro.py
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clases.prestamo import Prestamo
from estructura_datos.arbol_rojinegro.arbol_rojinegro import ArbolRojinegro as RBTree
from estructura_datos.arbol_rojinegro.nodo import Nodo
from typing import Optional




def _verificar_colores(nodo: Optional[Nodo]) -> bool:
    if nodo is None:
        return True
    if nodo.color not in ["Rojo", "Negro"]:
        return False
    return (_verificar_colores(nodo.izq) and _verificar_colores(nodo.der))

def _verificar_raiz_negra(arbol: RBTree) -> bool:
    if arbol.raiz is None:
        return True
    return arbol.raiz.color == "Negro"

def _verificar_rojo_padre_negro(nodo: Optional[Nodo]) -> bool:
    if nodo is None:
        return True
    if nodo.color == "Rojo":
        if nodo.izq is not None and nodo.izq.color == "Rojo":
            return False
        if nodo.der is not None and nodo.der.color == "Rojo":
            return False
    return (_verificar_rojo_padre_negro(nodo.izq) and 
            _verificar_rojo_padre_negro(nodo.der))

def _verificar_altura_negra(nodo: Optional[Nodo]) -> int:
    if nodo is None:
        return 1  # Las hojas NIL son negras
    altura_izq = _verificar_altura_negra(nodo.izq)
    altura_der = _verificar_altura_negra(nodo.der)
    if altura_izq == -1 or altura_der == -1 or altura_izq != altura_der:
        return -1
    if nodo.color == "Negro":
        return altura_izq + 1
    else:
        return altura_izq

def verificar_propiedades_rb(arbol: RBTree) -> dict:
    resultado = {
        "propiedad_1_colores": _verificar_colores(arbol.raiz),
        "propiedad_2_raiz_negra": _verificar_raiz_negra(arbol),
        "propiedad_4_rojo_hijos_negros": _verificar_rojo_padre_negro(arbol.raiz),
        "propiedad_5_altura_negra": _verificar_altura_negra(arbol.raiz) >= 0,
        "arbol_valido": True
    }
    if not all([resultado["propiedad_1_colores"], 
               resultado["propiedad_2_raiz_negra"],
               resultado["propiedad_4_rojo_hijos_negros"],
               resultado["propiedad_5_altura_negra"]]):
        resultado["arbol_valido"] = False
    return resultado

def main() -> None:
    """
    Parámetros: ninguno
    Devuelve:   None
    Descripción:
        Función principal que realiza pruebas exhaustivas del árbol Rojinegro.
        Inserta mas de 15 préstamos, verifica propiedades RB, elimina nodos y valida
        la integridad del árbol en cada operación.
    """

    print("=" * 80)
    print("PRUEBAS DEL ÁRBOL ROJINEGRO - SISTEMA DE GESTIÓN DE BIBLIOTECA UCR")
    print("=" * 80)

    arbol_rb = RBTree()

    print("\n" + "=" * 80)
    print("1. INSERTANDO 15+ PRÉSTAMOS EN EL ÁRBOL")
    print("=" * 80)

    # préstamos de prueba
    prestamos_prueba = [
        Prestamo(1, 102, 2023, "2024-06-10"),
        Prestamo(2, 105, 2025, "2024-06-11"),
        Prestamo(3, 101, 2024, "2024-06-12"),
        Prestamo(4, 103, 2022, "2024-06-13"),
        Prestamo(5, 104, 2021, "2024-06-14"),
        Prestamo(6, 107, 2026, "2024-06-15"),
        Prestamo(7, 106, 2027, "2024-06-16"),
        Prestamo(8, 108, 2028, "2024-06-17"),
        Prestamo(9, 109, 2029, "2024-06-18"),
        Prestamo(10, 110, 2030, "2024-06-19"),
        Prestamo(11, 111, 2031, "2024-06-20"),
        Prestamo(12, 112, 2032, "2024-06-21"),
        Prestamo(13, 113, 2033, "2024-06-22"),
        Prestamo(14, 114, 2034, "2024-06-23"),
        Prestamo(15, 115, 2035, "2024-06-24"),
        Prestamo(16, 116, 2036, "2024-06-25"),
    ]

    # Inserta cada préstamo y verificar propiedades RB
    for prestamo in prestamos_prueba:
        arbol_rb.insertar(arbol_rb.raiz, prestamo)
        print(
            f"Insertado préstamo código {prestamo.codigo_prestamo}: "
            f"Libro {prestamo.codigo_libro}, Estudiante {prestamo.carnet_estudiante}"
        )

    print(f"\nTotal de préstamos insertados: {len(prestamos_prueba)}")

    print("\n" + "-" * 80)
    print("RECORRIDO INORDEN (Verificar orden ascendente)")
    print("-" * 80)
    
    def imprimir_inorden_con_color(raiz_p):
        if raiz_p is not None:
            imprimir_inorden_con_color(raiz_p.izq)
            prestamo = raiz_p.valor
            print(f"Código: {prestamo.codigo_prestamo} | Color: {raiz_p.color} | Libro: {prestamo.codigo_libro} | Estudiante: {prestamo.carnet_estudiante}")
            imprimir_inorden_con_color(raiz_p.der)
    
    imprimir_inorden_con_color(arbol_rb.raiz)



    # Verificar propiedades después de inserciones
    print("\n" + "=" * 80)
    print("2. VERIFICACIÓN DE PROPIEDADES ROJINEGRAS DESPUÉS DE INSERCIONES")
    print("=" * 80)
    propiedades = verificar_propiedades_rb(arbol_rb)

    print(
        f"\nPropiedad 1 (Todos los nodos son rojo o negro): {propiedades['propiedad_1_colores']}"
    )
    print(f"Propiedad 2 (La raíz es negra): {propiedades['propiedad_2_raiz_negra']}")
    print(
        f"Propiedad 4 (Si rojo, hijos negros): {propiedades['propiedad_4_rojo_hijos_negros']}"
    )
    print(
        f"Propiedad 5 (Altura negra consistente): {propiedades['propiedad_5_altura_negra']}"
    )
    print(f"\n{'ÁRBOL VÁLIDO' if propiedades['arbol_valido'] else 'ÁRBOL INVÁLIDO'}")

    # Búsqueda
    print("\n" + "=" * 80)
    print("3. PRUEBAS DE BÚSQUEDA")
    print("=" * 80)

    codigos_buscar = [5, 10, 15, 9999]

    for codigo in codigos_buscar:
        prestamo_encontrado = arbol_rb.buscar_codigo(arbol_rb.raiz, codigo)
        if prestamo_encontrado:
            print(f"Préstamo {codigo} encontrado:")
            print(f"   {prestamo_encontrado}")
        else:
            print(f"Préstamo {codigo} NO encontrado")

    # Eliminación
    print("\n" + "=" * 80)
    print("4. ELIMINACIÓN DE PRÉSTAMOS Y VERIFICACIÓN DE PROPIEDADES")
    print("=" * 80)

    codigos_eliminar = [5, 10, 3]

    for codigo in codigos_eliminar:
        print(f"\nEliminando préstamo {codigo}...")
        resultado = arbol_rb.eliminar_codigo(arbol_rb.raiz, codigo)

        if resultado:
            print(f"Préstamo {codigo} eliminado exitosamente")

            # Verificar propiedades después de cada eliminación
            propiedades = verificar_propiedades_rb(arbol_rb)
            print(f"Árbol válido: {'SÍ' if propiedades['arbol_valido'] else 'NO'}")

            if not propiedades["arbol_valido"]:
                print(f"Propiedad 1: {propiedades['propiedad_1_colores']}")
                print(f"Propiedad 2: {propiedades['propiedad_2_raiz_negra']}")
                print(f"Propiedad 4: {propiedades['propiedad_4_rojo_hijos_negros']}")
                print(f"Propiedad 5: {propiedades['propiedad_5_altura_negra']}")
        else:
            print(f" Préstamo {codigo} no existe")

    # Mostrar estado actual
    print("\n" + "-" * 80)
    print("INORDEN DESPUÉS DE ELIMINACIONES")
    print("-" * 80)
    
    def imprimir_inorden_con_color(raiz_p):
        if raiz_p is not None:
            imprimir_inorden_con_color(raiz_p.izq)
            prestamo = raiz_p.valor
            print(f"Código: {prestamo.codigo_prestamo} | Color: {raiz_p.color} | Libro: {prestamo.codigo_libro} | Estudiante: {prestamo.carnet_estudiante}")
            imprimir_inorden_con_color(raiz_p.der)
    
    imprimir_inorden_con_color(arbol_rb.raiz)


    # lista de préstamos (para GUI)
    print("\n" + "=" * 80)
    print("5. OBTENCIÓN DE LISTA DE PRÉSTAMOS (Para GUI)")
    print("=" * 80)

    lista_prestamos = arbol_rb.inorden(arbol_rb.raiz)
    print(f"\nTotal de préstamos en el árbol: {len(lista_prestamos)}\n")

    for i, prestamo in enumerate(lista_prestamos, 1):
        print(f"{i:2d}. {prestamo}")

    # Prueba de árbol vacío
    print("\n" + "=" * 80)
    print("6. PRUEBA DE VALIDACIÓN - ÁRBOL VACÍO")
    print("=" * 80)

    arbol_vacio = RBTree()
    print(f"Árbol vacío está vacío?: {arbol_vacio.esta_vacia()}")
    print(
        f"Propiedades de árbol vacío válidas: {verificar_propiedades_rb(arbol_vacio)['arbol_valido']}"
    )

    # Prueba de duplicados
    print("\n" + "=" * 80)
    print("7. PRUEBA DE INSERCIÓN DE DUPLICADOS")
    print("=" * 80)

    print("\nIntentando insertar préstamo duplicado (código 0001)...")
    prestamo_duplicado = Prestamo(1, 999, 9999, "2024-07-01")
    arbol_rb.insertar(arbol_rb.raiz, prestamo_duplicado)
    print("Duplicado rechazado (código 0001 ya existe)")

    # Verificación ultima
    print("\n" + "=" * 80)
    print("8. VERIFICACIÓN FINAL")
    print("=" * 80)

    propiedades_final = verificar_propiedades_rb(arbol_rb)
    lista_final = arbol_rb.inorden(arbol_rb.raiz)

    print(f"\n Préstamos en el árbol: {len(lista_final)}")
    print(
        f" Árbol Rojinegro válido: {'SÍ' if propiedades_final['arbol_valido'] else 'NO'}"
    )
    print(
        f" Raíz es negra: {'SÍ' if propiedades_final['propiedad_2_raiz_negra'] else 'NO'}"
    )
    print(
        f" Altura negra consistente: {'SÍ' if propiedades_final['propiedad_5_altura_negra'] else 'NO'}"
    )

    print("\n" + "=" * 80)
    print("PRUEBAS COMPLETADAS EXITOSAMENTE")  # en caso de que todo funcione biens
    print("=" * 80)


if __name__ == "__main__":
    main()
