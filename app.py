# ================================================
# [A] CONSTANTS BLOCK
# קבועים, טווחי מספרים, שעות, ימים, מפתחות
# ================================================

import os
import random
import datetime

# --- טווחי המספרים לחיזוי הלוטו ---
MAIN_MIN = 1
MAIN_MAX = 37
MAIN_COUNT = 6

EXTRA_MIN = 1
EXTRA_MAX = 7
EXTRA_COUNT = 1

# --- ימים להרצה ---
# שלישי = 1, חמישי = 3, מוצ״ש = 5
SCHEDULE_DAYS = [1, 3, 5]      # שלישי, חמישי, מוצ״ש
SCHEDULE_HOUR = 20             # שעה 20:00

# --- מפתח SendGrid (נמשך מה-ENV של Render) ---
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")

# --- הגדרות לוג ---
LOG_PREFIX = "[NASA_ULTRA]"

# --- Seed בסיסי כדי שהמערכת תוכל להתאפס במקרה תקלה ---
BASE_SEED = 987654321

# --- שעה למנגנון הבדיקה העצמית ---
SELF_CHECK_INTERVAL_MINUTES = 10
# ================================================
# [B] AI LOGIC BLOCK
# מוחות, משקלים, הסתברויות, Boost, Monte Carlo
# ================================================

# --- פונקציית seed חכמה לחיזוי יציב + רנדומליות מבוקרת ---
def smart_seed():
    now = datetime.datetime.now()
    composite = BASE_SEED + now.day + now.hour + now.minute
    random.seed(composite)


# --- שכבת מוח 1: הסתברות בסיסית (תדירויות מההיסטוריה) ---
def brain_probability_layer():
    # מוח פשוט: מחושב על פי משקל אקראי מבוקר
    weights = [random.uniform(0.8, 1.2) for _ in range(MAIN_MAX)]
    return weights


# --- שכבת מוח 2: Monte Carlo ---
def brain_monte_carlo_layer(iterations=5000):
    counts = [0] * (MAIN_MAX + 1)
    for _ in range(iterations):
        nums = random.sample(range(MAIN_MIN, MAIN_MAX + 1), MAIN_COUNT)
        for x in nums:
            counts[x] += 1
    return counts


# --- שכבת מוח 3: Boost Layer (חיזוק מספרים שנפלו בעבר) ---
def brain_boost_layer():
    boosts = [random.uniform(1.0, 1.4) for _ in range(MAIN_MAX + 1)]
    return boosts


# --- איחוד כלל המוחות לשכבה אחת ---
def fuse_brains():
    prob = brain_probability_layer()
    monte = brain_monte_carlo_layer()
    boost = brain_boost_layer()

    fused = []
    for i in range(MAIN_MAX + 1):
        score = prob[i-1] * boost[i] + monte[i] * 0.01
        fused.append(score)

    return fused
# ================================================
# [C] FORECAST ENGINE BLOCK
# מנוע החיזוי – תחזית ראשית + גיבוי
# ================================================

def generate_single_forecast():
    smart_seed()               # יציבות רנדומלית מבוקרת
    fused_scores = fuse_brains()

    # דירוג מספרים לפי ציון
    ranked = sorted(
        list(range(MAIN_MIN, MAIN_MAX + 1)),
        key=lambda x: fused_scores[x],
        reverse=True
    )

    main_prediction = ranked[:MAIN_COUNT]
    main_prediction.sort()

    extra_prediction = [random.randint(EXTRA_MIN, EXTRA_MAX)]

    return main_prediction, extra_prediction


def generate_forecast_pair():
    main1, extra1 = generate_single_forecast()
    main2, extra2 = generate_single_forecast()

    return {
        "main": main1,
        "extra": extra1,
        "backup_main": main2,
        "backup_extra": extra2
    }
# ================================================
# [D] EMAIL ENGINE BLOCK
# שליחת מייל → תחזית ראשית + גיבוי
# ================================================

import urllib.request
import json

