"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Archivo:  gui/interfaz.py
Descripcion:
    Interfaz grafica principal del sistema de biblioteca.
    Usa ttk.Notebook con tres pestanas (Libros, Estudiantes, Prestamos).
    La GUI nunca implementa logica de negocio: solo llama a las capas ya
    existentes (ArbolAVL, TablaHash, SistemaPrestamos, GestorEliminacion).

Tkinter utilizado:
    tk.Tk()           — ventana principal
    ttk.Notebook      — contenedor de pestanas
    ttk.Treeview      — tabla con scroll para resultados
    ttk.Scrollbar     — scroll vertical para Treeview
    tk.LabelFrame     — agrupacion de campos de formulario
    tk.Entry          — cajas de texto
    tk.Button         — botones de accion
    messagebox        — dialogos de confirmacion y error
"""

import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox, ttk
from typing import List

from clases.estudiante import Estudiante
from clases.libro import Libro
from clases.prestamo import Prestamo
from estructura_datos.arbol_avl.arbol_avl import ArbolAVL
from estructura_datos.arbol_rojinegro.arbol_rojinegro import ArbolRojinegro
from estructura_datos.tabla_hash.tabla_hash import TablaHash
from gestor_eliminacion import GestorEliminacion
from sistema_prestamos import SistemaPrestamos
from xml_manager import XMLManager

# ── Paleta ───────────────────────────────────────────────────
BG_DARK    = "#1B2631"   # fondo ventana y treeview
BG_PANEL   = "#263545"   # fondo de cada pestana y frames
ACCENT     = "#2471A3"   # azul primario (botones, encabezados)
ACCENT_SEL = "#1A5276"   # azul seleccionado
BTN_DEL    = "#922B21"   # rojo para botones de eliminar
BTN_OK     = "#1E8449"   # verde para dar prestamo
BTN_VER    = "#27AE60"   # verde claro/teal para ver todos
FG_LIGHT   = "#FFFFFF"
FG_STATUS_OK  = "#A9DFBF"
FG_STATUS_ERR = "#F1948A"

FONT_TITLE = ("Segoe UI", 13, "bold")
FONT_LABEL = ("Segoe UI", 10)
FONT_BTN   = ("Segoe UI", 10, "bold")
FONT_MONO  = ("Consolas", 10)

DURACION_PRESTAMO_DIAS = 15


class App(tk.Tk):
    """
    Ventana principal del sistema Biblioteca UCR.
    Carga los datos del XML al iniciar y construye la GUI con tres pestanas.
    """

    def __init__(self) -> None:
        """
        Parametros: ninguno
        Devuelve:   None
        Descripcion:
            Inicializa la ventana, carga los datos desde XML, construye
            las estructuras de datos en memoria e instancia las capas
            de negocio antes de mostrar la interfaz.
        """
        super().__init__()
        self.title("Biblioteca UCR \u2013 Recinto de Grecia")
        self.geometry("960x660")
        self.minsize(800, 580)
        self.configure(bg=BG_DARK)
        self._init_data()
        self._apply_styles()
        self._build_ui()

    # ----------------------------------------------------------
    # INICIALIZACION DE DATOS
    # ----------------------------------------------------------

    def _init_data(self) -> None:
        """
        Parametros: ninguno
        Devuelve:   None
        Descripcion:
            Crea XMLManager, carga los tres archivos de datos y puebla
            AVL de libros, TablaHash de estudiantes y ArbolRojinegro de
            prestamos. Instancia SistemaPrestamos y GestorEliminacion.
        """
        self.xml_manager = XMLManager()
        libros, estudiantes, prestamos = self.xml_manager.cargar_todo()

        # AVL de libros
        self.avl: ArbolAVL = ArbolAVL()
        for libro in libros:
            self.avl.raiz = self.avl.insertar(self.avl.raiz, libro)

        # Tabla Hash de estudiantes
        self.tabla_hash: TablaHash = TablaHash(100)
        for estudiante in estudiantes:
            self.tabla_hash.insertar(estudiante)

        # Arbol Rojinegro de prestamos
        self.arbol_prestamos: ArbolRojinegro = ArbolRojinegro()
        for prestamo in prestamos:
            self.arbol_prestamos.insertar(self.arbol_prestamos.raiz, prestamo)

        # Capas de negocio
        self.sistema_prestamos = SistemaPrestamos(
            self.avl, self.tabla_hash, self.arbol_prestamos, self.xml_manager
        )
        self.gestor_eliminacion = GestorEliminacion(
            self.avl, self.tabla_hash, self.sistema_prestamos, self.xml_manager
        )

    # ----------------------------------------------------------
    # ESTILOS ttk
    # ----------------------------------------------------------

    def _apply_styles(self) -> None:
        """
        Parametros: ninguno
        Devuelve:   None
        Descripcion:
            Configura el tema y los estilos de ttk para toda la aplicacion.
        """
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TNotebook",
                        background=BG_DARK,
                        borderwidth=0,
                        tabmargins=[4, 4, 0, 0])
        style.configure("TNotebook.Tab",
                        background=BG_PANEL,
                        foreground=FG_LIGHT,
                        font=FONT_BTN,
                        padding=[14, 7])
        style.map("TNotebook.Tab",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", FG_LIGHT)])

        style.configure("Treeview",
                        font=FONT_MONO,
                        rowheight=26,
                        background=BG_DARK,
                        foreground=FG_LIGHT,
                        fieldbackground=BG_DARK)
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 10, "bold"),
                        background=ACCENT,
                        foreground=FG_LIGHT)
        style.map("Treeview",
                  background=[("selected", ACCENT_SEL)],
                  foreground=[("selected", FG_LIGHT)])

        style.configure("Vertical.TScrollbar",
                        troughcolor=BG_DARK,
                        background=ACCENT)

    # ----------------------------------------------------------
    # CONSTRUCCION DE LA UI
    # ----------------------------------------------------------

    def _build_ui(self) -> None:
        """
        Parametros: ninguno
        Devuelve:   None
        Descripcion:
            Construye encabezado, ttk.Notebook con tres pestanas
            y barra de estado inferior.
        """
        # Encabezado
        header = tk.Frame(self, bg=ACCENT, height=56)
        header.pack(fill=tk.X)
        
        # Intentar cargar y mostrar el logo
        try:
            # Usar firma blanca por el fondo azul (ACCENT)
            self.logo_img = tk.PhotoImage(file="gui/iconos/firma-promocional-con-texto-blanco.png")
            
            # Ajustar tamaño si es muy grande (Photoimage.subsample usa factores enteros)
            if self.logo_img.width() > 250:
                factor = self.logo_img.width() // 200
                if factor > 0:
                    self.logo_img = self.logo_img.subsample(factor, factor)
                    
            tk.Label(header, image=self.logo_img, bg=ACCENT, borderwidth=0).pack(side=tk.RIGHT, padx=16, pady=5)
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")

        tk.Label(
            header,
            text="Biblioteca UCR \u2013 Recinto de Grecia",
            bg=ACCENT, fg=FG_LIGHT, font=FONT_TITLE,
        ).pack(side=tk.LEFT, padx=16, pady=10)

        # Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(8, 4))

        self._build_libros_tab()
        self._build_estudiantes_tab()
        self._build_prestamos_tab()

        # Barra de estado
        self.status_var = tk.StringVar(value="  Sistema listo.")
        self._status_bar = tk.Label(
            self,
            textvariable=self.status_var,
            bg=BG_PANEL, fg=FG_STATUS_OK,
            font=("Segoe UI", 9),
            anchor=tk.W, padx=6,
        )
        self._status_bar.pack(fill=tk.X, side=tk.BOTTOM, ipady=5)

    # ===========================================================
    # PESTANA LIBROS
    # ===========================================================

    def _build_libros_tab(self) -> None:
        """
        Parametros: ninguno
        Devuelve:   None
        Descripcion:
            Crea la pestana de gestion de libros con formulario de busqueda,
            botones de accion y Treeview de resultados.
        """
        tab = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(tab, text="Libros")

        # -- Formulario --
        form = tk.LabelFrame(tab, text=" Buscar / Eliminar ",
                             bg=BG_PANEL, fg=FG_LIGHT, font=FONT_LABEL)
        form.pack(fill=tk.X, padx=12, pady=(10, 4))

        # Fila 0: codigo y titulo
        tk.Label(form, text="Código:", bg=BG_PANEL, fg=FG_LIGHT,
                 font=FONT_LABEL).grid(row=0, column=0, padx=8, pady=6, sticky="e")
        self.lib_codigo = tk.Entry(form, width=10, font=FONT_MONO,
                                   bg="#1B2631", fg=FG_LIGHT,
                                   insertbackground=FG_LIGHT)
        self.lib_codigo.grid(row=0, column=1, padx=10, pady=8, sticky="w")
        self.lib_codigo.bind("<Return>", lambda e: self._lib_buscar_codigo())

        tk.Label(form, text="Título:", bg=BG_PANEL, fg=FG_LIGHT,
                 font=FONT_LABEL).grid(row=0, column=2, padx=8, pady=6, sticky="e")
        self.lib_titulo = tk.Entry(form, width=28, font=FONT_MONO,
                                   bg="#1B2631", fg=FG_LIGHT,
                                   insertbackground=FG_LIGHT)
        self.lib_titulo.grid(row=0, column=3, padx=10, pady=8, sticky="w")
        self.lib_titulo.bind("<Return>", lambda e: self._lib_buscar_titulo())

        # Fila 1: autor
        tk.Label(form, text="Autor:", bg=BG_PANEL, fg=FG_LIGHT,
                 font=FONT_LABEL).grid(row=1, column=0, padx=8, pady=6, sticky="e")
        self.lib_autor = tk.Entry(form, width=28, font=FONT_MONO,
                                  bg="#1B2631", fg=FG_LIGHT,
                                  insertbackground=FG_LIGHT)
        self.lib_autor.grid(row=1, column=1, columnspan=3, padx=10, pady=8, sticky="w")
        self.lib_autor.bind("<Return>", lambda e: self._lib_buscar_autor())

        # -- Botones --
        btn_frame = tk.Frame(tab, bg=BG_PANEL)
        btn_frame.pack(fill=tk.X, padx=12, pady=4)

        botones_lib = [
            ("Buscar código",  ACCENT,   self._lib_buscar_codigo),
            ("Buscar título",  ACCENT,   self._lib_buscar_titulo),
            ("Buscar autor",   ACCENT,   self._lib_buscar_autor),
            ("Eliminar",       BTN_DEL,  self._lib_eliminar),
            ("Ver todos",      BTN_VER,  self._lib_ver_todos),
        ]
        for col, (txt, bg, cmd) in enumerate(botones_lib):
            self._btn(btn_frame, txt, cmd, bg).grid(row=0, column=col, padx=4, pady=2)

        # -- Treeview --
        self.lib_tree = self._make_treeview(
            tab,
            columns=("codigo", "titulo", "autor", "anio", "editorial", "area"),
            headings=("Código", "Título", "Autor", "Año", "Editorial", "Área"),
            widths=(70, 210, 160, 55, 130, 110),
        )

    # Callbacks libros ----------------------------------------

    def _lib_buscar_codigo(self) -> None:
        raw = self.lib_codigo.get().strip()
        if not raw:
            return self._status("Ingrese un código.", ok=False)
        try:
            codigo = int(raw)
        except ValueError:
            return self._status("El código debe ser un número entero.", ok=False)

        libro = self.avl.buscar_codigo(self.avl.raiz, codigo)
        if libro is None:
            self._clear_tree(self.lib_tree)
            self.lib_tree.insert("", tk.END, values=("Sin resultados", "", "", "", "", ""))
            return self._status(f"Libro {codigo} no encontrado.", ok=False)
        self._poblar_libros([libro])
        self._status(f"Libro {codigo} encontrado.")

    def _lib_buscar_titulo(self) -> None:
        titulo = self.lib_titulo.get().strip()
        if not titulo:
            return self._status("Ingrese un título.", ok=False)
        libro = self.avl.buscar_titulo(self.avl.raiz, titulo)
        if libro is None:
            self._clear_tree(self.lib_tree)
            self.lib_tree.insert("", tk.END, values=("Sin resultados", "", "", "", "", ""))
            return self._status(f"No se encontro '{titulo}'.", ok=False)
        self._poblar_libros([libro])
        self._status(f"Libro '{titulo}' encontrado.")

    def _lib_buscar_autor(self) -> None:
        autor = self.lib_autor.get().strip()
        if not autor:
            return self._status("Ingrese un autor.", ok=False)
        libros = self.avl.buscar_autor(self.avl.raiz, autor)
        if not libros:
            self._clear_tree(self.lib_tree)
            self.lib_tree.insert("", tk.END, values=("Sin resultados", "", "", "", "", ""))
            return self._status(f"No hay libros de '{autor}'.", ok=False)
        self._poblar_libros(libros)
        self._status(f"{len(libros)} libro(s) de '{autor}'.")

    def _lib_eliminar(self) -> None:
        raw = self.lib_codigo.get().strip()
        if not raw:
            return self._status("Ingrese el código del libro a eliminar.", ok=False)
        try:
            codigo = int(raw)
        except ValueError:
            return self._status("El código debe ser un número entero.", ok=False)
        if not messagebox.askyesno("Confirmar", f"Eliminar libro {codigo}?"):
            return
        ok, msg = self.gestor_eliminacion.eliminar_libro(codigo)
        self._status(msg, ok=ok)
        if ok:
            self._lib_ver_todos()

    def _lib_ver_todos(self) -> None:
        libros = self.avl.obtener_libros_inorden(self.avl.raiz)
        self._poblar_libros(libros)
        self._status(f"{len(libros)} libro(s) en el sistema (inorden AVL).")

    def _poblar_libros(self, libros: List[Libro]) -> None:
        self._clear_tree(self.lib_tree)
        for i, libro in enumerate(libros):
            tag = "par" if i % 2 == 0 else "impar"
            self.lib_tree.insert(
                "", tk.END,
                values=(libro.codigo, libro.titulo, libro.autor,
                        libro.anio, libro.editorial, libro.area),
                tags=(tag,)
            )

    # ===========================================================
    # PESTANA ESTUDIANTES
    # ===========================================================

    def _build_estudiantes_tab(self) -> None:
        """
        Parametros: ninguno
        Devuelve:   None
        Descripcion:
            Crea la pestana de gestion de estudiantes con formulario,
            botones de accion y Treeview de resultados.
        """
        tab = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(tab, text="Estudiantes")

        # -- Formulario --
        form = tk.LabelFrame(tab, text=" Buscar / Eliminar ",
                             bg=BG_PANEL, fg=FG_LIGHT, font=FONT_LABEL)
        form.pack(fill=tk.X, padx=12, pady=(10, 4))

        # Fila 0: carnet y nombre
        tk.Label(form, text="Carnet:", bg=BG_PANEL, fg=FG_LIGHT,
                 font=FONT_LABEL).grid(row=0, column=0, padx=8, pady=6, sticky="e")
        self.est_carnet = tk.Entry(form, width=12, font=FONT_MONO,
                                   bg="#1B2631", fg=FG_LIGHT,
                                   insertbackground=FG_LIGHT)
        self.est_carnet.grid(row=0, column=1, padx=10, pady=8, sticky="w")
        self.est_carnet.bind("<Return>", lambda e: self._est_buscar_carnet())

        tk.Label(form, text="Nombre:", bg=BG_PANEL, fg=FG_LIGHT,
                 font=FONT_LABEL).grid(row=0, column=2, padx=8, pady=6, sticky="e")
        self.est_nombre = tk.Entry(form, width=28, font=FONT_MONO,
                                   bg="#1B2631", fg=FG_LIGHT,
                                   insertbackground=FG_LIGHT)
        self.est_nombre.grid(row=0, column=3, padx=10, pady=8, sticky="w")
        self.est_nombre.bind("<Return>", lambda e: self._est_buscar_nombre())

        # Fila 1: carrera
        tk.Label(form, text="Carrera:", bg=BG_PANEL, fg=FG_LIGHT,
                 font=FONT_LABEL).grid(row=1, column=0, padx=8, pady=6, sticky="e")
        self.est_carrera = tk.Entry(form, width=28, font=FONT_MONO,
                                    bg="#1B2631", fg=FG_LIGHT,
                                    insertbackground=FG_LIGHT)
        self.est_carrera.grid(row=1, column=1, columnspan=3, padx=10, pady=8, sticky="w")
        self.est_carrera.bind("<Return>", lambda e: self._est_buscar_carrera())

        # -- Botones --
        btn_frame = tk.Frame(tab, bg=BG_PANEL)
        btn_frame.pack(fill=tk.X, padx=12, pady=4)

        botones_est = [
            ("Buscar carnet",   ACCENT,  self._est_buscar_carnet),
            ("Buscar nombre",   ACCENT,  self._est_buscar_nombre),
            ("Buscar carrera",  ACCENT,  self._est_buscar_carrera),
            ("Eliminar",        BTN_DEL, self._est_eliminar),
            ("Ver todos",       BTN_VER, self._est_ver_todos),
        ]
        for col, (txt, bg, cmd) in enumerate(botones_est):
            self._btn(btn_frame, txt, cmd, bg).grid(row=0, column=col, padx=4, pady=2)

        # -- Treeview --
        self.est_tree = self._make_treeview(
            tab,
            columns=("carnet", "nombre", "carrera", "telefono", "correo", "direccion"),
            headings=("Carnet", "Nombre", "Carrera", "Teléfono", "Correo", "Dirección"),
            widths=(80, 170, 130, 90, 170, 140),
        )

    # Callbacks estudiantes -----------------------------------

    def _est_buscar_carnet(self) -> None:
        raw = self.est_carnet.get().strip()
        if not raw:
            return self._status("Ingrese un carnet.", ok=False)
        try:
            carnet = int(raw)
        except ValueError:
            return self._status("El carnet debe ser un número entero.", ok=False)
        est = self.tabla_hash.buscar_por_carnet(carnet)
        if est is None:
            self._clear_tree(self.est_tree)
            self.est_tree.insert("", tk.END, values=("Sin resultados", "", "", "", "", ""))
            return self._status(f"Estudiante {carnet} no encontrado.", ok=False)
        self._poblar_estudiantes([est])
        self._status(f"Estudiante {carnet} encontrado.")

    def _est_buscar_nombre(self) -> None:
        nombre = self.est_nombre.get().strip()
        if not nombre:
            return self._status("Ingrese un nombre.", ok=False)
        est = self.tabla_hash.buscar_por_nombre(nombre)
        if est is None:
            self._clear_tree(self.est_tree)
            self.est_tree.insert("", tk.END, values=("Sin resultados", "", "", "", "", ""))
            return self._status(f"Estudiante '{nombre}' no encontrado.", ok=False)
        self._poblar_estudiantes([est])
        self._status(f"Estudiante '{nombre}' encontrado.")

    def _est_buscar_carrera(self) -> None:
        carrera = self.est_carrera.get().strip()
        if not carrera:
            return self._status("Ingrese una carrera.", ok=False)
        # buscar_por_carrera devuelve solo nombres; recorremos para objetos completos
        resultados: List[Estudiante] = []
        for lista in self.tabla_hash.tabla_hash:
            nodo = lista.primero
            while nodo is not None:
                if nodo.valor.carrera.lower() == carrera.lower():
                    resultados.append(nodo.valor)
                nodo = nodo.sig
        if not resultados:
            self._clear_tree(self.est_tree)
            self.est_tree.insert("", tk.END, values=("Sin resultados", "", "", "", "", ""))
            return self._status(f"No hay estudiantes en '{carrera}'.", ok=False)
        self._poblar_estudiantes(resultados)
        self._status(f"{len(resultados)} estudiante(s) en '{carrera}'.")

    def _est_eliminar(self) -> None:
        raw = self.est_carnet.get().strip()
        if not raw:
            return self._status("Ingrese el carnet del estudiante a eliminar.", ok=False)
        try:
            carnet = int(raw)
        except ValueError:
            return self._status("El carnet debe ser un número entero.", ok=False)
        if not messagebox.askyesno("Confirmar", f"Eliminar estudiante {carnet}?"):
            return
        ok, msg = self.gestor_eliminacion.eliminar_estudiante(carnet)
        self._status(msg, ok=ok)
        if ok:
            self._est_ver_todos()

    def _est_ver_todos(self) -> None:
        todos: List[Estudiante] = []
        for lista in self.tabla_hash.tabla_hash:
            nodo = lista.primero
            while nodo is not None:
                todos.append(nodo.valor)
                nodo = nodo.sig
        self._poblar_estudiantes(todos)
        self._status(f"{len(todos)} estudiante(s) en el sistema.")

    def _poblar_estudiantes(self, estudiantes: List[Estudiante]) -> None:
        self._clear_tree(self.est_tree)
        for i, e in enumerate(estudiantes):
            tag = "par" if i % 2 == 0 else "impar"
            self.est_tree.insert(
                "", tk.END,
                values=(e.carnet, e.nombre, e.carrera,
                        e.telefono, e.correo, e.direccion),
                tags=(tag,)
            )

    # ===========================================================
    # PESTANA PRESTAMOS
    # ===========================================================

    def _build_prestamos_tab(self) -> None:
        """
        Parametros: ninguno
        Devuelve:   None
        Descripcion:
            Crea la pestana de prestamos: formularios para dar y devolver,
            boton de listado y Treeview con fecha de vencimiento calculada.
        """
        tab = tk.Frame(self.notebook, bg=BG_PANEL)
        self.notebook.add(tab, text="Préstamos")

        # -- Dar prestamo --
        form_dar = tk.LabelFrame(tab, text=" Dar Préstamo ",
                                 bg=BG_PANEL, fg=FG_LIGHT, font=FONT_LABEL)
        form_dar.pack(fill=tk.X, padx=12, pady=(10, 2))

        tk.Label(form_dar, text="Cod. libro:", bg=BG_PANEL, fg=FG_LIGHT,
                 font=FONT_LABEL).grid(row=0, column=0, padx=8, pady=6, sticky="e")
        self.pres_cod_libro = tk.Entry(form_dar, width=10, font=FONT_MONO,
                                       bg="#1B2631", fg=FG_LIGHT,
                                       insertbackground=FG_LIGHT)
        self.pres_cod_libro.grid(row=0, column=1, padx=10, pady=8, sticky="w")
        self.pres_cod_libro.bind("<Return>", lambda e: self.pres_carnet.focus_set())

        tk.Label(form_dar, text="Carnet:", bg=BG_PANEL, fg=FG_LIGHT,
                 font=FONT_LABEL).grid(row=0, column=2, padx=8, pady=6, sticky="e")
        self.pres_carnet = tk.Entry(form_dar, width=12, font=FONT_MONO,
                                    bg="#1B2631", fg=FG_LIGHT,
                                    insertbackground=FG_LIGHT)
        self.pres_carnet.grid(row=0, column=3, padx=10, pady=8, sticky="w")
        self.pres_carnet.bind("<Return>", lambda e: self._pres_dar())

        self._btn(form_dar, "Dar Préstamo", self._pres_dar, BTN_OK).grid(
            row=0, column=4, padx=12, pady=6)

        # -- Devolver libro --
        form_dev = tk.LabelFrame(tab, text=" Devolver Libro ",
                                 bg=BG_PANEL, fg=FG_LIGHT, font=FONT_LABEL)
        form_dev.pack(fill=tk.X, padx=12, pady=2)

        tk.Label(form_dev, text="Cod. préstamo:", bg=BG_PANEL, fg=FG_LIGHT,
                 font=FONT_LABEL).grid(row=0, column=0, padx=8, pady=6, sticky="e")
        self.pres_cod_prestamo = tk.Entry(form_dev, width=10, font=FONT_MONO,
                                          bg="#1B2631", fg=FG_LIGHT,
                                          insertbackground=FG_LIGHT)
        self.pres_cod_prestamo.grid(row=0, column=1, padx=10, pady=8, sticky="w")
        self.pres_cod_prestamo.bind("<Return>", lambda e: self._pres_devolver())

        self._btn(form_dev, "Devolver", self._pres_devolver, ACCENT).grid(
            row=0, column=2, padx=12, pady=6)

        # -- Boton Ver todos --
        btn_frame = tk.Frame(tab, bg=BG_PANEL)
        btn_frame.pack(fill=tk.X, padx=12, pady=4)
        self._btn(btn_frame, "Ver todos (inorden RB)", self._pres_ver_todos, BTN_VER).pack(
            side=tk.LEFT)

        # -- Treeview --
        self.pres_tree = self._make_treeview(
            tab,
            columns=("codigo", "libro", "carnet", "fecha", "vence"),
            headings=("Cod. Préstamo", "Cod. Libro", "Carnet", "Fecha", "Vence"),
            widths=(120, 100, 100, 110, 110),
        )

    # Callbacks prestamos -------------------------------------

    def _pres_dar(self) -> None:
        raw_libro  = self.pres_cod_libro.get().strip()
        raw_carnet = self.pres_carnet.get().strip()
        if not raw_libro or not raw_carnet:
            return self._status("Ingrese codigo de libro y carnet.", ok=False)
        try:
            cod_libro = int(raw_libro)
            carnet    = int(raw_carnet)
        except ValueError:
            return self._status("Código y carnet deben ser números enteros.", ok=False)
        ok, msg = self.sistema_prestamos.dar_prestamo(cod_libro, carnet)
        self._status(msg, ok=ok)
        if ok:
            self._pres_ver_todos()

    def _pres_devolver(self) -> None:
        raw = self.pres_cod_prestamo.get().strip()
        if not raw:
            return self._status("Ingrese el código del préstamo.", ok=False)
        try:
            cod = int(raw)
        except ValueError:
            return self._status("El código debe ser un número entero.", ok=False)
        if not messagebox.askyesno("Confirmar", f"Registrar devolución del préstamo {cod}?"):
            return
        ok, msg = self.sistema_prestamos.devolver_libro(cod)
        self._status(msg, ok=ok)
        if ok:
            self._pres_ver_todos()

    def _pres_ver_todos(self) -> None:
        prestamos = self.sistema_prestamos.listar_prestamos()
        self._poblar_prestamos(prestamos)
        self._status(f"{len(prestamos)} prestamo(s) activo(s) (inorden Rojinegro).")

    def _poblar_prestamos(self, prestamos: List[Prestamo]) -> None:
        self._clear_tree(self.pres_tree)
        for i, p in enumerate(prestamos):
            try:
                vence = (
                    datetime.strptime(p.fecha_prestamo, "%Y-%m-%d")
                    + timedelta(days=DURACION_PRESTAMO_DIAS)
                ).strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                vence = "—"
            
            tag = "par" if i % 2 == 0 else "impar"
            self.pres_tree.insert(
                "", tk.END,
                values=(p.codigo_prestamo, p.codigo_libro,
                        p.carnet_estudiante, p.fecha_prestamo, vence),
                tags=(tag,)
            )

    # ===========================================================
    # HELPERS COMPARTIDOS
    # ===========================================================

    @staticmethod
    def _btn(parent: tk.Widget, text: str, command, bg: str) -> tk.Button:
        """
        Parametros: parent, text, command, bg
        Devuelve:   tk.Button configurado con el estilo del proyecto.
        Descripcion:
            Factoria de botones para evitar repeticion de configuracion.
        """
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=FG_LIGHT,
            font=FONT_BTN,
            relief=tk.FLAT,
            width=14,  # Ancho fijo para uniformidad
            padx=10,
            pady=5,
            cursor="hand2",
            activebackground=ACCENT_SEL,
            activeforeground=FG_LIGHT,
        )

    @staticmethod
    def _make_treeview(
        parent: tk.Widget,
        columns: tuple,
        headings: tuple,
        widths: tuple,
    ) -> ttk.Treeview:
        """
        Parametros: parent (tk.Widget), columns (tuple), headings (tuple), widths (tuple)
        Devuelve:   ttk.Treeview con scrollbar vertical integrada.
        Descripcion:
            Factoria de Treeview para evitar repeticion en cada pestana.
            Empaqueta el Treeview y su scrollbar en un Frame interno.
        """
        container = tk.Frame(parent, bg=BG_PANEL)
        container.pack(fill=tk.BOTH, expand=True, padx=12, pady=(2, 8))

        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tree = ttk.Treeview(
            container,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
        )
        scrollbar.config(command=tree.yview)
        tree.pack(fill=tk.BOTH, expand=True)

        for col, heading, width in zip(columns, headings, widths):
            tree.heading(col, text=heading)
            tree.column(col, width=width, minwidth=50, anchor=tk.CENTER)
            
        tree.tag_configure("par", background="#1e2a3a")
        tree.tag_configure("impar", background="#16202e")

        return tree

    @staticmethod
    def _clear_tree(tree: ttk.Treeview) -> None:
        """
        Parametros: tree (ttk.Treeview)
        Devuelve:   None
        Descripcion:
            Elimina todas las filas del Treeview antes de repoblarlo.
        """
        for item in tree.get_children():
            tree.delete(item)

    def _status(self, msg: str, ok: bool = True) -> None:
        """
        Parametros: msg (str), ok (bool) — True = exito, False = error.
        Devuelve:   None
        Descripcion:
            Actualiza la barra de estado inferior con el mensaje y el
            color correspondiente (verde para exito, rojo para error).
        """
        simbolo = "\u2713" if ok else "\u2717"
        self.status_var.set(f"  {simbolo}  {msg}")
        self._status_bar.config(fg=FG_STATUS_OK if ok else FG_STATUS_ERR)


if __name__ == "__main__":
    app = App()
    app.mainloop()
