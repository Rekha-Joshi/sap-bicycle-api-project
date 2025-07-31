import sqlite3
from csv import DictReader

#connect to database
with sqlite3.connect("02_Database/bike_project.db") as conn:
    cursor = conn.cursor()
    with open("02_Database/customers.csv") as file: #open file in read mode(default)
        reader = DictReader(file) # this is ordered dictionary of customers
        for row in reader:
            cursor.execute(
                """
                INSERT INTO customers (name, email, phone, address)
                VALUES (?,?,?,?)
                """,
                (row["name"], row["email"], row["phone"], row["address"])
            )
    conn.commit() # commit all the changes
print("Customer data imported successfully.")