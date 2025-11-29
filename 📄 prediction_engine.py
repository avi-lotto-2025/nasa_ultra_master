from stats_engine import StatsEngine
from kira_engine import KiraEngine
from quantum_engine import QuantumEngine


class PredictionEngine:
    def __init__(self):
        self.stats_engine = StatsEngine()
        self.kira_engine = KiraEngine()
        self.quantum_engine = QuantumEngine(
            stats_engine=self.stats_engine,
            kira_engine=self.kira_engine
        )

    def generate_main_prediction(self, records):
        """
        המנוע הראשי של NASA_ULTRA.
        מחבר בינה מלאכותית + קירה + קואנטום + סטטיסטיקה.
        """

        # שכבה 1 — נתוני סטטיסטיקה
        stats_data = self.stats_engine.frequency(records)

        # שכבה 2 — דפוסים קירה
        kira_data = self.kira_engine.trend_analysis(records)

        # שכבה 3 — תחזית קואנטום
        quantum_result = self.quantum_engine.generate_quantum_prediction(
            stats_records=stats_data,
            kira_records=kira_data
        )

        main_nums = quantum_result["main"]
        bonus = quantum_result["extra"]

        # שכבה 4 — אנטי דופליקציה + ייצוב
        main_nums = sorted(list(set(main_nums)))
        while len(main_nums) < 6:
            main_nums.append((max(main_nums) + 1) % 37 or 1)
        main_nums = sorted(main_nums)

        # תוצאה סופית
        return {
            "main": main_nums,
            "extra": bonus
        }
