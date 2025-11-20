# ===============================================================
#  NASA_ULTRA_MASTER — רמת נאס״א-על (UltraWave Quantum Level)
#  קובץ ראשי: engine.py
# ===============================================================

import os
import random
import datetime
import time
import numpy as np
import threading
import requests
from flask import Flask, jsonify

MAIN_RANGE = range(1, 38)
BONUS_RANGE = range(1, 8)

DAYS_ACTIVE = [1, 3, 5]   # Tue, Thu, Sat
RUN_HOUR = 20
