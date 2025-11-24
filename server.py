# ================================================
# NASA ULTRA – SERVER LAYER (FULL CLEAN VERSION)
# ================================================

from app import app
import threading
import time
import datetime
from engine import generate_forecast


# ================================================
# HEARTBEAT LOOP – AUTO RUN 24/7
# ================================================

def heartbeat_loop():
    while True:
        now = datetime.datetime.now()

        # ימים: שלישי, חמישי, מוצ"ש (weekday: 1=Tue, 3=Thu, 5=Sat)
        if now.weekday() in [1, 3, 5] and now.hour == 20 and now.minute == 0:
            forecast = generate_forecast()

            print("==============================================")
            print("🚀 HEARTBEAT – תחזית אוטומטית")
            print("יום:", now.strftime("%A"))
            print("שעה:", now.strftime("%H:%M"))
            print("תחזית:", forecast)
            print("==============================================")

            time.sleep(60)   # מניעת כפילות

        time.sleep(30)  # בדיקה כל 30 שניות


# ================================================
# RUN HEARTBEAT AS BACKGROUND THREAD
# ================================================

threading.Thread(target=heartbeat_loop, daemon=True).start()


# ================================================
# RUN FLASK APP (Render/Gunicorn)
# ================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
