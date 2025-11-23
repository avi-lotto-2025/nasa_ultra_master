# ===============================
# NASA_ULTRA_MASTER - SERVER LAYER
# ===============================

from flask import Flask, jsonify
import os
import traceback
import requests

# אם יש צורך להפעיל פונקציות מהקבצים שלך:
import app as nasa_brain
import engine as nasa_engine

# יצירת השרת
app = Flask(__name__)

# ===============================
# ROOT CHECK
# ===============================
@app.route("/")
def home():
    return jsonify({"status": "NASA_ULTRA ONLINE"})


# ===============================
# SENDGRID TEST MAIL
# ===============================
@app.route("/send_test")
def send_test():

    try:
        api_key = os.environ.get("SENDGRID_API_KEY")

        if not api_key:
            return jsonify({"error": "Missing SENDGRID_API_KEY"}), 500

        send_url = "https://api.sendgrid.com/v3/mail/send"

        email = {
            "personalizations": [
                {
                    "to": [{"email": "avi5588@gmail.com"}],
                    "subject": "NASA ULTRA TEST MAIL"
                }
            ],
            "from": {"email": "avi5588@gmail.com"},
            "content": [
                {
                    "type": "text/plain",
                    "value": "היי אבי! זה מבחן שליחת מייל מהשרת של NASA_ULTRA_MASTER."
                }
            ]
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        r = requests.post(send_url, json=email, headers=headers)

        return jsonify({
            "status": "sent",
            "sendgrid_status": r.status_code,
            "sendgrid_response": r.text
        })

    except Exception as e:
        return jsonify({
            "error": "SendTest failed",
            "trace": traceback.format_exc()
        }), 500


# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
