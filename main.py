"""
Proyecto: Biblioteca UCR - Recinto de Grecia
Curso: Estructuras de Datos
Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
Archivo: main.py
"""

from gui.interfaz import App


def main():
    """
    Integrantes: Marcos Ferreto Estrada - Paulo Anchía Correás
    Propósito: Función principal que sirve como punto de entrada para arrancar la aplicación.
    Parámetros: Ninguno.
    Devuelve: Nada (None).
    """
    # Se crea una instancia de la interfaz gráfica principal de la aplicación.
    app = App()
    # Se inicia el bucle principal de la interfaz para que la ventana se mantenga abierta y responda a las acciones.
    app.mainloop()


if __name__ == "__main__":
    main()
