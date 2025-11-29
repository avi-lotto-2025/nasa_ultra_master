import json
import time
from prediction_engine import PredictionEngine
from backup_engine import BackupEngine


class ForecastPackage:
    def __init__(self):
        self.pred_engine = PredictionEngine()
        self.back_engine = BackupEngine()

    def generate_package(self, records):
        """
        מחזיר תחזית ראשית + 5 גיבויים בפורמט JSON.
        """

        # תחזית ראשית
        main_forecast = self.pred_engine.generate_main_prediction(records)

        # חמש תחזיות גיבוי
        backups = self.back_engine.generate_all_backups(records)

        # זמן פעולה
        ts = int(time.time())

        # בניית חבילה מלאה
        package = {
            "status": "success",
            "timestamp": ts,
            "version": "NASA_ULTRA_MASTER_VX",
            "main_forecast": main_forecast,
            "backup_forecasts": backups,
        }

        return package

    def to_json(self, package):
        """
        המרה ל־JSON בצורה תקנית.
        """
        return json.dumps(package, ensure_ascii=False, indent=4)
