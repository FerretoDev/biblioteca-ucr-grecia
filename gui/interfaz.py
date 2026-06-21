"""
Breve descripción de las funciones de tkinter (interfaz gráfica) usadas aquí:
- tk.Tk(): Crea la ventana principal de la app
- geometry(): Define el tamaño de la ventana, por ejemplo "600x700" 
- title(): Pone el título arriba en la ventana
- config(): Permite cambiar configuraciones, como el color de fondo (bg)
- tk.Frame(): Hace un cuadrito o contenedor donde podemos agrupar otros elementos
- pack() / grid(): Son formas de acomodar las cosas en la pantalla (pack lo empaca de una vez, grid usa filas y columnas)
- tk.Label(): Pone un textito normal en la pantalla
- tk.Entry(): Pone una caja de texto para que el usuario escriba
- tk.Button(): Crea un botón y con 'command' le decimos qué función hacer al presionarlo
- messagebox: Saca ventanitas emergentes de error (#showerror), advertencia (#showwarning) o info (#showinfo)
- mainloop(): Mantiene la app esperando que hagamos clic en algo y no se cierre de inmediato
"""

import tkinter as tk
from tkinter import messagebox

from mascota import Mascota
from tabla import Tabla

BG_COLOR: str = "#2C3E50"   # negro azulado
FRAME_BG: str = "#ECF0F1"   # blanco
BTN_BG: str = "#3498DB"     # azul
BTN_FG: str = "white"


