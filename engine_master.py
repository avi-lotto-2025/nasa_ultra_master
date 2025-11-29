import json
import traceback

from data_processor import DataProcessor
from stats_engine import StatsEngine
from kira_engine import KiraEngine
from quantum_engine import QuantumEngine
from prediction_engine import PredictionEngine
from backup_engine import BackupEngine
from package_engine import ForecastPackage
from auto_heal import AutoHeal


class EngineMaster:
    """
    המוח הראשי של NASA_ULTRA_MASTER_VX
    מחבר את כל המנועים למערכת אחת.
    """

    def __init__(self, history_records=None):
        self.data_processor = DataProcessor()
        self.stats_engine = StatsEngine()
        self.kira_engine = KiraEngine()
        self.quantum_engine = QuantumEngine(
            stats_engine=self.stats_engine,
            kira_engine=self.kira_engine,
        )
        self.pred_engine = PredictionEngine()
        self.backup_engine = BackupEngine()
        self.package_engine = ForecastPackage()
        self.autoheal = AutoHeal()

        # היסטוריה — נטענת מבחוץ (כשיהיה קובץ תקין)
        self.history_records = history_records or []

    # -----------------------------------------------------

    def load_history(self, df):
        """
        מקבל DataFrame של היסטוריה → מנקה → מכין רשומות.
        """
        try:
            cleaned = self.data_processor.clean_dataframe(df)
            self.history_records = self.data_processor.to_records(cleaned)
            return {"status": "history_loaded", "records": len(self.history_records)}

        except Exception as e:
            return {"status": "history_load_failed", "error": str(e)}

    # -----------------------------------------------------

    def generate_safe_forecast(self):
        """
        מוציא תחזית מלאה + 5 גיבויים + Auto-Heal
        """
        try:
            if not self.history_records:
                return {
                    "status": "error",
                    "message": "No history data loaded",
                    "package": None,
                }

            # Auto-Heal
            result = self.autoheal.safe_generate(self.history_records)
            return result

        except Exception as e:
            return {
                "status": "fatal_error",
                "error": str(e),
                "trace": traceback.format_exc(),
            }

    # -----------------------------------------------------

    def generate_raw_forecast(self):
        """
        תחזית ללא Auto-Heal — משמשת לבדיקות.
        """
        if not self.history_records:
            return {"status": "error", "message": "No history loaded"}

        package = self.package_engine.generate_package(self.history_records)
        return package

    # -----------------------------------------------------

    def status(self):
        """
        מחזיר סטטוס מלא של כל המערכת.
        """
        return {
            "status": "online",
            "records_loaded": len(self.history_records),
            "autoheal_status": self.autoheal.heartbeat(),
        }
