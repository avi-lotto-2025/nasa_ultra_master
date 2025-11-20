# ============================================================
#  NASA_ULTRA_MASTER  —  רמת נאס״א-על (UltraWave Quantum Level)
#  קובץ ראשי: engine.py
# ============================================================

import os
import random
import datetime
import time
import numpy as np
import threading
import requests
from flask import Flask, jsonify

# טווחי מספרים ללוטו
MAIN_RANGE = range(1, 38)      # 1–37
BONUS_RANGE = range(1, 8)      # 1–7

# ימי הפעילות (שלישי / חמישי / שבת)
DAYS_ACTIVE = [1, 3, 5]        # Tue=1, Thu=3, Sat=5

# שעת ריצה רשמית: 20:00
RUN_HOUR = 20
