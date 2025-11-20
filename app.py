from flask import Flask, jsonify
from engine import MAIN_RANGE, BONUS_RANGE, DAYS_ACTIVE, RUN_HOUR
import random
import datetime

app = Flask(__name__)

# פונקציה ליצירת תחזית חד-פעמית
def generate_forecast():
    main_numbers = random.sample(list(MAIN_RANGE), 6)
    bonus_number = random.choice(list(BONUS_RANGE))
    main_numbers.sort()
    return {
        "main": main_numbers,
        "bonus": bonus_number
    }

@app.route("/")
def home():
    return jsonify({"status": "NASA_ULTRA_MASTER running"})

@app.route("/run_once")
def run_once():
    forecast = generate_forecast()
    return jsonify({
        "forecast": forecast,
        "timestamp": str(datetime.datetime.now())
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
