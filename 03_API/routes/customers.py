from flask import jsonify, request, Response, Blueprint
import sqlite3
import json

#Create Blueprint. It's like a mini app
customers_bp = Blueprint("customers", __name__)
#Blueprint is a Flask class that lets you define a group of routes.
#first varible is the name of the blueprint. 
#__name__ tells python that this file is the starting point of this blueprint.

#gloabal variable
DB_PATH = "02_Database/bike_project.db"

#Customers route. Defining end point to get customers
## Fetch and return all customers from the database (GET)
@customers_bp.route("/customers") #Fetch users
def get_customers():
    #create DB connections
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row #Allows access to each database row like a dictionary (e.g., row["name"])
        cursor = conn.cursor() #create the cursor
        result = cursor.execute("SELECT * FROM customers") #Runs a query to fetch all customer records
        rows = result.fetchall() #Give me all rows returned by the query, in a list
        customers = [ #doing this so that data is displayed with correct order
            {
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "phone": row["phone"],
                "address": row["address"]
            }
            for row in rows
        ] # turn each row into dict and return the list of ordered dictoniories
        #return jsonify(customers),200 # commenting this out because jsonify was messing with the order
        return Response(
            json.dumps(customers, indent=2), #converting dict to json string
            mimetype="application/json" #telling Flask to treat it as JSON string
        )
    
## Accepts JSON data and inserts a new customer record into the database
# Skips duplicates if email already exists (email must be unique)    
@customers_bp.route("/customers", methods = ["POST"] )
def create_customer():
    data = request.get_json()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO customers(name, email, phone, address)
                VALUES (?,?,?,?)
                """, (data["name"], data["email"], data["phone"], data["address"])
            )
            conn.commit()
            return jsonify({"message": "Customer added successfully"}), 201 
        #success code for creation
    except sqlite3.IntegrityError:
        return jsonify({"error": "Customer with this email already exists"}), 409