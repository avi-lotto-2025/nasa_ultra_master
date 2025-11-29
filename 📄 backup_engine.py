from prediction_engine import PredictionEngine
import numpy as np
import random


class BackupEngine:
    def __init__(self):
        self.pred_engine = PredictionEngine()

    def generate_backup(self, records, seed_boost=0):
        """
        מייצר סט גיבוי אחד עם שינויי רעש קטנים.
        """
        # שכבה 1 — תחזית בסיסית מהמנוע הראשי
        base = self.pred_engine.generate_main_prediction(records)

        main = base["main"]
        bonus = base["extra"]

        # שכבה 2 — רעש קטן לשינוי סט (שונה לכל גיבוי)
        noisy = []

        for n in main:
            val = n + np.random.normal(0, 1.4 + seed_boost)
            val = int(round(max(1, min(36, val))))
            noisy.append(val)

        # שכבה 3 — ניקוי חזרות + סידור סופי
        noisy = sorted(list(set(noisy)))
        while len(noisy) < 6:
            noisy.append((max(noisy) + 1) % 37 or 1)

        return {
            "main": sorted(noisy),
            "extra": bonus
        }

    def generate_all_backups(self, records):
        """
        מייצר 5 תחזיות גיבוי מלאות.
        """
        backups = []

        for i in range(5):
            pack = self.generate_backup(records, seed_boost=i * 0.5)
            backups.append(pack)

        return backups
