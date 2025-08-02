from flask import jsonify, request, Response, Blueprint
import sqlite3
import json

#Defining Blueprint
vendors_bp = Blueprint("vendors", __name__)

#gloabal variable
DB_PATH = "02_Database/bike_project.db"

#endpoint to fetch all vendors
@vendors_bp.route("/vendors")
def get_vendors():
    pass