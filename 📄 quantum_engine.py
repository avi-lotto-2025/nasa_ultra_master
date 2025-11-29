import random
import numpy as np

class QuantumEngine:
    def __init__(self, stats_engine=None, kira_engine=None):
        self.stats = stats_engine
        self.kira = kira_engine

    # שכבה 1 — רנדומיות קואנטית מתוקנת
    def quantum_random(self, low=1, high=37, size=6):
        """
        מחזיר 6 מספרים רנדומליים, אבל לא טהורים — 
        אלא ברנדומיות "מתוקנת" בעזרת רעש קואנטי.
        """

        base = np.random.randint(low, high, size)
        noise = np.random.normal(0, 1.2, size)
        adjusted = base + noise
        adjusted = np.clip(adjusted, low, high - 1)
        adjusted = [int(round(x)) for x in adjusted]
        return adjusted

    # שכבה 2 — Monte Carlo Simulation
    def monte_carlo(self, simulations=5000):
        """
        מבצע 5000 סימולציות ומחזיר התפלגות על מספרים.
        """
        results = []

        for _ in range(simulations):
            sample = np.random.randint(1, 37, 6)
            sample = list(sample)
            results.extend(sample)

        counts = {}
        for n in results:
            counts[n] = counts.get(n, 0) + 1

        return counts

    # שכבה 3 — בוסט קירה רדינסקי
    def kira_boost(self, record_stats, kira_stats):
        """
        מחזק מספרים שנמצאו ע"י קירה כדפוסים/מגמות.
        """
        boost = {}

        for num, info in kira_stats.items():
            if isinstance(info, dict) and "std_gap" in info:
                score = max(0.1, 3 - info["std_gap"])
                boost[num] = score

        return boost

    # שכבה 4 — משקל משולב
    def combined_weights(self, mc, boosts):
        """
        משלב את המשקלים מ-Monte Carlo + בוסט קירה.
        """
        final = {}

        for num in range(1, 37):
            mc_w = mc.get(num, 0)
            boost_w = boosts.get(num, 0)
            final[num] = mc_w + (boost_w * 50)

        return final

    # שכבה 5 — בחירת 6 מספרים סופיים
    def choose_numbers(self, weights):
        """
        בוחר 6 מספרים בעלי המשקל הגבוה ביותר.
        """
        sorted_nums = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        chosen = [n for n, w in sorted_nums[:6]]
        chosen = sorted(chosen)
        return chosen

    # שכבה 6 — בונוס (המספר החזק)
    def choose_bonus(self):
        """
        בוחר מספר חזק בין 1 ל-7 בצורה קואנטית.
        """
        base = np.random.randint(1, 8)
        noise = np.random.normal(0, 0.4)
        final = int(round(base + noise))
        final = max(1, min(7, final))
        return final

    # המנוע השלם
    def generate_quantum_prediction(self, stats_records=None, kira_records=None):
        """
        מחזיר תחזית מלאה:
        6 מספרים + בונוס.
        """

        # שכבה 2 — מונטה קרלו
        mc = self.monte_carlo(simulations=8000)

        # שכבה 3 — קירה
        kira_boosts = {}
        if kira_records:
            kira_boosts = self.kira_boost(stats_records, kira_records)

        # שכבה 4 — שילוב משקלים
        weights = self.combined_weights(mc, kira_boosts)

        # שכבה 5 — בחירת 6 מספרים
        main_nums = self.choose_numbers(weights)

        # שכבה 6 — בחירת מספר חזק
        bonus = self.choose_bonus()

        return {
            "main": main_nums,
            "extra": bonus
        }
