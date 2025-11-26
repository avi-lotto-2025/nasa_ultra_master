import json
import random
from collections import Counter

# =====================================================================
# ENGINE V1 – מנוע יציב, נקי, מוכן ל-Railway
# =====================================================================

def load_history():
    """טוען את קובץ היסטוריית הגרלות (history_full.json)."""
    with open("history_full.json", "r", encoding="utf-8") as f:
        return json.load(f)

def generate_forecast():
    """תחזית יציבה: מבוססת שכיחויות + בחירה אקראית מוגנת."""
    history = load_history()

    # איסוף כל המספרים
    all_numbers = []
    for draw in history:
        all_numbers.extend(draw["main"])

    freq = Counter(all_numbers)

    # 6 מספרים שכיחים ביותר
    main = [num for num, _ in freq.most_common(6)]
    main.sort()

    # בונוס חכם: לא אחד מהראשיים, טווח מלא
    bonus_candidates = [n for n in range(1, 38) if n not in main]
    bonus = random.choice(bonus_candidates)

    return {
        "main": main,
        "extra": bonus
    }
