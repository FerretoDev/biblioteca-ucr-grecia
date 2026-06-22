with open('test/test_arbol_rojinegro.py', 'r') as f:
    content = f.read()

# Replace where we used inorden to print
content = content.replace('arbol_rb.inorden(arbol_rb.raiz)', 'arbol_rb.mostrar(arbol_rb.raiz)\n    print()')

# Replace where we used obtener_prestamos_inorden to get the list
content = content.replace('arbol_rb.obtener_prestamos_inorden', 'arbol_rb.inorden')

with open('test/test_arbol_rojinegro.py', 'w') as f:
    f.write(content)

