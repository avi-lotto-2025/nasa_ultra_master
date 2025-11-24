from flask import Flask, jsonify
from engine import run_lotto_engine

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "NASA_ULTRA ONLINE"})

@app.route("/forecast")
def forecast():
    result = run_lotto_engine()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
# ==========================================
# NASA ULTRA – SERVER LAYER
# מחבר בין Flask ל-engine המלא
# ==========================================

from flask import Flask, jsonify
from engine import run_lotto_engine

app = Flask(__name__)

# בדיקת חיים
@app.route("/")
def home():
    return jsonify({"status": "NASA_ULTRA ONLINE"})

# תחזית מלאה
@app.route("/forecast")
def forecast():
    result = run_lotto_engine()
    return jsonify(result)

# להרצה מקומית בלבד
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
