from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import swisseph as swe
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from gpt4all import GPT4All

# =======================
# Creazione app Flask e modello GPT
# =======================
app = Flask(__name__)
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")

# =======================
# Route per file statici
# =======================
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(".", path)

# =======================
# Funzioni astrologiche
# =======================
def get_coordinates(city, retries=3):
    geolocator = Nominatim(user_agent="oroscopo_app", timeout=10)
    for _ in range(retries):
        try:
            location = geolocator.geocode(city)
            if location:
                return location.latitude, location.longitude
        except GeocoderTimedOut:
            continue
    raise ValueError("Luogo non trovato o timeout nella connessione")

def get_zodiac_sign(longitude):
    # se longitude è tuple, prendi il primo elemento
    if isinstance(longitude, (tuple, list)):
        longitude = longitude[0]
    signs = ["Ariete", "Toro", "Gemelli", "Cancro", "Leone", "Vergine",
             "Bilancia", "Scorpione", "Sagittario", "Capricorno", "Acquario", "Pesci"]
    index = int(longitude // 30) % 12
    return signs[index]

def calcola_tema_natale(data, ora, luogo):
    dt = datetime.fromisoformat(f"{data}T{ora}:00")
    lat, lon = get_coordinates(luogo)

    swe.set_topo(lon, lat, 0)
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60.0)

    sole = swe.calc_ut(jd, swe.SUN)[0]
    luna = swe.calc_ut(jd, swe.MOON)[0]
    ascendente = swe.houses(jd, lat, lon)[0][0]

    return {
        "segno_sole": get_zodiac_sign(sole),
        "segno_luna": get_zodiac_sign(luna),
        "ascendente": get_zodiac_sign(ascendente)
    }

# =======================
# Route principale /oroscopo
# =======================
@app.route("/oroscopo", methods=["POST"])
def oroscopo():
    try:
        data_json = request.get_json()
        nome = data_json.get("nome")
        data = data_json.get("data")
        ora = data_json.get("ora")
        luogo = data_json.get("luogo")

        if not all([nome, data, ora, luogo]):
            return jsonify({"error": "Dati incompleti"}), 400

        tema = calcola_tema_natale(data, ora, luogo)

        descrizione_tema = (
            f"Sole in {tema['segno_sole']}, Luna in {tema['segno_luna']}, "
            f"Ascendente in {tema['ascendente']}."
        )

        prompt = (
            f"Scrivi un oroscopo approfondito e positivo per {nome}, "
            f"nato il {data} alle {ora} a {luogo}. "
            f"Segno solare: {tema['segno_sole']}, Luna in {tema['segno_luna']}, "
            f"Ascendente in {tema['ascendente']}. "
            "Aggiungi consigli di crescita personale e amore."
        )

        with model.chat_session() as session:
            output = session.generate(prompt, max_tokens=200)

        return jsonify({
            "nome": nome,
            "segno": tema["segno_sole"],
            "luna": tema["segno_luna"],
            "ascendente": tema["ascendente"],
            "tema": descrizione_tema,
            "oroscopo": output
        })
    except Exception as e:
        return jsonify({"error": f"Errore nel calcolo del tema: {e}"}), 500

# =======================
# Avvio app
# =======================
if __name__ == "__main__":
    app.run(debug=True)
