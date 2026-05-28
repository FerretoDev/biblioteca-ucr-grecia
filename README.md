# 📚 Biblioteca UCR — Recinto de Grecia

Sistema de gestión de biblioteca desarrollado en Python para el curso de **Estructuras de Datos** de la Universidad de Costa Rica.

> **Integrantes:** Marcos Ferreto Estrada · Paulo Anchia Correas 
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
```

---

## Estructura del proyecto

```
biblioteca-ucr-grecia/
├── main.py                  ← Punto de entrada
├── pyproject.toml           ← Configuración uv
├── datos/
│   ├── libros.xml           ← Base de datos de libros
│   ├── estudiantes.xml      ← Base de datos de estudiantes
│   └── prestamos.xml        ← Base de datos de préstamos
├── estructuras_datos/
│   ├── avl.py               ← Árbol AVL (libros)
│   ├── rbtree.py            ← Árbol Rojinegro (préstamos)
│   └── hashtable.py         ← Tabla Hash (estudiantes)
├── clases/
│   ├── libro.py             ← Clase Libro
│   ├── estudiante.py        ← Clase Estudiante
│   └── prestamo.py          ← Clase Prestamo
├── gui/
│   └── app.py               ← Interfaz gráfica (tkinter)
|
├── docs/
|   └── informe.pdf 
└── xml_manager.py       ← Carga y guardado de archivos XML
    
```

---

## Formato de los archivos XML

Los datos se separan con `%` en cada línea.

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
codigo_prestamo%codigo_libro%carnet_estudiante
0001%001%1001
```

---

## Estructuras de datos utilizadas

| Estructura | Archivo                    | Datos que maneja | Clave |
|---|----------------------------|---|---|
| Árbol AVL | `estructuras_datos/avl.py` | Libros | Código del libro |
| Tabla Hash | `estructuras_datos/hashtable.py`  | Estudiantes | Carnet |
| Árbol Rojinegro | `estructuras_datos/rbtree.py`     | Préstamos | Código de préstamo |

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
### Tipo de Cambio

* **feat:** descripción corta - closes #N
* **fix:** corrección - refs #N
* **docs:** documentación - refs #N
* **test:** prueba - refs #N


---

## Estado del proyecto

| Componente | Estado |
|---|---|
| Archivos XML | 🟡 En progreso |
| Árbol AVL | 🟡 En progreso |
| Tabla Hash | ⬜ Pendiente |
| Árbol Rojinegro | ⬜ Pendiente |
| Búsquedas | ⬜ Pendiente |
| Préstamos | ⬜ Pendiente |
| Interfaz Gráfica | ⬜ Pendiente |

