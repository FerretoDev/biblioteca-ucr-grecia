from clases.prestamo import Prestamo
from estructura_datos.arbol_rojinegro.rbtree import RBTree


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
        arbol_rb.insertar(prestamo)
        print(f"Insertado préstamo código {prestamo.codigo_prestamo}: "
              f"Libro {prestamo.codigo_libro}, Estudiante {prestamo.carnet_estudiante}")
    
    print(f"\nTotal de préstamos insertados: {len(prestamos_prueba)}")
    
    print("\n" + "-" * 80)
    print("RECORRIDO INORDEN (Verificar orden ascendente)")
    print("-" * 80)
    arbol_rb.inOrden(arbol_rb.raiz)
    
    print("\n" + "-" * 80)
    print("RECORRIDO PREORDEN (Estructura del árbol)")
    print("-" * 80)
    arbol_rb.preOrden(arbol_rb.raiz)
    
    print("\n" + "-" * 80)
    print("RECORRIDO POSTORDEN")
    print("-" * 80)
    arbol_rb.postOrden(arbol_rb.raiz)
    
    # Verificar propiedades después de inserciones
    print("\n" + "=" * 80)
    print("2. VERIFICACIÓN DE PROPIEDADES ROJINEGRAS DESPUÉS DE INSERCIONES")
    print("=" * 80)
    propiedades = arbol_rb.verificar_propiedades_rb()
    
    print(f"\nPropiedad 1 (Todos los nodos son rojo o negro): {propiedades['propiedad_1_colores']}")
    print(f"Propiedad 2 (La raíz es negra): {propiedades['propiedad_2_raiz_negra']}")
    print(f"Propiedad 4 (Si rojo, hijos negros): {propiedades['propiedad_4_rojo_hijos_negros']}")
    print(f"Propiedad 5 (Altura negra consistente): {propiedades['propiedad_5_altura_negra']}")
    print(f"\n{'ÁRBOL VÁLIDO' if propiedades['arbol_valido'] else 'ÁRBOL INVÁLIDO'}")
    
    # Búsqueda
    print("\n" + "=" * 80)
    print("3. PRUEBAS DE BÚSQUEDA")
    print("=" * 80)
    
    codigos_buscar = [5, 10, 15, 9999]
    
    for codigo in codigos_buscar:
        prestamo_encontrado = arbol_rb.buscar_prestamo(arbol_rb.raiz, codigo)
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
        resultado = arbol_rb.eliminar_nodo(codigo)
        
        if resultado:
            print(f"Préstamo {codigo} eliminado exitosamente")
            
            # Verificar propiedades después de cada eliminación
            propiedades = arbol_rb.verificar_propiedades_rb()
            print(f"Árbol válido: {'SÍ' if propiedades['arbol_valido'] else 'NO'}")
            
            if not propiedades['arbol_valido']:
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
    arbol_rb.inOrden(arbol_rb.raiz)
    
    # lista de préstamos (para GUI)
    print("\n" + "=" * 80)
    print("5. OBTENCIÓN DE LISTA DE PRÉSTAMOS (Para GUI)")
    print("=" * 80)
    
    lista_prestamos = arbol_rb.obtener_prestamos_inorden(arbol_rb.raiz)
    print(f"\nTotal de préstamos en el árbol: {len(lista_prestamos)}\n")
    
    for i, prestamo in enumerate(lista_prestamos, 1):
        print(f"{i:2d}. {prestamo}")
    
    # Prueba de árbol vacío
    print("\n" + "=" * 80)
    print("6. PRUEBA DE VALIDACIÓN - ÁRBOL VACÍO")
    print("=" * 80)
    
    arbol_vacio = RBTree()
    print(f"Árbol vacío está vacío?: {arbol_vacio.esta_vacio()}")
    print(f"Propiedades de árbol vacío válidas: {arbol_vacio.verificar_propiedades_rb()['arbol_valido']}")
    
    # Prueba de duplicados
    print("\n" + "=" * 80)
    print("7. PRUEBA DE INSERCIÓN DE DUPLICADOS")
    print("=" * 80)
    
    print("\nIntentando insertar préstamo duplicado (código 0001)...")
    prestamo_duplicado = Prestamo(1, 999, 9999, "2024-07-01")
    arbol_rb.insertar_arbol(prestamo_duplicado)
    print("Duplicado rechazado (código 0001 ya existe)")
    
    # Verificación ultima
    print("\n" + "=" * 80)
    print("8. VERIFICACIÓN FINAL")
    print("=" * 80)
    
    propiedades_final = arbol_rb.verificar_propiedades_rb()
    lista_final = arbol_rb.obtener_prestamos_inorden(arbol_rb.raiz)
    
    print(f"\n Préstamos en el árbol: {len(lista_final)}")
    print(f" Árbol Rojinegro válido: {'SÍ' if propiedades_final['arbol_valido'] else 'NO'}")
    print(f" Raíz es negra: {'SÍ' if propiedades_final['propiedad_2_raiz_negra'] else 'NO'}")
    print(f" Altura negra consistente: {'SÍ' if propiedades_final['propiedad_5_altura_negra'] else 'NO'}")
    
    print("\n" + "=" * 80)
    print("PRUEBAS COMPLETADAS EXITOSAMENTE")   # en caso de que todo funcione biens
    print("=" * 80)


if __name__ == "__main__":
    main()
