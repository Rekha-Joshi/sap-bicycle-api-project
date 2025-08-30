from flask import Flask, request, Response, Blueprint, jsonify
import sqlite3
import json
from datetime import date

#define blueprint
expenses_bp = Blueprint("expenses", __name__)

#gloabal variable
DB_PATH = "02_Database/bike_project.db"

@expenses_bp.route("/expenses")
def get_expenses(): #get all expenses
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses")
        rows = cursor.fetchall()
        if not rows:
            return jsonify({"error":"There are no expenses."}),400
        expenses = [
            {
                "cost center id":row["cost_center_id"],
                "sales order id":row["sales_order_id"],
                "production order id": row["production_order_id"],
                "category": row["category"],
                "amount": row["amount"],
                "description":row["description"],
                "expense date":row["expense_date"]
            } for row in rows
        ]
        return Response(
            json.dumps(expenses, indent=2),
            mimetype="applications/json"
        ),200

@expenses_bp.route("/expenses/<int:exp_id>")
def get_expense(exp_id): #get expense by id
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses WHERE id=?",(exp_id,))
        data = cursor.fetchone()
        if not data:
            return jsonify({"error":"Expense not found."}), 404
        expense = [
            {
                "cost center id":data["cost_center_id"],
                "sales order id":data["sales_order_id"],
                "production order id": data["production_order_id"],
                "category": data["category"],
                "amount": data["amount"],
                "description":data["description"],
                "expense date":data["expense_date"]
            }
        ]
        return Response(
            json.dumps(expense, indent=2),
            mimetype="applications/json"
        ),200
    
@expenses_bp.route("/expenses", methods=["POST"])
def create_expenses():
    data = request.get_json() or {}

    #1) cost center id compulsory and is a number
    if not data or "cost_center_id" not in data:
        return jsonify({"error": "Cost center id is needed."}), 400
    if not isinstance(data["cost_center_id"], int):
        return jsonify({"error":"Cost center id must be an integer."}), 400
    
    #2) category is mandatory
    category = data["category"].strip()
    if "category" not in data:
        return jsonify({"error":"Category is mandatory."}), 400
    if category not in ("Manufacturing", "PostProduction"):
        return jsonify({"error":"Invalid category. Can only be either Manufacturing or PostProduction."}), 400
    
    #3) check for sales order id/production order id and are number
    sales_id, production_id = data.get("sales_order_id"), data.get("production_order_id")
    if (not sales_id and not production_id) or (sales_id and production_id):
        return jsonify({"error": "Provide exactly one: sales_order_id OR production_order_id"}), 400
    if sales_id is not None and not isinstance(sales_id, int):
        return jsonify({"error": "sales_order_id must be an integer"}), 400
    if production_id is not None and not isinstance(production_id, int):
        return jsonify({"error": "production_order_id must be an integer"}), 400
    if (sales_id and category != "PostProduction") or (production_id and category != "Manufacturing"):
        return jsonify({"error": "Category and order type mismatch"}), 400
    
    #4) check for amount and is a number and >=0
    if "amount" not in data:
        return jsonify({"error":"Amount is missing."}), 400
    if not isinstance(data["amount"],(int,float)):
        return jsonify({"error":"Amount must be a number."}), 400
    if data["amount"] < 0:
        return jsonify({"error":"Amount must be >= 0."}), 400
    
    #5) check cost center id is present in cost_centers
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row #Read each row as dictionary
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cost_centers WHERE id = ?", (data["cost_center_id"],))
        ccid = cursor.fetchone()
        if not ccid:
            return jsonify({"error":"Cost Center id not valid."}), 404
        if sales_id:
            cursor.execute("SELECT * FROM sales_orders WHERE id = ?", (sales_id,))
            sales = cursor.fetchone()
            if not sales:
                return jsonify({"error":"Sales order id not valid."}), 404
            if sales["status"] == "Cancelled":
                return jsonify({"error": "Cannot add expenses to a cancelled sales order."}), 400
        if production_id:
            cursor.execute("SELECT * FROM production_orders WHERE id = ?", (production_id,))
            prod = cursor.fetchone()
            if not prod:
                return jsonify({"error":"Production order id not valid."}), 404
            if prod["status"] == "Cancelled":
                return jsonify({"error": "Cannot add expenses to a cancelled production order."}), 400
        #6) All checks passed. Add an entry to expenses table
        cursor.execute("""
                    INSERT INTO expenses(cost_center_id, sales_order_id, production_order_id, category, 
                       amount, description, expense_date)
                    VALUES(?,?,?,?,?,?,COALESCE(?, DATE('now')))
                    """, (data["cost_center_id"], sales_id, production_id, data["category"], 
                          data["amount"], data.get("description"), data.get("expense_date"))
                )
        conn.commit()
    return jsonify({"message": "Expenses created successfully"}), 201
            
