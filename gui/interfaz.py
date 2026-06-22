"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto - Paulo Anchía Correás
Archivo: interfaz.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional
from datetime import datetime

from clases.libro import Libro
from clases.estudiante import Estudiante
from clases.prestamo import Prestamo

from estructura_datos.arbol_avl.arbol_avl import ArbolAVL
from estructura_datos.tabla_hash.tabla_hash import TablaHash
from estructura_datos.arbol_rojinegro.arbol_rojinegro import ArbolRojinegro

from gestor_eliminacion import GestorEliminacion
from sistema_prestamos import SistemaPrestamos
from xml_manager import XMLManager

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Biblioteca UCR - Recinto de Grecia")
        self.geometry("900x600")

        # Cargar los datos desde los archivos XML
        self.xml_manager = XMLManager()
        libros, estudiantes, prestamos = self.xml_manager.cargar_todo()

        # Llenar AVL de libros
        self.avl = ArbolAVL()
        for libro in libros:
            self.avl.raiz = self.avl.insertar(self.avl.raiz, libro)

        # Llenar Tabla Hash de estudiantes
        self.tabla_hash = TablaHash(100)
        for estudiante in estudiantes:
            self.tabla_hash.insertar(estudiante)

        # Llenar Arbol Rojinegro de prestamos
        self.arbol_prestamos = ArbolRojinegro()
        for prestamo in prestamos:
            self.arbol_prestamos.insertar(self.arbol_prestamos.raiz, prestamo)

        # Iniciar gestores de negocio
        self.sistema_prestamos = SistemaPrestamos(
            self.avl, self.tabla_hash, self.arbol_prestamos, self.xml_manager
        )
        self.gestor_eliminacion = GestorEliminacion(
            self.avl, self.tabla_hash, self.sistema_prestamos, self.xml_manager
        )

        # Crear Notebook (Pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Crear los frames para cada pestaña
        self.tab_libros = tk.Frame(self.notebook)
        self.tab_estudiantes = tk.Frame(self.notebook)
        self.tab_prestamos = tk.Frame(self.notebook)

        # Agregar los frames al notebook
        self.notebook.add(self.tab_libros, text="Gestión de Libros")
        self.notebook.add(self.tab_estudiantes, text="Gestión de Estudiantes")
        self.notebook.add(self.tab_prestamos, text="Gestión de Préstamos")

        # Construir el contenido de cada pestaña
        self.construir_tab_libros()
        self.construir_tab_estudiantes()
        self.construir_tab_prestamos()

        # Barra de estado inferior
        self.estado_label = tk.Label(self, text="Sistema iniciado correctamente", relief=tk.SUNKEN, anchor="w")
        self.estado_label.pack(side=tk.BOTTOM, fill=tk.X)

    def status(self, msj):
        """Muestra un mensaje en la barra inferior."""
        self.estado_label.config(text=msj)

    # ---------------------------------------------------------
    # PESTAÑA LIBROS
    # ---------------------------------------------------------
    def construir_tab_libros(self):
        # Formularios y entradas
        frame_top = tk.Frame(self.tab_libros)
        frame_top.pack(pady=10)

        tk.Label(frame_top, text="Código del libro:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_codigo_libro = tk.Entry(frame_top)
        self.entry_codigo_libro.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_top, text="Nombre del libro:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_nombre_libro = tk.Entry(frame_top)
        self.entry_nombre_libro.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_top, text="Autor:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_autor_libro = tk.Entry(frame_top)
        self.entry_autor_libro.grid(row=2, column=1, padx=5, pady=5)

        # Botones
        frame_botones = tk.Frame(self.tab_libros)
        frame_botones.pack(pady=5)

        tk.Button(frame_botones, text="Buscar por Código", command=self.buscar_libro_codigo).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="Buscar por Nombre", command=self.buscar_libro_nombre).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="Buscar por Autor", command=self.buscar_libro_autor).grid(row=0, column=2, padx=5)
        tk.Button(frame_botones, text="Eliminar Libro", command=self.eliminar_libro).grid(row=0, column=3, padx=5)
        tk.Button(frame_botones, text="Ver Inorden AVL", command=self.ver_libros_inorden).grid(row=0, column=4, padx=5)

        # Tabla (Treeview)
        self.tree_libros = ttk.Treeview(self.tab_libros, columns=("codigo", "autor", "titulo", "anio", "editorial", "area"), show="headings")
        self.tree_libros.heading("codigo", text="Código")
        self.tree_libros.heading("autor", text="Autor")
        self.tree_libros.heading("titulo", text="Título")
        self.tree_libros.heading("anio", text="Año")
        self.tree_libros.heading("editorial", text="Editorial")
        self.tree_libros.heading("area", text="Área")

        self.tree_libros.column("codigo", width=80)
        self.tree_libros.column("autor", width=150)
        self.tree_libros.column("titulo", width=200)
        self.tree_libros.column("anio", width=60)
        self.tree_libros.column("editorial", width=120)
        self.tree_libros.column("area", width=120)

        self.tree_libros.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def buscar_libro_codigo(self):
        try:
            codigo = int(self.entry_codigo_libro.get())
        except ValueError:
            messagebox.showerror("Error", "El código debe ser un número entero.")
            return
        
        libro = self.avl.buscar_codigo(self.avl.raiz, codigo)
        self.tree_libros.delete(*self.tree_libros.get_children())
        if libro:
            self.tree_libros.insert("", tk.END, values=(libro.codigo, libro.autor, libro.titulo, libro.anio, libro.editorial, libro.area))
            self.status("Libro encontrado.")
        else:
            self.status("Libro no encontrado en el sistema.")

    def buscar_libro_nombre(self):
        nombre = self.entry_nombre_libro.get()
        if not nombre:
            messagebox.showerror("Error", "Debe ingresar un nombre.")
            return
        
        libros = self.avl.buscar_nombre(self.avl.raiz, nombre)
        self.tree_libros.delete(*self.tree_libros.get_children())
        for libro in libros:
            self.tree_libros.insert("", tk.END, values=(libro.codigo, libro.autor, libro.titulo, libro.anio, libro.editorial, libro.area))
        
        if libros:
            self.status(f"Se encontraron {len(libros)} libros con ese nombre.")
        else:
            self.status("No se encontraron libros.")

    def buscar_libro_autor(self):
        autor = self.entry_autor_libro.get()
        if not autor:
            messagebox.showerror("Error", "Debe ingresar un autor.")
            return
        
        libros = self.avl.buscar_autor(self.avl.raiz, autor)
        self.tree_libros.delete(*self.tree_libros.get_children())
        for libro in libros:
            self.tree_libros.insert("", tk.END, values=(libro.codigo, libro.autor, libro.titulo, libro.anio, libro.editorial, libro.area))
        
        if libros:
            self.status(f"Se encontraron {len(libros)} libros de ese autor.")
        else:
            self.status("No se encontraron libros.")

    def eliminar_libro(self):
        try:
            codigo = int(self.entry_codigo_libro.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese el código del libro a eliminar en la caja de texto correspondiente.")
            return

        respuesta = messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar el libro con código {codigo}?")
        if respuesta:
            exito, msj = self.gestor_eliminacion.eliminar_libro(codigo)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self.ver_libros_inorden()
            else:
                messagebox.showerror("No se pudo eliminar", msj)
            self.status(msj)

    def ver_libros_inorden(self):
        libros = self.avl.obtener_libros_inorden(self.avl.raiz)
        self.tree_libros.delete(*self.tree_libros.get_children())
        for libro in libros:
            self.tree_libros.insert("", tk.END, values=(libro.codigo, libro.autor, libro.titulo, libro.anio, libro.editorial, libro.area))
        self.status("Mostrando todos los libros ordenados (in-orden).")

    # ---------------------------------------------------------
    # PESTAÑA ESTUDIANTES
    # ---------------------------------------------------------
    def construir_tab_estudiantes(self):
        frame_top = tk.Frame(self.tab_estudiantes)
        frame_top.pack(pady=10)

        tk.Label(frame_top, text="Carnet:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_carnet_est = tk.Entry(frame_top)
        self.entry_carnet_est.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_top, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_nombre_est = tk.Entry(frame_top)
        self.entry_nombre_est.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_top, text="Carrera:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_carrera_est = tk.Entry(frame_top)
        self.entry_carrera_est.grid(row=2, column=1, padx=5, pady=5)

        frame_botones = tk.Frame(self.tab_estudiantes)
        frame_botones.pack(pady=5)

        tk.Button(frame_botones, text="Buscar por Carnet", command=self.buscar_est_carnet).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="Buscar por Nombre", command=self.buscar_est_nombre).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="Buscar por Carrera", command=self.buscar_est_carrera).grid(row=0, column=2, padx=5)
        tk.Button(frame_botones, text="Eliminar Estudiante", command=self.eliminar_estudiante).grid(row=0, column=3, padx=5)
        tk.Button(frame_botones, text="Ver Todos", command=self.ver_todos_estudiantes).grid(row=0, column=4, padx=5)

        self.tree_estudiantes = ttk.Treeview(self.tab_estudiantes, columns=("carnet", "nombre", "carrera", "telefono", "correo", "direccion"), show="headings")
        self.tree_estudiantes.heading("carnet", text="Carnet")
        self.tree_estudiantes.heading("nombre", text="Nombre")
        self.tree_estudiantes.heading("carrera", text="Carrera")
        self.tree_estudiantes.heading("telefono", text="Teléfono")
        self.tree_estudiantes.heading("correo", text="Correo")
        self.tree_estudiantes.heading("direccion", text="Dirección")

        self.tree_estudiantes.column("carnet", width=80)
        self.tree_estudiantes.column("nombre", width=150)
        self.tree_estudiantes.column("carrera", width=120)
        self.tree_estudiantes.column("telefono", width=100)
        self.tree_estudiantes.column("correo", width=150)
        self.tree_estudiantes.column("direccion", width=150)

        self.tree_estudiantes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def buscar_est_carnet(self):
        try:
            carnet = int(self.entry_carnet_est.get())
        except ValueError:
            messagebox.showerror("Error", "El carnet debe ser un número entero.")
            return
        
        est = self.tabla_hash.buscar_por_carnet(carnet)
        self.tree_estudiantes.delete(*self.tree_estudiantes.get_children())
        if est:
            self.tree_estudiantes.insert("", tk.END, values=(est.carnet, est.nombre, est.carrera, est.telefono, est.correo, est.direccion))
            self.status("Estudiante encontrado.")
        else:
            self.status("Estudiante no encontrado.")

    def buscar_est_nombre(self):
        nombre = self.entry_nombre_est.get()
        if not nombre:
            messagebox.showerror("Error", "Debe ingresar el nombre del estudiante.")
            return
        
        lista = self.tabla_hash.buscar_por_nombre(nombre)
        self.tree_estudiantes.delete(*self.tree_estudiantes.get_children())
        for est in lista:
            self.tree_estudiantes.insert("", tk.END, values=(est.carnet, est.nombre, est.carrera, est.telefono, est.correo, est.direccion))
        
        self.status(f"Se encontraron {len(lista)} estudiantes.")

    def buscar_est_carrera(self):
        carrera = self.entry_carrera_est.get()
        if not carrera:
            messagebox.showerror("Error", "Debe ingresar una carrera.")
            return
        
        lista = self.tabla_hash.buscar_por_carrera(carrera)
        self.tree_estudiantes.delete(*self.tree_estudiantes.get_children())
        for est in lista:
            self.tree_estudiantes.insert("", tk.END, values=(est.carnet, est.nombre, est.carrera, est.telefono, est.correo, est.direccion))
        
        self.status(f"Se encontraron {len(lista)} estudiantes en esa carrera.")

    def eliminar_estudiante(self):
        try:
            carnet = int(self.entry_carnet_est.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese el carnet del estudiante a eliminar en la caja de texto.")
            return

        respuesta = messagebox.askyesno("Confirmar", f"¿Desea eliminar el estudiante {carnet}?")
        if respuesta:
            exito, msj = self.gestor_eliminacion.eliminar_estudiante(carnet)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self.ver_todos_estudiantes()
            else:
                messagebox.showerror("No se pudo eliminar", msj)
            self.status(msj)

    def ver_todos_estudiantes(self):
        self.tree_estudiantes.delete(*self.tree_estudiantes.get_children())
        count = 0
        for lista in self.tabla_hash.tabla_hash:
            actual = lista.primero
            while actual is not None:
                est = actual.valor
                self.tree_estudiantes.insert("", tk.END, values=(est.carnet, est.nombre, est.carrera, est.telefono, est.correo, est.direccion))
                actual = actual.sig
                count += 1
        self.status(f"Mostrando todos los {count} estudiantes almacenados.")

    # ---------------------------------------------------------
    # PESTAÑA PRESTAMOS
    # ---------------------------------------------------------
    def construir_tab_prestamos(self):
        frame_top = tk.Frame(self.tab_prestamos)
        frame_top.pack(pady=10)

        tk.Label(frame_top, text="Código Libro:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_prestamo_libro = tk.Entry(frame_top)
        self.entry_prestamo_libro.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_top, text="Carnet Estudiante:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_prestamo_est = tk.Entry(frame_top)
        self.entry_prestamo_est.grid(row=1, column=1, padx=5, pady=5)

        frame_botones = tk.Frame(self.tab_prestamos)
        frame_botones.pack(pady=5)

        tk.Button(frame_botones, text="Dar Préstamo", command=self.dar_prestamo).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="Ver Préstamos (Inorden)", command=self.ver_prestamos_inorden).grid(row=0, column=1, padx=5)

        self.tree_prestamos = ttk.Treeview(self.tab_prestamos, columns=("codigo_prestamo", "codigo_libro", "carnet", "fecha"), show="headings")
        self.tree_prestamos.heading("codigo_prestamo", text="Código Préstamo")
        self.tree_prestamos.heading("codigo_libro", text="Código Libro")
        self.tree_prestamos.heading("carnet", text="Carnet Estudiante")
        self.tree_prestamos.heading("fecha", text="Fecha de Préstamo")

        self.tree_prestamos.column("codigo_prestamo", width=120)
        self.tree_prestamos.column("codigo_libro", width=120)
        self.tree_prestamos.column("carnet", width=120)
        self.tree_prestamos.column("fecha", width=150)

        self.tree_prestamos.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def dar_prestamo(self):
        try:
            cod_libro = int(self.entry_prestamo_libro.get())
            carnet = int(self.entry_prestamo_est.get())
        except ValueError:
            messagebox.showerror("Error", "El código de libro y el carnet deben ser números.")
            return

        exito, msj = self.sistema_prestamos.dar_prestamo(cod_libro, carnet)
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.ver_prestamos_inorden()
        else:
            messagebox.showerror("Error", msj)
        self.status(msj)

    def ver_prestamos_inorden(self):
        prestamos = self.arbol_prestamos.inorden(self.arbol_prestamos.raiz)
        self.tree_prestamos.delete(*self.tree_prestamos.get_children())
        for p in prestamos:
            self.tree_prestamos.insert("", tk.END, values=(p.codigo_prestamo, p.codigo_libro, p.carnet_estudiante, p.fecha_prestamo))
        self.status("Mostrando préstamos en el árbol rojinegro (in-orden).")
