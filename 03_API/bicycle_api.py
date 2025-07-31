from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__) #create the app

@app.route("/") # this function runs when we run this program
def home():
    return("Hello API")

@app.route("/customers") #Fetch users
def get_customers():
    #create DB connections
    with sqlite3.connect("02_Database/bike_project.db") as conn:
        conn.row_factory = sqlite3.Row #Allows access to each database row like a dictionary (e.g., row["name"])
        cursor = conn.cursor() #create the cursor
        result = cursor.execute("SELECT * FROM customers") #Runs a query to fetch all customer records
        rows = result.fetchall() #Give me all rows returned by the query, in a list
        customers = [
            {
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "phone": row["phone"],
                "address": row["address"]
            }
            for row in rows
        ] # turn each row into dict and return the list of ordered dictoniories
        return jsonify(customers),200 #return all customers and sucess code 

if __name__ == "__main__":
    app.run(debug=True)