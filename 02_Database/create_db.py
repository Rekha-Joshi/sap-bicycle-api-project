import sqlite3

# Connect to database or create one if not already exists
with sqlite3.connect("02_Database/bike_project.db") as conn: #when using with, connection will close 
    cursor = conn.cursor() #used to execute sql queries

    # Read the schema.sql file
    with open("02_Database/schema.sql", "r") as file:
        sql_script = file.read() #reading the entire file as string
    
    #Execute all commands from the file
    cursor.executescript(sql_script) # because our file has many lines
    conn.commit()
print("Database and tables created successfully.")
