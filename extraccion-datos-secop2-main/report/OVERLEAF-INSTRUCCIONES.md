# Guía rápida para compilar el informe en Overleaf

## Pasos

1. Crear un proyecto nuevo en [Overleaf](https://www.overleaf.com/) → **New project** → **Blank Project**.
2. Borrar el `main.tex` que viene por defecto.
3. Copiar el contenido completo de `main.tex` (este repositorio) y pegarlo en el archivo `main.tex` de Overleaf.
4. Crear una carpeta llamada `imagenes/` dentro del proyecto Overleaf.
5. Subir los 26 archivos PNG de `report/imagenes/` a esa carpeta (selección múltiple).
6. Cambiar el compilador a **pdfLaTeX** (Menú → Settings → Compiler).
7. Hacer clic en **Recompile**.

## Si aparecen errores

- **"Missing image"**: verificar que las imágenes estén en `imagenes/` y con el mismo nombre exacto (sensitive a mayúsculas).
- **Compilación lenta**: la primera compilación toma 30–60 segundos por el volumen de contenido. Las siguientes son más rápidas.
- **Caracteres especiales**: si Overleaf reporta error con tildes, verificar que el archivo se guarde en codificación UTF-8.

## Personalización

- Cambiar el tipo de letra: línea con `\usepackage{times}`. Alternativas: `\usepackage{mathptmx}`, eliminar línea para usar Computer Modern.
- Cambiar interlineado: `\onehalfspacing` (1,5) o `\doublespacing` (2,0).
- Logo de la universidad: si tienes el logo de UFPS en formato PNG, súbelo a `imagenes/logo_ufps.png` y descomenta la línea correspondiente en la portada.

## Tiempo estimado de compilación

Aproximadamente 60 segundos en la primera compilación. La salida es un PDF de unas 60–80 páginas.
