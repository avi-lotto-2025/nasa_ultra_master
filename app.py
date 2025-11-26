from flask import Flask, request, jsonify
from engine import generate_forecast

app = Flask(__name__)


# ---------------------------------------------------------
# Endpoint 1 — בדיקת חיים
# ---------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "NASA_ULTRA_MASTER_VX ONLINE"}), 200


# ---------------------------------------------------------
# Endpoint 2 — יצירת תחזית
# ---------------------------------------------------------
@app.route("/forecast", methods=["POST", "GET"])
def forecast():

    # מצב GET — אין היסטוריה → fallback חכם
    if request.method == "GET":
        result = generate_forecast([])
        return jsonify(result), 200

    # מצב POST — קבלת היסטוריה מהמשתמש
    try:
        data = request.get_json(force=True, silent=True)

        if data is None:
            data = []

        result = generate_forecast(data)
        return jsonify(result), 200

    except Exception:
        # fallback חזק
        return jsonify({"main": [1, 2, 3, 4, 5, 6], "extra": 7}), 200


if __name__ == "__main__":
    # להרצה מקומית
    app.run(host="0.0.0.0", port=5000)
