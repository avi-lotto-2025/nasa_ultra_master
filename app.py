# ==========================================================
# NASA ULTRA – APP LAYER
# API ראשי
# ==========================================================

from flask import Flask, jsonify
from engine import generate_forecast

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "NASA_ULTRA ONLINE"})

@app.route("/status")
def status():
    return jsonify({"engine": "OK", "version": "ULTRA_FULL"})

@app.route("/forecast")
def forecast():
    result = generate_forecast()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
