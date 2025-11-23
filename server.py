# ==========================================
# NASA_ULTRA_MASTER – SERVER LAYER (Skeleton)
# ==========================================

from flask import Flask, jsonify
import engine

app = Flask(__name__)

# -------------------------
# STATUS CHECK ENDPOINT
# -------------------------
@app.route("/")
def status():
    return jsonify({"status": "NASA_ULTRA ONLINE"})

# -------------------------
# FORECAST ENDPOINT (SKELETON)
# -------------------------
@app.route("/forecast")
def forecast():
    result = engine.generate_brain_forecast()
    return jsonify(result)

# -------------------------
# RUN (LOCAL ONLY)
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
