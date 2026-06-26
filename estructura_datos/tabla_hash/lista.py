"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
Archivo: lista.py
"""

from estructura_datos.tabla_hash.nodo import Nodo
from typing import Optional, List
class Lista:
    """
    Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
    Clase que representa una lista enlazada simple.
    Esta estructura se usa en la tabla hash para resolver las colisiones 
    mediante el método de 'encadenamiento'. Si dos estudiantes tienen un 
    carnet que genera la misma posición en la tabla, ambos se guardarán 
    en esta lista.
    """
    
    def __init__(self):
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Constructor de la clase Lista.
        
        Parámetros:
        Ninguno.
        
        Devuelve:
        None (nada).
        
        Descripción: 
        Inicializa una lista enlazada simple completamente vacía.
        """
        # 'primero' es el apuntador que indica dónde comienza la lista.
        # Al iniciar, la lista no tiene elementos, por lo que apunta a None.
        self.primero = None
        
    def esta_vacia(self):
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Verifica si la lista enlazada tiene elementos o no.
        
        Parámetros:
        Ninguno.
        
        Devuelve:
        bool: Retorna True (verdadero) si la lista no tiene ningún nodo (está vacía), 
              o False (falso) si tiene al menos uno.
        
        Descripción: 
        Comprueba si el primer elemento ('primero') es nulo (None).
        """
        # Si 'self.primero' es None, significa que no hay elementos en la lista.
        return self.primero is None
    
    def insertar(self, estudiante):
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Añade un nuevo estudiante al final de la lista enlazada, pero primero 
        revisa que no exista ya otro estudiante con el mismo carnet.
        
        Parámetros:
        estudiante (Estudiante): El objeto Estudiante que deseamos guardar.
        
        Devuelve:
        None (nada).
        """
        # Creamos una 'caja' o nodo nuevo para guardar el estudiante
        nodo_nuevo = Nodo(estudiante)
        
        # Si la lista no tiene nada, el nuevo estudiante se convierte en el primero
        if self.esta_vacia():
            self.primero = nodo_nuevo
        else:
            # Si ya hay estudiantes, empezamos desde el 'primero'
            temp = self.primero
            
            # Recorremos la lista hasta llegar al último estudiante
            while temp.sig:
                # Comprobamos que el carnet del estudiante actual no sea igual al nuevo
                # Convertimos ambos a texto (str) para evitar errores si uno es número y otro texto
                if str(temp.valor.carnet) == str(estudiante.carnet):
                    return # Si el carnet ya está en la lista, terminamos y no hacemos nada
                
                # Avanzamos al siguiente nodo en la lista
                temp = temp.sig
                
            # Fuera del ciclo (while), verificamos el último nodo de la lista
            if str(temp.valor.carnet) == str(estudiante.carnet):
                return # Si el último tiene el mismo carnet, tampoco hacemos nada
                
            # Si llegamos aquí, sabemos que no hay carnets duplicados
            # Hacemos que el último nodo apunte a nuestro nodo nuevo, 
            # quedando así al final de la cola
            temp.sig = nodo_nuevo

    def buscar_por_carnet(self, carnet):
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Busca un estudiante específico dentro de la lista guiándose por su carnet.
        
        Parámetros:
        carnet (int o str): El número o texto de carnet que queremos encontrar.
        
        Devuelve:
        Estudiante o None: El objeto Estudiante si lo encuentra, o None si no existe en la lista.
        """
        # Comenzamos la búsqueda desde el primer elemento
        temp = self.primero
        
        # Mientras haya un elemento que revisar (es decir, temp no sea None)
        while temp:
            # Si el carnet de este elemento es igual al que buscamos...
            if str(temp.valor.carnet) == str(carnet):
                # ¡Lo encontramos! Devolvemos el estudiante
                return temp.valor
            
            # Si no era igual, pasamos al siguiente elemento
            temp = temp.sig
            
        # Si terminamos de recorrer toda la lista y no lo encontramos, devolvemos None
        return None

    def buscar_por_nombre(self, nombre):
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Busca un estudiante en la lista guiándose por su nombre.
        
        Parámetros:
        nombre (str): El nombre del estudiante a buscar.
        
        Devuelve:
        Estudiante o None: Retorna el primer Estudiante cuyo nombre coincida exactamente, 
                           o None si no encuentra ninguno.
        """
        # Comenzamos desde el principio de la lista
        temp = self.primero
        
        # Recorremos cada elemento mientras haya alguno
        while temp:
            # Comparamos el nombre. Usamos .lower() en ambos para que la comparación
            # sea igual sin importar si escribieron letras mayúsculas o minúsculas.
            if temp.valor.nombre.lower() == nombre.lower():
                return temp.valor # Encontramos al estudiante, lo devolvemos
                
            # Pasamos al siguiente
            temp = temp.sig
            
        # Si no lo encontramos tras revisar a todos
        return None

    def buscar_por_carrera(self, carrera):
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Busca a todos los estudiantes de la lista que cursan una carrera específica.
        
        Parámetros:
        carrera (str): El nombre de la carrera.
        
        Devuelve:
        List[str]: Una lista (de Python, no enlazada) que contiene únicamente los nombres
                   de los estudiantes que estudian la carrera solicitada.
        """
        # Creamos una lista vacía normal de Python para guardar los nombres
        nombres = []
        
        # Empezamos a revisar desde el primer nodo
        temp = self.primero
        
        while temp:
            # Comparamos ignorando mayúsculas y minúsculas con .lower()
            if temp.valor.carrera.lower() == carrera.lower():
                # Si coincide, guardamos el nombre del estudiante en nuestra lista
                nombres.append(temp.valor.nombre)
                
            # Seguimos buscando con el próximo
            temp = temp.sig
            
        # Devolvemos la lista de nombres recopilada (puede estar vacía si nadie cursaba esa carrera)
        return nombres

    def eliminar_por_carnet(self, carnet):
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Elimina de la lista al estudiante que tenga el carnet especificado.
        
        Parámetros:
        carnet (int o str): El carnet del estudiante a borrar.
        
        Devuelve:
        bool: Retorna True si se logró encontrar y eliminar al estudiante, 
              o False si el estudiante no estaba en la lista.
        """
        # Primer paso: Si la lista está vacía, no hay nada que eliminar
        if self.esta_vacia():
            return False

        # Segundo paso: ¿Qué pasa si el que queremos borrar es el primerito de la lista?
        if str(self.primero.valor.carnet) == str(carnet):
            # Hacemos que el primero ahora sea el segundo, olvidándonos del primerito.
            self.primero = self.primero.sig
            return True # ¡Eliminado con éxito!

        # Tercer paso: Si no era el primero, lo buscamos en el resto de la lista
        temp = self.primero
        
        # Vamos a revisar "el siguiente" elemento en lugar del actual, para poder borrarlo
        while temp.sig:
            # Si el carnet del SIGUIENTE estudiante es el que buscamos...
            if str(temp.sig.valor.carnet) == str(carnet):
                # Para borrarlo, hacemos que nuestro nodo actual (temp)
                # se "brinque" al siguiente y apunte al que le sigue a ese (temp.sig.sig).
                # Es decir, lo "desconectamos" de la cadena.
                temp.sig = temp.sig.sig
                return True
                
            # Si no es el que buscamos, avanzamos un paso más en la cadena
            temp = temp.sig
            
        # Si terminamos todo el recorrido y no lo encontramos, no se eliminó nada
        return False

