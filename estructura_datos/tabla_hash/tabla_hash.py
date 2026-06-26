"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
Archivo: tabla_hash.py
"""

from typing import List, Optional

from clases.estudiante import Estudiante
from estructura_datos.tabla_hash.lista import Lista


class TablaHash:
    """
    Estructura de datos 'Tabla Hash'. Funciona como un gran casillero numerado.
    Sirve para guardar y buscar estudiantes de forma súper rápida utilizando 
    su número de carnet como una clave para saber exactamente en qué 'casillero' 
    (bucket) debe ir.
    """
    def __init__(self, tamanio: int) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Constructor de la Tabla Hash.
        
        Parámetros: 
        tamanio (int) — Cantidad de casilleros (buckets) que tendrá la tabla.
        
        Devuelve:   
        None (nada).
        
        Descripción:
        Inicializa la tabla creando una lista del tamaño indicado. En cada espacio 
        coloca una Lista enlazada vacía (para resolver colisiones si dos estudiantes 
        caen en el mismo casillero).
        """
        # Se crea una lista de Python llena de objetos 'Lista' (enlazada) vacíos.
        # Es como comprar los casilleros y poner una caja vacía en cada uno.
        self.tabla_hash: List[Lista] = [Lista() for _ in range(tamanio)]
        
        # Guardamos el tamaño total para usarlo después al calcular dónde va cada quien.
        self.tamanio = tamanio

    def calculo_hash(self, clave: int) -> int:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Calcula en qué casillero (índice) debe ir un carnet específico.
        
        Parámetros: 
        clave (int) — El número de carnet del estudiante.
        
        Devuelve:   
        int — Un número que representa el índice o casillero en la tabla.
        
        Descripción:
        Usa la operación matemática de módulo (%). Al dividir el carnet entre 
        el tamaño de la tabla, el residuo siempre será un número entre 0 y 
        (tamaño - 1), lo que garantiza que nunca nos salgamos de la tabla.
        """
        # La magia de la tabla hash: carnet % cantidad de espacios
        return clave % self.tamanio

    def insertar(self, estudiante: Estudiante) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Guarda un nuevo estudiante en la tabla hash.
        
        Parámetros: 
        estudiante (Estudiante) — El objeto estudiante que se quiere guardar.
        
        Devuelve:   
        None (nada).
        
        Descripción:
        Primero averigua en qué casillero va (usando calculo_hash con su carnet).
        Luego, mete al estudiante en la lista enlazada que está en ese casillero.
        """
        # 1. Averiguamos la posición exacta
        index = self.calculo_hash(estudiante.carnet)
        
        # 2. Vamos a esa posición y lo agregamos a la lista que está allí
        self.tabla_hash[index].insertar(estudiante)

    def buscar_por_carnet(self, carnet: int) -> Optional[Estudiante]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Busca a un estudiante súper rápido, porque sabemos exactamente dónde mirar.
        
        Parámetros: 
        carnet (int) — El número de carnet del estudiante que buscamos.
        
        Devuelve:   
        Estudiante si existe en la tabla, o None si no se encuentra.
        
        Descripción:
        Tiempo de búsqueda O(1) en promedio, es decir, casi instantáneo. 
        En vez de revisar todos los estudiantes, calculamos el índice y buscamos 
        solamente en ese casillero.
        """
        # Calculamos el casillero donde debería estar
        index = self.calculo_hash(carnet)
        
        # Le pedimos a la lista de ese casillero que nos lo busque
        return self.tabla_hash[index].buscar_por_carnet(carnet)

    def buscar_por_nombre(self, nombre: str) -> Optional[Estudiante]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Busca a un estudiante por su nombre.
        
        Parámetros: 
        nombre (str) — El nombre completo (o parte exacta) del estudiante.
        
        Devuelve:   
        Estudiante si lo encuentra, o None si no.
        
        Descripción:
        Como la tabla está ordenada por carnet y no por nombre, no sabemos en qué 
        casillero está. Por eso, nos toca revisar casillero por casillero (O(n)).
        """
        # Recorremos todos los casilleros de la tabla (cada uno es una 'lista' enlazada)
        for lista in self.tabla_hash:
            # Buscamos por nombre dentro de esa lista específica
            encontrado = lista.buscar_por_nombre(nombre)
            
            # Si no devolvió None, es que lo encontró
            if encontrado is not None:
                return encontrado
                
        # Si revisamos todos los casilleros y no apareció, retornamos None
        return None

    def buscar_por_carrera(self, carrera: str) -> List[str]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Busca a TODOS los estudiantes que estén estudiando una carrera en particular.
        
        Parámetros: 
        carrera (str) — El nombre de la carrera que queremos consultar.
        
        Devuelve:   
        List[str] — Una lista con los nombres de todos los estudiantes de esa carrera.
        
        Descripción:
        Al igual que con el nombre, como la tabla se rige por carnet, tenemos que 
        revisar todos los casilleros de principio a fin (O(n)) y recolectar los datos.
        """
        # Aquí guardaremos todos los nombres que encontremos
        resultados: List[str] = []
        
        # Revisamos casillero por casillero
        for lista in self.tabla_hash:
            # Esta función nos devuelve una lista de nombres encontrados en el casillero actual
            nombres = lista.buscar_por_carrera(carrera)
            
            # Si encontró al menos uno, lo agregamos a nuestros resultados
            if nombres:
                # extend() sirve para agregar varios elementos de una lista a otra
                resultados.extend(nombres)
                
        return resultados

    def eliminar_estudiante(self, carnet: int) -> bool:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Elimina a un estudiante de la tabla usando su carnet.
        
        Parámetros: 
        carnet (int) — El número de carnet del estudiante a borrar.
        
        Devuelve:   
        bool — True (verdadero) si se logró borrar, o False (falso) si no existía.
        
        Descripción:
        Calcula rápido en qué casillero está y le pide a la lista de ese casillero 
        que lo borre. IMPORTANTE: el sistema que use esto debe verificar antes 
        si el estudiante tiene préstamos activos.
        """
        # 1. Encontramos en qué casillero debería estar
        index = self.calculo_hash(carnet)
        
        # 2. Le ordenamos a la lista de ese casillero que lo elimine
        return self.tabla_hash[index].eliminar_por_carnet(carnet)
