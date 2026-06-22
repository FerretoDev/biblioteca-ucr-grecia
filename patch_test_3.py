with open('test/test_arbol_rojinegro.py', 'r') as f:
    content = f.read()

# Replace the broken mostrar call with a helper loop
replacement = """
    def imprimir_inorden_con_color(raiz_p):
        if raiz_p is not None:
            imprimir_inorden_con_color(raiz_p.izq)
            prestamo = raiz_p.valor
            print(f"Código: {prestamo.codigo_prestamo} | Color: {raiz_p.color} | Libro: {prestamo.codigo_libro} | Estudiante: {prestamo.carnet_estudiante}")
            imprimir_inorden_con_color(raiz_p.der)
    
    imprimir_inorden_con_color(arbol_rb.raiz)
"""

content = content.replace('arbol_rb.mostrar(arbol_rb.raiz)\n    print()', replacement)

with open('test/test_arbol_rojinegro.py', 'w') as f:
    f.write(content)

