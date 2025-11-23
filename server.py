# ====================================================
# NASA_ULTRA_MASTER – SERVER LAYER (MAIN ENTRY POINT)
# ====================================================

from flask import Flask, jsonify, request
import os
import traceback
import engine as nasa_engine
import app as nasa_brain
import requests

app = Flask(__name__)

# ====================================================
# ROOT: STATUS CHECK
# ====================================================
@app.route("/")
def home():
    return jsonify({"status": "NASA_ULTRA ONLINE"})


# ====================================================
# RUN: הפעלת אלגוריתם החיזוי
# ====================================================
@app.route("/run")
def run_now():
    try:
        result = nasa_engine.generate_forecast_pair()
        return jsonify({"forecast": result})
    except Exception as e:
        return jsonify({
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500


# ====================================================
# SENDGRID TEST
# ====================================================
@app.route("/send_test")
def send_test():
    try:
        api_key = os.environ.get("SENDGRID_API_KEY")
        if not api_key:
            return jsonify({"error": "Missing SENDGRID_API_KEY"}), 500

        email = {
            "personalizations": [
                {
                    "to": [{"email": "avi5588@gmail.com"}],
                    "subject": "NASA ULTRA TEST MAIL"
                }
            ],
            "from": {"email": "avi5588@gmail.com"},
            "content": [{
                "type": "text/plain",
                "value": "היי אבי — זה מבחן שליחת מייל מהשרת החדש!"
            }]
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        r = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            json=email,
            headers=headers
        )

        return jsonify({
            "status": "sent",
            "sendgrid_status": r.status_code,
            "response": r.text
        })

    except Exception as e:
        return jsonify({
            "error": "SendTest failed",
            "trace": traceback.format_exc()
        }), 500


# ====================================================
# LOCAL RUN (NOT USED ON RENDER)
# ====================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
