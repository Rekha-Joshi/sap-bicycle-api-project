from flask import Flask , jsonify, Response, request, Blueprint
import sqlite3
import json

materials_bp = Blueprint("materials", __name__) #defining blueprint

DB_PATH = "02_Database/bike_project.db"
#get all materials
@materials_bp.route("/materials", methods=["GET"])
def get_materials():
    m_type = request.args.get("type")
    name_q = request.args.get("name")
    low_stock = request.args.get("low_stock", type=int)
    where = []
    params = []
    if m_type:
        where.append("LOWER(type) = ?")
        params.append(m_type.lower())
    if name_q:
        where.append("LOWER(name) like ?")
        params.append(f"%{name_q.lower()}%")
    if low_stock is not None:
        where.append("stock < ?")
        params.append(low_stock)
    sql = "SELECT * FROM  materials"
    if where:
        sql += " WHERE " + " AND ".join(where)
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute(sql,params)
        rows = cursor.fetchall()
        materials = [
            {
                "name": row["name"],
                "type": row["type"],
                "unit_price": row["unit_price"],
                "stock": row["stock"],
                "reorder_level": row["reorder_level"],
                "vendor_id": row["vendor_id"]
            }for row in rows
        ]
        return Response(
            json.dumps(materials, indent=2),
            mimetype="application/json"
        ),200

