import sqlite3
from csv import DictReader

with sqlite3.connect("02_Database/bike_project.db") as conn:
    cursor = conn.cursor()
    with open("02_Database/departments.csv" , "r") as file:
        reader = DictReader(file)
        for row in reader:
            cursor.execute (
                """
                INSERT INTO departments (name)
                VALUES (?)
                """,
                (row["name"],)
            )
    conn.commit()
print("Departments data imported successfully")