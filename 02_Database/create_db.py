from config import DB_PATH
import sqlite3

# Connect to database or create one if not already exists
with sqlite3.connect(DB_PATH) as conn: #when using with, connection will close 
    cursor = conn.cursor() #used to execute sql queries

    # Read the schema.sql file
    with open(DB_PATH, "r") as file:
        sql_script = file.read() #reading the entire file as string
    
    #Execute all commands from the file
    cursor.executescript(sql_script) # using executescript because our file has many lines
    conn.commit()
print("Database and tables created successfully.")
