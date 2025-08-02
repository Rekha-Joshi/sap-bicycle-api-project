import sqlite3
from csv import DictReader

with sqlite3.connect("02_Database/bike_project.db") as conn:
    cursor = conn.cursor()
    with open("02_Database/materials.csv" , "r") as file:
        reader = DictReader(file)
        for row in reader:
            cursor.execute (
                """
                INSERT INTO materials (name, type, unit, stock)
                VALUES (?,?,?,?)
                """,
                (row["name"], row["type"], row["unit_price"], row["stock"])
            )
    conn.commit()
print("Materials data imported successfully")