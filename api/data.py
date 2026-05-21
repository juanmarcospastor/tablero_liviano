import json
from lib import obtener_dolares, obtener_riesgo_pais, obtener_inflacion, obtener_commodities, obtener_calendario


def handler(request):
    data = {
        "dolares": obtener_dolares(),
        "riesgo_pais": obtener_riesgo_pais(),
        "inflacion": obtener_inflacion(),
        "commodities": obtener_commodities(),
        "calendario": obtener_calendario()
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json; charset=utf-8"
        },
        "body": json.dumps(data, ensure_ascii=False)
    }
