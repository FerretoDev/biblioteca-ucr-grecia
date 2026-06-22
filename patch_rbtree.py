with open('estructura_datos/arbol_rojinegro/rbtree.py', 'r') as f:
    lines = f.readlines()

new_lines = []
skip_obtener = False

for line in lines:
    if 'def _obtener_color' in line:
        skip_obtener = True
        continue
    if skip_obtener:
        if 'return nodo.color' in line:
            skip_obtener = False
        continue
        
    # Reemplazos en línea
    modified = line.replace('self._obtener_color(actual) == "Negro"', '(actual is None or actual.color == "Negro")')
    modified = modified.replace('self._obtener_color(hermano.izq) == "Negro"', '(hermano.izq is None or hermano.izq.color == "Negro")')
    modified = modified.replace('self._obtener_color(hermano.der) == "Negro"', '(hermano.der is None or hermano.der.color == "Negro")')
    
    new_lines.append(modified)

with open('estructura_datos/arbol_rojinegro/rbtree.py', 'w') as f:
    f.writelines(new_lines)

