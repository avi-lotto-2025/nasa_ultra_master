# =========================================================
# NASA ULTRA – APP LAYER
# =========================================================

from flask import Flask, jsonify
from engine import generate_forecast, MAIN_RANGE, EXTRA_RANGE, HISTORY_SIZE

app = Flask(__name__)

# Dummy history until we connect real lotto data
main_history = []
extra_history = []

@app.route("/")
def home():
    return jsonify({"status": "NASA_ULTRA ONLINE"})

@app.route("/status")
def status():
    return jsonify({
        "engine": "OK",
        "version": "ULTRA_FULL"
    })

@app.route("/forecast")
def forecast():
    result = generate_forecast(main_history, extra_history)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
