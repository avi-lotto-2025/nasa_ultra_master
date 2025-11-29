import pandas as pd
from collections import Counter
import itertools

class StatsEngine:
    def __init__(self):
        pass

    # חישוב שכיחויות של כל מספר
    def frequency(self, records: list) -> dict:
        """
        מקבל רשימת רשומות (dict) של הגרלות
        מחזיר שכיחויות של כל מספר.
        """
        all_nums = []
        for r in records:
            for key, val in r.items():
                if key.startswith("num") or key.startswith("ball") or "מספר" in key:
                    all_nums.append(val)

        counts = Counter(all_nums)
        return dict(counts)

    # זיהוי מספרים חמים/קרים
    def hot_cold(self, freq: dict) -> dict:
        """
        מחזיר {"hot": [...], "cold": [...]} לפי שכיחויות.
        """
        if not freq:
            return {"hot": [], "cold": []}

        values = list(freq.values())
        threshold_hot = pd.Series(values).quantile(0.75)
        threshold_cold = pd.Series(values).quantile(0.25)

        hot = [num for num, c in freq.items() if c >= threshold_hot]
        cold = [num for num, c in freq.items() if c <= threshold_cold]

        return {"hot": hot, "cold": cold}

    # טווחי הופעה
    def ranges(self, records: list) -> dict:
        """
        מחשב את המופע הראשון, האחרון והמרחק ביניהם.
        """
        positions = {}

        for i, r in enumerate(records):
            for key, val in r.items():
                if key.startswith("num") or key.startswith("ball") or "מספר" in key:
                    if val not in positions:
                        positions[val] = []
                    positions[val].append(i)

        ranges = {}
        for num, locs in positions.items():
            ranges[num] = {
                "first": locs[0],
                "last": locs[-1],
                "distance": locs[-1] - locs[0]
            }

        return ranges

    # ניתוח זוגות
    def pair_analysis(self, records: list) -> dict:
        """
        מחשב שכיחויות של זוגות מספרים.
        """
        pairs = []

        for r in records:
            nums = []
            for key, val in r.items():
                if key.startswith("num") or key.startswith("ball") or "מספר" in key:
                    nums.append(val)

            nums = sorted(nums)
            for pair in itertools.combinations(nums, 2):
                pairs.append(pair)

        counts = Counter(pairs)
        return dict(counts)

    # ניתוח שלישיות
    def triplet_analysis(self, records: list) -> dict:
        """
        מחשב שכיחויות של שלישיות.
        """
        trips = []

        for r in records:
            nums = []
            for key, val in r.items():
                if key.startswith("num") or key.startswith("ball") or "מספר" in key:
                    nums.append(val)

            nums = sorted(nums)
            for trip in itertools.combinations(nums, 3):
                trips.append(trip)

        counts = Counter(trips)
        return dict(counts)
