from flask import jsonify, request, Response, Blueprint
import sqlite3
import json

#Defining Blueprint
vendors_bp = Blueprint("vendors", __name__)

#gloabal variable
DB_PATH = "02_Database/bike_project.db"

#endpoint to fetch all vendors
@vendors_bp.route("/vendors")
def get_vendors():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row #allow the access each row as a dictionary
        cursor = conn.cursor() #create cursoe
        result = cursor.execute("SELECT * FROM vendors") #store the result of execute 
        rows = result.fetchall()# get all rows in a list
        vendors = [ #list comprehension to get the proper order result for output. 
            #each result is a dict
            {
                "name": row["name"],
                "contact": row["contact"]
            } for row in rows
        ]
        return Response ( # convert the list of dict to JSON string
             json.dumps(vendors, indent = 2),
            mimetype="application/json"
        )
@vendors_bp.route("/vendors", methods = ["POST"])
def set_vendors():
    data = request.get_json()
    try:
        with sqlite3.connect(DB_PATH) as conn:
           cursor = conn.cursor()
           cursor.execute (
                """
                INSERT INTO vendors(name, contact)
                VALUES (?,?)
                """, (data["name"], data["contact"])
           ) 
           conn.commit()
           return jsonify({"message": "Vendor added successfully"}), 201 
        #success code for creation
    except sqlite3.IntegrityError:
        return jsonify({"error": "Vendor with this name already exists"}), 409