class App(tk.Tk):
    """
    Interfaz gráfica para gestionar los animales atendidos en el hospital veterinario de Grecia
    Utiliza una Tabla Hash con manejo de colisiones mediante listas simples enlazadas.
    """

    def __init__(self) -> None:
        super().__init__()
        self.geometry("600x700")
        self.title("Hospital Veterinario Grecia")
        self.config(bg=BG_COLOR)
        # Inicializamos la tabla hash con máximo de 20 casillas
        self.tabla_hash = Tabla(20)
        self._build_ui()

    def _build_ui(self) -> None:
        """
        Construye y acomoda todo en la interfaz gráfica
        Pone los cuadros de texto, los textos de indicación y los 4 botones principales
        """
        self.frame = tk.Frame(
            self,
            bg=FRAME_BG,
            bd=3,
            relief=tk.RIDGE,
        )
        self.frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        titulo = tk.Label(
            self.frame,
            text="Gestión de Mascotas",
            bg=FRAME_BG,
            font=("Arial", 16, "bold"),
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=15)

        # Labels y Entries
        labels = [
            "Nombre Mascota:",
            "Nombre Dueño:",
            "Cédula Dueño:",
            "Dirección (distrito-cantón-provincia):",
            "Enfermedad:",
            "Especie:",
            "Edad:",
        ]

        self.entries: dict[str, tk.Entry] = {}
        for i, text in enumerate(labels):
            lbl = tk.Label(self.frame, text=text, bg=FRAME_BG, font=("Arial", 11))
            lbl.grid(row=i + 1, column=0, sticky="e", padx=10, pady=5)

            entry = tk.Entry(
                self.frame, width=30, font=("Arial", 11), bd=2, relief=tk.SUNKEN
            )
            entry.grid(row=i + 1, column=1, padx=10, pady=5)
            self.entries[text] = entry

        # Botones
        button_frame = tk.Frame(self.frame, bg=FRAME_BG)
        button_frame.grid(row=len(labels) + 1, column=0, columnspan=2, pady=20)

        botones = [
            ("Agregar mascota", self._on_agregar),
            ("Mostrar mascota", self._on_mostrar),
            ("Eliminar mascota", self._on_eliminar),
            ("Buscar índice y posición", self._on_buscar_indice_posicion),
        ]

        for i, (text, command) in enumerate(botones):
            btn = tk.Button(
                button_frame,
                text=text,
                bg=BTN_BG,
                fg=BTN_FG,
                font=("Arial", 11, "bold"),
                command=command,
                width=25,
            )
            btn.grid(row=i, column=0, pady=5)

        nota = tk.Label(
            button_frame,
            text="* Mostrar, eliminar y buscar usan solo\nNombre Mascota y Nombre Dueño",
            bg=FRAME_BG,
            fg="#7F8C8D",
            font=("Arial", 9, "italic"),
            justify=tk.CENTER,
        )
        nota.grid(row=len(botones), column=0, pady=(10, 0))

    def _obtener_clave_actual(self) -> str:
        """
        Toma lo que el usuario escribió en Nombre de Mascota y Dueño,
        y hace la clave juntándolos, en minúscula y sin espacios
        """
        nombre_mascota = self.entries["Nombre Mascota:"].get().strip().lower()
        nombre_dueno = self.entries["Nombre Dueño:"].get().strip().lower()
        return f"{nombre_mascota}{nombre_dueno}"

    def _limpiar_campos(self) -> None:
        """
        Borra todo lo que esté escrito en las cajas de texto de la interfaz
        """
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def _on_agregar(self) -> None:
        """
        Agrega la mascota a la tabla hash jalando los datos de los espacios escritos
        Avisa si faltan datos importantes y si sale bien limpia todos los campos
        """
        try:
            mascota = Mascota(
                self.entries["Nombre Mascota:"].get().strip(),
                self.entries["Nombre Dueño:"].get().strip(),
                self.entries["Cédula Dueño:"].get().strip(),
                self.entries["Dirección (distrito-cantón-provincia):"].get().strip(),
                self.entries["Enfermedad:"].get().strip(),
                self.entries["Especie:"].get().strip(),
                self.entries["Edad:"].get().strip(),
            )
            if not mascota.nombre_mascota or not mascota.nombre_dueno:
                messagebox.showwarning(
                    "Faltan datos",
                    "El nombre de la mascota y del dueño son obligatorios.",
                )
                return

            self.tabla_hash.agregar(mascota)
            messagebox.showinfo(
                "Éxito", "Mascota agregada correctamente a la Tabla Hash."
            )
            self._limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al agregar: {e}")

    def _on_mostrar(self) -> None:
        """
        Busca a la mascota usando su clave (nombre + dueño),
        y si la encuentra saca un mensaje con la info de la mascota y del dueño respectivo
        """
        clave = self._obtener_clave_actual()
        if not clave:
            messagebox.showwarning(
                "Faltan datos", "Ingrese nombre de mascota y dueño para buscar."
            )
            return

        mascota = self.tabla_hash.buscar(clave)
        if mascota:
            info = (
                f"Nombre Mascota: {mascota.nombre_mascota}\n"
                f"Dueño: {mascota.nombre_dueno}\n"
                f"Cédula: {mascota.cedula_dueno}\n"
                f"Dirección: {mascota.direccion}\n"
                f"Enfermedad: {mascota.enfermedad}\n"
                f"Especie: {mascota.especie}\n"
                f"Edad: {mascota.edad}"
            )
            messagebox.showinfo("Datos de la Mascota", info)
        else:
            messagebox.showwarning(
                "No encontrado", "Mascota no encontrada en la Tabla Hash."
            )

    def _on_eliminar(self) -> None:
        """
        Pide el nombre de la mascota y del dueño para borrar a la mascota de la tabla
        y tira un mensaje si lo logró hacer o no
        """
        clave = self._obtener_clave_actual()
        if not clave:
            messagebox.showwarning(
                "Faltan datos", "Ingrese nombre de mascota y dueño para eliminar."
            )
            return

        eliminado = self.tabla_hash.eliminar(clave)
        if eliminado:
            messagebox.showinfo(
                "Éxito", "Mascota eliminada correctamente de la Tabla Hash."
            )
        else:
            messagebox.showwarning(
                "No encontrado", "Mascota no encontrada para eliminar."
            )

    def _on_buscar_indice_posicion(self) -> None:
        """
        Devuelve información técnica: muestra cuál es el índice principal de la tabla 
        y la posición de lista en donde se quedó asignado el nodo de esta mascota
        """
        clave = self._obtener_clave_actual()
        if not clave:
            messagebox.showwarning(
                "Faltan datos", "Ingrese nombre de mascota y dueño para buscar."
            )
            return

        indice, posicion = self.tabla_hash.buscar_indice_y_posicion(clave)
        if indice != -1:
            messagebox.showinfo(
                "Ubicación en Memoria",
                f"La mascota (clave: '{clave}') se encuentra en:\n\n"
                f"- Índice de la Tabla Hash: {indice}\n"
                f"- Posición en la Lista Enlazada: {posicion}",
            )
        else:
            messagebox.showwarning("No encontrado", "Mascota no encontrada.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
