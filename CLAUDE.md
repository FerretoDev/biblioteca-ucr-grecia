# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Library management system for the UCR Recinto de Grecia Data Structures course. Members: Marcos Ferreto Estrada, Paulo Anchia Correas.

## Commands

```bash
# Install dependencies and create virtualenv
uv sync

# Run the project
uv run main.py
```

There are no tests yet (`test/` directory is empty).

## Architecture

The system has three layers:

1. **Domain models** (`clases/`) — Plain Python classes with no validation: `Libro`, `Estudiante`, `Prestamo`.

2. **Persistence** (`xml_manager.py`) — `XMLManager` reads/writes the `datos/*.xml` files. Despite the name and extension, the files use a plain-text `%`-delimited format (not real XML). Each load method follows a two-step pipeline:
   - `% line → dict` (intermediate JSON representation)
   - `dict → domain object`
   Saving reverses that. `cargar_todo()` / `guardar_todo()` load or save all three files at once.

3. **Data structures** (`estructuras_datos/`) — To be implemented:
   - AVL tree (balanced binary search tree) → books, sorted by `codigo` (3-digit string, unique)
   - Hash table with chaining (lists) → students, keyed by `carnet` (4-digit string, unique)
   - Red-Black tree → loans, keyed by `codigo_prestamo` (4-digit string, unique)

4. **GUI** (`gui/app.py`) — tkinter interface (pending), must support: queries, deletion, loans, and data visualization.

## Data file format

Files in `datos/` use `%` as a field separator (one record per line):

```
# libros.xml — codigo%autor%titulo%anio%editorial%areas
# 'areas' es una lista de strings (ej. "Computación,Matemáticas")
001%Silvia Guardi%Estructuras de Datos%2006%MCGrawHill%Computación
002%Juan Orós%PYTHON. Curso Práctico de Formación%2022%Alfaomega%programación

# estudiantes.xml — carnet%nombre%carrera%telefono%correo%direccion
1001%Ana García%Informática%8888-1111%ana@ucr.ac.cr%Grecia

# prestamos.xml — codigo_prestamo%codigo_libro%carnet_estudiante
0001%001%1001
```

Note: the actual `datos/*.xml` files currently contain real XML markup (from an earlier iteration). `XMLManager` expects the `%`-delimited format described above. When regenerating test data, use the `%` format.

## Required operations

**Books (AVL — in-order traversal):**
- `buscar_por_autor(autor)` → list of books
- `buscar_por_titulo(titulo)` → full book record
- `buscar_por_codigo(codigo)` → full book record
- `eliminar_libro(codigo)` — only if the book is not currently on loan

**Students (Hash table):**
- `buscar_por_carnet(carnet)` → full student record
- `buscar_por_nombre(nombre)` → full student record
- `buscar_por_carrera(carrera)` → list of names
- `eliminar_estudiante(carnet)` — only if the student has no active loans

**Loans (Red-Black tree — in-order traversal):**
- `realizar_prestamo(codigo_libro, carnet_estudiante)` — only if the book is not already on loan
- Loan duration: 15 days

## Grading rubric (total 100 pts + 10 extra)

| Component | Points |
|---|---|
| XML files | 6 |
| AVL tree | 15 |
| Hash table | 7 |
| Red-Black tree | 20 |
| Search operations | 12 |
| Load & deletion | 10 |
| Loans | 5 |
| GUI | 5 (+10 extra if outstanding) |
| Internal documentation | 7 |
| External report | ~13 |

## Internal documentation requirement

Every function must have a docstring with:
- **Parámetros**: parameter names and types
- **Devuelve**: return type and value
- **Descripción**: what the function does

## Commit convention

```
feat: new feature - closes #N
fix: bug fix - refs #N
docs: documentation - refs #N
refactor: refactoring - refs #N
test: tests - refs #N
```
