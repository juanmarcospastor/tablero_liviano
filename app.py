from flask import Flask, render_template
from lib import obtener_dolares, obtener_riesgo_pais, obtener_inflacion, obtener_commodities, obtener_calendario

app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        "index.html",
        dolares=obtener_dolares(),
        riesgo_pais=obtener_riesgo_pais(),
        inflacion=obtener_inflacion(),
        commodities=obtener_commodities(),
        calendario=obtener_calendario()
    )


if __name__ == "__main__":
    app.run(debug=True)
