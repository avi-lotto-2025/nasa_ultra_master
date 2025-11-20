from flask import Flask, jsonify
from engine import MAIN_RANGE, BONUS_RANGE, DAYS_ACTIVE, RUN_HOUR
import datetime
import random

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "OK", "message": "NASA_ULTRA_MASTER READY"})

@app.route("/run")
def run_forecast():
    now = datetime.datetime.now()
    weekday = now.isoweekday()
    hour = now.hour

    # בדיקה אם היום והזמן מתאימים
    if weekday in DAYS_ACTIVE and hour == RUN_HOUR:
        main = random.sample(MAIN_RANGE, 6)
        bonus = random.choice(BONUS_RANGE)

        return jsonify({
            "ok": True,
            "main_numbers": sorted(main),
            "bonus": bonus,
            "timestamp": str(now)
        })

    return jsonify({
        "ok": False,
        "message": "Not the correct time to run",
        "weekday": weekday,
        "hour": hour
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
