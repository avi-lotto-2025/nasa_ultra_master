# ================================================
# NASA_ULTRA_MASTER – APP LAYER (FULL CLEAN FILE)
# ================================================

import os
import json
import requests
import threading
import time
import datetime
from flask import Flask
from engine import generate_forecast

# ================================================
# FLASK APP
# ================================================
app = Flask(__name__)

# Route ראשי – חובה כדי ש-Render ישאיר את השרת חי
@app.route("/")
def home():
    return "NASA_ULTRA_MASTER is running"


# ================================================
# HEARTBEAT – AUTO RUN 24/7 בענן (ללא מיילים)
# ================================================
def heartbeat_loop():
    while True:
        now = datetime.datetime.now()

        # ימים שלישי, חמישי, מוצ״ש  (Tue=1, Thu=3, Sat=5)
        if now.weekday() in [1, 3, 5] and now.hour == 20 and now.minute == 0:
            forecast = generate_forecast()

            print("==============================================")
            print("🚀 HEARTBEAT – תחזית אוטומטית")
            print("יום:", now.strftime("%A"))
            print("שעה:", now.strftime("%H:%M"))
            print("תחזית:", forecast)
            print("==============================================")

            time.sleep(60)   # למנוע כפילות של אותה דקה

        time.sleep(30)  # בדיקה כל 30 שניות


# מפעיל את ה-HEARTBEAT ברקע
threading.Thread(target=heartbeat_loop, daemon=True).start()


# ================================================
# ROUTES
# ================================================

# מחזיר תחזית רגילה
@app.route("/forecast", methods=["GET"])
def forecast_route():
    result = generate_forecast()
    return result, 200


# מחזיר תחזית ראשית+גיבוי (ללא מייל כרגע)
@app.route("/forecast/send", methods=["GET"])
def forecast_send():
    main_forecast = generate_forecast()
    backup_forecast = generate_forecast()

    return {
        "status": "ok",
        "main": main_forecast,
        "backup": backup_forecast,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }, 200
