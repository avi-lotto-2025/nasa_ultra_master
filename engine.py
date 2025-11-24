# ===============================================
# NASA ULTRA ENGINE – FULL ENGINE
# כל הלוגיקה של תחזיות הלוטו
# ===============================================

import random
import statistics
import numpy as np

# טווחי מספרים
MAIN_RANGE = range(1, 38)     # 1–37
EXTRA_RANGE = range(1, 8)     # 1–7

# גודל היסטוריה
HISTORY_SIZE = 200

# כמות ריצות במונטה-קרלו
MC_RUNS = 5000


# ------------------------------------------------
# יצירת היסטוריה רנדומלית לצורך הדמיה
# בהמשך יוחלף בהיסטוריה אמיתית של לוטו ישראל
# ------------------------------------------------
def generate_mock_history(n=HISTORY_SIZE):
    history = []
    extra_history = []

    for _ in range(n):
        main_nums = sorted(random.sample(MAIN_RANGE, 6))
        extra_num = random.choice(list(EXTRA_RANGE))

        history.append(main_nums)
        extra_history.append(extra_num)

    return history, extra_history


# ------------------------------------------------
# לוגיקת מונטה-קרלו מלאה
# ------------------------------------------------
def monte_carlo_predict(history):
    weights = {}

    for run in range(MC_RUNS):
        ticket = random.sample(MAIN_RANGE, 6)

        score = 0
        for past_ticket in history:
            overlap = len(set(ticket) & set(past_ticket))
            score += overlap ** 2

        ticket_key = tuple(sorted(ticket))
        weights[ticket_key] = weights.get(ticket_key, 0) + score

    best_ticket = max(weights, key=weights.get)
    return list(best_ticket)


# ------------------------------------------------
# תחזית מספר נוסף
# ------------------------------------------------
def predict_extra_number(extra_history):
    counts = {}

    for x in extra_history:
        counts[x] = counts.get(x, 0) + 1

    return max(counts, key=counts.get)


# ------------------------------------------------
# פונקציה ראשית שנקראת ע"י ה־API
# ------------------------------------------------
def generate_forecast():
    history, extra_hist = generate_mock_history()

    main_forecast = monte_carlo_predict(history)
    extra_forecast = predict_extra_number(extra_hist)

    return {
        "main": main_forecast,
        "extra": extra_forecast
    }
