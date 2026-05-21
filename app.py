from flask import Flask, render_template
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# ======================================================
# URLs APIs
# ======================================================

URL_DOLARES = "https://api.argentinadatos.com/v1/cotizaciones/dolares"
URL_RIESGO_PAIS = "https://api.argentinadatos.com/v1/finanzas/indices/riesgo-pais"
URL_INFLACION = "https://api.argentinadatos.com/v1/finanzas/indices/inflacion"
URL_WTI = "https://query1.finance.yahoo.com/v8/finance/chart/CL=F?range=1mo&interval=1d"
URL_BRENT = "https://query1.finance.yahoo.com/v8/finance/chart/BZ=F?range=1mo&interval=1d"


# ======================================================
# Funciones auxiliares
# ======================================================

def get_json(url, timeout=15):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error consultando {url}: {e}")
        return None


def formato_pesos(valor):
    try:
        return f"$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "s/d"


def formato_numero(valor):
    try:
        return f"{float(valor):,.0f}".replace(",", ".")
    except Exception:
        return "s/d"


def formato_porcentaje(valor):
    try:
        return f"{float(valor):,.1f}%".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "s/d"


# ======================================================
# Dólares ArgentinaDatos
# ======================================================

def obtener_dolares():
    data = get_json(URL_DOLARES)

    if not data:
        return []

    orden = {
        "oficial": "Oficial",
        "blue": "Blue",
        "bolsa": "MEP",
        "contadoconliqui": "CCL",
        "mayorista": "Mayorista",
        "cripto": "Cripto",
        "tarjeta": "Tarjeta"
    }

    resultado = []

    for item in data:
        casa = item.get("casa", "")
        if casa in orden:
            resultado.append({
                "nombre": orden.get(casa, casa.title()),
                "compra": formato_pesos(item.get("compra")),
                "venta": formato_pesos(item.get("venta")),
                "fecha": item.get("fecha", "")
            })

    return resultado


# ======================================================
# Riesgo País
# ======================================================

def obtener_riesgo_pais():
    data = get_json(URL_RIESGO_PAIS)

    if not data:
        return {
            "valor": "s/d",
            "fecha": "s/d"
        }

    ultimo = data[-1]

    return {
        "valor": formato_numero(ultimo.get("valor")),
        "fecha": ultimo.get("fecha", "s/d")
    }


# ======================================================
# Inflación Argentina
# ======================================================

def obtener_inflacion():
    data = get_json(URL_INFLACION)

    if not data:
        return {
            "mensual": "s/d",
            "fecha": "s/d",
            "serie": []
        }

    ultimos = data[-12:]
    ultimo = data[-1]

    serie = []
    for item in ultimos:
        serie.append({
            "fecha": item.get("fecha", ""),
            "valor": item.get("valor", 0)
        })

    return {
        "mensual": formato_porcentaje(ultimo.get("valor")),
        "fecha": ultimo.get("fecha", "s/d"),
        "serie": serie
    }


# ======================================================
# Commodities Yahoo Finance
# ======================================================

def obtener_commodity_yahoo(url, nombre):
    data = get_json(url)

    try:
        result = data["chart"]["result"][0]
        timestamps = result["timestamp"]
        closes = result["indicators"]["quote"][0]["close"]

        serie = []

        for ts, close in zip(timestamps, closes):
            if close is not None:
                fecha = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                serie.append({
                    "fecha": fecha,
                    "valor": round(float(close), 2)
                })

        ultimo = serie[-1]["valor"] if serie else None

        return {
            "nombre": nombre,
            "valor": f"USD {ultimo:,.2f}" if ultimo is not None else "s/d",
            "serie": serie
        }

    except Exception as e:
        print(f"Error commodity {nombre}: {e}")
        return {
            "nombre": nombre,
            "valor": "s/d",
            "serie": []
        }


def obtener_commodities():
    return {
        "wti": obtener_commodity_yahoo(URL_WTI, "WTI"),
        "brent": obtener_commodity_yahoo(URL_BRENT, "Brent")
    }


# ======================================================
# Calendario simple desde CSV
# ======================================================

def obtener_calendario():
    path = DATA_DIR / "calendario.csv"

    if not path.exists():
        return []

    try:
        df = pd.read_csv(path, sep=";", encoding="utf-8-sig")

        df.columns = [c.strip().lower() for c in df.columns]

        posibles_fechas = ["fecha", "date", "periodo"]
        col_fecha = next((c for c in posibles_fechas if c in df.columns), None)

        if col_fecha:
            df[col_fecha] = pd.to_datetime(df[col_fecha], errors="coerce", dayfirst=True)
            df = df.dropna(subset=[col_fecha])
            df = df.sort_values(col_fecha)
            df["fecha_formateada"] = df[col_fecha].dt.strftime("%d/%m/%Y")
        else:
            df["fecha_formateada"] = ""

        eventos = []

        for _, row in df.head(20).iterrows():
            eventos.append({
                "fecha": row.get("fecha_formateada", ""),
                "evento": row.get("evento", row.get("descripcion", row.get("nombre", "Evento"))),
                "pais": row.get("pais", ""),
                "importancia": row.get("importancia", "")
            })

        return eventos

    except Exception as e:
        print(f"Error leyendo calendario.csv: {e}")
        return []


# ======================================================
# Página principal
# ======================================================

@app.route("/")
def index():
    dolares = obtener_dolares()
    riesgo_pais = obtener_riesgo_pais()
    inflacion = obtener_inflacion()
    commodities = obtener_commodities()
    calendario = obtener_calendario()

    return render_template(
        "index.html",
        dolares=dolares,
        riesgo_pais=riesgo_pais,
        inflacion=inflacion,
        commodities=commodities,
        calendario=calendario
    )


if __name__ == "__main__":
    app.run(debug=True)
