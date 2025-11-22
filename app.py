import os
import random
import datetime
from flask import Flask, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# -----------------------------------------------------
# הגדרות מערכת
# -----------------------------------------------------

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
TARGET_EMAIL = "avi5588@gmail.com"

# ימים פעילים: שלישי (2), חמישי (4), שבת (6)
DAYS_ACTIVE = [2, 4, 6]

# שעה להרצה: 20:00
RUN_HOUR = 20

# טווחי מספרים ללוטו
MAIN_RANGE = list(range(1, 38))   # 1–37
BONUS_RANGE = list(range(1, 8))    # 1–7

app = Flask(__name__)

# -----------------------------------------------------
# פונקציה – יצירת תחזית (1+1 בלבד)
# -----------------------------------------------------
def generate_forecast():
    main_numbers = sorted(random.sample(MAIN_RANGE, 6))
    bonus_number = random.choice(BONUS_RANGE)

    backup_main = sorted(random.sample(MAIN_RANGE, 6))
    backup_bonus = random.choice(BONUS_RANGE)

    main_prediction = f"{main_numbers} + {bonus_number}"
    backup_prediction = f"{backup_main} + {backup_bonus}"

    return main_prediction, backup_prediction

# -----------------------------------------------------
# פונקציה – שליחת מייל (חדש, נקי, 1+1)
# -----------------------------------------------------
def send_email(main_prediction, backup_prediction):
    try:
        sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)

        subject = "תחזית לוטו - NASA_ULTRA (ראשית + גיבוי)"
        body = (
            f"🟦 תחזית ראשית:\n{main_prediction}\n\n"
            f"🟩 תחזית גיבוי:\n{backup_prediction}\n\n"
            "— נשלח אוטומטית ע״י NASA_ULTRA_V19_FINAL_SELF_AWARENESS —"
        )

        message = Mail(
            from_email=TARGET_EMAIL,
            to_emails=TARGET_EMAIL,
            subject=subject,
            plain_text_content=body,
        )

        response = sg.send(message)
        print(f"[EMAIL] נשלח בהצלחה. סטטוס: {response.status_code}")

    except Exception as e:
        print("[EMAIL ERROR] שגיאה בשליחה:", str(e))

# -----------------------------------------------------
# פונקציה – דף בית
# -----------------------------------------------------
@app.route("/")
def home():
    return jsonify({"status": "NASA_ULTRA ONLINE"})

# -----------------------------------------------------
# פונקציה – הרצה אוטומטית (Heartbeat)
# -----------------------------------------------------
def run_auto():
    now = datetime.datetime.now()
    if now.weekday() in DAYS_ACTIVE and now.hour == RUN_HOUR:
        main_prediction, backup_prediction = generate_forecast()
        send_email(main_prediction, backup_prediction)

# -----------------------------------------------------
# התחלת שרת Flask (Render מריץ דרך gunicorn app:app)
# -----------------------------------------------------
if __name__ == "__main__":
    # הפעלה מקומית
    print("Running NASA_ULTRA locally...")
    main_prediction, backup_prediction = generate_forecast()
    send_email(main_prediction, backup_prediction)
    app.run(host="0.0.0.0", port=5000)
