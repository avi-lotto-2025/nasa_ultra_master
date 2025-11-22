import os
import random
import datetime
from flask import Flask, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# --------------------------------------------------------
# הגדרות מערכת
# --------------------------------------------------------

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
TARGET_EMAIL = "avi5588@gmail.com"

# שלישי (2), חמישי (4), שבת (6)
DAYS_ACTIVE = [2, 4, 6]

# 20:00
RUN_HOUR = 20

MAIN_RANGE = list(range(1, 38))    # 1–37
BONUS_RANGE = list(range(1, 8))    # 1–7

app = Flask(__name__)

# --------------------------------------------------------
# יצירת תחזית
# --------------------------------------------------------

def generate_forecast():
    main_numbers = sorted(random.sample(MAIN_RANGE, 6))
    bonus_number = random.choice(BONUS_RANGE)

    return {
        "main": main_numbers,
        "bonus": bonus_number
    }

# --------------------------------------------------------
# שליחת מייל
# --------------------------------------------------------

def send_email(main, backup):
    subject = "תחזית לוטו — NASA ULTRA MASTER"
    body = f"""
    תחזית ראשית:
    {main['main']}  |  בונוס: {main['bonus']}

    תחזית גיבוי:
    {backup['main']}  |  בונוס: {backup['bonus']}
    """

    message = Mail(
        from_email="noreply@nasa-ultra-master.com",
        to_emails=TARGET_EMAIL,
        subject=subject,
        plain_text_content=body
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print("MAIL ERROR:", e)

# --------------------------------------------------------
# עמוד בית
# --------------------------------------------------------

@app.route("/")
def home():
    return jsonify({"status": "OK", "message": "NASA_ULTRA_MASTER READY"})

# --------------------------------------------------------
# מסלול הרצה אוטומטי רגיל (לא שולח מייל)
# --------------------------------------------------------

@app.route("/run")
def run_auto():
    now = datetime.datetime.now()
    weekday = now.isoweekday()
    hour = now.hour

    if weekday in DAYS_ACTIVE and hour == RUN_HOUR:
        forecast = generate_forecast()
        backup = generate_forecast()

        return jsonify({
            "ok": True,
            "main": forecast,
            "backup": backup,
            "timestamp": str(now)
        })

    return jsonify({
        "ok": False,
        "message": "לא הזמן הנכון להרצה",
        "weekday": weekday,
        "hour": hour
    })

# --------------------------------------------------------
# מסלול ידני לבדיקות — שולח מייל בלבד
# --------------------------------------------------------

@app.route("/run_now", methods=["GET"])
def run_now():
    main = generate_forecast()
    backup = generate_forecast()

    send_email(main, backup)

    return "EMAIL_SENT"

# --------------------------------------------------------
# הפעלה
# --------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
