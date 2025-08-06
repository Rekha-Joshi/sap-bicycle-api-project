from flask import Flask , jsonify, Response, request, Blueprint
import sqlite3
import json

materials_bp = Blueprint("materials", __name__)

DB_PATH = "02_Database/bike_project.db"
#get all materials
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
#add new materials
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

#lists materials which are low in stock
@materials_bp.route("/materials/low-stock")
def check_stock():
    threshold = int(request.args.get("threshold", 30)) #default = 30
    #request.args gives you access to query parameters in the URL
    #.get("threshold") tries to fetch the value of threshold
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM materials where stock < ?",(threshold,))
        rows = result.fetchall()
        items = [
            {
                "name": row["name"],
                "type": row["type"],
                "unit_price": row["unit_price"],
                "stock": row["stock"]
            }for row in rows
        ]
        if not items:
            response_data = {
               "message": "All materials are sufficiently stocked",
                "items": []
            }
        else:
            response_data = {
                "message": f"Following materials are below {threshold} units",
                "items": items # this is the list of dict
            }
        return Response(
            json.dumps(response_data, indent=2),
            status = 200,
            mimetype="application/json"
        )
    
@materials_bp.route("/materials/<int:id>/stock", methods = ["PUT"])
def update_material_stock(id):
    data = request.get_json()
    #validating if json body is present, there is stock and it's a number
    if not data or "stock" not in data:
        return jsonify({"error": "'stock' field is required"}), 400
    if not isinstance(data["stock"], (int, float)):
        return jsonify({"error": "'stock' must be a number"}), 400
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        new_stock_value = int(data["stock"])
        cursor.execute ("UPDATE materials SET stock = ? where id = ?",(new_stock_value,id,))
        #this is to check if the id was valid. If invalid it will update 0 rows
        if cursor.rowcount == 0:
            return jsonify({"error": f"Material with ID {id} not found"}), 404
        conn.commit()
        return jsonify({"message":"Stock updated successfully"}), 200
