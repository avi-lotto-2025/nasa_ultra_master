import json
import random
import statistics


# -------------------------
#  LOAD FULL HISTORY
# -------------------------
def load_history():
    with open("history_full.json", "r", encoding="utf-8") as f:
        return json.load(f)


# -------------------------
#  FREQUENCY MAP
# -------------------------
def build_frequency_map(history):
    freq = {}
    for draw in history:
        for num in draw["main"]:
            freq[num] = freq.get(num, 0) + 1
    return freq


# -------------------------
#  HOT/COLD CLASSIFICATION
# -------------------------
def classify_hot_cold(freq):
    values = list(freq.values())
    mean_v = statistics.mean(values)

    hot = [n for n, c in freq.items() if c > mean_v]
    cold = [n for n, c in freq.items() if c < mean_v]

    return hot, cold


# -------------------------
#  RANGE ENFORCEMENT
# -------------------------
def pick_by_ranges(final_pool):
    # חובה מספרים מכל הטווחים
    r1 = [n for n in final_pool if 1 <= n <= 12]
    r2 = [n for n in final_pool if 13 <= n <= 25]
    r3 = [n for n in final_pool if 26 <= n <= 37]

    chosen = []

    if r1:
        chosen.append(random.choice(r1))
    if r2:
        chosen.append(random.choice(r2))
    if r3:
        chosen.append(random.choice(r3))

    return chosen


# -------------------------
#  BOOSTER
# -------------------------
def apply_booster(freq):
    booster = {}
    max_f = max(freq.values())

    for n, c in freq.items():
        score = c / max_f
        booster[n] = score ** 2  # בוסטר אמיתי – מדגיש את החזקים
    return booster


# -------------------------
#  PROBABILITY PICK
# -------------------------
def weighted_pick(pool, weights, k):
    chosen = []
    items = list(pool)

    for _ in range(k):
        current_w = [weights[n] for n in items]
        pick = random.choices(items, weights=current_w, k=1)[0]
        chosen.append(pick)
        items.remove(pick)

    return sorted(chosen)


# -------------------------
#  BONUS SMART PICK
# -------------------------
def pick_bonus(history):
    bonus_freq = {}

    for draw in history:
        b = draw["extra"]
        bonus_freq[b] = bonus_freq.get(b, 0) + 1

    max_b = max(bonus_freq.values())
    weights = {b: bonus_freq[b] / max_b for b in bonus_freq}

    return random.choices(list(weights.keys()), weights=list(weights.values()), k=1)[0]


# -------------------------
#  MAIN FORECAST FUNCTION
# -------------------------
def generate_forecast():
    history = load_history()

    freq = build_frequency_map(history)
    hot, cold = classify_hot_cold(freq)
    booster = apply_booster(freq)

    # מאחדים בריכה: חמים + קרירים + רגילים
    pool = list(freq.keys())

    # טווחים – בחירה ראשונית
    seeded = pick_by_ranges(pool)

    # בחירה משוקללת
    remaining_to_pick = 6 - len(seeded)
    weighted_part = weighted_pick(pool, booster, remaining_to_pick)

    # מאחדים ומנקים כפולים
    final_main = sorted(list(set(seeded + weighted_part)))
    while len(final_main) < 6:
        extra_pick = random.choice(pool)
        if extra_pick not in final_main:
            final_main.append(extra_pick)

    final_main = sorted(final_main)

    # בחירת בונוס חכמה
    bonus = pick_bonus(history)

    return {
        "main": final_main,
        "extra": bonus
    }


# -------------------------
#  ENTRYPOINT FOR RAILWAY
# -------------------------
def run():
    return generate_forecast()
