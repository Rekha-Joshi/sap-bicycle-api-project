from flask import Flask, jsonify, request, Response, Blueprint
import sqlite3
import json
from datetime import date

#defining blueprint
sales_orders_bp = Blueprint("sales_orders", __name__)

#gloabal variable
DB_PATH = "02_Database/bike_project.db"

@sales_orders_bp.route("/sales_orders")
def get_sales_orders():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales_orders")
        rows = cursor.fetchall()
        sales = [
            {
                "customer id": row["customer_id"],
                "material id": row["material_id"],
                "quantity": row["quantity"],
                "order date": row["order_date"],
                "status": row["status"]
            } for row in rows
        ]
        return Response(
            json.dumps(sales, indent=2),
            mimetype="applications/json"
        )

@sales_orders_bp.route("/sales_orders/<int:so_id>", methods=["GET"])
def get_sale_order(so_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales_orders WHERE id = ?", (so_id,))
        row = cursor.fetchone()
        sales = [
            {
                "customer id": row["customer_id"],
                "material id": row["material_id"],
                "quantity": row["quantity"],
                "order date": row["order_date"],
                "status": row["status"]
            } 
        ]
        return Response(
            json.dumps(sales, indent=2),
            mimetype="applications/json"
        )

@sales_orders_bp.route("/sales_orders", methods=["POST"])
def create_sales_order():
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
        conn.execute("PRAGMA foreign_keys = ON")
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

@sales_orders_bp.route("/sales_orders/<int:so_id>/ship", methods=["POST"])
def ship_sales_order(so_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales_orders WHERE id = ?", (so_id,))
        so = cursor.fetchone()
        if not so:
            return jsonify({"error":"Sales order not found."}), 404
        if so["status"] == "Pending":
            return jsonify({ "error": "Only confirmed sales orders can be shipped." }), 400
        if so["status"] == "Cancelled":
            return jsonify({ "error": "Cancelled sales orders cannot be shipped." }), 400
        if so["status"] == "Shipped":
            return jsonify({ "error": "Sales order is already shipped." }), 400
        cursor.execute("UPDATE sales_orders SET status = 'Shipped' WHERE id = ?", (so_id,))
        conn.commit()
        return jsonify(
            {
                "message": "Sales order shipped successfully.",
                "sales_order_id": so_id,
                "status": "Shipped"
                }
        ), 200

@sales_orders_bp.route("/sales_orders/<int:so_id>/cancel", methods=["POST"])
def cancel_sales_order(so_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales_orders WHERE id = ?", (so_id,))
        so = cursor.fetchone()
        if not so:
            return jsonify({"error":"Sales order not found."}), 404
        if so["status"] == "Cancelled":
            return jsonify({ "error": "Sales order is already cancelled." }), 400
        if so["status"] == "Shipped":
            return jsonify({ "error": "Shipped sales orders cannot be cancelled." }), 400
        if so["status"] != "Pending":
            return jsonify({ "error": "Only pending sales orders can be cancelled." }), 400
        #find attached production order. One sale order can have multiple prod orders. so fecting only completed
        cursor.execute("""
                       SELECT 1 FROM production_orders WHERE sales_order_id = ? AND status = 'Completed'
                    LIMIT 1""",(so_id,)
                    )
        if cursor.fetchone():
            return jsonify({ "error": "Production completed; cancellation not allowed." }), 400
        else:
            cursor.execute("""
                           UPDATE production_orders SET status = 'Cancelled', end_date = DATETIME('now') 
                           WHERE sales_order_id=? AND status IN ('Created', 'In-Progress')
                           """, (so_id,)
                        )
            cancelled_pos = cursor.rowcount
        cursor.execute("UPDATE sales_orders SET status = 'Cancelled' WHERE id = ?", (so_id,))
        conn.commit()
        return jsonify(
            {
                "message": "Sales order cancelled successfully.",
                "sales_order_id": so_id,
                "production_orders_cancelled":cancelled_pos,
                "status": "Cancelled"
                }
        ), 200