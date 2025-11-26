from app import app

"""
server.py — שכבת ההפעלה העליונה של NASA_ULTRA_MASTER_VX
הקובץ הזה נטען על ידי gunicorn בענן.
כל תפקידו להחזיק מופע יציב של האפליקציה.
אין בו לוגיקה נוספת ואין בו תלות חיצונית.
"""

# האובייקט ש-gunicorn מחפש — חובה
application = app


# Fallback במקרה שמשהו נדפק בטעינה
def get_app():
    try:
        return application
    except Exception:
        # fallback אפס מאמץ — Flask ריק שלא קורס
        from flask import Flask
        fallback_app = Flask(__name__)

        @fallback_app.route("/")
        def fallback_home():
            return {"status": "FALLBACK_RUNNING"}, 200

        return fallback_app


# זה מה ש-gunicorn יטען בפועל
app = get_app()
