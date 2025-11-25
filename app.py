from flask import Flask, jsonify
from engine import generate_forecast

app = Flask(__name__)

@app.route("/forecast", methods=["GET"])
def forecast():
    result = generate_forecast()
    return jsonify(result)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "NASA_ULTRA_MASTER API running"})