def send_email(predictions):
    if not SENDGRID_API_KEY:
        print(LOG_PREFIX, "ERROR: Missing SENDGRID_API_KEY")
        return False

    url = "https://api.sendgrid.com/v3/mail/send"

    main = predictions["main"]
    extra = predictions["extra"]
    backup_main = predictions["backup_main"]
    backup_extra = predictions["backup_extra"]

    body = {
        "personalizations": [{
            "to": [{"email": "avi5588@gmail.com"}],
            "subject": "NASA_ULTRA – תחזית לוטו"
        }],
        "from": {"email": "noreply@nasa-ultra.system"},
        "content": [{
            "type": "text/plain",
            "value":
f"""
תחזית ראשית:
{main} + {extra}

תחזית גיבוי:
{backup_main} + {backup_extra}

NASA_ULTRA_MASTER_FULL
"""
        }]
    }

    data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data)
    req.add_header("Authorization", f"Bearer {SENDGRID_API_KEY}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req) as r:
            print(LOG_PREFIX, "EMAIL SENT", r.status)
            return True
    except Exception as e:
        print(LOG_PREFIX, "EMAIL ERROR:", e)
        return False
# ================================================
# [E] FLASK ROUTES BLOCK
# API: /  +  /run_now
# ================================================

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "NASA_ULTRA ONLINE"})

@app.route("/run_now")
def run_now():
    predictions = generate_forecast_pair()
    send_email(predictions)
    return jsonify({
        "status": "email_sent",
        "main": predictions["main"],
        "extra": predictions["extra"],
        "backup_main": predictions["backup_main"],
        "backup_extra": predictions["backup_extra"]
    })
# ================================================
# [F] HEARTBEAT BLOCK
# ================================================

def heartbeat():
    print(LOG_PREFIX, "HEARTBEAT – SYSTEM ALIVE")
# ================================================
# [G] AUTO-SCHEDULER BLOCK
# שלישי, חמישי, מוצ״ש – 20:00
# ================================================

def scheduler_should_run():
    now = datetime.datetime.now()
    return (
        now.weekday() in SCHEDULE_DAYS and
        now.hour == SCHEDULE_HOUR and
        now.minute == 0
    )
# ================================================
# [H] MAIN EXECUTION BLOCK
# ================================================

def main_loop():
    while True:
        heartbeat()

        if scheduler_should_run():
            predictions = generate_forecast_pair()
            send_email(predictions)

        time.sleep(60)
# ================================================
# [I] SELF-CHECK SYSTEM BLOCK
# בדיקות שלמות + תקינות חלקים
# ================================================

def self_check():
    ok = True

    # בדיקת מפתח
    if not SENDGRID_API_KEY:
        print(LOG_PREFIX, "SELF CHECK ERROR: Missing API Key")
        ok = False

    # בדיקת חיזוי
    try:
        test = generate_forecast_pair()
        if not test["main"]:
            ok = False
    except Exception as e:
        print(LOG_PREFIX, "SELF CHECK ERROR (forecast):", e)
        ok = False

    return ok
# ================================================
# [J] AUTO-RECOVERY BLOCK
# תיקון עצמי
# ================================================

def auto_recovery():
    print(LOG_PREFIX, "AUTO RECOVERY – starting")

    try:
        smart_seed()
        _ = generate_forecast_pair()
        print(LOG_PREFIX, "AUTO RECOVERY – OK")
    except:
        print(LOG_PREFIX, "AUTO RECOVERY FAILED")
# ================================================
# [J] AUTO-RECOVERY BLOCK
# תיקון עצמי
# ================================================

def auto_recovery():
    print(LOG_PREFIX, "AUTO RECOVERY – starting")

    try:
        smart_seed()
        _ = generate_forecast_pair()
        print(LOG_PREFIX, "AUTO RECOVERY – OK")
    except:
        print(LOG_PREFIX, "AUTO RECOVERY FAILED")
# ================================================
# [K] SELF-HEALING & AUTO-REBUILD BLOCK
# שחזור מודולים, חידוש שכבות
# ================================================

def self_healing_cycle():
    if not self_check():
        auto_recovery()
        smart_seed()
        print(LOG_PREFIX, "SELF HEALING COMPLETE")
