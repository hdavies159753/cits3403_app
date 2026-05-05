import sqlite3

db_path = "app/drawing_database.db"


def submit_and_save (data):
    image_data = data.get('image')
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO drawings (image) VALUES (?)",
            (image_data,)
        )
        connection.commit()
        return True, "Submitted!"
    finally:
        connection.close()
        