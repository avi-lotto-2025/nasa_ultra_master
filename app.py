import os
import json
import requests
from engine import generate_forecast
from datetime import datetime

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = "avi5588@gmail.com"
TO_EMAIL = "avi5588@gmail.com"

def format_forecast_set(title, forecast):
    main = ", ".join(str(n) for n in forecast["main"])
    extra = forecast["extra"]
    return f"{title}:\nמספרים: {main}\nהמספר הנוסף: {extra}\n"

def send_email_with_two_sets():
    # יוצרים תחזית ראשית
    main_forecast = generate_forecast()

    # יוצרים תחזית גיבוי אחת בלבד
    backup_forecast = generate_forecast()

    # בונים טקסט מייל
    main_txt = format_forecast_set("🟦 תחזית ראשית", main_forecast)
    backup_txt = format_forecast_set("🟨 תחזית גיבוי", backup_forecast)

    final_text = (
        "NASA_ULTRA_MASTER – התחזיות שלך:\n\n"
        + main_txt + "\n"
        + backup_txt + "\n"
        + f"\nנשלח ב־{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    # בניית Payload ל־SendGrid
    message = {
        "personalizations": [
            {"to": [{"email": TO_EMAIL}]}
        ],
        "from": {"email": FROM_EMAIL},
        "subject": "תחזית לוטו – NASA_ULTRA_MASTER",
        "content": [{"type": "text/plain", "value": final_text}]
    }

    # שליחה
    response = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": f"Bearer {SENDGRID_API_KEY}",
            "Content-Type": "application/json"
        },
        data=json.dumps(message)
    )

    return {
        "status": response.status_code,
        "body": final_text,
        "sendgrid_response": response.text
    }
