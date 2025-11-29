import time
import traceback
from package_engine import ForecastPackage


class AutoHeal:
    def __init__(self):
        self.package_engine = ForecastPackage()
        self.last_good = None
        self.last_error = None

    def safe_generate(self, records):
        """
        המנוע הבטוח — מנסה לייצר תחזית,
        ואם יש בעיה → מתקן את עצמו ומחזיר תחזית מגיבוי.
        """

        try:
            # ניסיון ראשי
            result = self.package_engine.generate_package(records)

            # שמירה של חבילה תקינה אחרונה
            self.last_good = result
            self.last_error = None

            return {
                "status": "ok",
                "autoheal": "healthy",
                "package": result
            }

        except Exception as e:
            # שגיאה – לא נבהלים, עוברים לאוטו־הל
            self.last_error = {
                "error": str(e),
                "trace": traceback.format_exc(),
                "time": int(time.time())
            }

            # אם יש חבילה תקינה אחרונה – משתמשים בה
            if self.last_good:
                return {
                    "status": "degraded",
                    "autoheal": "recovered_from_error",
                    "used_backup_package": True,
                    "error_info": self.last_error,
                    "package": self.last_good
                }

            # אם אין חבילה קודמת – מחזירים מינימלית
            return {
                "status": "failed",
                "autoheal": "no_previous_success",
                "error_info": self.last_error,
                "package": {
                    "main_forecast": [0, 0, 0, 0, 0, 0],
                    "backup_forecasts": [],
                    "timestamp": int(time.time())
                }
            }

    def heartbeat(self):
        """
        מחזיר סטטוס מערכת — לניטור 24/7.
        """
        return {
            "status": "alive",
            "last_good_package": self.last_good,
            "last_error": self.last_error,
            "heartbeat_time": int(time.time())
        }
