# ================================================
# NASA_ULTRA_MASTER – APP LAYER (FULL CLEAN FILE)
# ================================================

import os
import json
import requests
from flask import Flask
from engine import generate_forecast
from datetime import datetime

# Flask
app = Flask(__name__)

# ====== ROUTE ראשי להשאיר את המערכת חיה ב-Render ======
@app.route("/")
def home():
    return "NASA_ULTRA_MASTER is running"

# ================================================
# FORMAT HELPERS
# ================================================
def format_forecast_set(title, forecast):
    main = ", ".join(str(n) for n in forecast["main"])
    extra = forecast["extra"]
    return f"{title}:\nמספרים: {main}\nהמספר הנוסף: {extra}\n"

# ================================================
# SENDGRID CONFIG
# ================================================
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = "avi5588@gmail.com"
TO_EMAIL = "avi5588@gmail.com"

# ================================================
# MAIN + BACKUP FORECAST (לא שולחים כרגע מייל)
# ================================================
def send_email_with_two_sets():
    # תחזית ראשית
    main_forecast = generate_forecast()

    # תחזית גיבוי אחת
    backup_forecast = generate_forecast()

    # בניית טקסט
    main_txt = format_forecast_set("🟦 תחזית ראשית", main_forecast)
    backup_txt = format_forecast_set("🟨 תחזית גיבוי", backup_forecast)

    final_text = (
        "NASA_ULTRA_MASTER – התחזיות שלך:\n\n"
        + main_txt + "\n"
        + backup_txt + "\n"
        + f"\nנשלח ב־{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    # לא שולחים מייל כרגע — רק מחזירים תוצאה
    return {
        "status": "ok (no email sent)",
        "body": final_text
    }

# ================================================
# ROUTE לשליחת תחזית (כרגע רק מחזיר טקסט)
# ================================================
@app.route("/forecast/send", methods=["GET"])
def send_forecast_email():
    result = send_email_with_two_sets()
    return result, 200

# ================================================
# ROUTE לקבלת תחזית רגילה
# ================================================
@app.route("/forecast", methods=["GET"])
def forecast_only():
    result = generate_forecast()
    return result, 200
