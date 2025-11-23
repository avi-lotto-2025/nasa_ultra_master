from flask import Flask, jsonify

app = Flask(__name__)

# ---------------------------------------------------------
# STATUS CHECK
# ---------------------------------------------------------
@app.route("/")
def home():
    return jsonify({"status": "NASA_ULTRA ONLINE"}), 200

@app.route("/status")
def status():
    return jsonify({"engine": "OK", "brain": "OK"}), 200


# ---------------------------------------------------------
# FORECAST PLACEHOLDER (שלד ריק)
# ---------------------------------------------------------
@app.route("/forecast")
def forecast():
    # מחזיר מספרים זמניים — רק כדי שהשלד יעבוד
    return jsonify({
        "forecast": {
            "main": [1, 2, 3, 4, 5, 6],
            "extra": 1
        }
    }), 200


# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
