from flask import Flask, request, Response, Blueprint, jsonify
import sqlite3
import json

cost_centers_bp = Blueprint("cost_centers",__name__)

#gloabal variable
DB_PATH = "02_Database/bike_project.db"

@cost_centers_bp.route("/cost_centers")
def get_cost_centers(): #get all cost centers
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cost_centers")
        rows = cursor.fetchall()
        if not rows:
            return jsonify({"error":"There are no cost centers."}),400
        co_centers = [
            {
               "code":row["code"],
               "name":row["name"]
            } for row in rows
        ]
        return Response(
            json.dumps(co_centers, indent=2),
            mimetype="applications/json"
        ),200

@cost_centers_bp.route("/cost_centers/<int:co_id>")
def get_cost_center(co_id): #get cost centers by ID
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cost_centers WHERE id=?",(co_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"error":"Invalid cost center id."}),404
        co_centers = [
            {
               "code":row["code"],
               "name":row["name"]
            }
        ]
        return Response(
            json.dumps(co_centers, indent=2),
            mimetype="applications/json"
        ),200
@cost_centers_bp.route("/cost_centers", methods=["POST"])
def add_cost_center():
    data = request.get_json()
    #1) validate input data
    if not data or not isinstance(data, dict):
        return jsonify({"error":"Invalid data provided."})  
    
    #2) allowed data
    allowed = ["code", "name"]
    updates = {k:v for k,v in data.items() if k in allowed}
    if "code" not in updates or "name" not in updates:
        return jsonify({"error":"Code and Name must be provided."})

    #3) validate code and name. must be non empty string
    code = updates["code"]
    if not isinstance(code, str) or not code.lower().strip():
        return jsonify({"error":"Code must be non empty string."}), 400
    name = updates["name"]
    if not isinstance(name, str) or not name.lower().strip():
        return jsonify({"error":"Name must be non empty string."}), 400
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute("""
                           INSERT INTO cost_centers (code, name) VALUES (?,?)
                           """, (code,name)
                        )
            conn.commit()
            return jsonify({"message":"Cost center added successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Cost center with this name already exists"}), 409
