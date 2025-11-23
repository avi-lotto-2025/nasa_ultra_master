from app import app

# זה הכל – Render מפעיל את Gunicorn שמריץ את app הזה.
if __name__ == "__main__":
    app.run()
