from flask import Flask, jsonify, request, Response, Blueprint
import sqlite3
import json
from datetime import date

#defining blueprint
production_orders_bp = Blueprint("production_orders", __name__)

#gloabal variable
DB_PATH = "02_Database/bike_project.db"

@production_orders_bp.route("/production_orders", methods = ["POST"])
def create_prod_order():
    data = request.get_json() or {}
    if not data or "sales_order_id" not in data:
        return jsonify({"Error":"Sales order id missing."}), 400
    if not isinstance(data["sales_order_id"], int):
        return jsonify({"error": "'Sales order id' must be a number"}), 400
    if "planned_quantity" not in data:
        return jsonify({"error": "planned_quantity is required"}), 400
    try:
        so_id = int(data["sales_order_id"])
        planned_qty = int(data["planned_quantity"])
        if planned_qty <= 0:
            return jsonify({"error": "planned_quantity must be > 0"}), 400
    except (TypeError, ValueError):
        return jsonify({"error": "sales_order_id and planned_quantity must be numbers"}), 400
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales_orders where id = ? AND status = 'Pending'", (so_id,))
        sales_order = cursor.fetchone()
        if not sales_order: #if sales order not found, exit now
            return jsonify({"Error":"Pending sales order not found."}), 404
        cursor.execute("SELECT * FROM materials WHERE id = ? AND type = 'finished'", (sales_order["material_id"],))
        materials = cursor.fetchone()
        if not materials: #if material not found or not a finished product, exit now
            return jsonify({"error": "Only finished products can be ordered"}), 404
        cursor.execute("""
                    INSERT INTO production_orders(sales_order_id, material_id, planned_quantity, start_date, 
                    end_date, status) Values(?,?,?,?,?,?)
                    """, (sales_order["id"], materials["id"], planned_qty, data["start_date"],
                            data["end_date"],"Planned")
        )
        conn.commit()
        order_id = cursor.lastrowid
    return jsonify({
        "message": "Production order created successfully.",
        "order_id": order_id,
    }), 201

@production_orders_bp.route("/production_orders/<int:po_id>/complete", methods = ["PUT"])
def complete_production_order(po_id):
    data = request.get.json() or {}
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        #1) Load PO
        cursor.execute("SELECT * FROM production_orders WHERE id = ?", po_id)
        po = cursor.fetchone()
        if not po: return jsonify({"error":"Production order not found"}), 404
        if po["status"] == "completed": return jsonify({"error":"Already completed"}), 400
        
        #2) Decide quantity
        qty = int(data.get("actual_quantity", po["planned_quantity"]))
        if qty <= 0: return jsonify({"error":"Quantity must be > 0"}), 400

        #3) Add stock
        cursor.execute("UPDATE materials SET stock = stock + ? WHERE id = ?", (qty,po["material_id"]))

        #4) Mark production order completed
        cursor.execute("UPDATE production_orders SET status = 'Completed', end_date = datetime('now') WHERE id = ?", (po_id,))

        #5) confirm Sales order and materials
        cursor.execute("SELECT * FROM sales_orders WHERE id = ? ", (po["sales_order_id"],))
        so = cursor.fetchone()
        if so and so["status"] == "Pending":
            cursor.execute("SELECT stock FROM materials WHERE id = ? ",(po["material_id"],))
            stock_now = cursor.fetchone["stock"]
            if stock_now >= so["quantity"]:
                cursor.execute("UPDATE materials SET stock = stock - ? WHERE id=?", (so["quantity"], po["material_id"]))
                cursor.execute("UPDATE sales_orders SET status='Confirmed' WHERE id=?", (so["id"],))
        conn.commit()
    return jsonify({"message":"Production completed"}), 200