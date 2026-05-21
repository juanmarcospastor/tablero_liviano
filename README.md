# Tablero Económico Liviano

Versión liviana del tablero, lista para desplegar en Vercel usando una función Python serverless.

Incluye:

- Consulta a APIs externas con Python
- JSON serverless en `api/data.py`
- Frontend estático en `index.html`
- Gráficas con Plotly
- Calendario desde `data/calendario.csv`

## Ejecutar localmente

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abrir:

```text
http://127.0.0.1:5000
```

## Deploy en Vercel

1. Subir el proyecto a GitHub.
2. Ir a Vercel y crear un nuevo proyecto.
3. Seleccionar el repositorio.
4. Vercel detectará la función Python en `api/data.py` y servirá `index.html` como sitio estático.

La ruta de datos en producción será:

```text
/api/data
```

## Estructura de archivos

```text
api/data.py
app.py
index.html
lib.py
static/style.css
data/calendario.csv
requirements.txt
vercel.json
```
