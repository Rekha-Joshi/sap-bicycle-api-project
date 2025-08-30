from flask import Flask, jsonify, request, Response, Blueprint
import sqlite3
import json

employees_bp = Blueprint("employees", __name__)

DB_PATH = "02_Database/bike_project.db"

@employees_bp.route("/employees")
def get_employees():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        if not rows:
            return jsonify({"error":"No employees."}),400
        employees = [
            {
                "name": row["name"],
                "department": row["department_name"],
                "job title": row["job_title"],
            } for row in rows
        ]
        return Response(
            json.dumps(employees, indent=2),
            mimetype="applications/json"
        ),200
    
@employees_bp.route("/employees", methods = ["POST"])
def add_employees(): #create new employee
    data = request.get_json()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        if not all (key in data for key in ("name", "department_name", "job_title")):
            return jsonify({"error": "Missing required fields"}), 400
        cursor.execute("SELECT * FROM departments WHERE name = ?", (data["department_name"],))
        dept = cursor.fetchone()
        if dept:
            cursor.execute(
                """
                INSERT INTO employees(name, department_name, job_title)
                VALUES (?,?,?)
                """,(data["name"], data["department_name"], data["job_title"])
            )
            conn.commit()
            return jsonify({"message":"Employee added successfully."}), 201
        else:
            return jsonify({"error": "Department does not exist"}), 400

