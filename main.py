import os
import random
from flask import Flask, request, jsonify
import datetime
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

FRASES_MOTIVACIONALES = [
    "Cada esfuerzo suma. No pares.",
    "La disciplina es tu mejor aliada. Dale con todo.",
    "No tiene que salir perfecto. Tiene que salir real.",
    "Lo que hagas hoy, tu yo del futuro te lo va a agradecer.",
    "No esperes el momento perfecto. Hacelo ahora."
]

def enviar_a_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje
    }
    requests.post(url, json=payload)

@app.route('/actualizar_tareas', methods=['POST'])
def actualizar_tareas():
    datos = request.json

    # Convertir fechas
    def fecha_formateada(fecha_str):
        try:
            fecha = datetime.datetime.strptime(fecha_str, "%d/%m/%Y")
            return fecha.strftime("%-d de %B de %Y")
        except:
            return None

    fecha_hoy = fecha_formateada(datetime.datetime.now().strftime("%d/%m/%Y"))
    fecha_limite = fecha_formateada(datos["F2"]) if datos["F2"] else None

    # Construcción del mensaje en prosa
    mensaje = f"📌 Recordá que hoy, {fecha_hoy}, "

    if datos["E2"]:
        mensaje += f"tenés que {datos['E2'].strip().lower()}"
        if datos["D2"]:
            mensaje += f", en el área de {datos['D2'].strip().lower()}"
        if datos["J2"]:
            mensaje += f", lo cual implica {datos['J2'].strip().lower()}"
        mensaje += "."

    if datos["C2"]:
        mensaje += f" Esta tarea tiene prioridad {datos['C2'].strip().lower()}."

    if fecha_limite:
        mensaje += f" Debe estar completada antes del {fecha_limite}."

    # Frase motivacional al final
    mensaje += f"\n\n🔥 {random.choice(FRASES_MOTIVACIONALES)} 🔥"

    enviar_a_telegram(mensaje)
    return jsonify({"status": "ok", "message": "Mensaje enviado correctamente."})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
