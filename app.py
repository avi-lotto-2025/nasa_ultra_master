from flask import Flask, jsonify, request
from engine_master import EngineMaster
import pandas as pd
import json

app = Flask(__name__)

# ---------------------------------------------------------
# טעינת היסטוריה (אם קיימת)
# ---------------------------------------------------------

engine = EngineMaster()

# מנסים לטעון את history_full.json אם קיים
try:
    with open("history_full.json", "r", encoding="utf-8") as f:
        raw = json.load(f)
        df = pd.DataFrame(raw)
        engine.load_history(df)
except:
    pass


# ---------------------------------------------------------
# מסלול סטטוס
# ---------------------------------------------------------

@app.route("/status", methods=["GET"])
def status_page():
    return jsonify(engine.status())


# ---------------------------------------------------------
# מסלול תחזית מלאה
# ---------------------------------------------------------

@app.route("/forecast", methods=["GET"])
def get_forecast():
    result = engine.generate_safe_forecast()
    return jsonify(result)


# ---------------------------------------------------------
# index
# ---------------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "system": "NASA_ULTRA_MASTER_VX",
        "status": engine.status(),
        "endpoints": ["/forecast", "/status"]
    })


# ---------------------------------------------------------
# הרצה מקומית (Railway משתמש ב-server.py)
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
