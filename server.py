from flask import Flask, jsonify
from engine import run_lotto_engine

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "NASA_ULTRA ONLINE"})

@app.route("/forecast")
def forecast():
    result = run_lotto_engine()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
