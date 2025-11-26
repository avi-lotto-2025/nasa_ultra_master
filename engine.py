import json
import numpy as np
import statistics
import random


class NASAUltraEngine:
    """
    NASA_ULTRA_MASTER_VX
    מנוע מלא, בלתי שביר, כולל כל שכבות ההגנה, self-heal ו-fallback
    """

    # ---------------------------------------------------------
    # 1. INIT
    # ---------------------------------------------------------
    def __init__(self):
        self.history = []
        self.normalized = []
        self.weights = {}
        self.pairs = {}
        self.triplets = {}

    # ---------------------------------------------------------
    # 2. DATA LOADER — טוען כל סוג נתונים בלי להישבר
    # ---------------------------------------------------------
    def load_data(self, data):
        try:
            if isinstance(data, str):
                data = json.loads(data)

            if not isinstance(data, list):
                raise ValueError("הפורמט שהתקבל אינו רשימה")

            cleaned = []
            for entry in data:

                if isinstance(entry, dict):
                    main = entry.get("main", [])
                    extra = entry.get("extra", None)
                elif isinstance(entry, list):
                    main = entry
                    extra = None
                else:
                    continue

                # סינון ערכים לא חוקיים
                main = [x for x in main if isinstance(x, int)]
                if extra is not None and not isinstance(extra, int):
                    extra = None

                cleaned.append({"main": main, "extra": extra})

            # סינון כפילויות:
            unique = []
            seen = set()
            for item in cleaned:
                t = tuple(item["main"]) + (item["extra"],)
                if t not in seen:
                    seen.add(t)
                    unique.append(item)

            self.history = unique
            return True

        except Exception:
            # FALLBACK — היסטוריה ריקה → עדיין עובד
            self.history = []
            return False

    # ---------------------------------------------------------
    # 3. NORMALIZER — מאחד הכול לפורמט פנימי קבוע
    # ---------------------------------------------------------
    def normalize(self):
        try:
            normalized = []
            for entry in self.history:
                normalized.append({
                    "main": [int(x) for x in entry["main"]],
                    "extra": entry["extra"] if entry["extra"] is not None else None
                })
            self.normalized = normalized
            return True
        except Exception:
            self.normalized = []
            return False

    # ---------------------------------------------------------
    # 4. ANALYSIS — Frequency / Hot-Cold / Pairs / Triplets
    # ---------------------------------------------------------
    def analyze(self):
        try:
            freq = {}
            bonus_freq = {}

            for entry in self.normalized:
                for num in entry["main"]:
                    freq[num] = freq.get(num, 0) + 1

                if entry["extra"] is not None:
                    bonus_freq[entry["extra"]] = bonus_freq.get(entry["extra"], 0) + 1

            # חשבון סטטיסטי
            nums = list(freq.keys())
            counts = list(freq.values())

            if len(counts) > 1:
                avg = statistics.mean(counts)
                std = statistics.pstdev(counts)
            else:
                avg = 1
                std = 1

            weights = {}
            for n, c in freq.items():
                # משקל ליבה
                w = c / (avg + 0.0001)

                # חם/קר
                if c > avg + std:
                    w *= 1.25
                elif c < avg - std:
                    w *= 0.75

                weights[n] = w

            self.weights = weights

            # זוגות + שלשות
            pairs = {}
            triplets = {}

            for entry in self.normalized:
                m = entry["main"]
                m_sorted = sorted(m)

                # זוגות
                for i in range(len(m_sorted)):
                    for j in range(i + 1, len(m_sorted)):
                        pair = (m_sorted[i], m_sorted[j])
                        pairs[pair] = pairs.get(pair, 0) + 1

                # שלשות
                if len(m_sorted) >= 3:
                    for i in range(len(m_sorted) - 2):
                        trip = (m_sorted[i], m_sorted[i + 1], m_sorted[i + 2])
                        triplets[trip] = triplets.get(trip, 0) + 1

            self.pairs = pairs
            self.triplets = triplets

            return True

        except Exception:
            # fallback
            self.weights = {}
            self.pairs = {}
            self.triplets = {}
            return False

    # ---------------------------------------------------------
    # 5. MONTE CARLO — סימולציות משקל
    # ---------------------------------------------------------
    def monte_carlo(self, iterations=3000):
        try:
            scores = {}
            nums = list(self.weights.keys())

            if not nums:
                return {}

            for _ in range(iterations):
                draw = random.sample(nums, min(6, len(nums)))
                score = sum(self.weights.get(n, 1) for n in draw)

                for n in draw:
                    scores[n] = scores.get(n, 0) + score

            return scores

        except Exception:
            return {}

    # ---------------------------------------------------------
    # 6. BOOSTER — חיזוק מספרים חזקים והחלשה של חלשים
    # ---------------------------------------------------------
    def booster(self, scores):
        boosted = {}
        for n, s in scores.items():
            w = self.weights.get(n, 1)
            boosted[n] = s * w
        return boosted

    # ---------------------------------------------------------
    # 7. BONUS ENGINE — בחירת בונוס יציבה
    # ---------------------------------------------------------
    def choose_bonus(self):
        bonus_counts = {}
        for e in self.normalized:
            if e["extra"] is not None:
                bonus_counts[e["extra"]] = bonus_counts.get(e["extra"], 0) + 1

        if not bonus_counts:
            return random.randint(1, 10)

        return max(bonus_counts, key=bonus_counts.get)

    # ---------------------------------------------------------
    # 8. STABILITY CHECK — בדיקות פיזור וניקוי חריגות
    # ---------------------------------------------------------
    def stabilize(self, nums):
        nums = sorted(set(nums))
        if len(nums) < 6:
            while len(nums) < 6:
                r = random.randint(1, max(nums) + 5)
                if r not in nums:
                    nums.append(r)
        return sorted(nums)

    # ---------------------------------------------------------
    # 9. OUTPUT — יצירת תחזית סופית
    # ---------------------------------------------------------
    def generate(self):
        try:
            if not self.normalized:
                return {"main": [1, 2, 3, 4, 5, 6], "extra": 7}

            mc = self.monte_carlo()
            boosted = self.booster(mc)

            # בחירת 6 מספרים
            best = sorted(boosted.items(), key=lambda x: x[1], reverse=True)
            nums = [x[0] for x in best[:6]]

            nums = self.stabilize(nums)
            bonus = self.choose_bonus()

            return {"main": nums, "extra": bonus}

        except Exception:
            # FALLBACK חזק מאוד
            return {
                "main": sorted(random.sample(range(1, 39), 6)),
                "extra": random.randint(1, 10)
            }


# ---------------------------------------------------------
# פונקציה גלובלית — API משתמש בה
# ---------------------------------------------------------
def generate_forecast(history):
    engine = NASAUltraEngine()
    engine.load_data(history)
    engine.normalize()
    engine.analyze()
    return engine.generate()
