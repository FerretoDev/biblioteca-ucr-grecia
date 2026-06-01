from nodo import Nodo

class Lista:
    
    def __init__(self):
        self.primero = None
        
    def esta_vacia(self):
        return self.primero is None
    
    def insertar(self, valor_nuevo):
        nodo_nuevo = Nodo(valor_nuevo)
        if self.esta_vacia():
            self.primero = nodo_nuevo
        else:
            temp = self.primero
            while temp.sig:
                temp = temp.sig
            temp.sig = nodo_nuevo

    def buscar(self, valor_buscar):
        temp = self.primero
        while temp:
            if temp.valor == valor_buscar:
                return True
            temp = temp.sig
        return False