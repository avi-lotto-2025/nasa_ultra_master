from flask import Flask, jsonify
import datetime
import threading
import time
import os

app = Flask(__name__)

# ------------------------------
#  נקודת בדיקה בסיסית לענן
# ------------------------------
@app.route("/")
def home():
    return jsonify({
        "status": "OK",
        "message": "NASA_ULTRA_MASTER — המערכת בענן פועלת תקין",
        "time": str(datetime.datetime.now())
    })

# ------------------------------
#  הפעלה של engine.py
# ------------------------------
def run_engine():
    import engine
    print("Engine loaded and running...")

# ------------------------------
#  Thread Autostart
# ------------------------------
engine_thread = threading.Thread(target=run_engine)
engine_thread.daemon = True
engine_thread.start()

# ------------------------------
#  הפעלת שרת Flask
# ------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
