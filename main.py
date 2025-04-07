import os
import random
import datetime
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

MENSAJES_MOTIVACIONALES = [
    "Cada esfuerzo suma. No pares.",
    "La disciplina es la clave. Seguí avanzando.",
    "Estás cada vez más cerca. No te detengas.",
    "Hoy es un gran día para dar un paso más.",
    "No hace falta que sea perfecto. Hace falta que sea real."
]

def enviar_a_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

@app.route('/actualizar_tareas', methods=['POST'])
def actualizar_tareas():
    datos = request.json

    def fecha_actual_larga():
        hoy = datetime.datetime.now()
        return hoy.strftime("%-d de %B de %Y").capitalize()

    def prioridad_texto(p):
        p = p.lower()
        if "alta" in p:
            return "alta"
        elif "media" in p:
            return "media"
        elif "baja" in p:
            return "baja"
        else:
            return ""

    tarea = datos["E2"].strip().lower() if datos.get("E2") else ""
    categoria = datos["D2"].strip().lower() if datos.get("D2") else ""
    prioridad = prioridad_texto(datos["C2"]) if datos.get("C2") else ""
    detalles = datos["J2"].strip() if datos.get("J2") else ""

    mensaje = f"📌 Recordá que hoy, {fecha_actual_larga()}, tenés que {tarea}"
    if categoria:
        mensaje += f" correspondiente a {categoria}"
    mensaje += "."

    if prioridad:
        mensaje += f" Esta tarea tiene prioridad {prioridad}"
        if prioridad == "alta":
            mensaje += " 🔴"
        elif prioridad == "media":
            mensaje += " 🟡"
        elif prioridad == "baja":
            mensaje += " 🟢"
        mensaje += "."

    if detalles:
        mensaje += f" Implica {detalles}."

    mensaje += f"\n🔥 {random.choice(MENSAJES_MOTIVACIONALES)} 🔥"

    enviar_a_telegram(mensaje)
    return jsonify({"status": "ok", "message": "Recordatorio enviado correctamente."})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
