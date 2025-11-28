import pandas as pd

class DataProcessor:
    def __init__(self):
        pass

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        מנקה ומעבד את נתוני ההגרלות.
        מתקן טיפוסים, מוחק שדות ריקים, מסדר תאריכים.
        """

        # מוריד שורות ריקות
        df = df.dropna(how='all')

        # מנרמל שמות עמודות
        df.columns = [c.strip().lower() for c in df.columns]

        # מוודא שכל המספרים הם מספרים
        num_cols = [col for col in df.columns if "מספר" in col or "num" in col or "ball" in col]

        for col in num_cols:
            df[col] = df[col].astype(str).str.replace(r"[^0-9]", "", regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # מוחק שורות עם מספרים לא חוקיים (ניקוי תקני)
        df = df.dropna(subset=num_cols)

        # מסדר לפי תאריך אם קיים
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.sort_values('date')

        df = df.reset_index(drop=True)
        return df

    def to_records(self, df: pd.DataFrame) -> list:
        """
        ממיר את הדאטה־פריים לרשימת רשומות (dict) למנועים אחרים.
        """
        return df.to_dict(orient='records')
