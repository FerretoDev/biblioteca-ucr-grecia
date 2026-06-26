"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
Archivo: sistema_prestamos.py
"""

from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from clases.prestamo import Prestamo
from estructura_datos.arbol_avl.arbol_avl import ArbolAVL
from estructura_datos.arbol_rojinegro.arbol_rojinegro import ArbolRojinegro
from estructura_datos.tabla_hash.tabla_hash import TablaHash
from gui.xml_manager import XMLManager

DURACION_PRESTAMO_DIAS = 15


class SistemaPrestamos:
    """
    Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
    Propósito: Clase que maneja todas las reglas del negocio relacionadas con los préstamos.
               Es como el "cerebro" que coordina que se pueda prestar un libro solo si está disponible,
               y que el estudiante exista, etc.
    """
    def __init__(
        self,
        avl_libros: ArbolAVL,
        hash_estudiantes: TablaHash,
        arbol_prestamos: ArbolRojinegro,
        xml_manager: XMLManager,
    ) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Inicializar el sistema de préstamos dándole acceso a los datos almacenados en memoria (árboles y hash) 
                   y al gestor de archivos para guardar cambios.
        Parámetros: 
            avl_libros (ArbolAVL) - El árbol donde están guardados todos los libros.
            hash_estudiantes (TablaHash) - La tabla que guarda todos los estudiantes por su carnet.
            arbol_prestamos (ArbolRojinegro) - El árbol que lleva el control de los préstamos activos.
            xml_manager (XMLManager) - Herramienta para escribir los datos de vuelta a los archivos en el disco duro.
        Devuelve:   None
        Descripción:
            Solo guarda en variables propias (self) las estructuras que le pasaron, para usarlas más adelante.
            No lee archivos, solo usa lo que ya está en memoria.
        """
        # Guardamos la referencia al árbol de libros para poder buscar si un libro existe
        self.avl_libros = avl_libros
        # Guardamos la tabla de estudiantes para verificar que quien pide prestado exista
        self.hash_estudiantes = hash_estudiantes
        # Guardamos el árbol rojinegro de préstamos para saber qué está prestado
        self.arbol_prestamos = arbol_prestamos
        # Guardamos el administrador de archivos para poder guardar si hacemos un nuevo préstamo
        self.xml_manager = xml_manager

    # ----------------------------------------------------------
    # CONSULTAS
    # ----------------------------------------------------------

    def libro_esta_prestado(self, codigo_libro: int) -> bool:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Comprobar rápidamente si un libro específico ya está prestado a alguien.
        Parámetros: codigo_libro (int) — El número de código del libro que queremos consultar.
        Devuelve:   bool — True (Verdadero) si el libro está prestado a alguien, False (Falso) si está libre.
        Descripción:
            Saca todos los préstamos actuales y busca uno por uno a ver si alguno menciona nuestro libro.
        """
        # Pedimos todos los préstamos actuales sacándolos del árbol rojinegro en orden ascendente (inorden)
        prestamos = self.arbol_prestamos.inorden(self.arbol_prestamos.raiz)
        # Revisamos préstamo por préstamo
        for prestamo in prestamos:
            # Si el código de libro del préstamo es igual al que andamos buscando, significa que está ocupado
            if prestamo.codigo_libro == codigo_libro:
                return True
        # Si revisamos todos y no lo encontramos, entonces está libre
        return False

    def estudiante_tiene_prestamos(self, carnet: int) -> bool:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Saber si a un estudiante específico se le han prestado libros y todavía no los ha devuelto.
        Parámetros: carnet (int) — El número de carnet del estudiante a consultar.
        Devuelve:   bool — True (Verdadero) si el estudiante debe al menos un libro, False (Falso) si no debe nada.
        Descripción:
            Revisa todos los préstamos y se fija si aparece el carnet de ese estudiante.
        """
        # Obtenemos la lista de préstamos activos directamente del árbol rojinegro
        prestamos = self.arbol_prestamos.inorden(self.arbol_prestamos.raiz)
        # Iteramos o recorremos cada préstamo registrado
        for prestamo in prestamos:
            # Si vemos que el carnet en el préstamo es del estudiante que buscamos, bingo, tiene algo prestado
            if prestamo.carnet_estudiante == carnet:
                return True
        # Si dimos la vuelta a todo y no estaba, entonces no tiene préstamos activos
        return False

    def listar_prestamos(self) -> List[Prestamo]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Devolver una lista con todos los préstamos activos actualmente en el sistema.
        Parámetros: ninguno
        Devuelve:   List[Prestamo] con todos los préstamos en orden de menor a mayor.
        Descripción:
            Solo hace la consulta al árbol rojinegro usando recorrido inorden, lo que asegura el orden.
        """
        # El recorrido inorden de un árbol nos da los elementos ordenados, así que devolvemos justo eso
        return self.arbol_prestamos.inorden(self.arbol_prestamos.raiz)

    def _generar_codigo(self) -> int:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Inventar o generar un código numérico nuevo y único para identificar un nuevo préstamo.
        Parámetros: ninguno
        Devuelve:   int — El número (código de préstamo único) que va desde el 1000 hasta el 9999.
        Descripción:
            Busca el código de préstamo más alto que haya en uso y le suma 1 para hacer el siguiente.
        """
        # Sacamos todos los préstamos para ver cuáles códigos existen
        prestamos = self.arbol_prestamos.inorden(self.arbol_prestamos.raiz)
        # Si no hay ningún préstamo en absoluto, empezamos la cuenta desde 1000 como número inicial
        if not prestamos:
            return 1000
        # Encontramos el valor máximo entre todos los códigos de préstamo usando la función max()
        maximo = max(p.codigo_prestamo for p in prestamos)
        # El siguiente código será el máximo más uno
        siguiente = maximo + 1
        # Si por alguna razón nos pasamos de 9999 (un límite artificial nuestro), hacemos explotar (falla) el programa
        if siguiente > 9999:
            raise ValueError("Se alcanzo el limite de 9999 prestamos.")
        # Retornamos el código nuevecito y seguro
        return siguiente

    # ----------------------------------------------------------
    # OPERACIONES
    # ----------------------------------------------------------

    def dar_prestamo(
        self, codigo_libro: int, carnet_estudiante: int
    ) -> Tuple[bool, str]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Efectuar oficialmente el préstamo de un libro a un estudiante.
        Parámetros: 
            codigo_libro (int) — Identificador del libro que se van a llevar.
            carnet_estudiante (int) — Identificador del estudiante que se lo lleva.
        Devuelve:   Tuple[bool, str] — Una parejita: (éxito, mensaje de explicación). Si es True salió bien, si False salió mal.
        Descripción:
            Aplica TODAS las reglas: ¿El libro existe? ¿El estudiante existe? ¿El libro está libre?
            Si todo está perfecto, lo anota en el sistema y lo guarda en el disco duro.
        """
        # 1. Verificar que el libro existe usando nuestro árbol de libros
        libro = self.avl_libros.buscar_codigo(self.avl_libros.raiz, codigo_libro)
        if libro is None:
            # Si buscar_codigo devuelve None, es que no existe. Así que rechazamos el préstamo devolviendo False
            return False, f"El libro {codigo_libro} no existe en el sistema."

        # 2. Verificar que el estudiante existe buscándolo en la tabla hash
        estudiante = self.hash_estudiantes.buscar_por_carnet(carnet_estudiante)
        if estudiante is None:
            # Si buscar_por_carnet dice que no hay nadie, rechazamos devolviendo False
            return False, f"El estudiante con carnet {carnet_estudiante} no existe."

        # 3. Verificar que el libro no se lo haya llevado nadie más
        if self.libro_esta_prestado(codigo_libro):
            # Si nuestra propia función nos dice que sí está prestado, abortamos el proceso
            return False, f"El libro {codigo_libro} ya esta prestado."

        # 4. Crear los datos del nuevo préstamo
        # Pedimos a nuestra función interna que nos invente el nuevo código único
        codigo_prestamo = self._generar_codigo()
        # Sacamos la fecha y hora exacta del momento, pero nos quedamos solo con Año-Mes-Día
        fecha_prestamo = datetime.now().strftime("%Y-%m-%d")

        # Armamos un nuevo objeto Prestamo con todos los datos recolectados
        nuevo_prestamo = Prestamo(
            codigo_prestamo=codigo_prestamo,
            codigo_libro=codigo_libro,
            carnet_estudiante=carnet_estudiante,
            fecha_prestamo=fecha_prestamo,
        )

        # 5. Insertar y guardar este préstamo dentro del árbol rojinegro
        # Le decimos al árbol de préstamos que acomode este nuevo préstamo en el sistema en memoria
        self.arbol_prestamos.insertar(self.arbol_prestamos.raiz, nuevo_prestamo)

        # 6. Persistir y guardar definitivamente los cambios en el archivo XML (disco duro)
        self._guardar_prestamos_xml()

        # Calculamos cuál es la fecha máxima para devolver, sumándole nuestros 15 días fijos a la fecha de hoy
        fecha_devolucion = (
            datetime.strptime(fecha_prestamo, "%Y-%m-%d")
            + timedelta(days=DURACION_PRESTAMO_DIAS)
        ).strftime("%Y-%m-%d")

        # Regresamos True porque todo fue un éxito, más un bonito mensaje de confirmación
        return (
            True,
            f"Prestamo {codigo_prestamo} registrado. Devolucion: {fecha_devolucion}.",
        )

    def devolver_libro(self, codigo_prestamo: int) -> Tuple[bool, str]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Registrar cuando el estudiante viene y devuelve el libro a la biblioteca.
        Parámetros: codigo_prestamo (int) — El código de identificación único del préstamo que queremos cerrar/terminar.
        Devuelve:   Tuple[bool, str] — (éxito True/False, mensaje de resultado para el usuario).
        Descripción:
            Busca el préstamo, si existe lo borra del árbol y de los archivos, porque ya el libro regresó y el préstamo acabó.
        """
        # Intentamos encontrar el préstamo en el árbol rojinegro usando su código
        prestamo = self.arbol_prestamos.buscar_codigo(
            self.arbol_prestamos.raiz, codigo_prestamo
        )
        # Si no lo hallamos, seguro tipearon mal el código. Abortamos devolviendo False
        if prestamo is None:
            return False, f"No existe un prestamo con codigo {codigo_prestamo}."

        # Como el préstamo sí existe y ya entregaron el libro, eliminamos el préstamo del árbol
        self.arbol_prestamos.eliminar_codigo(
            self.arbol_prestamos.raiz, codigo_prestamo
        )
        # Guardamos en el disco duro esta actualización para que el sistema ya no tenga este préstamo guardado
        self._guardar_prestamos_xml()

        # Devolvemos éxito True indicando que la devolución finalizó en regla
        return True, f"Libro {prestamo.codigo_libro} devuelto correctamente."

    # ----------------------------------------------------------
    # PERSISTENCIA
    # ----------------------------------------------------------

    def _guardar_prestamos_xml(self) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Ayudante interno para enviar todo el árbol de préstamos hacia el archivo XML.
        Parámetros: ninguno
        Devuelve:   None
        Descripción:
            Es un método de uso interno que recopila todos los préstamos actuales y le pide al XMLManager que los guarde.
        """
        # Obtenemos la lista ordenada de todos los préstamos activos actualmente en el árbol
        prestamos = self.arbol_prestamos.inorden(self.arbol_prestamos.raiz)
        # Le decimos al administrador de archivos que agarre esa lista y sobreescriba el archivo de disco
        self.xml_manager.guardar_prestamos(prestamos)