@materials_bp.route("/materials/<int:mat_id>", methods=["GET"])
def get_material(mat_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM materials WHERE id = ?",(mat_id,))
        material = cursor.fetchone()
        if material:
            data = {
                "name": material["name"],
                "type": material["type"],
                "unit_price": material["unit_price"],
                "stock": material["stock"],
                "reorder_level": material["reorder_level"],
                "vendor_id": material["vendor_id"]
            }
        else:
            return jsonify({"error":"Material ID not found."}), 404
        return jsonify(data), 200
    
#add new materials. single or bulk
@materials_bp.route("/materials", methods=["POST"])
def set_materials():  # create materials (single or bulk)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid JSON body"}), 400

    items = data if isinstance(data, list) else [data] if isinstance(data, dict) else None
    if items is None:
        return jsonify({"error": "Body must be an object or an array of objects"}), 400

    allowed_types = {"Raw", "Finished"}
    errors = []
    inserted_count = 0
    had_validation_error = False
    had_conflict_error = False

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        for idx, raw in enumerate(items, 1):
            item_errors = []

            # name
            if "name" not in raw or not isinstance(raw["name"], str) or not raw["name"].strip():
                item_errors.append(f"Item {idx}: Name is required and must be a non-empty string")
            else:
                m_name = raw["name"].strip()

            # type
            if "type" not in raw or not isinstance(raw["type"], str) or not raw["type"].strip():
                item_errors.append(f"Item {idx}: Type is required and must be either 'Raw' or 'Finished'")
                m_type = None
            else:
                m_type = raw["type"].strip().title()
                if m_type not in allowed_types:
                    item_errors.append(f"Item {idx}: Type must be Raw or Finished")

            # unit_price > 0
            if "unit_price" not in raw or not isinstance(raw["unit_price"], (int, float)) or raw["unit_price"] <= 0:
                item_errors.append(f"Item {idx}: Unit price is required and must be a number > 0")
            else:
                m_unit_price = float(raw["unit_price"])

            # stock >= 0
            if "stock" not in raw or not isinstance(raw["stock"], int) or raw["stock"] < 0:
                item_errors.append(f"Item {idx}: Stock is required and must be an integer >= 0")
            else:
                m_stock = int(raw["stock"])

            # reorder_level (default 30)
            if "reorder_level" in raw and raw["reorder_level"] is not None:
                if not isinstance(raw["reorder_level"], int) or raw["reorder_level"] < 0:
                    item_errors.append(f"Item {idx}: Reorder level must be a non-negative integer")
                    m_reorder_level = 30
                else:
                    m_reorder_level = int(raw["reorder_level"])
            else:
                m_reorder_level = 30

            # vendor rules
            m_vendor_id = None
            if m_type == "Raw":
                if "vendor_id" not in raw or not isinstance(raw["vendor_id"], int) or raw["vendor_id"] <= 0:
                    item_errors.append(f"Item {idx}: vendor_id is required for Raw materials and must be a positive integer")
                else:
                    m_vendor_id = raw["vendor_id"]
            elif m_type == "Finished":
                if "vendor_id" in raw:
                    item_errors.append(f"Item {idx}: vendor_id must not be provided for Finished materials")

            # if any validation failed, skip insert
            if item_errors:
                had_validation_error = True
                errors.extend(item_errors)
                continue

            # insert
            try:
                cursor.execute(
                    """
                    INSERT INTO materials (name, type, unit_price, stock, reorder_level, vendor_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (m_name, m_type, m_unit_price, m_stock, m_reorder_level, m_vendor_id)
                )
                inserted_count += 1
            except sqlite3.IntegrityError as e:
                had_conflict_error = True
                msg = str(e).lower()
                if "foreign key" in msg:
                    errors.append(f"Item {idx}: vendor not found")
                elif "unique" in msg or "materials.name" in msg:
                    errors.append(f"Item {idx}: {m_name} already exists.")
                else:
                    errors.append(f"Item {idx}: integrity error")
                continue

        conn.commit()

    # Decide status
    if inserted_count == 0 and had_validation_error:
        return jsonify({"message": "Invalid input", "errors": errors}), 400
    if had_validation_error or had_conflict_error:
        return jsonify({"message": "Some materials were not added", "errors": errors}), 409
    return jsonify({"message": "Material(s) added successfully."}), 201


#lists materials which are low in stock
@materials_bp.route("/materials/low-stock")
def check_stock():
    threshold = int(request.args.get("threshold", 30)) #default = 30
    #request.args gives you access to query parameters in the URL
    #.get("threshold") tries to fetch the value of threshold
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM materials where stock < ?",(threshold,))
        rows = result.fetchall()
        items = [
            {
                "name": row["name"],
                "type": row["type"],
                "unit_price": row["unit_price"],
                "stock": row["stock"],
                "reorder_level": row["reorder_level"],
                "vendor_id": row["vendor_id"]   
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
    
@materials_bp.route("/materials/<int:id>/stock", methods = ["PATCH"])
def update_material_stock(id):
    data = request.get_json()
    #validating if json body is present, there is stock and it's a number
    if not data or "stock" not in data:
        return jsonify({"error": "'stock' field is required"}), 400
    if not isinstance(data["stock"], (int, float)):
        return jsonify({"error": "'stock' must be a number"}), 400
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        new_stock_value = int(data["stock"])
        cursor.execute ("UPDATE materials SET stock = ? where id = ?",(new_stock_value,id,))
        #this is to check if the id was valid. If invalid it will update 0 rows
        if cursor.rowcount == 0:
            return jsonify({"error": f"Material with ID {id} not found"}), 404
        conn.commit()
        return jsonify({"message":"Stock updated successfully"}), 200

#assign vendor id to materials
@materials_bp.route("/materials/assign_vendor", methods = ["PATCH"])
def assign_vendor():
    data = request.get_json()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        if not data or "material_name" not in data or "vendor_id" not in data:
            return jsonify ({"error": "Missing mandatory filed. Check if 'material_name' and 'vendor_id' are present."}), 400
        #check if material exists
        cursor.execute("SELECT * FROM materials WHERE name = ?",(data["material_name"],))
        material = cursor.fetchone()
        #check if vendor exists
        cursor.execute("SELECT * FROM vendors WHERE id = ?",(data["vendor_id"],))
        vendor = cursor.fetchone()
        if material and vendor:
            material_type = material["type"]
            if material_type == "finished":
                return jsonify({
                    "error": "Cannot assign a vendor to a finished product."
                }), 400
            cursor.execute("UPDATE materials SET vendor_id = ? WHERE name = ?",(data["vendor_id"],data["material_name"]))
            conn.commit()
            return jsonify({"message":f"Vendor id updated successfully for '{data["material_name"]}'"}),200
        else:
            return jsonify ({"error":"Please check if material exists and vendor exists."}),404

@materials_bp.route("/materials/<int:mat_id>", methods=["PATCH"])
def update_materials(mat_id):
    data = request.get_json()
    #1) check material id is positive number
    if mat_id <=0:
            return jsonify({"error":"Invalid material id."}), 400
    #2) checking if body is present and is a dict
    if not isinstance(data, dict):
        return jsonify({"error": "JSON body required"}), 400
    
    allowed = {"name", "type", "unit_price", "reorder_level"}
    forbidden = {"stock", "vendor_id"}

    #3) Reject forbidden fields
    reject_keys = [k for k in data.keys() if k in forbidden]
    if reject_keys:
        return jsonify({"error": f"Invalid field(s): {', '.join(reject_keys)}. Use dedicated endpoints for stock/vendor updates."}), 400

    #4) Atleast one allowed key is present
    updates = {k:v for k,v in data.items() if k in allowed}
    if not updates:
        return jsonify({"error": "Provide at least one of: name, type, unit_price, reorder_level"}), 400
    
    #5) check if name and is a non empty string
    if "name" in updates:
        if not isinstance(updates["name"], str) or not updates["name"].strip():
            return jsonify({"error": "name must be a non-empty string"}), 400
        updates["name"] = updates["name"].strip()
    
    #6) check if type is either raw or finished
    if "type" in updates:
        if not isinstance(updates["type"], str):
            return jsonify({"error": "type must be a string"}), 400
        t = updates["type"].strip().lower()
        if t not in {"raw", "finished"}:
            return jsonify({"error": "type must be one of: Raw, Finished"}), 400
        updates["type"] = "Raw" if t == "raw" else "Finished"
    #7) check unit price is >=0 
    if "unit_price" in updates:
        val = updates["unit_price"]
        if not isinstance(val, (int, float)):
            return jsonify({"error": "unit_price must be a number"}), 400
        if val < 0:
            return jsonify({"error": "unit_price must be >= 0"}), 400      
    #8) check reorder level >= 0 (30 is default)
    if "reorder_level" in updates:
        val = updates["reorder_level"]
        if not isinstance(val, int):
            return jsonify({"error": "reorder_level must be an integer"}), 400
        if val < 0:
            return jsonify({"error": "reorder_level must be >= 0"}), 400
    
    set_parts = []
    params =[]
    for k,v in updates.items():
        set_parts.append(f"{k} =?")
        params.append(v)
    params.append(mat_id) #for where id = ?

    sql = f"UPDATE materials SET {', '.join(set_parts)} where id = ?"

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        #check if material exists
        cursor.execute("SELECT * FROM materials WHERE id = ?",(mat_id,))
        if not cursor.fetchone():
            return jsonify({"error":"Material not found"}), 404
        cursor.execute(sql, params)
        conn.commit()
        # return updated row (optional but nice)
    cursor.execute("SELECT * FROM materials WHERE id = ?", (mat_id,))
    row = cursor.fetchone()
    return jsonify({
        "id": row["id"],
        "name": row["name"],
        "type": row["type"],
        "unit_price": row["unit_price"],
        "stock": row["stock"],
        "reorder_level": row["reorder_level"],
        "vendor_id": row["vendor_id"],
    }), 200
        
