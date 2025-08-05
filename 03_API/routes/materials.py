from flask import Flask , jsonify, Response, request, Blueprint
import sqlite3
import json

materials_bp = Blueprint("materials", __name__)

DB_PATH = "02_Database/bike_project.db"

@materials_bp.route("/materials")
def get_materials():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM  materials")
        rows = result.fetchall()
        materials = [
            {
                "name": row["name"],
                "type": row["type"],
                "unit": row["unit_price"],
                "stock": row["stock"]
            }for row in rows
        ]
        return Response(
            json.dumps(materials, indent=2),
            mimetype="application/json"
        )

@materials_bp.route("/materials", methods=["POST"])
def set_materials():
    data = request.get_json()
    error = [] # to store errors when trying to add multiple materials. 
    def insert_materials(material): #helper function
        try:
            cursor.execute (
                """
                INSERT INTO materials(name, type, unit_price, stock)
                VALUES (?,?,?,?)
                """, 
                (
                        material["name"], 
                        material["type"], 
                        material["unit_price"], 
                        material["stock"]
                )
            )
        except sqlite3.IntegrityError:
            error.append(f"{material['name']} already exists.")
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        if isinstance(data, list):
            for item in data:
                insert_materials(item)
        else:
            insert_materials(data)
        conn.commit()
    if error:
        return jsonify({"message": "Some materials were not added", "errors": error}), 409

    return jsonify({"message": "Material(s) added successfully."}), 201