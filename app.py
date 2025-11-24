# ================================================
# NASA_ULTRA_MASTER – FINAL APP (KEEP-ALIVE + HEARTBEAT)
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

# Route ראשי – חובה להשאיר את השירות חי
@app.route("/")
def home():
    return "NASA_ULTRA_MASTER is running (FINAL VERSION)"

# ================================================
# ROUTES לקבלת תחזיות
# ================================================
@app.route("/forecast", methods=["GET"])
def forecast_route():
    return generate_forecast(), 200

@app.route("/forecast/send", methods=["GET"])
def forecast_send_route():
    return {
        "status": "ok",
        "main": generate_forecast(),
        "backup": generate_forecast(),
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }, 200

# ================================================
# HEARTBEAT – ריצה אוטומטית בשלישי/חמישי/מוצאי־שבת
# ================================================
def heartbeat_loop():
    while True:
        now = datetime.datetime.now()
        if now.weekday() in [1, 3, 5] and now.hour == 20 and now.minute == 0:
            forecast = generate_forecast()
            print("====== HEARTBEAT ======")
            print("Time:", now)
            print("Forecast:", forecast)
            print("=======================")
            time.sleep(60)
        time.sleep(10)

# ================================================
# KEEP ALIVE – פינג פנימי שמחזיק את Render ער
# ================================================
def keep_alive_loop():
    while True:
        try:
            # קריאת פינג לעצמי — Render רואה "תנועה" ולא מכבה
            requests.get("http://localhost:10000/")
        except:
            pass
        time.sleep(15)   # כל 15 שניות תנועה פנימית

# Thread הפעלת HEARTBEAT
threading.Thread(target=heartbeat_loop, daemon=True).start()

# Thread הפעלת KEEP-ALIVE
threading.Thread(target=keep_alive_loop, daemon=True).start()
