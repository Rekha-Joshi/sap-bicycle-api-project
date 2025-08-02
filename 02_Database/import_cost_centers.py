import sqlite3
from csv import DictReader

with sqlite3.connect("02_Database/bike_project.db") as conn:
    cursor = conn.cursor()
    with open("02_Database/cost_centers.csv" , "r") as file:
        reader = DictReader(file)
        for row in reader:
            cursor.execute (
                """
                INSERT INTO cost_centers (code, name)
                VALUES (?,?)
                """,
                (row["code"], row["name"])
            )
    conn.commit()
print("Cost centers data imported successfully")