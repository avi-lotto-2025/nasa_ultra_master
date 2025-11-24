# ==========================================================
# NASA ULTRA ENGINE – PART 1
# Imports + Constants
# ==========================================================

import random
import statistics
import numpy as np


# ==========================================================
# CONSTANTS
# ==========================================================

MAIN_RANGE = range(1, 38)   # מספרים ראשיים 1–37
EXTRA_RANGE = range(1, 8)   # מספר נוסף 1–7
HISTORY_SIZE = 200          # נזין אח"כ היסטוריה אמיתית
MC_RUNS = 5000              # מספר סימולציות למונטה-קרלו
MC_RUNS = 5000
# ===============================================
# NASA ULTRA ENGINE – PART 2
# Probability Weight Layer (Weighted Brain)
# ===============================================

def load_history():
    """
    טוען היסטוריית הגרלות ללוטו.
    בשלב זה: fallback בטיחותי בלבד.
    בהמשך נטעין נתונים אמיתיים מ-history.json.
    """
    try:
        # בעתיד נטען נתוני עבר אמיתיים
        return [
            [1, 7, 12, 23, 26, 34],
            [3, 8, 14, 22, 27, 30],
            [4, 11, 19, 25, 29, 35],
            [2, 6, 13, 21, 24, 33],
        ]
    except:
        return []


def compute_weight_layer(history):
    """
    מקבלת היסטוריה ומחזירה וקטור משקלים לכל מספר
    מ-1 עד 37 (MAIN_RANGE).
    """
    weight_map = {n: 0 for n in MAIN_RANGE}

    # ספירת הופעות
    for draw in history:
        for num in draw:
            if num in weight_map:
                weight_map[num] += 1

    # Normalization
    max_val = max(weight_map.values()) if max(weight_map.values()) > 0 else 1
    for k in weight_map:
        weight_map[k] = weight_map[k] / max_val

    return weight_map
# ===============================================
# NASA ULTRA ENGINE – PART 3
# Monte Carlo Simulation Layer
# ===============================================

def monte_carlo_simulation(weights, simulations=MC_RUNS):
    results = []

    all_numbers = list(MAIN_RANGE)
    weight_list = [weights[n] for n in all_numbers]

    for _ in range(simulations):
        chosen = random.choices(
            population=all_numbers,
            weights=weight_list,
            k=6
        )
        chosen = sorted(list(set(chosen)))
        while len(chosen) < 6:
            extra_choice = random.choices(
                population=all_numbers,
                weights=weight_list,
                k=1
            )[0]
            if extra_choice not in chosen:
                chosen.append(extra_choice)
        chosen = sorted(chosen)
        results.append(tuple(chosen))

    freq = {}
    for r in results:
        freq[r] = freq.get(r, 0) + 1

    best = max(freq, key=freq.get)
    return list(best)
# ===============================================
# NASA ULTRA ENGINE – PART 4
# Hybrid Probability Fusion Layer
# שילוב משקלים + מונטה קרלו + שכיחות בסיסית
# ===============================================

def fuse_probability_layers(weight_layer, monte_result):
    """
    משלב בין:
    1. משקלי שכיחות (weight_layer)
    2. תוצאות מונטה קרלו (monte_result)
    כדי ליצור שכבת הסתברות היברידית חזקה יותר.
    """

    fused = {}

    # משקל בסיסי
    for n in MAIN_RANGE:
        fused[n] = weight_layer.get(n, 0) * 0.6

    # חיזוק לפי בחירות מונטה קרלו
    for n in monte_result:
        if n in fused:
            fused[n] += 0.4

    # Normalize
    max_v = max(fused.values()) if max(fused.values()) > 0 else 1
    for k in fused:
        fused[k] = fused[k] / max_v

    return fused
# ===============================================
# NASA ULTRA ENGINE – PART 5
# Final Selection Layer
# בחירת הסט הראשי (FINAL)
# ===============================================

def select_final_set(fused_layer):
    """
    מקבל שכבה היברידית (fused) ומחזיר סט ראשי חכם.
    הבחירה מבוססת על:
    - ניקוד משולב
    - בחירה אוטומטית של המספרים הגבוהים ביותר
    """

    # הפיכת המפה לרשימה מסודרת לפי ערך גבוה → נמוך
    sorted_nums = sorted(
        fused_layer.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # בחירת 6 המספרים החזקים ביותר
    final_main = [num for num, score in sorted_nums[:6]]
    final_main = sorted(final_main)

    # בחירת מספר נוסף (extra) לפי משקלים / בחירה אקראית חכמה
    extra_candidates = list(EXTRA_RANGE)
    extra = random.choice(extra_candidates)

    return {
        "main": final_main,
        "extra": extra
    }
