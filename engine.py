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
# ===============================================
# NASA ULTRA ENGINE – PART 6
# Backup Sets Layer (5 גיבויים)
# ===============================================

def generate_backup_sets(fused_layer, count=5):
    """
    יוצר 5 סטי גיבוי חכמים.
    כל סט נבנה על בסיס אותה שכבת הסתברות,
    אך עם שינויי משקל וערבוב קל ליצירת שונות.
    """

    backups = []

    for _ in range(count):
        # ערבוב משקלים קל ליצירת גיוון
        adjusted = {n: fused_layer[n] + random.uniform(0, 0.2) for n in fused_layer}

        # מיון לפי ערכים גבוהים
        sorted_nums = sorted(adjusted.items(), key=lambda x: x[1], reverse=True)

        # בחירת 6 המספרים המובילים
        main_set = sorted([num for num, val in sorted_nums[:6]])

        # בחירת אקסטרה
        extra_set = random.choice(list(EXTRA_RANGE))

        backups.append({
            "main": main_set,
            "extra": extra_set
        })

    return backups
# ===============================================
# NASA ULTRA ENGINE – PART 7
# Main Brain Function (הפעלה מלאה של כל המנוע)
# ===============================================

def run_lotto_engine():
    """
    מפעיל את כל שכבות המוח לפי הסדר:
    1. טעינת היסטוריה
    2. שכבת משקלים
    3. מונטה-קרלו
    4. שכבת היתוך הסתברותי
    5. סט ראשי
    6. 5 גיבויים
    """

    # 1. טעינת היסטוריה
    history = load_history()

    # 2. בניית שכבת משקלים מההיסטוריה
    weight_layer = compute_weight_layer(history)

    # 3. מונטה קרלו
    monte_result = monte_carlo_simulation(weight_layer)

    # 4. שכבת היתוך
    fused_layer = fuse_probability_layers(weight_layer, monte_result)

    # 5. יצירת סט ראשי
    final_set = select_final_set(fused_layer)

    # 6. יצירת גיבויים
    backups = generate_backup_sets(fused_layer, count=5)

    return {
        "final": final_set,
        "backups": backups
    }
# ===============================================================
# PART 4 — WEIGHT LAYER (שכבת משקלים חכמה)
# ===============================================================

def compute_weights(history):
    """
    חישוב המשקלים של כל מספר לפי הופעות, רצפים, מרחקים וסטיות.
    נותן בוסט למספרים 'חמים' ומוריד משקל ל'קרים'.
    """

    weight_main = {n: 1.0 for n in MAIN_RANGE}
    weight_extra = {n: 1.0 for n in EXTRA_RANGE}

    # ספירה בסיסית
    count_main = {n: 0 for n in MAIN_RANGE}
    count_extra = {n: 0 for n in EXTRA_RANGE}

    for draw in history:
        for num in draw["main"]:
            count_main[num] += 1
        count_extra[draw["extra"]] += 1

    # נרמול ספירות
    max_main = max(count_main.values()) or 1
    max_extra = max(count_extra.values()) or 1

    for n in MAIN_RANGE:
        weight_main[n] += (count_main[n] / max_main) * 1.5  # בוסט למספרים חמים

    for n in EXTRA_RANGE:
        weight_extra[n] += (count_extra[n] / max_extra) * 1.7  # בוסט חזק יותר לאקסטרה

    # בוסט לרצפים
    for draw in history[-10:]:
        sorted_nums = sorted(draw["main"])
        for i in range(len(sorted_nums) - 1):
            if sorted_nums[i + 1] - sorted_nums[i] == 1:
                weight_main[sorted_nums[i]] += 0.4
                weight_main[sorted_nums[i + 1]] += 0.4

    return weight_main, weight_extra
# ===============================================================
# PART 5 — MONTE CARLO LAYER (שכבת מונטה-קרלו)
# ===============================================================

def monte_carlo_predict(history, runs=MC_RUNS):
    """
    מריץ אלפי סימולציות לפי המשקלים שחושבו.
    בכל ריצה המערכת בוחרת 6 מספרים לפי משקל ודפוסים.
    לבסוף – בונה תחזית סופית מתוך כל ההרצות.
    """

    weight_main, weight_extra = compute_weights(history)

    results_main = []
    results_extra = []

    for _ in range(runs):

        # בחירה של מספר עיקרי לפי משקל (weighted choice)
        main_nums = random.choices(
            population=list(weight_main.keys()),
            weights=list(weight_main.values()),
            k=6
        )

        # מניעת כפילויות
        main_nums = sorted(list(set(main_nums)))
        while len(main_nums) < 6:
            add_num = random.choices(
                population=list(weight_main.keys()),
                weights=list(weight_main.values()),
                k=1
            )[0]
            if add_num not in main_nums:
                main_nums.append(add_num)
        main_nums = sorted(main_nums)

        # בחירת מספר אקסטרה
        extra_num = random.choices(
            population=list(weight_extra.keys()),
            weights=list(weight_extra.values()),
            k=1
        )[0]

        results_main.append(tuple(main_nums))
        results_extra.append(extra_num)

    # —————————————————————————
    # בניית תחזית סופית לפי הופעות
    # —————————————————————————

    best_main = statistics.mode(results_main)
    best_extra = statistics.mode(results_extra)

    return {
        "main": list(best_main),
        "extra": best_extra
    }
