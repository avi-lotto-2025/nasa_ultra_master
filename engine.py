import random
import statistics
from datetime import datetime

# -----------------------------
# 1. היסטוריה ראשונית (נכניס REAL DATA בשלב הבא)
# -----------------------------
HIST = [
    [1, 3, 8, 23, 26, 34, 5],
    [1, 3, 11, 25, 30, 33, 7],
    [4, 8, 18, 23, 35, 36, 3],
    [15, 24, 26, 28, 30, 36, 2],
    [2, 6, 11, 15, 23, 33, 5],
]

# -----------------------------
# 2. שכבת BOOSTER לחיזוק מספרים חמים
# -----------------------------
def booster_layer(history):
    freq = {}
    for draw in history:
        main = draw[:6]
        for num in main:
            freq[num] = freq.get(num, 0) + 1

    # לוקחים את 12 המספרים החזקים ביותר
    hot = sorted(freq, key=freq.get, reverse=True)[:12]
    return hot

# -----------------------------
# 3. שכבת Monte-Carlo
# -----------------------------
def monte_carlo(hot_nums, n=5000):
    weights = {n: 3 if n in hot_nums else 1 for n in range(1, 38)}
    population = list(weights.keys())
    weight_list = list(weights.values())

    sims = []
    for _ in range(n):
        pick = random.choices(population, weights=weight_list, k=6)
        sims.append(sorted(pick))

    # בוחרים את ה־6 מספרים שמופיעים הכי הרבה בסימולציות
    freq = {}
    for seq in sims:
        for num in seq:
            freq[num] = freq.get(num, 0) + 1

    best = sorted(freq, key=freq.get, reverse=True)[:6]
    return sorted(best)

# -----------------------------
# 4. שכבת FINAL ASSEMBLY
# -----------------------------
def generate_forecast():
    hot = booster_layer(HIST)
    main = monte_carlo(hot)

    # מספר נוסף (1–7)
    extra = random.randint(1, 7)

    return {
        "main": main,
        "extra": extra,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
