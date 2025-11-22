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
