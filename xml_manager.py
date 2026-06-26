"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
Archivo: xml_manager.py
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from clases.estudiante import Estudiante
from clases.libro import Libro
from clases.prestamo import Prestamo


class XMLManager:
    """
    Propósito: Clase encargada de manejar la lectura y escritura de los archivos de texto planos 
               que simulan ser XML, usando en realidad un formato donde los valores están separados por '%'.
    """
    def __init__(self) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Inicializa las rutas donde se van a guardar y leer los datos del sistema.
        Parámetros: Ninguno
        Devuelve:   None
        Descripción:
           Define las ubicaciones relativas a la carpeta 'datos' para los archivos de libros, estudiantes y préstamos.
        """
        # Ruta del archivo para los libros
        self.ruta_libros = "datos/libros.xml"
        # Ruta del archivo para los estudiantes
        self.ruta_estudiantes = "datos/estudiantes.xml"
        # Ruta del archivo para los préstamos
        self.ruta_prestamos = "datos/prestamos.xml"

    # ----------------------------------------------------------
    # HELPERS GENERICOS
    # ----------------------------------------------------------

    def _leer_lineas(self, ruta: str) -> List[str]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Leer un archivo en disco línea por línea, saltándose las líneas vacías.
        Parámetros: ruta (str) - La dirección del archivo a leer.
        Devuelve:   List[str] - Una lista de textos, donde cada texto es una línea con información del archivo.
        Descripción:
           Verifica si el archivo existe. Si existe, lo abre y extrae las líneas, limpiando espacios en blanco y saltos.
        """
        # Creamos un objeto Path que representa la ruta física del archivo
        archivo = Path(ruta)
        # Si el archivo no existe en el disco, imprimimos una alerta y retornamos una lista vacía para no hacer que el programa falle
        if not archivo.exists():
            print(f"[XMLManager] '{ruta}' no encontrado.")
            return []

        # Lista donde vamos a ir guardando las líneas de texto útiles
        lineas: List[str] = []
        # Abrimos el archivo en modo lectura ("r") con codificación utf-8 (para soportar tildes, ñ, etc.)
        with archivo.open("r", encoding="utf-8") as f:
            for linea in f:
                # Quitamos los espacios en blanco, tabuladores o saltos de línea que estén al inicio o al final del texto
                cruda = linea.strip()
                # Si después de quitar los espacios la línea no quedó vacía, la guardamos
                if cruda:
                    lineas.append(cruda)
        return lineas

    @staticmethod
    def _linea_a_partes(
        linea: str,
        num_esperado: int,
        permitir_faltantes: int = 0,
    ) -> List[str] | None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Tomar una línea de texto con datos separados por '%' y dividirla en una lista de valores.
        Parámetros: 
            linea (str) - El texto crudo a dividir.
            num_esperado (int) - La cantidad exacta de datos (columnas) que debería tener la línea.
            permitir_faltantes (int) - La cantidad de datos al final que pueden faltar sin que se considere error (por defecto es 0).
        Devuelve:   List[str] con las partes separadas, o None si la línea no tiene los datos esperados (inválida).
        Descripción:
           Divide la línea separada por %. Si faltan campos permitidos, rellena el faltante con textos vacíos ("").
        """
        # Partimos la línea de texto cada vez que aparezca un símbolo de porcentaje "%"
        partes = linea.split("%")
        # Calculamos cuál es la cantidad mínima aceptable de campos (columnas) que debe tener la línea
        min_campos = num_esperado - permitir_faltantes
        # Si tiene menos campos de los mínimos permitidos, o más de los esperados, entonces es una línea corrupta/inválida
        if len(partes) < min_campos or len(partes) > num_esperado:
            return None
        # Si la línea tiene una cantidad válida de campos, pero son menos que los que el sistema espera en total
        if len(partes) < num_esperado:
            # Agregamos textos vacíos al final de la lista hasta completar el tamaño esperado
            partes += [""] * (num_esperado - len(partes))
        # Devolvemos la lista de partes lista para ser usada
        return partes

    # ----------------------------------------------------------
    # LIBROS
    # ----------------------------------------------------------

    def cargar_libros(self) -> List[Libro]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Leer el archivo de libros y convertir cada línea en un objeto de la clase Libro.
        Parámetros: ninguno
        Devuelve:   List[Libro] con los datos de cada libro convertido en un objeto de programación.
        Descripción:
           Lee el archivo de libros, divide cada línea usando el separador %, y crea los objetos Libro necesarios.
        """
        # Obtenemos todas las líneas de texto del archivo libros usando nuestra función ayudante
        lineas = self._leer_lineas(self.ruta_libros)
        # Lista vacía donde guardaremos los objetos Libro que vayamos creando
        libros: List[Libro] = []
        # Recorremos cada línea del archivo, llevando la cuenta del número de línea para dar mensajes de error útiles (iniciando en 1)
        for num, linea in enumerate(lineas, start=1):
            # Dividimos la línea en 6 partes esperadas (código, autor, título, año, editorial, área)
            partes = self._linea_a_partes(linea, 6)
            # Si _linea_a_partes nos devolvió None, significa que la línea está mala, así que la ignoramos
            if partes is None:
                print(f"[XMLManager] Linea {num} ignorada (libros): {linea}")
                continue
            try:
                # Intentamos construir el objeto Libro con los datos extraídos
                # Nota: convertimos código y año a números enteros (int) porque el archivo de texto nos da "strings"
                libros.append(Libro(
                    codigo=int(partes[0]),
                    autor=partes[1],
                    titulo=partes[2],
                    anio=int(partes[3]),
                    editorial=partes[4],
                    area=partes[5],
                ))
            except ValueError:
                # Si falló la conversión de número (por ejemplo, si en vez de un año dice "no se sabe"), atrapamos el error y avisamos
                print(f"[XMLManager] Error de conversion en linea {num} (libros): {linea}")
        return libros

    def guardar_libros(self, libros: List[Libro]) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Tomar una lista de objetos Libro y guardarlos permanentemente en el archivo de texto.
        Parámetros: libros (List[Libro]) - Una lista que contiene objetos de la clase Libro.
        Devuelve:   None
        Descripción:
           Extrae los datos de cada objeto Libro, los junta separándolos con '%' y escribe cada libro en una línea del archivo.
        """
        # Nos aseguramos de que las carpetas donde va el archivo (ej: 'datos/') existan, y si no, las creamos
        Path(self.ruta_libros).parent.mkdir(parents=True, exist_ok=True)
        # Abrimos el archivo en modo escritura ("w"). Cuidado: Esto borra todo lo que había y lo reescribe desde cero
        with open(self.ruta_libros, "w", encoding="utf-8") as f:
            for l in libros:
                # Metemos todos los atributos del libro en una lista de textos. Los números hay que convertirlos a texto con str()
                partes = [str(l.codigo), l.autor, l.titulo, str(l.anio), l.editorial, l.area]
                # Pegamos las partes usando un '%' entre cada una, agregamos un salto de línea (\n) al final, y lo guardamos
                f.write("%".join(partes) + "\n")

    # ----------------------------------------------------------
    # ESTUDIANTES
    # ----------------------------------------------------------

    def cargar_estudiantes(self) -> List[Estudiante]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Leer el archivo de estudiantes y convertir cada línea en un objeto de la clase Estudiante.
        Parámetros: ninguno
        Devuelve:   List[Estudiante] con los datos de cada estudiante.
        Descripción:
           Lee estudiantes.xml, extrae los campos separados por % y crea instancias de Estudiante.
        """
        # Obtenemos todas las líneas válidas del archivo de estudiantes
        lineas = self._leer_lineas(self.ruta_estudiantes)
        # Lista vacía para acumular los objetos de tipo Estudiante que crearemos
        estudiantes: List[Estudiante] = []
        # Recorremos cada línea, usando enumerate para saber el número de línea (para mostrar si hay errores)
        for num, linea in enumerate(lineas, start=1):
            # Dividimos la línea esperando 6 campos (carnet, nombre, carrera, teléfono, correo, dirección)
            partes = self._linea_a_partes(linea, 6)
            # Si el formato está mal, saltamos al siguiente registro sin hacer que el programa estalle
            if partes is None:
                print(f"[XMLManager] Linea {num} ignorada (estudiantes): {linea}")
                continue
            try:
                # Creamos el objeto Estudiante convirtiendo el carnet a número (int)
                estudiantes.append(Estudiante(
                    carnet=int(partes[0]),
                    nombre=partes[1],
                    carrera=partes[2],
                    telefono=partes[3],
                    correo=partes[4],
                    direccion=partes[5],
                ))
            except ValueError:
                # Si el carnet tenía letras en lugar de números, caemos aquí y evitamos un "crash" del programa
                print(f"[XMLManager] Error de conversion en linea {num} (estudiantes): {linea}")
        return estudiantes

    def guardar_estudiantes(self, estudiantes: List[Estudiante]) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Escribir la lista de estudiantes en el archivo de texto para que no se pierdan al cerrar el programa.
        Parámetros: estudiantes (List[Estudiante]) - Lista de objetos Estudiante a guardar.
        Devuelve:   None
        Descripción:
           Reescribe el archivo de estudiantes convirtiendo la información a un texto delimitado por %.
        """
        # Aseguramos que la carpeta padre ('datos') exista en el sistema
        Path(self.ruta_estudiantes).parent.mkdir(parents=True, exist_ok=True)
        # Abrimos el archivo en modo sobreescritura ("w")
        with open(self.ruta_estudiantes, "w", encoding="utf-8") as f:
            # Iteramos por cada estudiante que nos mandaron
            for e in estudiantes:
                # Extraemos y convertimos sus propiedades a texto (str)
                partes = [str(e.carnet), e.nombre, e.carrera, e.telefono, e.correo, e.direccion]
                # Los juntamos con el símbolo % y grabamos la línea en el archivo
                f.write("%".join(partes) + "\n")

    # ----------------------------------------------------------
    # PRESTAMOS
    # ----------------------------------------------------------

    def cargar_prestamos(self) -> List[Prestamo]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Leer el archivo de préstamos y generar la lista de objetos de clase Prestamo.
        Parámetros: ninguno
        Devuelve:   List[Prestamo] con la información de los préstamos registrados.
        Descripción:
           Lee prestamos.xml, partiendo por % (espera 4 campos pero admite que falte el último) y genera objetos Prestamo.
        """
        # Conseguimos las líneas no vacías del archivo
        lineas = self._leer_lineas(self.ruta_prestamos)
        # Esta lista almacenará los préstamos creados en memoria
        prestamos: List[Prestamo] = []
        for num, linea in enumerate(lineas, start=1):
            # Buscamos 4 partes, pero por si acaso permitimos que falte 1 parte (por ejemplo, una fecha en blanco)
            partes = self._linea_a_partes(linea, 4, permitir_faltantes=1)
            # Si está súper mal formateada, avisamos y pasamos de largo
            if partes is None:
                print(f"[XMLManager] Linea {num} ignorada (prestamos): {linea}")
                continue
            try:
                # Transformamos los 3 primeros datos numéricos a enteros y dejamos la fecha como texto
                prestamos.append(Prestamo(
                    codigo_prestamo=int(partes[0]),
                    codigo_libro=int(partes[1]),
                    carnet_estudiante=int(partes[2]),
                    fecha_prestamo=partes[3],
                ))
            except ValueError:
                # Si fallamos transformando a números, lo reportamos para que el usuario pueda corregir el archivo
                print(f"[XMLManager] Error de conversion en linea {num} (prestamos): {linea}")
        return prestamos

    def guardar_prestamos(self, prestamos: List[Prestamo]) -> None:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Almacenar los objetos de Préstamo de vuelta en el archivo del sistema para mantener los datos.
        Parámetros: prestamos (List[Prestamo]) - Lista de los préstamos en memoria.
        Devuelve:   None
        Descripción:
           Toma cada objeto Prestamo, convierte sus datos a texto y los une con %, guardándolos en el archivo de texto.
        """
        # Nos preparamos asegurando que exista la ruta y la carpeta contenedora
        Path(self.ruta_prestamos).parent.mkdir(parents=True, exist_ok=True)
        # Abrimos para reemplazar el archivo de préstamos (modo "w")
        with open(self.ruta_prestamos, "w", encoding="utf-8") as f:
            for p in prestamos:
                # Pequeña verificación lógica por si hay un error extraño donde el carnet sea igual al código de préstamo
                if p.codigo_prestamo == p.carnet_estudiante:
                    print(
                        "[XMLManager] Aviso: codigo_prestamo y carnet_estudiante son iguales."
                    )
                # Formamos la lista de piezas convirtiendo todo a texto
                partes = [str(p.codigo_prestamo), str(p.codigo_libro), str(p.carnet_estudiante), p.fecha_prestamo]
                # Si las últimas partes son vacías, las removemos para no guardar puros %% al final de la línea
                while partes and partes[-1] == "":
                    partes.pop()
                # Armamos la línea uniéndola con % y la guardamos en el archivo
                f.write("%".join(partes) + "\n")

    # ----------------------------------------------------------
    # OPERACIONES CONJUNTAS
    # ----------------------------------------------------------

    def cargar_todo(self) -> tuple[List[Libro], List[Estudiante], List[Prestamo]]:
        """
        Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
        Propósito: Cargar todos los datos del sistema de un solo golpe para no tener que llamar a cada función por aparte.
        Parámetros: ninguno
        Devuelve:   Una tupla que contiene tres cosas: (lista de libros, lista de estudiantes, lista de prestamos).
        Descripción:
           Llama internamente a cargar_libros, cargar_estudiantes y cargar_prestamos, devolviendo todos los resultados.
        """
        # Devolvemos un "paquete" de 3 listas con todos los datos recién cargados de los archivos
        return (
            self.cargar_libros(),
            self.cargar_estudiantes(),
            self.cargar_prestamos(),
        )
