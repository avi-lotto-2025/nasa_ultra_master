import random

# ============================================================
# ENGINE – BASIC FORECAST ENGINE (VERSION B)
# שלב בסיסי יציב – לפני הכנסת המוח המלא
# ============================================================

def generate_basic_forecast():
    """
    שלב בסיסי: יוצר תחזית זמנית בלבד.
    בשכבות הבאות נוסיף:
    - משקלים
    - הסתברויות
    - נתוני עבר
    - Monte Carlo
    - שכבות מוח
    - 5 גיבויים
    """

    main = sorted(random.sample(range(1, 38), 6))
    extra = random.randint(1, 7)

    return {
        "main": main,
        "extra": extra
    }


# ============================================================
# TEST FUNCTION
# ============================================================

def engine_status():
    return "ENGINE_BASIC_OK"

