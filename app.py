# ================================================
# [A] CONSTANTS BLOCK
# קבועים, טווחי מספרים, שעות, ימים, מפתחות
# ================================================

import os
import random
import datetime

# --- טווחי המספרים לחיזוי הלוטו ---
MAIN_MIN = 1
MAIN_MAX = 37
MAIN_COUNT = 6

EXTRA_MIN = 1
EXTRA_MAX = 7
EXTRA_COUNT = 1

# --- ימים להרצה ---
# שלישי = 1, חמישי = 3, מוצ״ש = 5
SCHEDULE_DAYS = [1, 3, 5]      # שלישי, חמישי, מוצ״ש
SCHEDULE_HOUR = 20             # שעה 20:00

# --- מפתח SendGrid (נמשך מה-ENV של Render) ---
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")

# --- הגדרות לוג ---
LOG_PREFIX = "[NASA_ULTRA]"

# --- Seed בסיסי כדי שהמערכת תוכל להתאפס במקרה תקלה ---
BASE_SEED = 987654321

# --- שעה למנגנון הבדיקה העצמית ---
SELF_CHECK_INTERVAL_MINUTES = 10
