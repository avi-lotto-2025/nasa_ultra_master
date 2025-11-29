import pandas as pd
import numpy as np

class KiraEngine:
    def __init__(self):
        pass

    def detect_jumps(self, records: list) -> dict:
        """
        מזהה קפיצות בין הגרלות (עלייה או ירידה חזקה של מספרים).
        """
        jumps = {}

        for i in range(1, len(records)):
            prev_nums = []
            curr_nums = []

            for key, val in records[i-1].items():
                if isinstance(val, (int, float)):
                    prev_nums.append(val)

            for key, val in records[i].items():
                if isinstance(val, (int, float)):
                    curr_nums.append(val)

            prev_nums = sorted(prev_nums)
            curr_nums = sorted(curr_nums)

            diffs = []
            for a, b in zip(prev_nums, curr_nums):
                diffs.append(abs(a - b))

            jumps[i] = {
                "max_jump": max(diffs),
                "avg_jump": sum(diffs) / len(diffs),
                "jumps": diffs
            }

        return jumps

    def trend_analysis(self, records: list) -> dict:
        """
        ניתוח מגמות לטווח ארוך (trend) של כל מספר.
        """
        positions = {}

        for i, r in enumerate(records):
            for key, val in r.items():
                if isinstance(val, (int, float)):
                    if val not in positions:
                        positions[val] = []
                    positions[val].append(i)

        trends = {}
        for num, pos in positions.items():
            if len(pos) < 2:
                continue
            diffs = np.diff(pos)
            trends[num] = {
                "avg_gap": np.mean(diffs),
                "min_gap": np.min(diffs),
                "max_gap": np.max(diffs),
                "std_gap": np.std(diffs)
            }

        return trends

    def anomaly_detection(self, records: list) -> dict:
        """
        מזהה הופעות לא טיפוסיות של מספרים.
        """
        appearances = {}

        for i, r in enumerate(records):
            for key, val in r.items():
                if isinstance(val, (int, float)):
                    if val not in appearances:
                        appearances[val] = []
                    appearances[val].append(i)

        anomalies = {}
        for num, pos in appearances.items():
            if len(pos) < 3:
                continue

            diffs = np.diff(pos)
            mean = np.mean(diffs)
            std = np.std(diffs)

            # אנומליה = פער גדול פי 2 נקודות סטייה
            anoms = [i for i, d in enumerate(diffs) if abs(d - mean) > 2 * std]

            anomalies[num] = {
                "gaps": list(diffs),
                "mean_gap": mean,
                "std_gap": std,
                "anomalies": anoms
            }

        return anomalies

    def range_behavior(self, records: list) -> dict:
        """
        ניתוח התנהגות מספרים בתוך טווחי 18:
        1–18, 19–36, 37–52
        """
        ranges = {1: 0, 2: 0, 3: 0}

        for r in records:
            for key, val in r.items():
                if isinstance(val, int):
                    if 1 <= val <= 18:
                        ranges[1] += 1
                    elif 19 <= val <= 36:
                        ranges[2] += 1
                    elif 37 <= val <= 52:
                        ranges[3] += 1

        return {
            "range_1_18": ranges[1],
            "range_19_36": ranges[2],
            "range_37_52": ranges[3],
        }
