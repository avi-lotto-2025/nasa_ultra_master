import os
import random
import datetime
from flask import Flask, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# ------------------------------------------
# הגדרות מרכזיות
# ------------------------------------------

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
TARGET_EMAIL = "avi5588@gmail.com"

# ימי שליחה: שלישי (2), חמישי (4), שבת (6)
DAYS_ACTIVE = [2, 4, 6]

# שעה: 20:00
RUN_HOUR = 20

# טווחי מספרים ללוטו (לפי ההגדרות שלך)
MAIN_RANGE = list(range(1, 38))     # 1–37
BONUS_RANGE = list(range(1, 8))     # 1–7

app = Flask(__name__)


# ------------------------------------------
# יצירת תחזית
# ------------------------------------------

def generate_forecast():
    main = random.sample(MAIN_RANGE, 6)
    bonus = random.choice(BONUS_RANGE)

    return {
        "main": sorted(main),
        "bonus": bonus
    }


# ------------------------------------------
# שליחת מייל
# ------------------------------------------

def send_email(main, backup):
    subject = "תחזית לוטו – NASA ULTRA"
    content = f"""
    תחזית ראשית:
    {main['main']}  |  בונוס: {main['bonus']}

    תחזית גיבוי:
    {backup['main']}  |  בונוס: {backup['bonus']}

    נשלח אוטומטית בשעה 20:00.
    """

    message = Mail(
        from_email="noreply@nasa-ultra.com",
        to_emails=TARGET_EMAIL,
        subject=subject,
        plain_text_content=content
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        print("Email sent.")
    except Exception as e:
        print("Email failed:", str(e))


# ------------------------------------------
# הרצה אוטומטית בענן
# ------------------------------------------

_last_sent_date = None   # כדי לא לשלוח פעמיים


def auto_scheduler():
    global _last_sent_date

    now = datetime.datetime.utcnow() + datetime.timedelta(hours=2)  # GMT+2
    weekday = now.isoweekday()
    hour = now.hour
    today = now.date()

    # אם לא יום הגרלה – יציאה
    if weekday not in DAYS_ACTIVE:
        return

    # שעה לא נכונה – יציאה
    if hour != RUN_HOUR:
        return

    # כבר נשלח היום – יציאה
    if _last_sent_date == today:
        return

    # יצירת תחזית ראשית
    main = generate_forecast()

    # יצירת תחזית גיבוי
    backup = generate_forecast()

    # שליחת מייל
    send_email(main, backup)

    # סימון שנשלח
    _last_sent_date = today


# ------------------------------------------
# ראוטים
# ------------------------------------------

@app.route("/")
def home():
    return jsonify({"status": "OK", "message": "NASA ULTRA – LIVE"})


@app.route("/run")
def run_now():
    main = generate_forecast()
    backup = generate_forecast()
    send_email(main, backup)

    return jsonify({
        "ok": True,
        "main": main,
        "backup": backup
    })


# ------------------------------------------
# לולאת Heartbeat רצה בענן
# ------------------------------------------

@app.before_request
def before_request():
    auto_scheduler()


# ------------------------------------------
# הפעלת השירות
# ------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
# ----------------------------------------------------
# שליחה מיידית לבדיקה
# ----------------------------------------------------
from flask import request

@app.route("/run-now")
def run_now():
    # מייצר תחזית ראשית
    main = generate_forecast()
    # מייצר תחזית גיבוי
    backup = generate_forecast()

    # שולח מייל
    send_email(main, backup)

    return jsonify({
        "ok": True,
        "message": "Forecast sent to email",
        "main": main,
        "backup": backup
    })
