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
def get_customers(): #List all customers
    #create DB connections
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row #Allows access to each database row like a dictionary (e.g., row["name"])
        conn.execute("PRAGMA foreign_keys = ON")
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
def create_customer(): #create new customer
    data = request.get_json()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
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
    
@customers_bp.route("/customers/by-email", methods = ["GET"])
def get_customer_by_email(): #get customer by email
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Email query parameter is required"}), 400
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE email = ?",(email,))
        row = cursor.fetchone()
        if row:
            customer = dict(row)
            return jsonify(customer), 200
        else:
            return jsonify({"message": "Customer not found"}), 404
    
@customers_bp.route("/customers/<int:cust_id>", methods=["PATCH"])
def update_customer(cust_id):
    if cust_id <=0:
        return jsonify({"error":"Invalid customer id."}), 400
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "JSON body required."}), 400
    allowed = ["name", "email", "phone", "address"]
    updates = {k:v for k,v in data.items() if k in allowed}
    if not updates:
        return jsonify({"error": "Provide at least one of: name, email, phone, address."}), 400
    if "name" in updates:
        if not isinstance(updates["name"], str) or not updates["name"].strip():
            return jsonify({"error": "Name must be a non-empty string"}), 400
        updates["name"] = updates["name"].strip()
    if "address" in updates:
        if not isinstance(updates["address"], str) or not updates["address"].strip():
            return jsonify({"error": "Address must be a non-empty string"}), 400
        updates["address"] = updates["address"].strip()
    if "phone" in updates:
        if any(ch.isalpha() for ch in updates["phone"]):
            return jsonify({"error": "Phone cannot contain letters"}), 400
        digits = "".join(ch for ch in updates["phone"] if ch.isdigit())
        if len(digits) < 7:
            return jsonify({"error":"Phone number is too short"}), 400
        updates["phone"] = updates["phone"].strip()
    if "email" in updates:
        if not isinstance(updates["email"], str) or not updates["email"].strip():
            return jsonify({"error": "Email must be a non-empty string"}), 400
        if "@" not in updates["email"] or "." not in updates["email"]:
            return jsonify({"error":"Invalid email format"}), 400
        updates["email"] = updates["email"].strip().lower()
    set_parts=[]
    params =[]
    for k,v in updates.items():
        set_parts.append(f"{k} =?")
        params.append(v)
    params.append(cust_id) #for where clause
    sql = f"UPDATE customers SET {', '.join(set_parts)} WHERE id = ?"
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute(sql,params)
            conn.commit()
            cursor.execute("SELECT * FROM customers WHERE id = ?", (cust_id,))
            row = cursor.fetchone()
            data = {
                "message": "Customer updated successfully",
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "phone": row["phone"],
                "address": row["address"],
            }
            return Response(
                json.dumps(data, indent=2),
                mimetype = "application/json"
            )
        #success code for creation
    except sqlite3.IntegrityError:
        return jsonify({"error": "Customer with this email already exists"}), 409