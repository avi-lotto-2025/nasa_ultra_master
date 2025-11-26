from flask import Flask, jsonify
from engine import generate_forecast

app = Flask(__name__)

@app.route("/forecast", methods=["GET"])
def forecast():
    """נקודת API שמחזירה תחזית."""
    return jsonify(generate_forecast())

@app.route("/", methods=["GET"])
def home():
    """בדיקת חיים של השרת."""
    return jsonify({"status": "running", "service": "NASA_ULTRA_MASTER_BASE"})
