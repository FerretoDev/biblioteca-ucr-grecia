# 📚 Biblioteca UCR — Recinto de Grecia

Sistema de gestión de biblioteca desarrollado en Python para el curso de **Estructuras de Datos** de la Universidad de Costa Rica.

> **Integrantes:** Marcos Ferreto Estrada · [Nombre 2]
> **Entrega:** Viernes 26 de junio, 17:00 hrs

---

## Requisitos previos

- [Python 3.12+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) — gestor de entornos y dependencias

### Instalar `uv` (si no lo tenés)

**Linux / macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Configuración inicial (solo la primera vez)

```bash
# 1. Clonar el repositorio
git clone https://github.com/FerretoDev/biblioteca-ucr-grecia.git
cd biblioteca-ucr-grecia

# 2. Crear el entorno virtual e instalar dependencias
uv sync

# 3. Verificar que todo esté bien
uv run python --version
```

---

## Correr el proyecto

```bash
uv run main.py
# O alternativamente sin uv:
python main.py
```

---

## Estructura del proyecto

```
biblioteca-ucr-grecia/
├── main.py                          ← Punto de entrada
├── pyproject.toml                   ← Configuración uv
├── datos/
│   ├── libros.xml                   ← Base de datos de libros
│   ├── estudiantes.xml              ← Base de datos de estudiantes
│   └── prestamos.xml                ← Base de datos de préstamos
├── estructura_datos/
│   ├── arbol_avl/arbol_avl.py       ← Árbol AVL (libros)
│   ├── arbol_rojinegro/arbol_rojinegro.py ← Árbol Rojinegro (préstamos)
│   └── tabla_hash/tabla_hash.py     ← Tabla Hash (estudiantes)
├── clases/
│   ├── libro.py                     ← Clase Libro
│   ├── estudiante.py                ← Clase Estudiante
│   └── prestamo.py                  ← Clase Prestamo
├── gui/
│   └── interfaz.py                  ← Interfaz gráfica principal (tkinter)
├── docs/
│   └── informe.pdf                  ← Documentación del proyecto
├── xml_manager.py                   ← Carga y guardado de archivos de datos (%)
├── sistema_prestamos.py             ← Lógica de negocio para préstamos
└── gestor_eliminacion.py            ← Lógica de negocio para eliminaciones seguras
```

---

## Formato de los archivos de datos

Los datos se separan con `%` en cada línea (los archivos conservan la extensión `.xml` pero usan formato de texto plano delimitado).

**libros.xml**
```
codigo%autor%titulo%anio%editorial%area
001%Silvia Guardi%Estructuras de Datos%2006%MCGrawHill%Computación
```

**estudiantes.xml**
```
carnet%nombre%carrera%telefono%correo%direccion
1001%Ana García%Informática%8888-1111%ana@ucr.ac.cr%Grecia
```

**prestamos.xml**
```
codigo_prestamo%codigo_libro%carnet_estudiante%fecha_prestamo
0001%001%1001%2026-06-21
```

---

## Estructuras de datos utilizadas

| Estructura | Archivo | Datos que maneja | Clave de ordenamiento/búsqueda |
|---|---|---|---|
| **Árbol AVL** | `estructura_datos/arbol_avl/arbol_avl.py` | Libros | Código del libro |
| **Tabla Hash** | `estructura_datos/tabla_hash/tabla_hash.py` | Estudiantes | Carnet (resolución de colisiones por listas) |
| **Árbol Rojinegro** | `estructura_datos/arbol_rojinegro/arbol_rojinegro.py` | Préstamos | Código de préstamo |

---

## Flujo de trabajo en Git

```bash
# Antes de empezar a trabajar, siempre jalá los últimos cambios
git pull origin main

# Crear una rama para tu feature
git checkout -b feature/avl-tree

# Cuando terminés, subir cambios
git add .
git commit -m "feat: implementar inserción AVL"
git push origin feature/avl-tree

# Luego hacer Pull Request a main en GitHub
```

### Convención de commits

```
feat: nueva funcionalidad
fix: corrección de bug
docs: cambios en documentación
refactor: refactorización de código
```

---

## Estado del proyecto

| Componente | Estado | Detalles |
|---|---|---|
| Archivos de texto (`%`) | ✅ Completado | Carga y guardado directo de objetos vía `XMLManager` |
| Árbol AVL | ✅ Completado | Inserción, búsqueda, eliminación y rotaciones |
| Tabla Hash | ✅ Completado | Inserción, búsqueda y eliminación (por encadenamiento) |
| Árbol Rojinegro | ✅ Completado | Inserción y balanceo por color y rotaciones |
| Préstamos | ✅ Completado | Control de asignación y devolución (`SistemaPrestamos`) |
| Eliminación Segura | ✅ Completado | Validación de dependencias antes de borrar (`GestorEliminacion`) |
| Interfaz Gráfica | ✅ Completado | Pestañas, búsquedas y visualización vía `tkinter` (`gui/interfaz.py`) |
