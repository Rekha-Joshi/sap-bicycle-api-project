from flask import Flask, jsonify, request, Response, Blueprint
import sqlite3
import json

#defining blueprint
sales_orders_bp = Blueprint("sales_orders", __name__)

#gloabal variable
DB_PATH = "02_Database/bike_project.db"

@sales_orders_bp.route("/sales_orders", methods=["POST"])
def add_new_sales_order():
    data = request.get_json() or {}
    required = ("customer_id", "material_id", "quantity", "order_date")
    missing = [key for key in required if key not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    # parse/validate quantity early
    try:
        qty = int(data["quantity"])
        if qty <= 0:
            return jsonify({"error": "Quantity must be > 0"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Quantity must be a number"}), 400

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        def get_customer(cid):
            cursor.execute("SELECT id FROM customers WHERE id = ?", (cid,))
            return cursor.fetchone()

        def get_material(mid):
            cursor.execute("SELECT id, name, type, unit_price, stock FROM materials WHERE id = ?", (mid,))
            return cursor.fetchone()

        # guard clauses: fail fast, no deep nesting
        if not get_customer(data["customer_id"]):
            return jsonify({"error": "Customer not found."}), 404

        mat = get_material(data["material_id"])
        if not mat:
            return jsonify({"error": "Material not found"}), 404
        if mat["type"] != "finished":
            return jsonify({"error": "Only finished products can be ordered"}), 400

        in_stock = mat["stock"] >= qty #checking if stock is greater or equal to asked qty
        status = "Confirmed" if in_stock else "Pending"
        note = "Enough Stock. Order Confirmed." if in_stock else "Less Stock. Order Pending/Backorder."

        # create order
        cursor.execute(
            """INSERT INTO sales_orders (customer_id, material_id, quantity, order_date, status)
               VALUES (?, ?, ?, ?, ?)""",
            (data["customer_id"], data["material_id"], qty, data["order_date"], status)
        )
        order_id = cursor.lastrowid #fetching the order id of just created sales order

        # update stock only when confirmed
        if in_stock:
            cursor.execute("UPDATE materials SET stock = stock - ? WHERE id = ?", (qty, data["material_id"]))

        conn.commit()

    return jsonify({
        "message": "Sales order created successfully.",
        "order_id": order_id,
        "status": status,
        "note": note
    }), 201