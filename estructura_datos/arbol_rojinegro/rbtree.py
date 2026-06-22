from typing import List, Optional
from clases.prestamo import Prestamo
from estructura_datos.arbol_rojinegro.nodo import Nodo
class RBTree:
    def __init__(self) -> None:
        self.raiz: Optional[Nodo] = None
    def buscar_codigo(self, raiz_p: Optional[Nodo], codigo_prestamo: int) -> Optional[Prestamo]:
        if raiz_p is None:
            return None
        if codigo_prestamo == raiz_p.valor.codigo_prestamo:
            return raiz_p.valor
        elif codigo_prestamo < raiz_p.valor.codigo_prestamo:
            return self.buscar_codigo(raiz_p.izq, codigo_prestamo)
        else:
            return self.buscar_codigo(raiz_p.der, codigo_prestamo)
    def _buscar_nodo(self, raiz_p: Optional[Nodo], codigo_prestamo: int) -> Optional[Nodo]:
        if raiz_p is None:
            return None
        if codigo_prestamo == raiz_p.valor.codigo_prestamo:
            return raiz_p
        elif codigo_prestamo < raiz_p.valor.codigo_prestamo:
            return self._buscar_nodo(raiz_p.izq, codigo_prestamo)
        else:
            return self._buscar_nodo(raiz_p.der, codigo_prestamo)
    def rotacion_dd(self, raiz_p: Nodo) -> Nodo:
        nuevo_raiz = raiz_p.der
        if nuevo_raiz is None:
            return raiz_p
        raiz_p.der = nuevo_raiz.izq
        if nuevo_raiz.izq is not None:
            nuevo_raiz.izq.padre = raiz_p
        nuevo_raiz.padre = raiz_p.padre
        nuevo_raiz.izq = raiz_p
        raiz_p.padre = nuevo_raiz
        return nuevo_raiz
    def rotacion_ii(self, raiz_p: Nodo) -> Nodo:
        nuevo_raiz = raiz_p.izq
        if nuevo_raiz is None:
            return raiz_p
        raiz_p.izq = nuevo_raiz.der
        if nuevo_raiz.der is not None:
            nuevo_raiz.der.padre = raiz_p
        nuevo_raiz.padre = raiz_p.padre
        nuevo_raiz.der = raiz_p
        raiz_p.padre = nuevo_raiz
        return nuevo_raiz
    def insertar(self, prestamo_nuevo: Prestamo) -> None:
        nuevo_nodo = Nodo(prestamo_nuevo)
        if self.raiz is None:
            self.raiz = nuevo_nodo
            self.raiz.color = "Negro"
            return
        actual = self.raiz
        padre = None
        while actual is not None:
            padre = actual
            if prestamo_nuevo.codigo_prestamo < actual.valor.codigo_prestamo:
                actual = actual.izq
            elif prestamo_nuevo.codigo_prestamo > actual.valor.codigo_prestamo:
                actual = actual.der
            else:
                return
        nuevo_nodo.padre = padre
        if prestamo_nuevo.codigo_prestamo < padre.valor.codigo_prestamo:
            padre.izq = nuevo_nodo
        else:
            padre.der = nuevo_nodo
        self._reparar_insercion(nuevo_nodo)
    def _reparar_insercion(self, raiz_p: Nodo) -> None:
        while raiz_p != self.raiz and raiz_p.padre is not None and raiz_p.padre.color == "Rojo":
            actual = raiz_p.padre
            padre = actual.padre
            if actual == padre.izq:
                hermano = padre.der
                if hermano is not None and hermano.color == "Rojo":
                    actual.color = "Negro"
                    hermano.color = "Negro"
                    padre.color = "Rojo"
                    raiz_p = padre
                else:
                    if raiz_p == actual.der:
                        raiz_p = actual
                        self.raiz = self._rotacion_dd_interna(self.raiz, raiz_p)
                        actual = raiz_p.padre
                        padre = actual.padre
                    actual.color = "Negro"
                    padre.color = "Rojo"
                    self.raiz = self._rotacion_ii_interna(self.raiz, padre)
            else:
                hermano = padre.izq
                if hermano is not None and hermano.color == "Rojo":
                    actual.color = "Negro"
                    hermano.color = "Negro"
                    padre.color = "Rojo"
                    raiz_p = padre
                else:
                    if raiz_p == actual.izq:
                        raiz_p = actual
                        self.raiz = self._rotacion_ii_interna(self.raiz, raiz_p)
                        actual = raiz_p.padre
                        padre = actual.padre
                    actual.color = "Negro"
                    padre.color = "Rojo"
                    self.raiz = self._rotacion_dd_interna(self.raiz, padre)
        self.raiz.color = "Negro"
    def _rotacion_dd_interna(self, raiz: Optional[Nodo], raiz_p: Nodo) -> Optional[Nodo]:
        padre = raiz_p.padre
        nueva_raiz = self.rotacion_dd(raiz_p)
        if padre is None:
            raiz = nueva_raiz
        else:
            if raiz_p == padre.izq:
                padre.izq = nueva_raiz
            else:
                padre.der = nueva_raiz
        return raiz
    def _rotacion_ii_interna(self, raiz: Optional[Nodo], raiz_p: Nodo) -> Optional[Nodo]:
        padre = raiz_p.padre
        nueva_raiz = self.rotacion_ii(raiz_p)
        if padre is None:
            raiz = nueva_raiz
        else:
            if raiz_p == padre.izq:
                padre.izq = nueva_raiz
            else:
                padre.der = nueva_raiz
        return raiz
    def eliminar_codigo(self, codigo_prestamo: int) -> bool:
        nodo_a_eliminar = self._buscar_nodo(self.raiz, codigo_prestamo)
        if nodo_a_eliminar is None:
            return False
        self._eliminar_nodo_interno(nodo_a_eliminar)
        return True
    def _eliminar_nodo_interno(self, raiz_p: Nodo) -> None:
        color_original = raiz_p.color
        x: Optional[Nodo] = None
        x_padre: Optional[Nodo] = None
        es_izq_de_padre = False
        if raiz_p.izq is None:
            nodo_reemplazo = raiz_p.der
            self._reemplazar_nodo(raiz_p, raiz_p.der)
        elif raiz_p.der is None:
            nodo_reemplazo = raiz_p.izq
            self._reemplazar_nodo(raiz_p, raiz_p.izq)
        else:
            sucesor = self._get_min_valor_nodo(raiz_p.der)
            raiz_padre = sucesor.padre
            if sucesor.padre == raiz_p:
                nodo_reemplazo = sucesor.der
            else:
                x_padre = sucesor.padre
                es_izq_de_padre = True
                self._reemplazar_nodo(sucesor, sucesor.der)
                sucesor.der = raiz_p.der
                sucesor.der.padre = sucesor
            self._reemplazar_nodo(raiz_p, sucesor)
            sucesor.izq = raiz_p.izq
            sucesor.izq.padre = sucesor
            sucesor.color = raiz_p.color
        if color_original == "Negro":
            if x is None:
                temp = Nodo(Prestamo(-1, -1, -1, ""))
                temp.color = "Negro"
                temp.padre = x_padre
                if x_padre is None:
                    self.raiz = temp
                elif es_izq_de_padre:
                    x_padre.izq = temp
                else:
                    x_padre.der = temp
                self._reparar_eliminacion(temp)
                if temp.padre is None:
                    self.raiz = None
                elif temp == temp.padre.izq:
                    temp.padre.izq = None
                else:
                    temp.padre.der = None
            else:
                self._reparar_eliminacion(x)
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
                    self.raiz = self._rotacion_dd_interna(self.raiz, padre)
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
                            self.raiz = self._rotacion_ii_interna(self.raiz, hermano)
                            hermano = padre.der
                        hermano.color = padre.color
                        padre.color = "Negro"
                        if hermano.der is not None:
                            hermano.der.color = "Negro"
                        self.raiz = self._rotacion_dd_interna(self.raiz, padre)
                        actual = self.raiz
            else:
                hermano = padre.izq
                if hermano is not None and hermano.color == "Rojo":
                    hermano.color = "Negro"
                    padre.color = "Rojo"
                    self.raiz = self._rotacion_ii_interna(self.raiz, padre)
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
                            self.raiz = self._rotacion_dd_interna(self.raiz, hermano)
                            hermano = padre.izq
                        hermano.color = padre.color
                        padre.color = "Negro"
                        if hermano.izq is not None:
                            hermano.izq.color = "Negro"
                        self.raiz = self._rotacion_ii_interna(self.raiz, padre)
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
    def preorden(self, raiz_p: Optional[Nodo]) -> None: # este se va
        if raiz_p is not None:
            prestamo = raiz_p.valor
            print(f"Código: {prestamo.codigo_prestamo} | Color: {raiz_p.color} | "
                  f"Libro: {prestamo.codigo_libro} | Estudiante: {prestamo.carnet_estudiante}")
            self.preorden(raiz_p.izq)
            self.preorden(raiz_p.der)
    def postorden(self, raiz_p: Optional[Nodo]) -> None: # este no va porque no lo vamos a usar, se de de usar 
        if raiz_p is not None:
            self.postorden(raiz_p.izq)
            self.postorden(raiz_p.der)
            prestamo = raiz_p.valor
            print(f"Código: {prestamo.codigo_prestamo} | Color: {raiz_p.color} | "
                  f"Libro: {prestamo.codigo_libro} | Estudiante: {prestamo.carnet_estudiante}")
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
    def mostrar(self, raiz_p: Optional[Nodo]) -> None:
        if raiz_p is not None:
            prestamo = raiz_p.valor
            print(f"[{prestamo.codigo_prestamo}({raiz_p.color[0]})]", end=" ")
            self.mostrar(raiz_p.izq)
            self.mostrar(raiz_p.der)
    def esta_vacia(self) -> bool:
        return self.raiz is None