from flask import jsonify, request, Response, Blueprint
import sqlite3
import json

#Defining Blueprint
vendors_bp = Blueprint("vendors", __name__)

#gloabal variable
DB_PATH = "02_Database/bike_project.db"

#endpoint to fetch all vendors
@vendors_bp.route("/vendors")
def get_vendors(): #get all vendors
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row #allow the access each row as a dictionary
        conn.execute("PRAGMA foreign_keys = ON")
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
        ),200

@vendors_bp.route("/vendors/<int:v_id>")
def get_vendor(v_id): #get one vendor based on vendor id
    if v_id <=0:
        return jsonify({"error":"Invalid vendor ID."}), 400
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vendors WHERE id =?",(v_id,))
        data = cursor.fetchone()
        if not data:
            return jsonify({"error":"Vendor not found."}), 404
        vendor = {
            "name":data["name"],
            "contact":data["contact"]
        }
        return jsonify(vendor), 200
@vendors_bp.route("/vendors", methods = ["POST"])
def set_vendors(): #create new vendor
    data = request.get_json()
    try:
        with sqlite3.connect(DB_PATH) as conn:
           conn.execute("PRAGMA foreign_keys = ON")
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

@vendors_bp.route("/vendors/<int:v_id>/materials")
def list_vendor_materials(v_id):
    if v_id <=0:
        return jsonify({"error":"Invalid vendor ID."}), 400
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vendors WHERE id =?",(v_id,))
        data = cursor.fetchone()
        if not data:
            return jsonify({"error":"Vendor not found."}), 404
        cursor.execute("SELECT name, type, stock FROM materials WHERE vendor_id=?",(v_id,))
        materials = cursor.fetchall()
        if not materials:
            return jsonify({"error":"There are no materials supplied by this vendor."}), 400
        data = [
            {
                "name":row["name"],
                "type":row["type"],
                "stock":row["stock"]
            } for row in materials
        ] 
        payload = {
            "message": "Materials found for vendor",
            "materials": data
        }
        #return jsonify(payload),200
        return Response(
            json.dumps(payload, indent=2),
            mimetype="application/json"
        )