from flask import Flask, jsonify
import os
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)


# ==========================================================
# ROOT
# ==========================================================
@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "NASA_ULTRA_BASE_ACTIVE"}), 200


# ==========================================================
# STATUS CHECK
# ==========================================================
@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "engine": "OK",
        "mail": "READY" if os.getenv("SENDGRID_API_KEY") else "MISSING_KEY"
    }), 200


# ==========================================================
# FORECAST (BASIC VERSION)
# ==========================================================
@app.route("/forecast", methods=["GET"])
def forecast():
    # שלד יציב — מספרים זמניים. המוח המלא יבוא אחר כך.
    main = sorted(random.sample(range(1, 38), 6))
    extra = random.randint(1, 7)

    return jsonify({
        "forecast": {
            "main": main,
            "extra": extra
        }
    }), 200


# ==========================================================
# SEND TEST EMAIL
# ==========================================================
@app.route("/send_test", methods=["GET"])
def send_test():
    api_key = os.getenv("SENDGRID_API_KEY")

    if not api_key:
        return jsonify({"error": "SENDGRID_API_KEY not found"}), 500

    message = Mail(
        from_email="avi5588@gmail.com",
        to_emails="avi5588@gmail.com",
        subject="NASA ULTRA – MAIL TEST",
        html_content="<h1>המייל עובד</h1><p>בדיקה מהשרת בענן.</p>"
    )

    try:
        sg = SendGridAPIClient(api_key)
        sg.send(message)
        return jsonify({"mail": "sent"}), 200
    except Exception as e:
        return jsonify({"mail_error": str(e)}), 500


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    # Render משתמש ב־gunicorn, אבל זה שימושי להרצה מקומית.
    app.run(host="0.0.0.0", port=10000)
# ==========================================
# NASA ULTRA – APP LAYER
# שכבת API עליונה
# ==========================================

from flask import Flask, jsonify
from engine import run_lotto_engine

app = Flask(__name__)

# בדיקת חיים
@app.route("/")
def home():
    return jsonify({"status": "NASA_ULTRA ONLINE"})

# תחזית מלאה (Main + Backups)
@app.route("/forecast")
def forecast():
    result = run_lotto_engine()
    return jsonify(result)

# סטטוס שרת
@app.route("/status")
def status():
    return jsonify({"engine": "OK", "version": "ULTRA_FULL"})

# להרצה מקומית בלבד
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
