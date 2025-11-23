# =============================================
# NASA_ULTRA_MASTER – MAIL TEST ONLY
# קובץ ריק לחלוטין למעט שליחת מייל בסיסית
# =============================================

from flask import Flask, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

app = Flask(__name__)

# שלוחת בדיקה
@app.route("/", methods=["GET"])
def root_status():
    return jsonify({"status": "MAIL_TEST_ONLINE"})

# שליחת מייל בלבד
@app.route("/send", methods=["GET"])
def send_mail():
    message = Mail(
        from_email="avi5588@gmail.com",
        to_emails="avi5588@gmail.com",
        subject="NASA MAIL TEST",
        html_content="<h1>המייל עובד!</h1><p>בדיקת שליחת מייל מהשרת.</p>"
    )

    try:
        sg = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
        sg.send(message)
        return jsonify({"mail": "sent"})
    except Exception as e:
        return jsonify({"mail_error": str(e)})

# הרצה
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
