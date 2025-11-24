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
