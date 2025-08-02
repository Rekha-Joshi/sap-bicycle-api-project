import sqlite3
from csv import DictReader

with sqlite3.connect("02_Database/bike_project.db") as conn:
    cursor = conn.cursor()
    with open("02_Database/employees.csv" , "r") as file:
        reader = DictReader(file)
        for row in reader:
            #print("Looking for department_id:", row["department_id"])
            dept_id = int(row["department_id"])  # convert string to int
            cursor.execute ("SELECT name FROM departments WHERE id = ?", (dept_id,))
            result = cursor.fetchone()
            #print(result)
            if result:
                dept_name = result[0]
                cursor.execute (
                    """
                    INSERT INTO employees (name, department_name, job_title)
                    VALUES (?,?,?)
                    """,
                    (row["name"], dept_name, row["job_title"])
                )
    conn.commit()
print("Employees data imported successfully")