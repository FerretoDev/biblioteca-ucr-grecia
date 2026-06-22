from typing import List, Optional
from clases.prestamo import Prestamo
from estructura_datos.arbol_rojinegro.nodo import Nodo

class RBTree:
    def __init__(self) -> None:
        self.raiz: Optional[Nodo] = None

    def esta_vacia(self) -> bool:
        return self.raiz is None

    def buscar_codigo(self, raiz_p: Optional[Nodo], codigo_prestamo: int) -> Optional[Prestamo]:
        nodo = self._buscar_nodo(raiz_p, codigo_prestamo)
        return nodo.valor if nodo is not None else None

    def _buscar_nodo(self, raiz_p: Optional[Nodo], codigo_prestamo: int) -> Optional[Nodo]:
        if raiz_p is None:
            return None
        if codigo_prestamo == raiz_p.valor.codigo_prestamo:
            return raiz_p
        elif codigo_prestamo < raiz_p.valor.codigo_prestamo:
            return self._buscar_nodo(raiz_p.izq, codigo_prestamo)
        else:
            return self._buscar_nodo(raiz_p.der, codigo_prestamo)

    def rotacion_ii(self, raiz_p: Nodo) -> Nodo:
        nuevo_raiz = raiz_p.izq
        raiz_p.izq = nuevo_raiz.der
        if nuevo_raiz.der is not None:
            nuevo_raiz.der.padre = raiz_p
        
        nuevo_raiz.padre = raiz_p.padre
        if raiz_p.padre is None:
            self.raiz = nuevo_raiz
        elif raiz_p == raiz_p.padre.izq:
            raiz_p.padre.izq = nuevo_raiz
        else:
            raiz_p.padre.der = nuevo_raiz
            
        nuevo_raiz.der = raiz_p
        raiz_p.padre = nuevo_raiz
        return nuevo_raiz

    def rotacion_dd(self, raiz_p: Nodo) -> Nodo:
        nuevo_raiz = raiz_p.der
        raiz_p.der = nuevo_raiz.izq
        if nuevo_raiz.izq is not None:
            nuevo_raiz.izq.padre = raiz_p
            
        nuevo_raiz.padre = raiz_p.padre
        if raiz_p.padre is None:
            self.raiz = nuevo_raiz
        elif raiz_p == raiz_p.padre.izq:
            raiz_p.padre.izq = nuevo_raiz
        else:
            raiz_p.padre.der = nuevo_raiz
            
        nuevo_raiz.izq = raiz_p
        raiz_p.padre = nuevo_raiz
        return nuevo_raiz

    def insertar(self, raiz_p: Optional[Nodo], prestamo_nuevo: Prestamo) -> Optional[Nodo]:
        nuevo_nodo = Nodo(prestamo_nuevo)
        if self.raiz is None:
            self.raiz = nuevo_nodo
            self.raiz.color = "Negro"
            return self.raiz

        if raiz_p is None:
            return None

        if prestamo_nuevo.codigo_prestamo < raiz_p.valor.codigo_prestamo:
            if raiz_p.izq is None:
                
                nuevo_nodo.padre = raiz_p
                # conecta el nuevo nodo como hijo izquierdo
                raiz_p.izq = nuevo_nodo

                # Chequeo para auto-balancear color al insertar
                if raiz_p.color == "Rojo":
                    self.cambio_color(nuevo_nodo)

                return nuevo_nodo

            return self.insertar(raiz_p.izq, prestamo_nuevo)

        if prestamo_nuevo.codigo_prestamo > raiz_p.valor.codigo_prestamo:
            if raiz_p.der is None:
            
                nuevo_nodo.padre = raiz_p
                # conecta el nuevo nodo como hijo derecho
                raiz_p.der = nuevo_nodo

                # Chequeo para auto-balancear color al insertar
                if raiz_p.color == "Rojo":
                    self.cambio_color(nuevo_nodo)

                return nuevo_nodo

            return self.insertar(raiz_p.der, prestamo_nuevo)

        return raiz_p

    def cambio_color(self, hijo: Nodo) -> None:
        while hijo != self.raiz and hijo.padre is not None and hijo.padre.color == "Rojo":
            actual = hijo.padre   # actual es el padre rojo
            padre = actual.padre  # padre es el abuelo

            if padre is None:
                break

            if padre.izq == actual:
                hermano = padre.der  # hermano de actual (el tío)

                # Tu código original para el Caso 1 (hermano rojo)
                if hermano is not None and hermano.color == "Rojo":
                    actual.color = "Negro"
                    hermano.color = "Negro"
                    
                    if padre == self.raiz:
                        padre.color = "Negro"
                    else:
                        padre.color = "Rojo"
                        
                    hijo = padre # Iteramos hacia arriba
                else:
                    # Caso 2 y 3: Hermano negro (requiere rotaciones)
                    if hijo == actual.der:
                        hijo = actual
                        self.rotacion_dd(hijo)
                        actual = hijo.padre
                        padre = actual.padre
                    
                    actual.color = "Negro"
                    padre.color = "Rojo"
                    self.rotacion_ii(padre)
            else:
                hermano = padre.izq
                
                # Tu código original para el Caso 1 (hermano rojo)
                if hermano is not None and hermano.color == "Rojo":
                    actual.color = "Negro"
                    hermano.color = "Negro"
                    
                    if padre == self.raiz:
                        padre.color = "Negro"
                    else:
                        padre.color = "Rojo"
                        
                    hijo = padre # Iteramos hacia arriba
                else:
                    # Caso 2 y 3: Hermano negro (requiere rotaciones)
                    if hijo == actual.izq:
                        hijo = actual
                        self.rotacion_ii(hijo)
                        actual = hijo.padre
                        padre = actual.padre
                        
                    actual.color = "Negro"
                    padre.color = "Rojo"
                    self.rotacion_dd(padre)
                    
        self.raiz.color = "Negro"

    def eliminar_codigo(self, raiz_p: Optional[Nodo], codigo_prestamo: int) -> Optional[Nodo]:
        if raiz_p is None:
            return None

        if codigo_prestamo < raiz_p.valor.codigo_prestamo:
            self.eliminar_codigo(raiz_p.izq, codigo_prestamo)
        elif codigo_prestamo > raiz_p.valor.codigo_prestamo:
            self.eliminar_codigo(raiz_p.der, codigo_prestamo)
        else:
            # Encontrado!
            if raiz_p.izq is not None and raiz_p.der is not None:
                # Caso 2 hijos: buscamos el sucesor
                temp = self._get_min_valor_nodo(raiz_p.der)
                raiz_p.valor = temp.valor
                # Borramos el sucesor recursivamente
                self.eliminar_codigo(raiz_p.der, temp.valor.codigo_prestamo)
            else:
                # Caso 0 o 1 hijo
                color_original = raiz_p.color
                actual = raiz_p.izq if raiz_p.izq is not None else raiz_p.der
                padre = raiz_p.padre
                es_izq_de_padre = (padre is not None and raiz_p == padre.izq)

                if actual is None:
                    # 0 hijos (es hoja). Usamos un nodo NIL temporal para reparar
                    actual = Nodo(Prestamo(-1, -1, -1, "")) 
                    actual.color = "Negro"
                    actual.padre = padre
                    if padre is None:
                        self.raiz = actual
                    elif es_izq_de_padre:
                        padre.izq = actual
                    else:
                        padre.der = actual
                    
                    if color_original == "Negro":
                        self._reparar_eliminacion(actual)
                    
                    # Removemos el nodo NIL temporal
                    if actual.padre is None:
                        self.raiz = None
                    elif actual.padre.izq == actual:
                        actual.padre.izq = None
                    else:
                        actual.padre.der = None
                else:
                    # 1 hijo
                    actual.padre = padre
                    if padre is None:
                        self.raiz = actual
                    elif es_izq_de_padre:
                        padre.izq = actual
                    else:
                        padre.der = actual

                    if color_original == "Negro":
                        self._reparar_eliminacion(actual)
                        
        return self.raiz

    def _reemplazar_nodo(self, raiz_p: Nodo, nodo_reemplazo: Optional[Nodo]) -> None:
        if raiz_p.padre is None:
            self.raiz = nodo_reemplazo
        elif raiz_p == raiz_p.padre.izq:
            raiz_p.padre.izq = nodo_reemplazo
        else:
            raiz_p.padre.der = nodo_reemplazo
        if nodo_reemplazo is not None:
            nodo_reemplazo.padre = raiz_p.padre
    def _get_min_valor_nodo(self, raiz_p: Nodo) -> Nodo:
        actual = raiz_p
        while actual.izq is not None:
            actual = actual.izq
        return actual
    def _reparar_eliminacion(self, actual: Nodo) -> None:
        while actual != self.raiz and self._obtener_color(actual) == "Negro":
            padre = actual.padre
            if actual == padre.izq:
                hermano = padre.der
                if hermano is not None and hermano.color == "Rojo":
                    hermano.color = "Negro"
                    padre.color = "Rojo"
                    self.rotacion_dd(padre)
                    hermano = padre.der
                if (hermano is not None and 
                    self._obtener_color(hermano.izq) == "Negro" and 
                    self._obtener_color(hermano.der) == "Negro"):
                    if hermano is not None:
                        hermano.color = "Rojo"
                    actual = padre
                else:
                    if hermano is not None:
                        if self._obtener_color(hermano.der) == "Negro":
                            if hermano.izq is not None:
                                hermano.izq.color = "Negro"
                            hermano.color = "Rojo"
                            self.rotacion_ii(hermano)
                            hermano = padre.der
                        hermano.color = padre.color
                        padre.color = "Negro"
                        if hermano.der is not None:
                            hermano.der.color = "Negro"
                        self.rotacion_dd(padre)
                        actual = self.raiz
            else:
                hermano = padre.izq
                if hermano is not None and hermano.color == "Rojo":
                    hermano.color = "Negro"
                    padre.color = "Rojo"
                    self.rotacion_ii(padre)
                    hermano = padre.izq
                if (hermano is not None and 
                    self._obtener_color(hermano.izq) == "Negro" and 
                    self._obtener_color(hermano.der) == "Negro"):
                    if hermano is not None:
                        hermano.color = "Rojo"
                    actual = padre
                else:
                    if hermano is not None:
                        if self._obtener_color(hermano.izq) == "Negro":
                            if hermano.der is not None:
                                hermano.der.color = "Negro"
                            hermano.color = "Rojo"
                            self.rotacion_dd(hermano)
                            hermano = padre.izq
                        hermano.color = padre.color
                        padre.color = "Negro"
                        if hermano.izq is not None:
                            hermano.izq.color = "Negro"
                        self.rotacion_ii(padre)
                        actual = self.raiz
        if actual is not None:
            actual.color = "Negro"
    def _obtener_color(self, nodo: Optional[Nodo]) -> str:
        if nodo is None:
            return "Negro"
        return nodo.color
    def inorden(self, raiz_p: Optional[Nodo]) -> None:
        if raiz_p is not None:
            self.inorden(raiz_p.izq)
            prestamo = raiz_p.valor
            print(f"Código: {prestamo.codigo_prestamo} | Color: {raiz_p.color} | "
                  f"Libro: {prestamo.codigo_libro} | Estudiante: {prestamo.carnet_estudiante}")
            self.inorden(raiz_p.der)
    def obtener_prestamos_inorden(self, raiz_p: Optional[Nodo]) -> List[Prestamo]:
        if raiz_p is None:
            return []
        prestamos = []
        prestamos.extend(self.obtener_prestamos_inorden(raiz_p.izq))
        prestamos.append(raiz_p.valor)
        prestamos.extend(self.obtener_prestamos_inorden(raiz_p.der))
        return prestamos
    def verificar_propiedades_rb(self) -> dict:
        resultado = {
            "propiedad_1_colores": self._verificar_colores(self.raiz),
            "propiedad_2_raiz_negra": self._verificar_raiz_negra(),
            "propiedad_4_rojo_hijos_negros": self._verificar_rojo_padre_negro(self.raiz),
            "propiedad_5_altura_negra": self._verificar_altura_negra(self.raiz) >= 0,
            "arbol_valido": True
        }
        if not all([resultado["propiedad_1_colores"], 
                   resultado["propiedad_2_raiz_negra"],
                   resultado["propiedad_4_rojo_hijos_negros"],
                   resultado["propiedad_5_altura_negra"]]):
            resultado["arbol_valido"] = False
        return resultado
    def _verificar_colores(self, nodo: Optional[Nodo]) -> bool:
        if nodo is None:
            return True
        if nodo.color not in ["Rojo", "Negro"]:
            return False
        return (self._verificar_colores(nodo.izq) and 
                self._verificar_colores(nodo.der))
    def _verificar_raiz_negra(self) -> bool:
        if self.raiz is None:
            return True
        return self.raiz.color == "Negro"
    def _verificar_rojo_padre_negro(self, nodo: Optional[Nodo]) -> bool:
        if nodo is None:
            return True
        if nodo.color == "Rojo":
            if nodo.izq is not None and nodo.izq.color == "Rojo":
                return False
            if nodo.der is not None and nodo.der.color == "Rojo":
                return False
        return (self._verificar_rojo_padre_negro(nodo.izq) and 
                self._verificar_rojo_padre_negro(nodo.der))
    def _verificar_altura_negra(self, nodo: Optional[Nodo]) -> int:
        if nodo is None:
            return 1  # Las hojas NIL son negras
        altura_izq = self._verificar_altura_negra(nodo.izq)
        altura_der = self._verificar_altura_negra(nodo.der)
        if altura_izq == -1 or altura_der == -1:
            return -1
        if altura_izq != altura_der:
            return -1
        if nodo.color == "Negro":
            return altura_izq + 1
        else:
            return altura_izq


    # test
    def mostrar(self, raiz_p) -> None:
        if raiz_p is None:
            return

        print(f"{raiz_p.valor}({raiz_p.color})", end=" ")

        self.mostrar(raiz_p.izq)
        self.mostrar(raiz_p.der)