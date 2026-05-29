class Libro:
    
    def __init__(self, codigo, autor, titulo, anio, editorial, area):
        self.codigo = codigo
        self.autor = autor
        self.titulo = titulo
        self.anio = anio
        self.editorial = editorial
        self.area = area

    def __str__(self):
        return f"Libro: {self.titulo} por {self.autor} ({self.anio})"

    def __repr__(self):
        return f"Libro('{self.codigo}', '{self.autor}', '{self.titulo}', {self.anio}, '{self.editorial}', '{self.area}')"
