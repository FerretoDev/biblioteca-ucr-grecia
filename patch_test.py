import sys

with open('test/test_arbol_rojinegro.py', 'r') as f:
    content = f.read()

# Add imports
content = content.replace(
    'from estructura_datos.arbol_rojinegro.rbtree import RBTree',
    'from estructura_datos.arbol_rojinegro.rbtree import RBTree\nfrom estructura_datos.arbol_rojinegro.nodo import Nodo\nfrom typing import Optional'
)

# Add the functions before main()
functions = """

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

"""
content = content.replace('def main() -> None:', functions + 'def main() -> None:')

# Replace method calls
content = content.replace('arbol_rb.verificar_propiedades_rb()', 'verificar_propiedades_rb(arbol_rb)')
content = content.replace('arbol_vacio.verificar_propiedades_rb()', 'verificar_propiedades_rb(arbol_vacio)')

with open('test/test_arbol_rojinegro.py', 'w') as f:
    f.write(content)

