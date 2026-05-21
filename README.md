# Tablero Económico Liviano

Versión mínima del tablero para publicar en Vercel.

Incluye:

- Flask
- Jinja templates
- Dólar desde ArgentinaDatos
- Riesgo País desde ArgentinaDatos
- Inflación mensual desde ArgentinaDatos
- WTI y Brent desde Yahoo Finance
- Calendario simple desde CSV

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

## Publicar en Vercel

1. Subir el proyecto a GitHub.
2. Entrar a Vercel.
3. Importar el repositorio.
4. Hacer Deploy.

## Estructura

```text
app.py
templates/index.html
static/style.css
data/calendario.csv
requirements.txt
vercel.json
```
