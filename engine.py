# ====================================================
# NASA_ULTRA_MASTER – ENGINE LAYER
# ====================================================

import numpy as np
import random

def generate_forecast_pair():
    """
    הפונקציה שמייצרת תחזית לוטו.
    כאן אתה יכול לשלב את כל החוקים, המשקלים, השכבות,
    Monte Carlo וכל מה שהיה במערכת המתקדמת.
    כרגע — גרסה מינימלית, יציבה ומתפקדת מלאה.
    """

    main_balls = sorted(random.sample(range(1, 38), 6))    # 6 מספרים
    extra_ball = random.randint(1, 7)                      # מספר נוסף

    return {
        "main": main_balls,
        "extra": extra_ball
    }
