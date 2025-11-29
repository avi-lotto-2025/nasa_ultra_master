import sendgrid
from sendgrid.helpers.mail import Mail
import json
import time
import os


class EmailEngine:
    def __init__(self):
        # המפתח צריך להיות קיים במשתני הסביבה ב־Railway
        self.api_key = os.getenv("SENDGRID_API_KEY")

        # המייל שממנו נשלח
        self.sender = "noreply@nasalotto.ai"

        # המייל של אבי (נקבע מראש)
        self.receiver = "avi5588@gmail.com"

    def build_email_body(self, package):
        """
        בונה את גוף המייל – טקסט נקי, מסודר וברור.
        """
        main = package["main_forecast"]
        backups = package["backup_forecasts"]

        text = []
        text.append("🚀 תחזית לוטו — NASA_ULTRA_MASTER_VX")
        text.append("")
        text.append(f"🕒 Timestamp: {package['timestamp']}")
        text.append("")
        text.append("🎯 תחזית ראשית:")
        text.append(f"מספרים: {main['main']}")
        text.append(f"מספר חזק: {main['extra']}")
        text.append("")
        text.append("🛡 5 סטי גיבוי:")

        for i, b in enumerate(backups, start=1):
            text.append(f"גיבוי {i}: {b['main']} | חזק: {b['extra']}")

        text.append("")
        return "\n".join(text)

    def send_email(self, package):
        """
        שולח מייל אחד בלבד עם החבילה המלאה.
        """

        if not self.api_key:
            return {
                "status": "failed",
                "error": "Missing SENDGRID_API_KEY",
                "time": int(time.time())
            }

        sg = sendgrid.SendGridAPIClient(api_key=self.api_key)

        body = self.build_email_body(package)

        message = Mail(
            from_email=self.sender,
            to_emails=self.receiver,
            subject="🎯 תחזית לוטו — NASA_ULTRA_MASTER_VX",
            plain_text_content=body
        )

        try:
            response = sg.send(message)
            return {
                "status": "sent",
                "code": response.status_code,
                "time": int(time.time())
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "time": int(time.time())
            }
