# 📚 Biblioteca UCR — Recinto de Grecia

Sistema de gestión de biblioteca desarrollado en Python para el curso de **Estructuras de Datos** de la Universidad de Costa Rica. Este proyecto implementa estructuras de datos avanzadas (Árboles y Tablas Hash) sin el uso de librerías externas para la lógica fundamental.

> **Integrantes:** Marcos Ferreto Estrada · Paulo Anchía Correás  
> **Entrega:** Viernes 26 de junio, antes de las 17:00 horas.  

---

## 🎯 Cumplimiento de la Rúbrica del Proyecto

El proyecto ha sido implementado y verificado en su totalidad según las especificaciones del documento `ProyectoProgramado.pdf`. 

| Requisito (Rúbrica) | Estado | Detalles de Implementación |
|---------------------|:---:|----------------------------|
| **Archivos .xml** | ✅ | Los datos se almacenan y persisten correctamente en `libros.xml`, `estudiantes.xml` y `prestamos.xml`, separados por `%`. Gestionado por `XMLManager`. |
| **Árbol Binario (AVL)** | ✅ | Estructura principal para almacenar `Libro`s. Se balancea automáticamente y ordena los registros por código de libro. |
| **Tabla Hash** | ✅ | Estructura para almacenar `Estudiante`s. Resuelve colisiones de llaves mediante encadenamiento (Listas Enlazadas). Llave: *Carnet*. |
| **Árbol Rojinegro** | ✅ | Estructura para controlar los `Prestamo`s. Garantiza balanceo estricto por color y rotaciones. Clave de orden: *Código de préstamo (4 dígitos)*. |
| **Búsquedas** | ✅ | Búsquedas de libros (código, autor, título) en O(log n) o recorrido. Búsquedas de estudiantes (carnet, nombre, carrera) en O(1) u O(n). |
| **Carga / Eliminación** | ✅ | Eliminación segura implementada en `GestorEliminacion`. **No se elimina** un libro prestado ni un estudiante con deudas. |
| **Préstamos** | ✅ | Lógica en `SistemaPrestamos`. Asigna préstamos por 15 días, previene que un libro prestado se vuelva a prestar. |
| **Interfaz Gráfica** | ✅ | Creada nativamente con `tkinter`. Incluye barras de estado, notificaciones, text-placeholders y visualización de árboles *in-orden*. (Optando a los +10 pts extra). |
| **Documentación Interna** | ✅ | Todas las funciones y clases incluyen el encabezado con los nombres de los integrantes, parámetros, retornos y descripción explícita del algoritmo. |
| **Documentación Externa** | ✅ | Documento `main.pdf` en la carpeta `docs/informe` generado en LaTeX, con conclusiones, problemas y referencias en APA. |

---

## 🚀 Requisitos previos e Instalación

1. **Python 3.12+**
2. **uv** (Gestor de dependencias ultrarrápido):
   - Linux/macOS: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

### Configuración
```bash
# 1. Clonar el repositorio
git clone https://github.com/FerretoDev/biblioteca-ucr-grecia.git
cd biblioteca-ucr-grecia

# 2. Instalar dependencias
uv sync
```

### Ejecutar la Aplicación
```bash
uv run main.py
# O usando Python puro:
python main.py
```

---

## 📂 Estructura del Proyecto

```text
biblioteca-ucr-grecia/
├── main.py                          ← Punto de entrada (Lanza la GUI)
├── pyproject.toml                   ← Configuración de entorno (uv)
├── datos/
│   ├── libros.xml                   ← Almacenamiento plano delimitado (%)
│   ├── estudiantes.xml              
│   └── prestamos.xml                
├── estructura_datos/
│   ├── arbol_avl/arbol_avl.py       ← Maneja la inserción/búsqueda de Libros
│   ├── arbol_rojinegro/arbol_rojinegro.py ← Maneja préstamos por código
│   └── tabla_hash/                  
│       ├── tabla_hash.py            ← Tablas hash - Implemetada como una un arreglo de arreglos, 
│       └── lista.py                 ← Lista enlazada para colisiones
├── clases/
│   ├── libro.py                     ← Modelo Entidad Libro
│   ├── estudiante.py                ← Modelo Entidad Estudiante
│   └── prestamo.py                  ← Modelo Entidad Prestamo
├── gui/
│   ├── interfaz.py                  ← Capa visual (Tkinter y ttk)
│   ├── xml_manager.py               ← Serializador/Deserializador (Persistencia)
│   ├── sistema_prestamos.py         ← Reglas de negocio (Préstamos a 15 días)
│   └── gestor_eliminacion.py        ← Validaciones de borrado (Dependencias)
└── ...                              ← Otras carpetas
```

---

## 💾 Formato de Archivos (Persistencia)

A pesar de tener extensión `.xml`, los archivos se comportan como archivos planos con campos delimitados por el carácter porcentaje (`%`), cumpliendo exactamente la especificación del curso.

**libros.xml** (Código % Autor % Título % Año % Editorial % Área)
```text
1001%Silvia Guardi%Estructuras de Datos%2006%MCGrawHill%Computación
```

**estudiantes.xml** (Carnet % Nombre % Carrera % Teléfono % Correo % Dirección)
```text
1001%Ana García%Informática%8888-1111%ana@ucr.ac.cr%Grecia
```

**prestamos.xml** (Cod. Préstamo % Cod. Libro % Carnet % Fecha de Préstamo)
```text
1000%1001%1001%2026-06-20
```

---

## 🤝 Flujo de Colaboración Git

Para futuras adiciones, se sigue una convención estricta:

```bash
git pull origin main
git checkout -b feature/nombre-tarea
git add .
git commit -m "feat: descripción"  # Usar feat, fix, docs, refactor
git push origin feature/nombre-tarea
```
